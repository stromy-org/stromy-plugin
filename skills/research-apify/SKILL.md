---
name: research-apify
description: "Agent-driven web research and data extraction backed by the official Apify MCP, bring-your-own-key (BYOK). Use when the user wants to gather data on a topic from the web, search the live web for current information, scrape or crawl a website or a list of URLs, or extract structured records (directory listings, product specs, profiles) — and turn the results into a branded deliverable. Drives a short list of vetted Apify actors with hard per-run caps and a confirm-before-large-pull step, reshapes the dataset into the standard {workflow_type, query_params, results, metadata} envelope, then hands the envelope to a format-* skill (format-docx, format-pdf-hd) for the branded document. Triggers on: web research, gather data on a topic, scrape, crawl a site, extract structured data from URLs, data extraction, web data, competitor/market scan."
license: Proprietary. LICENSE.txt has complete terms
---

# Web Research via the official Apify MCP (BYOK)

Drive the **official Apify MCP** (`@apify/actors-mcp-server`, wired per-plugin
under the server key `apify`) to run vetted Apify actors for web search, site
crawling, and structured extraction — then reshape the results into the standard
Stromy envelope and hand off to a `format-*` skill for a branded deliverable.

This skill owns **policy**, not infrastructure: which actors to use, what caps to
set, when to stop and confirm, and what shape to emit. Apify maintains the MCP and
the actors; Stromy hosts nothing for this capability.

## Bring-your-own-key (BYOK) — the defining constraint

Every Apify run is authorized by the **client's own** `APIFY_TOKEN`, set in the
client's local `.env` and read by the client's local Apify MCP subprocess. All
Apify spend lands on the **client's** Apify account. The token goes
**client machine → Apify directly** and **never transits any Stromy-hosted
process**. There is no Stromy container, no proxy, and no Stromy log that ever
sees the token.

This skill is **brand-agnostic** — it takes no client-data input and does not
resolve a `client_slug`. Brand is injected only later, at the `format-*` step.
This skill therefore declares **no client-data inputs** (no overlay block), which
the plugin-completeness validator treats as "no client-data dependency".

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

## Tools provided by the wired Apify MCP

The plugin wires the official Apify MCP under the `apify` server key. The tools
you drive (documented names; your client surfaces them namespaced under that
server):

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

## Edge cases

- **`APIFY_TOKEN` unset or rejected.** The Apify MCP returns its own auth error.
  Surface it plainly and tell the user to set `APIFY_TOKEN` in the plugin's `.env`
  (it is BYOK — their token, billed to their account). Do not retry blindly.
- **Apify MCP subprocess won't start.** The local server needs Node.js ≥ 18.
  Check the version and retry; the official hosted `https://mcp.apify.com` (OAuth)
  is a non-BYOK-token fallback configuration.
- **Actor returns no dataset.** Emit empty `results` and a `metadata.warnings`
  entry; do not invent data.
- **Over-threshold request.** Confirm first (step 4); never run until the user
  agrees.
- **Wrong/expensive actor risk.** Stay on the curated list; when you must pick a
  new actor, justify it from `fetch-actor-details` (capability + price) before
  running.

## Self-containment

This skill reads no client-data, hardcodes no `client_slug`, and calls no other
skill. Its only external dependency is the wired `apify` MCP (the client's own
key) and, by mention only, the downstream `format-*` skills the agent routes to.
