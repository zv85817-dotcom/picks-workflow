# NBA World Project Instructions

When a request contains NBA fixtures, community lines, game guides, or game banners, follow the [NBA World Picks Workflow](.agents/skills/nba-world-picks-workflow/SKILL.md). Answer questions about the method directly when production is not requested.

The coordinator owns the batch, verifies shared inputs, and reviews delivery. Only the coordinator delegates. Assign one `nba-match-worker` per game, with up to three workers active at a time. Workers handle only their assigned game and return their files and verification status to the coordinator.
