import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
import json
from time import perf_counter
from urllib.request import Request, urlopen

from prepare_boxscores import (
    GAME_ID, NEXT_DATA, PHT, ROOT, build_research, completed_schedule, fetch_boxes, save_json,
)


def nba_page(url):
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=15) as response:
        match = NEXT_DATA.search(response.read().decode('utf-8'))
    if match is None:
        raise ValueError(f'The NBA page did not return structured data: {url}')
    return json.loads(match[1])['props']['pageProps']


def day_games(day):
    source = f'https://www.nba.com/games?date={day.isoformat()}'
    page = nba_page(source)
    if page['selectedDate'] != day.isoformat() or page.get('hasError'):
        raise ValueError(f'The NBA schedule did not return the requested date: {source}')
    return [
        (card['cardData'], source)
        for group in page['gameCardFeed']['modules'] for card in group.get('cards', [])
        if card['cardType'] == 'game' and GAME_ID.fullmatch(card['cardData']['gameId'])
    ]


def get_team(team_id):
    source = f'https://www.nba.com/stats/team/{team_id}/traditional'
    team = nba_page(source)['team']
    if int(team['id']) != team_id or not team['schedule']:
        raise ValueError(f'The NBA team schedule is incomplete: {source}')
    return team, source


def preload(day, selected_matches=()):
    started = perf_counter()
    output = ROOT / day.isoformat() / '_prep'
    with ThreadPoolExecutor(max_workers=6) as pool:
        # 菲律宾的一天横跨两个美国东部日期，按 UTC 开赛时间归回菲律宾日期。
        dates = [day - timedelta(days=1), day]
        games = {}
        for cards in pool.map(day_games, dates):
            for game, source in cards:
                tipoff = datetime.fromisoformat(game['gameTimeUtc']).astimezone(PHT)
                if tipoff.date() != day:
                    continue
                matchup = f"{game['awayTeam']['teamTricode']}-{game['homeTeam']['teamTricode']}"
                if selected_matches and matchup not in selected_matches:
                    continue
                games[game['gameId']] = (game, source, tipoff)
        teams = {side['teamTricode'].lower(): side['teamId'] for game, _, _ in games.values()
                 for side in (game['awayTeam'], game['homeTeam'])}
        tasks = {tag: pool.submit(get_team, team_id) for tag, team_id in teams.items()}
        snapshots, team_errors = {}, {}
        for tag, task in tasks.items():
            try:
                snapshots[tag], source = task.result()
            except (OSError, ValueError, KeyError, TypeError) as error:
                team_errors[tag] = str(error)
                continue
            team = snapshots[tag]
            save_json(output / 'team-schedules' / f'{tag}-team.json', team | {'source_url': source})

    matches = {}
    unique_history = {}
    for game_id, (game, source, tipoff) in sorted(games.items(), key=lambda item: item[1][2]):
        away, home = (game[side]['teamTricode'].lower() for side in ('awayTeam', 'homeTeam'))
        label = f'{away.upper()}-{home.upper()}'
        match = {
            'game_id': game_id, 'match': label, 'tipoff_pht': tipoff.isoformat(),
            'away_team': away.upper(), 'home_team': home.upper(), 'game_status': game['gameStatus'],
            'schedule_source': source, 'game_url': game['shareUrl'],
        }
        samples = {}
        for tag in (away, home):
            if tag not in snapshots:
                continue
            team = snapshots[tag]
            target = next((entry for entry in team['schedule'] if entry['gameId'] == game_id), None)
            if target is None or datetime.fromisoformat(target['gameDateTimeUTC']) != tipoff:
                match.setdefault('schedule_conflicts', []).append(tag)
                continue
            match['arena'] = target['arenaName']
            history = completed_schedule(team, tag, tipoff)
            samples[tag] = history
            if history:
                last = history[-1]
                last_tipoff = datetime.fromisoformat(last['gameDateTimeUTC']).astimezone(PHT)
                match.setdefault('last_games', {})[tag] = {
                    'id': last['gameId'], 'tipoff_pht': last_tipoff.isoformat(),
                    'arena': last['arenaName'], 'arena_city': last['arenaCity'],
                }
                unique_history.update((entry['gameId'], entry) for entry in history)
        matches[game_id] = (match, samples, tipoff)

    # 全部对阵共用一次取数，按比赛 ID 去重，比分和失误继续用原流程校验。
    boxes, origins, failed = fetch_boxes(unique_history, output)
    manifest = []
    for match, samples, tipoff in matches.values():
        data = build_research(samples, tipoff, boxes, origins, failed)
        path = output / match['match'] / 'boxscore-research.json'
        save_json(path, data | {'game': match})
        match['research'] = str(path.relative_to(output))
        match['sample_sizes'] = {tag.upper(): len(team['games']) for tag, team in data['teams'].items()}
        match['expected_sample_sizes'] = {tag.upper(): len(entries) for tag, entries in samples.items()}
        manifest.append(match)

    actual_matches = {match['match'] for match in manifest}
    missing_matches = sorted(set(selected_matches) - actual_matches)
    result = {
        'date_pht': day.isoformat(), 'checked_at_pht': datetime.now(PHT).isoformat(timespec='seconds'),
        'missing_matches': missing_matches, 'matches': manifest, 'scheduled_games': len(manifest), 'teams': len(snapshots),
        'historical_games': len(boxes), 'shared_cache_hits': list(origins.values()).count('cache'),
        'downloaded': list(origins.values()).count('NBA.com'), 'team_errors': team_errors,
        'boxscore_errors': failed, 'seconds': round(perf_counter() - started, 2),
    }
    path = output / 'slate.json'
    save_json(path, result)
    print(json.dumps(result | {'matches': [game['match'] for game in manifest], 'output': str(path)}, ensure_ascii=False))
    incomplete = any(len(game['sample_sizes']) != 2 or game.get('schedule_conflicts') for game in manifest)
    return 1 if team_errors or failed or incomplete or missing_matches else 0


def main():
    parser = argparse.ArgumentParser(description='Preload the NBA schedule and the last 3, 5, and 10 games per team for a Philippine game date')
    parser.add_argument('date_pht', type=date.fromisoformat, help='Philippine game date: YYYY-MM-DD')
    parser.add_argument('--match', action='append', default=[], type=str.upper, metavar='AWAY-HOME',
                        help='Preload only this matchup. Repeat to select multiple games.')
    args = parser.parse_args()
    return preload(args.date_pht, args.match)


if __name__ == '__main__':
    raise SystemExit(main())
