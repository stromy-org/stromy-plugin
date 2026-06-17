---
name: research-apify
description: "Agent-driven web research and data extraction backed by the official Apify MCP, bring-your-own-key (BYOK). Use when the user wants to gather data on a topic from the web, search the live web for current information, scrape or crawl a website or a list of URLs, or extract structured records (directory listings, product specs, profiles) — and turn the results into a branded deliverable. Drives a short list of vetted Apify actors with hard per-run caps and a confirm-before-large-pull step, reshapes the dataset into the standard {workflow_type, query_params, results, metadata} envelope, then hands the envelope to a format-* skill (format-docx, format-pdf-hd) for the branded document. Triggers on: web research, gather data on a topic, scrape, crawl a site, extract structured data from URLs, data extraction, web data, competitor/market scan."
license: Proprietary. LICENSE.txt has complete terms
---

# Web Research via the official Apify MCP (BYOK)

Drive the **official Apify MCP** (the hosted server `https://mcp.apify.com`, added
as an **OAuth workspace connector**) to run vetted Apify actors for web search,
site crawling, and structured extraction — then reshape the results into the
standard Stromy envelope and hand off to a `format-*` skill for a branded
deliverable.

This skill owns **policy**, not infrastructure: which actors to use, what caps to
set, when to stop and confirm, and what shape to emit. Apify maintains the MCP and
the actors; Stromy hosts nothing for this capability.

## Bring-your-own-key (BYOK) — the defining constraint

Every Apify run is authorized by the **client's own Apify account**, via the
hosted Apify MCP connector's **OAuth sign-in** (`https://mcp.apify.com`). There is
no token to paste and no `.env` to maintain — the client connects the Apify MCP
connector once and authorizes it against their own Apify login. All Apify spend
lands on the **client's** Apify account. Auth goes **client → Apify directly**;
**no Stromy-hosted process** ever sees a credential — no container, no proxy, no
log.

> **Why OAuth, not a plugin-declared stdio token.** An authenticated HTTP MCP is
> consumed as a workspace connector, never declared in a plugin (connection model
> + plugin-completeness Invariant #13). A stdio `APIFY_TOKEN=${VAR}` wiring also
> silently fails in the desktop app, which does not expand `${VAR}` in a plugin
> connector's env. So the apify connector is added at the **workspace** level and
> authorized by the user — this skill simply drives whichever apify tools that
> authorized connector exposes.

This skill is **brand-agnostic** — it takes no client-data input and does not
resolve a `client_slug`. Brand is injected only later, at the `format-*` step.
This skill therefore declares **no client-data inputs** (no overlay block), which
the plugin-completeness validator treats as "no client-data dependency".

## Opt-in only — never a silent fallback (the cost rule that comes first)

Every actor run spends real money on the **client's** Apify account, so this
capability is **explicitly opt-in**. Two hard behavioural rules:

1. **Invoke only on an explicit web-research / scrape / extract request.** Run this
   skill when the user actually asked to gather data from the web, search the live
   web, crawl a site, or extract structured records — the intents in the description.
   It is never the default research path.
2. **Never reach for it as an automatic fallback.** If some *other* tool fails or is
   unavailable — `WebSearch` disabled, a `WebFetch` page comes back empty, no browser
   connector present — do **not** silently fall through to a billed Apify run, and do
   **not** borrow a connected browser. **Stop and tell the user** that no free
   research path is available and ask whether to run a (billed) Apify pull, naming the
   estimate from the §4 cost gate. The user opts in per request; default is off.

This sits above the governance section because the cheapest run is the one you don't
make: confirm the intent *before* you even price the actor.

## Governance is advisory; the console spend cap is the backstop

The official Apify MCP exposes **no** account-usage / limits / billing tool, so
this skill cannot read live spend. Enforcement is therefore **advisory** and rests
on two things you must make prominent:

1. **The client's Apify console spend cap** (Settings → Limits → *Maximum monthly
   usage*). This is the authoritative hard limit and a **required onboarding step**
   — confirm with the user it is set before running anything sizeable.
2. **A confirm-before-large-pull step in this skill** (below), backed by the
   per-actor pricing returned by `fetch-actor-details`.

You set per-run caps (`maxItems`/`maxCrawlPages` + a timeout) on every run, but
they are *advisory* run inputs, not code-enforced ceilings. Be conservative.

