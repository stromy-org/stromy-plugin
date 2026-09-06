---
name: do-transparency-requests
description: "Investigar el sistema dominicano de acceso a la información pública (SAIP, Ley 200-04): qué le han preguntado ya a una institución, qué respondió literalmente, cuánto tarda, qué niega y con qué motivo, y a quién dirigirse para pedir información oficial. Cubre ~131.000 solicitudes en 345 instituciones desde 2016 y el directorio de las 359 Oficinas de Acceso a la Información (OAI). Usar para «¿alguien ya preguntó esto?», «¿qué contestó tal ministerio?», «¿esta institución responde en plazo?», «¿a quién le escribo para pedir X?», transparencia, derecho de acceso, Ley 200-04, o antes de redactar una solicitud de información. Use for Dominican freedom-of- information requests, SAIP, right-to-information research, or public-body responsiveness."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/do-gov-data/skills/do-transparency-requests/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# do-transparency-requests — acceso a la información (Ley 200-04) (MCP-hosted skill)

This skill's full instructions are hosted on the `do-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `do-gov-data` MCP with `path="skills/do-transparency-requests/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/do-transparency-requests"` (and `path="skills/do-transparency-requests/references"`),
   → call `fs_read` with `path="skills/do-transparency-requests/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `do-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `do-gov-data` MCP is slow to respond

This server scales to zero to save cost, so the first call after an idle period wakes the container — typically ~10–30s, and up to ~1–2 min for a heavier image (media / browser tier). If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
