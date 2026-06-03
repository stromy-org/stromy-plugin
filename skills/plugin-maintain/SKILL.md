---
name: plugin-maintain
description: "Maintain the stromy Claude Code plugin for Stromy — wire MCP skill stubs, refresh client-data overlay, add example skills, bump version, push to its marketplace. Use whenever the user wants to extend, modify, or maintain this plugin — even if they don't say 'plugin' explicitly. Triggers on: 'wire skill', 'expose skill', 'add stub', 'refresh client data', 'rebrand the plugin', 'bump plugin version', 'release plugin', 'update marketplace pointer', or any request to change this plugin's behavior."
---

# Plugin Maintain — stromy

Source of truth for maintaining the **stromy** Claude Code plugin (client: Stromy). Authored in `claude-plugin-template`; synced into every plugin satellite and into `stromy-org/.claude/skills/plugin-maintain/`.

## When to use

- Wiring a skill stub that points at an MCP-hosted skill.
- Refreshing the client-data overlay (`companies/stromy/`).
- Adding a local skill (rare — most skills live in MCPs).
- Bumping plugin version and pushing to the matching marketplace.
- Rebranding (e.g., new logo, new brand tokens) — usually just re-runs the sync.

## When NOT to use

- Creating a new plugin → `repo-scaffold client-plugin <slug>` at org level.
- Building a brand from scratch → `brand-builder`.
- Cross-repo client work spanning MCP+plugin+marketplace → `client-package`.

## Repo layout (recap)

```
stromy/
├── .claude-plugin/
│   └── plugin.json             # Plugin manifest (required by Claude Code)
├── AGENTS.md                   # Source of truth
├── skills/
│   └── <skill>/SKILL.md        # Stubs (~25 lines) — wrappers fetching live SKILL.md from an MCP
├── companies/
│   └── stromy/      # Brand + company data (synced from client-data/)
│       ├── charter.json
│       ├── brand/
│       └── assets/
├── pyproject.toml              # (if Python helpers needed)
├── package.json                # (if Node helpers needed)
└── scripts/
    └── render-agent-md.py
```

## Workflows

### Wire a skill stub from an MCP

1. Confirm the source: MCP name + skill name (e.g., `nl-gov-data` + `dutch-gov-data`).
2. Create `skills/<skill>/SKILL.md` as a stub:
   ```markdown
   ---
   name: <skill>
   description: <copy from MCP's live SKILL.md frontmatter>
   ---
   This skill lives in the `<mcp>-http` MCP server. Read the live SKILL.md via
   `ReadMcpResourceTool(server="<mcp>-http", uri="skill://<skill>/SKILL.md")`
   before performing any task. Brand context resolves from
   `companies/stromy/`.
   ```
3. Add an entry (or extend an existing one) in `stromy-org/sync-manifest.json` `mcp-skill-mirrors`, appending `stromy` to the `plugins` list.
4. From `stromy-org`: `./scripts/sync.sh mcp-skill-stubs --check` — confirms the stub matches the canonical format.

(Step 2 is normally done by the sync script — only do it by hand if you're bootstrapping a new mirror entry.)

### Refresh client-data overlay

```bash
cd <stromy-org-root>
./scripts/sync.sh client-data
```

Sync pulls from `client-data/clients/stromy/` into `companies/stromy/` here. Commit via `/conventional-commit`.

### Add a local skill (rare)

Most skills should live in an MCP. Use this path only when:
- The skill has no need for IP protection.
- It has no expensive dependencies (everything runs in the agent).
- It will only be used by this single plugin.

1. Create `skills/<skill>/SKILL.md` with full content (no stub).
2. Add to `skills/` directory.
3. Test the trigger in a fresh Claude Code session.

### Bump version & push to marketplace

1. Update `version` in `.claude-plugin/plugin.json`.
2. Commit via `/conventional-commit`.
3. In the matching marketplace repo (`stromy-marketplace`), update `marketplace.json` to point at the new plugin commit/tag.
4. Push both, then bump submodule pointers in stromy-org.

## Critical rules

- **Stubs are tiny.** A plugin SKILL.md should be ~25 lines — frontmatter + a paragraph telling the agent to fetch the live SKILL.md. If a plugin skill is large, it should probably live in an MCP instead.
- **`companies/stromy/` is synced, not authored.** Edits must happen in `client-data/clients/stromy/`, then propagate via `sync-client-data.sh`.
- **`plugin.json` lives at `.claude-plugin/plugin.json`**, not at the repo root.
- **AGENTS.md is canonical.** Edit AGENTS.md, regenerate `CLAUDE.md` and `.github/copilot-instructions.md` via `python3 scripts/render-agent-md.py`.

## Reference

- Stub pattern reference: `MCPs/nl-gov-data/.claude/skills/dutch-gov-data/SKILL.md` (canonical example)
- Plan: `stromy-org/SCAFFOLDING_REFACTOR_PLAN.md` §5 (sync pipelines), §5b (client deployment)
- Plugin standards: `stromy-org/.claude/skills/plugin-creator/references/plugin-standards.md` (until plugin-creator is sunset in Phase 5)
- Template source: `stromy-org/scaffolds/claude-plugin-template/template/skills/plugin-maintain/SKILL.md.jinja`
