# Curated actor catalog

A short, vetted list of Apify actors for the three research workflows. This is
**curation, not enforcement** — prefer these, but always confirm the actor's live
input schema and pricing with `fetch-actor-details` before running, because actor
slugs, input fields, and prices change over time on the Apify Store.

All costs below are **approximate** and bill the **client's** Apify account
(BYOK). The official Apify MCP exposes no usage/billing tool, so these notes plus
`fetch-actor-details` pricing are your only basis for the confirm-before-large-pull
estimate. The client's Apify **console spend cap** is the authoritative backstop.

> Verified against the Apify Store / MCP docs on 2026-06-16, re-verified
> 2026-07-16: `apify/rag-web-browser` is a default MCP tool; the
> `search-actors` / `fetch-actor-details` / `call-actor` / `get-actor-output`
> tools are current, and specific actors can be pinned as first-class tools via
> the connector's `?tools=` parameter. Always re-verify a slug + its input keys
> with `fetch-actor-details` at runtime — the keys below are the common ones,
> not a guarantee.

## Pricing-model migration (2026) — how to read an actor's price

Apify is retiring the **rental** (flat monthly) actor model: no new rental
actors since 2026-04-01, and remaining rentals migrate to pay-per-usage on
**2026-10-01**. Most Store actors now price as:

- **Pay-per-event (PPE)** — a per-run **start fee** plus a per-item (or
  per-event) price. Estimate = *start fee + cap × unit price*, not just
  cap × unit price; for small capped runs the start fee can dominate.
- **Pay-per-usage** — platform compute units (CU) only; cost scales with pages
  × page weight. Harder to estimate up front — keep caps low and lean on the
  confirm gate.

`fetch-actor-details` returns the live pricing model — read it, don't assume.
If an actor still shows as *rental* after 2026-10-01, the listing is stale;
prefer a PPE/usage-priced alternative.

## `web_research` → `apify/rag-web-browser`

Live-web search + browse, returns cleaned page content suited to RAG / LLM
ingestion. The official MCP loads this actor as a default tool.

| Concern | Field (verify with `fetch-actor-details`) | Recommended default |
|---|---|---|
| Result cap | `maxResults` | `5` (raise on request) |
| Per-page content cap | `maxResultsPerCrawl` / content length opts | leave default |
| Timeout | `timeoutSecs` | `120` |
| Retries | `maxRequestRetries` | `1` |

**Cost (approximate):** small per-query/per-result charge. A 5-result query is
typically a few US cents. Confirm with `fetch-actor-details` pricing.

## `site_crawl` → `apify/website-content-crawler`

Crawl a site or a list of start URLs and return cleaned main-content text per
page. Apify's flagship content crawler for building corpora.

> Curated but **verify the slug + fields with `fetch-actor-details`** before the
> first run — this actor was not re-confirmed live at authoring time.

| Concern | Field (verify with `fetch-actor-details`) | Recommended default |
|---|---|---|
| Start URLs | `startUrls` | required input |
| Page cap | `maxCrawlPages` | `10` (this is the spend lever — keep low) |
| Depth cap | `maxCrawlDepth` | `1`–`2` |
| Timeout | `timeoutSecs` | `300` |
| Content format | `crawlerType` / `htmlTransformer` | leave default |

**Cost (approximate):** scales with pages crawled (compute + per-result). A
10-page crawl is usually well under US$1; a few-hundred-page crawl is where the
confirm gate matters most.

## `structured_extract` → discover via `search-actors`

There is no single universal extract actor — the right one depends on the source
(a generic web-scraper, a site-specific scraper, or a structured-data extractor).

1. `search-actors` with the capability ("extract structured data", "scrape
   listings", the target site name).
2. `fetch-actor-details` on the candidate — confirm its **input schema** and
   **pricing**.
3. Pick the cheapest actor that fits; record the choice + why in
   `metadata.assumptions`.

| Concern | Field (varies per actor) | Recommended default |
|---|---|---|
| Item cap | `maxItems` / `maxResults` / `maxCrawlPages` | `25` (raise on request) |
| Timeout | `timeoutSecs` | `300` |

**Cost (approximate):** entirely actor-dependent — read pricing from
`fetch-actor-details` and apply the cost gate.

**Commonly fitting example** (verify live before running, as always):
`compass/crawler-google-places` (the Google Maps scraper — places / local
business listings) is the Store's most-used extract actor and a sound default
for place/business directory pulls. For anything else, discover per-task.

### Personal-data & compliance caveats (binding for people-shaped data)

When a `structured_extract` target is **people data** (profiles, contact
details, employee lists), extra rules apply on top of the cost gate:

- **Treat every scraped person field as personal data** (GDPR/CCPA). Before
  running, tell the user the pull returns personal data and that lawful basis,
  retention, and opt-out handling are *their* responsibility; record that
  notice in `metadata.warnings`.
- **Cookieless actors only.** Never run an actor that asks for the client's
  platform session cookies or login (LinkedIn especially) — session-based
  scraping defeats authentication and carries account-ban risk for the
  client's account. `fetch-actor-details` shows required inputs; a
  `cookies`/`sessionCookie` field is a hard stop.
- **Never use any actor to defeat auth, CAPTCHAs, or paywalls** — same
  discipline as every other Stromy fetch surface.

## Caps discipline (applies to every actor)

- **Always** set a result/page cap **and** a timeout in `run_input`.
- Default low; raise only on explicit user request.
- Estimate cost = cap × unit price (from `fetch-actor-details`).
- If the estimate exceeds **~25 results/pages or ~US$1**, STOP and confirm with
  the user before calling the actor (it bills *their* account).
- Record the caps in both `query_params` and `metadata.apify.caps`.
