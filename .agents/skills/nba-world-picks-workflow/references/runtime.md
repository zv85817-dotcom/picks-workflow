# Skills and Runtime

Check the capabilities needed for the batch. Reuse the results until the environment changes.

| Task | Resource | Use |
| --- | --- | --- |
| Guide research | [Writing NBA Previews](../../writing-nba-previews/SKILL.md) | Reuse the evidence and matchup methods. Follow this project's English format, chart requirements, and results placement. |
| Banner | [OpenAI ImageGen](../../imagegen/SKILL.md) | Prefer the available built-in reference image tool. The bundled upstream skill documents options; a skill file alone does not provide an image service. |
| Word output | Official Documents capability | Generate Word and inspect rendered pages. Local Word or LibreOffice is also suitable for rendering. |
| Editable PowerPoint template | Official Presentations capability | Use only when requested. The default banner is PNG. |

The coordinator checks Python 3.11+, public NBA schedule and injury sources, Word rendering, reference-based image generation, and the source portrait. Record capability availability separately from successful output. If a tool is available only to the coordinator, the worker sends the inputs and prompt to the coordinator, then checks the result.

Codex discovers project skills under `.agents/skills/` and loads the trusted project settings from `.codex/`. Documents and Presentations are provided by the relevant installed runtime. If using the upstream ImageGen API helper, configure credentials locally as documented.

If image assets or tools are missing, deliver the available guide and banner prompt. Mark any Word output awaiting visual inspection as pending review and explain what was unavailable.
