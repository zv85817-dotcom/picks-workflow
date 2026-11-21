import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent / 'work'
CACHE = ROOT / 'cache' / 'boxscores'
PHT = timezone(timedelta(hours=8))
GAME_ID = re.compile(r'002\d{7}')
NEXT_DATA = re.compile(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.DOTALL)


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save_json(path, value):
    # 先写临时文件再替换，避免并发读取到尚未写完的缓存。
    path.parent.mkdir(parents=True, exist_ok=True)
    staged = None
    try:
        with NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as file:
            staged = Path(file.name)
            file.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        staged.replace(path)
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)


def validate_box(game, game_id, scheduled=None):
    if game['gameId'] != game_id or game['gameStatus'] != 3:
        raise ValueError(f'{game_id} has a mismatched ID or is not final')
    for side in ('awayTeam', 'homeTeam'):
        team = game[side]
        stat = team['statistics']
        chart = game['postgameCharts'][side]['statistics']
        points = 2 * stat['fieldGoalsMade'] + stat['threePointersMade'] + stat['freeThrowsMade']
        if points != stat['points'] or points != team['score']:
            raise ValueError(f'{game_id} has box-score statistics that do not match the final score')
        if stat['turnovers'] != chart['turnovers'] or chart['turnovers'] + chart['turnoversTeam'] != chart['turnoversTotal']:
            raise ValueError(f'{game_id} has inconsistent player, team, and total turnover counts')
        if scheduled is not None:
            expected = scheduled[side]
            if team['teamId'] != expected['teamId'] or points != expected['score']:
                raise ValueError(f'{game_id} has a team or score mismatch against the official schedule')


def completed_schedule(snapshot, tag, tipoff):
    team_id = int(snapshot['id'])
    # 赛后重跑旧比赛时也以目标开赛时间为界，排除目标场次和后续比赛。
    schedule = {}
    for game in snapshot['schedule']:
        game_id = game['gameId']
        if not GAME_ID.fullmatch(game_id) or game['gameStatus'] != 3:
            continue
        own = next((game[side] for side in ('awayTeam', 'homeTeam') if game[side]['teamId'] == team_id), None)
        if own is None or own['teamTricode'] != tag.upper():
            raise ValueError(f'{tag} schedule snapshot does not match game {game_id}')
        if datetime.fromisoformat(game['gameDateTimeUTC']) < tipoff:
            schedule[game_id] = game
    return sorted(schedule.values(), key=lambda game: game['gameDateTimeUTC'])[-10:]


def get_box(scheduled, work):
    game_id = scheduled['gameId']
    name = f'box-{game_id}.json'
    target = CACHE / name
    local = work / name
    # 缓存缺失、损坏或比分修订时，继续检查本场档案或重新取官方数据。
    for path, origin in ((target, 'cache'), (local, 'local')):
        try:
            game = load_json(path)
            validate_box(game, game_id, scheduled)
        except (OSError, TypeError, KeyError, ValueError):
            continue
        if origin == 'local':
            save_json(target, game)
        return game_id, game, origin

    url = f'https://www.nba.com/game/{game_id}/box-score'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=12) as response:
            html = response.read().decode('utf-8')
    except (URLError, TimeoutError, ConnectionError) as error:
        # 本次九场批量取数出现过上游 502 和读超时，针对这类错误仅重试一次。
        if isinstance(error, HTTPError) and error.code not in (502, 503, 504):
            raise
        with urlopen(req, timeout=18) as response:
            html = response.read().decode('utf-8')
    match = NEXT_DATA.search(html)
    if match is None:
        raise ValueError(f'The NBA game page did not return box-score data: {game_id}')
    game = json.loads(match[1])['props']['pageProps']['game']
    validate_box(game, game_id, scheduled)
    save_json(target, game)
    return game_id, game, 'NBA.com'


def game_row(game, tag):
    side = 'homeTeam' if game['homeTeam']['teamTricode'] == tag.upper() else 'awayTeam'
    other = 'awayTeam' if side == 'homeTeam' else 'homeTeam'
    own, opp = game[side], game[other]
    a, b = own['statistics'], opp['statistics']
    turnovers = game['postgameCharts'][side]['statistics']['turnoversTotal']
    opp_turnovers = game['postgameCharts'][other]['statistics']['turnoversTotal']
    expected_possessions = (
        a['fieldGoalsAttempted'] + b['fieldGoalsAttempted']
        + 0.44 * (a['freeThrowsAttempted'] + b['freeThrowsAttempted'])
        - a['reboundsOffensive'] - b['reboundsOffensive'] + turnovers + opp_turnovers
    ) / 2
    return {
        'id': game['gameId'], 'date': game['gameCode'].split('/')[0], 'home': side == 'homeTeam',
        'opp': opp['teamTricode'], 'pf': a['points'], 'pa': b['points'],
        'minutes': 48 + 5 * max(0, game['period'] - 4), 'poss_est': expected_possessions,
        'fga': a['fieldGoalsAttempted'], 'fta': a['freeThrowsAttempted'],
        '3pm': a['threePointersMade'], '3pa': a['threePointersAttempted'],
        'oreb': a['reboundsOffensive'], 'opp_dreb': b['reboundsDefensive'],
        'tov': turnovers, 'opp_tov': opp_turnovers,
    }


