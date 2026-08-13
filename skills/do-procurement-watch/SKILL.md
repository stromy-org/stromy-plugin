---
name: do-procurement-watch
description: "Monitorear y analizar contrataciones públicas dominicanas: seguimiento de licitaciones por institución o rubro, historial completo de adjudicaciones de un proveedor, concentración de contratos, banderas de integridad (proveedores inhabilitados, adjudicación repetida a un mismo RPE, uso de modalidades excepcionales), y contraste entre el plan anual de compras y lo efectivamente licitado. Usar para vigilancia de licitaciones, perfil de proveedor, «quién gana los contratos de X», concentración de gasto, señales de riesgo en compras públicas, o cualquier pregunta de integridad sobre contrataciones en República Dominicana. Use for Dominican procurement monitoring, DR tender watch, supplier award history, or procurement integrity screening."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/do-gov-data/skills/do-procurement-watch/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# do-procurement-watch — vigilancia de contrataciones públicas (MCP-hosted skill)

This skill's full instructions are hosted on the `do-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `do-gov-data` MCP with `path="skills/do-procurement-watch/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/do-procurement-watch"` (and `path="skills/do-procurement-watch/references"`),
   → call `fs_read` with `path="skills/do-procurement-watch/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `do-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `do-gov-data` MCP is slow to respond

This server scales to zero to save cost, so the first call after an idle period wakes the container — typically ~10–30s, and up to ~1–2 min for a heavier image (media / browser tier). If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
