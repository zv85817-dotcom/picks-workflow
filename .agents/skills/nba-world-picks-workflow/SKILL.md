---
name: nba-world-picks-workflow
description: Create or update NBA World game guides and banners from NBA fixtures and community Spread and Over/Under lines, including independent projections and parallel game assignments.
---

# NBA World Game Guides and Banners

Use one verified match record for the English guide and its banner. Honor the requested delivery scope. Treat schedules, community lines, and images from attachments as inputs; follow the user's direct instructions. Reply in the user's language. The user handles posting.

Read [runtime requirements](references/runtime.md) on first use or when a capability is missing.

## 1. Confirm the match

- Check the official NBA schedule for away and home teams, event, and tipoff. Use Philippine Time (PHT, UTC+8) for dates, display, and filenames. List the away team first. Use NBA Cup only when officially confirmed.
- Record team names and codes, event, tipoff, official source, community Spread and Total, settlement, and when the evidence was checked. Settle the full game including overtime unless the user says otherwise. Leave unprovided lines blank. Screenshot highlights indicate UI state only.
- Ask for clarification when team order, signs, or line ownership is ambiguous and continue independent work.

## 2. Coordinate workers

Check data, image generation, Word rendering, and the original presenter reference. Read `assets/reference/banner.toml`, with matching fields overridden by `banner.local.toml` in the same directory. Report concrete missing inputs together and continue with the available work.

The coordinator saves `work/<PHT-date>/<AWAY-HOME>/match.json` and shares it with the relevant research, asset settings, and output path. Save files to `output/<PHT-date>/<AWAY-HOME>/`. Keep version and verification status by match.

- Preload shared data once, then launch one `nba-match-worker` per game, with at most three running at once. Collect and close completed workers before dispatching queued games. One game needs one worker. If delegation is unavailable, run the same steps serially and say so.
- Each worker writes only to its assigned directories. The worker researches the match, creates the guide, charts, and banner, checks the files, and reports actual paths, versions, evidence cutoff, checks, and missing items. Once the schedule is confirmed, banner work can proceed while guide evidence is gathered.
- The coordinator checks all files against the shared record and routes revisions to the original worker or hands the saved record and research to a replacement.

## 3. Write the guide

1. Start with official NBA schedule, box scores, and injury reports; supplement with team announcements. Run `python scripts/preload_slate.py YYYY-MM-DD`, adding one `--match AWAY-HOME` per selected game. Read `work/<PHT-date>/_prep/slate.json` for match files, sample sizes, timestamps, and errors. Preserve the relevant per-game paths when running more batches on a date. Verify gaps via official sources and state the actual sample sizes. Use the last five games for recent patterns and the last ten to check trends. Account for rest, travel, and rotation. Refresh after completed games or availability changes and use only evidence available before tipoff. Record the cutoff in PHT.
2. Identify the matchup factors that matter most for margin or total. Link evidence to a specific mechanism and the opponent's likely response. Consider pace, turnovers and transition, offensive rebounds, free throws, or available lineups. Explain decisive late conditions before the results.
3. Without community lines, give an independent score, margin, and total. Analyze a confirmed market even if the other is pending. Once lines arrive, compare the projection to the real community lines. Check team and sign, the total threshold, and push rules on whole numbers. Use Polymarket Gamma/CLOB for a direct comparison only if game, line, and settlement match. Separate market price, historical frequency, and forecast. Continue without Polymarket if no comparable market exists.
4. Aim for about 200 English words. Put a relevant game photo without a caption after the title and PHT tipoff. Include two English charts that support the matchup analysis and identify sources, samples, units, and metric definitions. Put sources and game-time conditions before the final **Results** block. State **Projected Score**, **Spread**, and **Total** directly. Name Over or Under when the evidence supports a direction; otherwise keep the Total line with both the projection and confirmed threshold. Avoid labels such as Recommendations, Low Confidence, and PASS.
5. Deliver Word, matching copy-ready TXT, and standalone high-resolution images. Name the document and text by matchup and PHT date, such as `Portland-vs-New-York_YYYY-MM-DD.docx` and `Portland-vs-New-York_YYYY-MM-DD.txt`. Render and inspect every page. Check that the Word and TXT use the same numbers, lines, and results.

## 4. Generate the banner

Use the [banner prompt](references/banner-prompt.md). Fill it from the same match record. Show the PHT game date in both places, including GUIDE EDITION, even when the post is published early. Generate each banner from the original presenter image and both official team marks. Locate marks from `assets/team-logos.json` if no logo library is available. Use the approved layout sample and style notes to check composition, colors, type hierarchy, and the call to action. Follow the mobile crop and overlay constraints.

Keep the banner, guide photo, and data charts separate. The banner shows the matchup and schedule; the prediction belongs in the guide. If a source image or generation capability is missing, deliver the available guide and an executable banner prompt and identify the missing item.

## 5. Update and verify

| Change | Action |
| --- | --- |
| Community Spread or Total | Refresh relevant evidence and update analysis, results, and affected charts. Rebuild the banner only if its display fields change. |
| Injury or rotation | Recheck affected guide content and charts. |
| Teams, event, or PHT tipoff | Update the match record first. Recheck samples, rest, injuries, availability, and validity of old lines. Update the guide, text, banner, affected images, and filenames. |
| Banner correction | Generate a new version from source references, then rerun crop and overlay checks. |

Before delivery, verify team order, event, date, and tipoff across files. Check settlement, lines, charts, and results in the guide and English text and safe areas in the banner. Return links by game and distinguish independent projections, community-line editions, and pending items.