def summarize(rows):
    totals = {key: sum(row[key] for row in rows) for key in ('pf', 'pa', 'minutes', 'poss_est', 'fga', 'fta', '3pm', '3pa', 'oreb', 'opp_dreb', 'tov', 'opp_tov')}
    n = len(rows)
    return {
        'n': n, 'from': rows[0]['date'], 'to': rows[-1]['date'],
        'pf_pg': round(totals['pf'] / n, 2), 'pa_pg': round(totals['pa'] / n, 2),
        'pace48_est': round(totals['poss_est'] * 48 / totals['minutes'], 2),
        'ortg_est': round(totals['pf'] * 100 / totals['poss_est'], 2),
        'drtg_est': round(totals['pa'] * 100 / totals['poss_est'], 2),
        'own_tov': round(totals['tov'] / n, 2), 'opp_tov': round(totals['opp_tov'] / n, 2),
        'oreb_rate': 100 * (totals['oreb'] / (totals['oreb'] + totals['opp_dreb'])),
        'ft_rate': 100 * (totals['fta'] / totals['fga']),
        'three_accuracy': 100 * (totals['3pm'] / totals['3pa']) if totals['3pa'] else None,
    }


def fetch_boxes(games, work):
    boxes, origins, failed = {}, {}, {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        pending = {game_id: pool.submit(get_box, game, work) for game_id, game in games.items()}
        for game_id, future in pending.items():
            try:
                _, boxes[game_id], origins[game_id] = future.result()
            except (OSError, ValueError, KeyError, TypeError) as error:
                failed[game_id] = str(error)
    return boxes, origins, failed


def build_research(samples, tipoff, boxes, origins, failed):
    teams = {}
    game_ids = {game['gameId'] for schedule in samples.values() for game in schedule}
    for tag, schedule in samples.items():
        ids = [game['gameId'] for game in schedule]
        rows = {game_id: game_row(boxes[game_id], tag) for game_id in ids if game_id in boxes}
        # 缺少样本时不拿更早的比赛补位，保留实际日期与样本数。
        summaries = {}
        for size in (3, 5, 10):
            window = ids[-size:]
            if window and all(game_id in rows for game_id in window):
                summaries[f'last{size}'] = summarize([rows[game_id] for game_id in window])
        teams[tag] = {
            'expected_game_ids': ids, 'games': list(rows.values()), 'summaries': summaries,
        }
    return {
        'tipoff_pht': tipoff.isoformat(),
        'method': 'NBA final box scores, overtime included; turnovers include team turnovers; pace estimated per 48 minutes',
        'teams': teams,
        'origins': {game_id: origin for game_id, origin in origins.items() if game_id in game_ids},
        'failed': {game_id: error for game_id, error in failed.items() if game_id in game_ids},
    }


def prepare(work, tags, tipoff):
    samples = {tag: completed_schedule(load_json(work / f'{tag}-team.json'), tag, tipoff) for tag in tags}
    games = {game['gameId']: game for sample in samples.values() for game in sample}
    return build_research(samples, tipoff, *fetch_boxes(games, work))


def main():
    parser = argparse.ArgumentParser(description='Summarize the last 3, 5, and 10 games using completed NBA box scores')
    parser.add_argument('work', type=Path, help='Match work directory containing both official NBA team schedule snapshots')
    parser.add_argument('teams', nargs=2, type=str.lower, metavar='TEAM', help='Three-letter codes for both teams')
    parser.add_argument('--tipoff-pht', required=True, help='Tipoff in Philippine Time: YYYY-MM-DD HH:MM')
    args = parser.parse_args()
    if len(set(args.teams)) != 2 or any(not re.fullmatch('[a-z]{3}', tag) for tag in args.teams):
        parser.error('Supply two distinct three-letter team codes')
    tipoff = datetime.strptime(args.tipoff_pht, '%Y-%m-%d %H:%M').replace(tzinfo=PHT)
    started = perf_counter()
    result = prepare(args.work, args.teams, tipoff)
    output = args.work / 'boxscore-research.json'
    save_json(output, result)
    origins = list(result['origins'].values())
    print(json.dumps({
        'output': str(output), 'shared_cache_hits': origins.count('cache'),
        'local_archive_hits': origins.count('local'), 'downloaded': origins.count('NBA.com'),
        'failed': result['failed'], 'sample_sizes': {tag: len(team['games']) for tag, team in result['teams'].items()},
        'seconds': round(perf_counter() - started, 2),
    }, ensure_ascii=False))
    return 1 if result['failed'] or not all(team['games'] for team in result['teams'].values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