## Tools provided by the Apify MCP connector

The workspace has the official Apify MCP connected (hosted, OAuth). The tools you
drive (documented names; your client surfaces them namespaced under that
connector — e.g. a "Call Actor" / `call-actor` form):

| Tool | Use |
|---|---|
| `search-actors` | Find an actor by capability when the curated list (below) does not cover the task. |
| `fetch-actor-details` | Read an actor's input schema **and pricing** before running — the basis for the cost estimate in the confirm step. |
| `call-actor` | Run an actor with your capped `run_input`; returns a (truncated) preview of the dataset. |
| `get-actor-output` | Fetch the **full** dataset for a finished run, beyond the `call-actor` preview limit. |
| `search-apify-docs` / `fetch-apify-docs` | Look up actor usage / input-field meaning when an input schema is unclear. |
| `get-actor-run`, `get-actor-run-list`, `get-actor-log` | Inspect run status / history / logs on failure. |
| `get-dataset`, `get-dataset-items`, `get-dataset-schema` | Read dataset storage directly when you have a dataset id. |

The MCP enforces a **30 requests/second per-user** rate limit — batch sensibly.

The curated actors, their cap-input keys, and approximate costs live in
[`references/actor-catalog.md`](references/actor-catalog.md). The output envelope
contract lives in [`references/output-contract.md`](references/output-contract.md).

## Workflow

### 1. Classify the request → pick a `workflow_type`

| User intent | `workflow_type` | Default actor |
|---|---|---|
| "Gather data / research a topic from the web", search the live web | `web_research` | `apify/rag-web-browser` |
| "Crawl this site / these URLs", pull page content for a corpus | `site_crawl` | `apify/website-content-crawler` |
| "Extract structured records from a known source set" (listings, specs) | `structured_extract` | a vetted extract actor — discover via `search-actors` |

Prefer the curated actor for the `workflow_type`. Only reach for `search-actors`
when the task genuinely falls outside the curated list; when you do, **verify the
chosen actor with `fetch-actor-details`** (input schema + pricing) before running.

### 2. Confirm the actor's input schema and price

Call `fetch-actor-details` for the actor you intend to run. Read:

- its **input schema** — confirm the cap-input field names (they vary per actor;
  the catalog lists the common ones but actors evolve), and
- its **pricing** — pay-per-result, pay-per-event, or compute-unit. Use this for
  the cost estimate in the confirm step.

Always verify slugs/fields here rather than trusting the catalog blindly — actor
inputs change over time.

### 3. Build a capped `run_input`

Every run MUST set a result/page cap **and** a timeout. Use the cap-input keys
from `fetch-actor-details` (see the catalog for the common ones, e.g.
`maxResults` / `maxCrawlPages` / `maxItems`, plus `timeoutSecs` / `maxRequestRetries`).
Default low and raise only on explicit user request.

### 4. Cost gate — confirm before any large pull

