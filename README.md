# NBA World Picks Workflow

Turn an NBA schedule and your community's Spread and Over/Under into an English game guide and a matching banner. Each game produces a Word document, copy-ready text, a game photo, two data charts, and a separate banner.

## Quick start

1. Clone or download this repository. Open its root in Codex and trust the project when prompted so Codex can load `.agents/` and `.codex/`.
2. Check that Python 3.11 or newer is available by running `python scripts/preload_slate.py --help`. The preload scripts use only the standard library. On Windows, use `py -3` in place of `python` if needed.
3. Follow the [operations manual](OPERATIONS.md) to set up your banner references and check image generation and Word rendering.
4. Paste the [batch prompt](WORKFLOW_PROMPT.md) into the Codex project chat and replace the example with your games and community lines. You can also attach schedule and line screenshots.

Once configured, the schedule and the community lines are the only routine inputs. The coordinator shares schedule and box-score data, delegates one game per worker, and verifies the combined delivery. The project allows up to three workers at a time. Add more games to the same batch to queue them.

Your community lines govern the guide. Comparable Polymarket markets are optional context; no Polymarket token is required. The default settlement covers the full game, including overtime. All dates and times use Philippine Time (PHT), including both date fields on the banner.

## Repository map

- [Operations manual](OPERATIONS.md) and [copy-ready workflow prompt](WORKFLOW_PROMPT.md)
- [Workflow skill](.agents/skills/nba-world-picks-workflow/SKILL.md), [runtime checks](.agents/skills/nba-world-picks-workflow/references/runtime.md), and [banner prompt](.agents/skills/nba-world-picks-workflow/references/banner-prompt.md)
- [Project concurrency](.codex/config.toml) and [game worker role](.codex/agents/nba-match-worker.toml)
- [Schedule preload](scripts/preload_slate.py), [official team logo index](assets/team-logos.json), and [banner configuration](assets/reference/banner.toml)
- [Third-party credits and licenses](THIRD_PARTY.md)

Keep personal assets, credentials, generated picks, and caches local. The root [`.gitignore`](.gitignore) excludes the default locations. This project prepares files for manual posting.
