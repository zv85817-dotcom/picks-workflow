# Banner Generation Prompt

Fill the variables from the verified match record. Both date fields use the same PHT game date, for example NOV 22, 2026. Use NBA or NBA CUP as confirmed on the schedule. Show a 12-hour tipoff with PHT. Pass the original portrait, official away logo, then official home logo as generation references. Use the effective presenter_name. Use layout_reference to review composition, colors, type hierarchy, and CTA placement. Generate from the original portrait and logos each time; never use the sample as a base image. Use the approved style_notes for intentional layout changes; otherwise only change the match variables.

## Image Prompt

> Create a new NBA World game guide banner using the original portrait of {PRESENTER_NAME}, the official {AWAY_TEAM} primary logo and the official {HOME_TEAM} primary logo as your three image references. Use a landscape 16:9 composition like the approved 1672 × 941 reference. Keep the source proportions of the face, body and logos. Choose an available export size that preserves the composition.
>
> Set the scene in a deep blue basketball arena. On the left, show a photographic half-length {PRESENTER_NAME} wearing a navy blazer and a white T-shirt, with a lapel mic and tablet. Match the original identity and preserve natural eyes, teeth, smile and hands. Put a compact navy nameplate with a thin red accent around x = 12–32%, y = 59–68%. Print “PRESENTED BY” and “{PRESENTER_NAME}” on separate lines.
>
> Compose all essential elements inside x = 10–88%, y = 13–69%. Keep the bottom 30% free of text, logos, buttons and plaques. Fill it naturally with the arena, court or lower part of the pose. This space accommodates the app’s crop and its title and page-number overlay.
>
> On the right, use “TODAY’S” and “GAME PICKS” as a compact heading. Place “GUIDE EDITION” with “{GAME_DATE_PHT}” at upper right. In the matchup row, show the official {AWAY_TEAM} logo on the left, “VS” in the center and the official {HOME_TEAM} logo on the right. Keep the logo row within x = 50–87%, y = 27–43%. Use compact, balanced logo sizes and retain the colors and geometry of the official marks. Use the two marks as the team identifiers.
>
> Below the matchup, print “{EVENT_LABEL} · {GAME_DATE_PHT}” and then “{TIPOFF_PHT}”. Add a red rounded “VIEW FULL GUIDE” button with a right-pointing arrow, fully inside x = 53–86%, y = 61–69%. Render only the listed English copy. Deliver the final image with the reserved overlay area clear.

Integrate approved style_notes into the relevant instructions and resolve any conflicts. Keep the PHT date and platform safe-area rules. Use the schedule, team marks, and presenter configured for this game.

## Export Checks

- Compare the result with the approved sample or default layout. Check composition, main color, text hierarchy, placement, and bottom clearance. Regenerate from the originals for unapproved deviations and mark unresolved versions as pending revision.
- Check logo order, event label, both dates, tipoff, and English spelling against the match record. Preserve the aspect ratio; recompose if the platform dimensions change.
- Simulate the crop using the actual slot or a current platform screenshot. Otherwise use an approximately 2.065:1 center crop and simulate the bottom title and page number. Check that logos, schedule, nameplate, and button remain readable. Inspect the face, teeth, hands, and logos for distortion. Distinguish simulated checks from verification on the actual platform.
- Export PNG as Away-vs-Home_Banner_YYYY-MM-DD_vNN.png and retain earlier versions. Use the PHT game date in the filename.
