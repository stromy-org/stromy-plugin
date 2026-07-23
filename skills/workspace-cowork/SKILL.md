---
name: workspace-cowork
description: "Work safely on co-edited artifacts in a shared workspace or SharePoint collaboration space. Use when asked to publish to the space, fetch the latest version, review or edit a shared client deliverable, process comments, or co-edit a workspace file."
license: Proprietary. LICENSE.txt has complete terms
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-local-skills.py (operator-run: ./scripts/sync.sh local-skills)
  Source:      workspace-studio/.claude/skills/workspace-cowork/SKILL.md
  This file is a mirror of its canonical source. A local edit here will be
  overwritten by the next mirror run. Edit the source, then:
    ./scripts/sync.sh local-skills
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# Workspace Co-work Protocol

Apply this protocol only when the session can reach SharePoint through an M365
workspace connector, the ms365 MCP, or an equivalent tool **and** the task
touches an artifact in a shared collaboration space. Otherwise state that this
protocol does not apply and stop using it.

This skill is self-contained. It does not call or activate other skills.
`m365-manager` and `project-publish` are related operator-side context only.

## Normative protocol

1. **The workspace is the source of truth.** The shared copy is the artifact.
   Never make a local fork the new truth or deliver around the workspace.
2. **Fetch latest before every use.** Before reading, editing, building on, or
   reviewing an artifact, fetch its current version and record its version/eTag
   in the run notes. A previously opened copy is stale until re-fetched.
3. **Write back in place.** Keep the same path and filename; SharePoint version
   history is the audit trail. For metadata updates send `If-Match` with the
   fetched eTag. On **412 Precondition Failed**, re-fetch, re-apply the intended
   change once, and retry once. If it conflicts again, surface the conflict.
   After every write, read the item back and verify its version and size.
4. **Treat locks as contention.** There is no supported lock-probe API. A
   **423 Locked** response or `resourceLocked` error means retryable contention,
   often from a browser or desktop editor. If this flow created an upload
   session, cancel that exact session first by deleting its `uploadUrl`; a
   direct `PUT /content` creates no session and has nothing to delete. Retry
   only after 2s, 5s, and 15s. If still locked, name the exact file and ask
   people to close editing copies, or explicitly queue/defer the write. Never
   wait indefinitely or silently switch delivery channels.
5. **Prevent avoidable contention.** Give reviewers `read` access by default
   when an artifact will be republished; reserve `write` for real co-editors.
   Humans close editing copies before an agreed publish window. Agents follow
   open → work → close and never hold long-lived editing sessions. This reduces
   contention but does not guarantee that SharePoint will never lock a file.
6. **Honor the feedback loop.** In-file comments are directional feedback for
   the next run. Small direct human edits are allowed and must survive. Union
   unresolved comments with the task list; human wording wins on overlap. Mark
   or report processed comments so the loop stays auditable.
7. **Keep records in the space.** Every project keeps a
   `Meeting Transcripts/` folder with dated `YYYY-MM-DD <topic>.md` files.
   Treat those transcripts as shared reference material and agent-run input.
8. **Surface blockers; never branch the document.** Report a blocked write,
   lost lock race, or unmergeable edit to the humans. Never silently supersede
   the workspace copy with a private version.

## Mechanics

- Direct Graph `PUT /content` supports files up to 250 MiB. Prefer an upload
  session above 10 MiB when the available tool supports resumable upload.
- The single-purpose ms365 tools (`upload-file-content`,
  `create-upload-session`, and `move-rename-onedrive-item`) do not expose an
  `If-Match` parameter. Use `graph-batch` with a raw per-request
  `headers: {"if-match": "<etag>"}` field for a conditional metadata `PATCH`.
- Use `includeHeaders: true` with `graph-batch` when the response headers are
  needed to capture the new eTag for the next fetch-latest step.
- A 412 is a stale-version conflict; a 423 or case-insensitive
  `resourceLocked` is lock contention. They require different recovery paths.
- Delete only an upload session created by the current flow, and only through
  the exact pre-authorized `uploadUrl` returned for that session.
