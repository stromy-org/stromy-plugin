---
name: do-guide
description: "Guía de inicio para investigar el gobierno, el gasto público y la legislación de República Dominicana — qué pedir, qué es excepcionalmente fuerte en esta fuente y qué no existe, qué salvedades esperar, y cómo un hallazgo se convierte en un documento con tu marca. Usar cuando alguien pregunte «cómo investigo contrataciones/gobierno/leyes de República Dominicana», «qué puede hacer esto con datos dominicanos», «cómo empiezo con los datos de RD», o cualquier pregunta de orientación sobre investigación de asuntos públicos dominicanos. Use for \"how do I research Dominican government data\", \"what can this do for the DR\", or any orientation question about Dominican public-affairs research. Enruta al flujo correcto y entrega a las herramientas de documento; no produce documentos por sí misma. Para instalar el plugin o encender conectores por primera vez, la puerta de entrada es `getting-started`."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/do-gov-data/skills/do-guide/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# Guía DO — cómo investigar datos públicos dominicanos (MCP-hosted skill)

This skill's full instructions are hosted on the `do-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `do-gov-data` MCP with `path="skills/do-guide/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/do-guide"` (and `path="skills/do-guide/references"`),
   → call `fs_read` with `path="skills/do-guide/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `do-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `do-gov-data` MCP is slow to respond

This server scales to zero to save cost, so the first call after an idle period wakes the container — typically ~10–30s, and up to ~1–2 min for a heavier image (media / browser tier). If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
