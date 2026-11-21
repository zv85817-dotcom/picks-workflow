---
name: writing-nba-previews
description: Use when writing NBA game previews, betting-style predictions, matchup watch points, Chinese sports articles, or article cover image prompts/generation for upcoming NBA games.
---

# Writing NBA Previews

## Overview

Create current, source-grounded NBA previews in Chinese, with clear predictions, matchup angles, and a usable article cover direction. Treat roster status, odds, standings, and schedules as live information that must be verified before writing.

## Core Workflow

1. Confirm the game: teams, venue, tipoff date/time, competition context, and whether it is regular season, play-in, playoffs, Summer League, preseason, or NBA Cup.
2. Gather current data from reliable sources before making claims: official NBA pages, team injury reports, reputable beat reports, odds/sportsbook pages if betting lines are requested, and recent box scores or standings.
3. Build the preview around the most decision-relevant factors: availability, rest/travel, matchup style, recent form, coaching adjustments, standings pressure, and late-game execution.
4. Separate facts from judgment. Say "based on current reports" or "if X plays" when availability is uncertain.
5. Write in polished Chinese sports-media style: energetic, concrete, and analytical; avoid empty hype and unverifiable rumors.
6. Include a cover image concept. If the user asks to generate the cover, use the image generation tool after drafting a safe, specific visual prompt.

## Article Shape

Use this default structure unless the user requests another format:

- Title: concise, conflict-driven, and specific to the matchup.
- Lead: 2-3 sentences explaining why the game matters now.
- Matchup background: standings, recent form, schedule pressure, season series, and context.
- Key watch points: 3-5 angles, each with evidence and likely impact.
- Prediction: winner, score range or margin, confidence level, and conditional caveats.
- Betting/risk note: only when relevant; frame as analysis, not guaranteed advice.
- Cover image: one prompt-ready concept plus optional headline text.

For more structure options, read `references/article-structure.md`.

## Prediction Discipline

Prioritize these inputs, roughly in order:

| Input | How to use it |
| --- | --- |
| Player availability | Injuries, minutes limits, back-to-back management, suspensions |
| Matchup mechanics | Pick-and-roll coverage, rim pressure, three-point volume, transition defense, rebounding |
| Recent form | Last 5-10 games, but account for opponent quality and roster changes |
| Rest and travel | Back-to-back, altitude, road trip length, time-zone shifts |
| Stakes | Playoff seeding, elimination pressure, rivalry, tanking/rest incentives |
| Market signal | Use odds only as one data point; do not outsource the conclusion to the line |

Avoid pretending precision. Use probability language such as "slightly favors", "upset path", "swing factor", and "high-variance matchup".

## Cover Image Direction

For covers, favor editorial sports art over literal copyrighted branding:

- Use team colors, city cues, arena lights, hardwood texture, scoreboard drama, silhouettes, jersey-number hints, and matchup symbolism.
- Avoid official NBA/team logos unless the user supplies licensed assets or explicitly requests brand-accurate work they have rights to use.
- Avoid generating a realistic likeness of a named player unless the user explicitly requests it and policy/tooling allows it.
- Leave negative space for headline text if the image will be used as an article thumbnail.

For prompt templates and variants, read `references/cover-image-prompts.md`.

## Output Checklist

Before finalizing:

- Verify dates, tipoff time, injuries, and standings are current.
- Name sources or provide links when web research was used.
- Make the prediction conditional when injuries or rest decisions are unresolved.
- Include at least one non-obvious tactical watch point.
- Keep the cover prompt visually specific and usable by an image generator.

## Common Mistakes

- Writing from memory when the schedule, injuries, odds, or standings may have changed.
- Treating last-game performance as a trend without checking opponent strength and roster context.
- Making betting advice sound guaranteed.
- Generating a cover that depends on protected logos, exact jerseys, or unlicensed player likenesses when a symbolic editorial image would work better.
