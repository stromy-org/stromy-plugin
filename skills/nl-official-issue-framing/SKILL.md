---
name: nl-official-issue-framing
description: "Analyze how a named subject — a company, product, organisation, technology, sector, or specific policy issue — is framed in official Dutch government and parliamentary records through nl-gov-data. Use this whenever the user wants official-source reputation or issue framing for a specific entity or issue: how an organisation is portrayed, how a product or technology is treated in policy, how a contested issue is characterised, what reputational risks surface in official records. Sector domain packs (e.g. pharma/medicine — Novo Nordisk, GLP-1s, Wegovy, Ozempic, semaglutide, reimbursement, shortages, package management) supply ready keyword banks, default frames, and legal anchors. Produces narrative analysis, mention/context tables, issue maps, PA/PR implications, and DOCX-ready source appendices."
---

# Dutch Official Issue & Entity Framing (MCP-hosted skill)

This skill's full instructions are hosted on the `nl-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `nl-gov-data` MCP with `path="skills/nl-official-issue-framing/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/nl-official-issue-framing"` (and `path="skills/nl-official-issue-framing/references"`),
   → call `fs_read` with `path="skills/nl-official-issue-framing/references/<file>"`.

Follow the instructions returned by the MCP exactly.
