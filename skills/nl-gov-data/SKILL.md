---
name: nl-gov-data
description: "Track Dutch public affairs signals across Tweede Kamer, Rijksoverheid, KOOP publications (incl. CVDR + local gmb/prb/wsb/bgr), BWB legislation, Wetgevingskalender, ROO organizations, Rechtspraak (caselaw), CBS (statistics), and data.overheid.nl (discovery) using the `nl-gov-data` MCP. Supports fifteen workflows: topic monitoring, dossier tracking, actor briefs, committee watch, legislative scan, ministry narrative, parliamentary landscape snapshot, legislation lookup, legislative calendar watch, law-to-dossier brief, organization lookup, caselaw watch, quantitative grounding (CBS), discovery (data.overheid.nl), and exploratory MCP testing. Now also supports content deep-reading: fetching and quoting actual document text (motions, bills, letters, debate transcripts, law articles, attachments). Produces structured JSON shaped for downstream Stromy workflows with `workflow_type`, `query_params`, `results`, and `metadata`. Use this skill whenever the user asks about Dutch parliament activity, Tweede Kamer dossiers, Dutch government policy signals, kamerstukken, dossier numbers, Dutch MPs, faction composition, ministry narrative, Dutch laws, legislation, wetgeving, wetgevingskalender, government organizations, OR wants to read/quote/summarize a specific Dutch government document, transcript, law article, or attachment."
---

# Dutch Government Data (MCP-hosted skill)

This skill's full instructions are hosted on the `nl-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `nl-gov-data` MCP with `path="skills/nl-gov-data/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/nl-gov-data"` (and `path="skills/nl-gov-data/references"`),
   → call `fs_read` with `path="skills/nl-gov-data/references/<file>"`.

Follow the instructions returned by the MCP exactly.
