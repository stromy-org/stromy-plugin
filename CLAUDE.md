<!--
  GENERATED FILE — DO NOT EDIT.
  Source of truth: AGENTS.md (cross-vendor standard).
  Override file:   .agent-overrides/claude.md (optional, appended below)
  Regenerate with: scripts/render-agent-md.py
-->

# AGENTS.md — stromy

Canonical, self-contained instructions for any coding agent (Claude Code, Codex CLI, Gemini CLI, GitHub Copilot) working in this plugin repo.

> **AGENTS.md is the canonical instruction file** for this repo (cross-vendor standard).
> `CLAUDE.md` and `.github/copilot-instructions.md` are generated from this file by
> `scripts/render-agent-md.py`. Gemini CLI reads this file directly via
> `context.fileName: ["AGENTS.md"]` in `.gemini/settings.json`. **Do not hand-edit
> the generated files.**

## Overview

stromy is a Claude Code plugin for Stromy. It is a **distribution artifact** — skills are authored in Cowork and cherry-picked here for client deployment.

## Repository Structure

```
stromy/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/                   # Deliverable skills (from Cowork)
├── companies/stromy/  # Brand data (charter, logos, colors)
├── src/                      # Shared workspace utilities
│   ├── workspace.js
│   └── workspace.py
├── package.json              # Node.js dependencies
├── pyproject.toml            # Python dependencies
├── hooks/
│   └── hooks.json            # Lifecycle hooks
├── settings.json             # Default permissions
├── .github/
│   ├── CODEOWNERS
│   └── dependabot.yml
├── LICENSE
└── README.md
```

## Brand Architecture

This plugin defaults to **Stromy** brand data at `companies/stromy/`. Skills read `charter.json`, `logos/`, `images/`, and `tokens.css` from this path automatically — no prompt-time client selection needed.

For collaborative brands (e.g., "Stromy x Partner"), skills fall back to the Stromy charter for any missing fields.

**Slug discipline (`client_slug` is `stromy`):**
The `companies/<slug>/` folder name MUST match the corresponding folder in `client-data/clients/` (the source of truth). Compound client names drop hyphens in the data slug — `client-data/clients/dukestrategies/`, not `duke-strategies/`. When syncing brand data via `scripts/sync-plugin-brand.sh` or onboarding a new client, copy the directory name verbatim from `client-data/clients/`. The plugin repo's `clients/<client-slug>/` parent folder uses kebab form for the GitHub repo path; this is a different slug from `companies/<slug>/`. See `stromy-org/.claude/rules/org-patterns.md` § "Client slug convention" for the full two-tier rule.

## Commands

```bash
npm install                    # Install Node dependencies
uv sync                        # Install Python dependencies
claude --plugin-dir .          # Test locally
claude plugin validate .       # Validate plugin structure
```

## Updating Skills

Skills are maintained in Cowork and cherry-picked into this plugin:

1. Update the skill in `Cowork/.claude/skills/<skill-name>/`
2. Copy updated files to `skills/<skill-name>/`
3. Re-apply portability transforms (`.claude/companies/` → `companies/`, etc.)
4. Bump version in `.claude-plugin/plugin.json` and `package.json`

## Key Rules

- All paths are plugin-relative: `companies/`, `skills/`, `src/` — never `.claude/companies/` or `.claude/skills/`
- Node requires are flat: `require('pkg')` not `require('../../../../node_modules/pkg')`
- Workspace imports: `require('../../src/workspace')` (2 levels from skill scripts)
- Default brand: `companies/stromy/` — hardwired, no discovery needed

## Agent-md & MCP rendering

This repo treats `AGENTS.md` and (optionally) `.agents/mcp.json` as the only authored sources. Run:

```bash
python scripts/render-agent-md.py            # CLAUDE.md + .github/copilot-instructions.md
python scripts/render-agent-md.py --check    # exit 1 if stale
python scripts/render-mcp.py                 # .mcp.json + .gemini/settings.json mcpServers + .codex/config.toml + .vscode/mcp.json
python scripts/render-mcp.py --check         # exit 1 if stale
```

**Never hand-edit** `CLAUDE.md`, `.github/copilot-instructions.md`, or any of the four per-agent MCP files — they all carry a "GENERATED FILE" banner; edits are wiped on next render.