Estimate the run from the cap × the actor's unit price. If the run would exceed a
conservative threshold — **roughly > 25 results/pages, or an estimated > ~US$1 on
the client's account** — **STOP and ask the user to confirm before calling the
actor**, naming the estimate and that it bills their Apify account. Do not run
until they agree. (Example: "This crawl could fetch ~80 pages on your Apify
account at ~$X — proceed, or cap it lower?")

This is a hard behavioural rule: the confirm step plus the console spend cap are
the only governance — there is no server-side ceiling.

### 5. Run, then fetch the full output

Call `call-actor` with the capped input. If the returned preview is truncated,
call `get-actor-output` (or `get-dataset-items` with the run's dataset id) to read
the complete dataset. Surface `get-actor-run` / `get-actor-log` detail on failure.

### 6. Reshape into the standard envelope

Map the raw dataset into `{workflow_type, query_params, results, metadata}` per
[`references/output-contract.md`](references/output-contract.md):

- `workflow_type` ∈ `{web_research, site_crawl, structured_extract}`.
- `query_params` — the effective inputs you actually used (query, URL set, the
  caps).
- `results[]` — one stable record shape per workflow; each carries `source`,
  `url`, `retrieved_at`, and a quoted `content_evidence` for any passage you quote
  from the crawled/searched text (never from a title or snippet).
- `metadata` — `tool_calls`, `returned_count`, `warnings`, `assumptions`, and an
  `apify` block (`actor`, `run_id`, `dataset_id`, `est_cost_note`).

Do not hide gaps: empty dataset → empty `results` + a `metadata.warnings` note;
never fabricate records.

### 7. Hand off to a format skill

When the user wants a document, the envelope is the input to a branded
deliverable. The agent then routes the envelope to the appropriate **`format-*`**
skill — `format-docx` for a report/memo, `format-pdf-hd` for a polished
client-facing PDF, `format-xlsx` for a table of structured records. Brand is
applied there from the plugin overlay, not here.

> This skill **mentions** the `format-*` skills as the next step for the agent to
> route to. It does **not** itself invoke or command-activate another skill — the
> agent orchestrates the research→format handoff at the plugin layer. MCPs/skills
> never call each other directly.

## Exact MCP tool calls (worked sequence)

The Apify MCP is a connected workspace connector; your client surfaces its tools
namespaced (e.g. a "Call Actor" / `call-actor` form). The **actor input** shapes
below match the Apify Store actor schemas; the **MCP tool argument** names
(`actor`, `input`, `runId`, `datasetId`, …) are whatever the connected Apify tools
expose — read each tool's input schema once the connector is authorized; it is
authoritative.

A typical `web_research` run, end to end:

**1 — (optional) discover an actor** when the curated one doesn't fit:
```jsonc
// tool: search-actors
{ "search": "extract company profiles from a directory", "limit": 5 }
```

**2 — read schema + pricing of the chosen actor** (always, before running):
```jsonc
// tool: fetch-actor-details
{ "actor": "apify/rag-web-browser" }
// → returns the input JSON schema + pricing model; use it to set caps and to
//   estimate cost for the §4 confirm gate.
```

**3 — run the actor with a capped input** (`apify/rag-web-browser` for search):
```jsonc
// tool: call-actor
{
  "actor": "apify/rag-web-browser",
  "input": {
    "query": "EU AI Act enforcement timeline 2026",
    "maxResults": 5,
    "timeoutSecs": 120,
    "maxRequestRetries": 1
  }
}
// site_crawl instead → actor "apify/website-content-crawler",
//   input: { "startUrls": [{ "url": "https://example.com/docs" }],
//            "maxCrawlPages": 10, "maxCrawlDepth": 1, "timeoutSecs": 300 }
```

**4 — fetch the full dataset** if `call-actor`'s preview is truncated:
```jsonc
// tool: get-actor-output            // by run
{ "runId": "<runId from call-actor>" }
// or, by dataset:
// tool: get-dataset-items
{ "datasetId": "<defaultDatasetId from the run>", "limit": 100 }
```

**5 — on failure**, inspect the run:
```jsonc
// tool: get-actor-run   { "runId": "<runId>" }
// tool: get-actor-log   { "runId": "<runId>" }
```

Then map the dataset items into the
`{workflow_type, query_params, results, metadata}` envelope (§6) and hand off (§7).
Record the actor + `runId` + `datasetId` + the caps in `metadata.apify` for
traceability.

## Edge cases

- **Apify connector not authorized / auth rejected.** The Apify MCP returns its own
  auth error when the connector isn't signed in. Surface it plainly and tell the user
  to **connect (or re-connect) the Apify MCP connector** — add `https://mcp.apify.com`
  as a workspace connector and complete the OAuth sign-in to their own Apify account
  (BYOK — their account, their spend). There is no token to set. Do not retry blindly.
- **Apify tools missing entirely.** The Apify MCP connector isn't added to this
  workspace. Tell the user to add it (`https://mcp.apify.com`, OAuth) — it is **not**
  shipped inside the plugin (authenticated HTTP MCPs are workspace connectors, never
  plugin-declared). Do not fall back to a billed pull or a browser.
- **Actor returns no dataset.** Emit empty `results` and a `metadata.warnings`
  entry; do not invent data.
- **Over-threshold request.** Confirm first (step 4); never run until the user
  agrees.
- **Wrong/expensive actor risk.** Stay on the curated list; when you must pick a
  new actor, justify it from `fetch-actor-details` (capability + price) before
  running.

## Self-containment

This skill reads no client-data, hardcodes no `client_slug`, and calls no other
skill. Its only external dependency is the connected Apify MCP connector (hosted,
OAuth — the client's own Apify account) and, by mention only, the downstream
`format-*` skills the agent routes to.
