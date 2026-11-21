# Operations Manual

## Set up a project

Open the repository root in Codex and keep the hidden `.agents` and `.codex` directories intact. Trust the project so Codex can load its configuration. The repository includes three skills: NBA World Picks Workflow, Writing NBA Previews, and OpenAI ImageGen. You do not need to copy them into your personal skills directory.

Check access to public NBA data, Python 3.11+, image generation with reference input, and a Word renderer. Use the official Documents capability when available; local Word or LibreOffice can also be used for rendering. Presentations is only needed for an editable PowerPoint banner template. The bundled ImageGen skill contains instructions and an optional API helper. The helper requires separate credentials stored in the local environment. The normal workflow can use the available built-in image tool.

## Configure and replace banner references

1. Place your original presenter image at `assets/reference/presenter.png`.
2. Optionally place an approved layout sample at `assets/reference/layout.png`. Without one, use the default layout in the [banner prompt](.agents/skills/nba-world-picks-workflow/references/banner-prompt.md).
3. Copy [banner.toml](assets/reference/banner.toml) to `assets/reference/banner.local.toml` and enter the presenter name. Update the paths for JPGs, other filenames, or files outside the repository. Relative paths are resolved from the project root. Use `style_notes` for approved changes to the layout or appearance.

Each banner uses the original presenter image and both official team marks. The layout sample constrains composition, colors, text placement, and crop margins. Replacing that sample is how you change the visual reference. Keep the sample separate from the source image and do not edit a previous banner into the next one.

## Run a batch

Paste the [batch prompt](WORKFLOW_PROMPT.md) in Codex. For each matchup, supply the Philippine game date, away and home teams, the Spread with the team and sign for each side, and the Over/Under threshold. The coordinator validates the official tipoff and uses it in both the guide and banner. The default settlement includes overtime. If a community line is pending, the guide can start with an independent projection and be updated later.

The coordinator preloads shared data and delegates one match per worker. You can also run the preload yourself from the repository root after replacing `YYYY-MM-DD`:

```sh
python scripts/preload_slate.py YYYY-MM-DD --match POR-NYK
```

Repeat `--match AWAY-HOME` to select more games on the same date. Omit it for the entire slate. Check `work/<PHT-date>/_prep/slate.json` for missing games, sample sizes, and data errors. If an upstream page is unavailable, verify the missing facts from official sources before using them.

## Verify and deliver

- Check team order, event label, PHT tipoff, the Spread signs and threshold, the Over/Under threshold, and settlement terms against the shared match record.
- Confirm the guide explains how the most relevant matchup, rotation, rest, and pace evidence affects the margin or total. Keep the conclusions under **Results** at the bottom. Verify agreement between Word, text, and charts.
- Render the Word document and inspect each page. If rendering is unavailable, flag it as pending review. Verify the banner's English text, team marks, both PHT game dates, and readability after a mobile crop and overlay simulation. If image generation or the presenter image is unavailable, return the written guide and banner prompt and list what is missing.
- Retrieve files from `output/<PHT-date>/<AWAY-HOME>/`. Deliverables are named by matchup and PHT date. Copy the text for your post and attach its banner and images as needed.

When only the community lines change, recheck the analysis, results, and affected charts. When the teams, event label, or tipoff change, update the shared record and regenerate both the affected guide and banner.

## Before sharing this repository

Run `git status --short` and inspect the proposed files. Keep source portraits, layout samples, credentials, database files, caches, and outputs out of Git. Preserve the project configuration, skill directories, and [third-party credits](THIRD_PARTY.md).
