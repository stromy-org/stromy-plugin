# Output Contract

The skill emits structured JSON that downstream Stromy workflows (the `format-*`
skills) can consume directly. This is the **same envelope** used across Stromy
research skills, reused from the canonical `nl-gov-shared/output-contract.md`; only
the `workflow_type` enum and the result record shapes are specialised for Apify
web-research / extraction.

## Base shape

```json
{
  "workflow_type": "web_research | site_crawl | structured_extract",
  "query_params": {},
  "results": [],
  "metadata": {}
}
```

## Field semantics

### `workflow_type`

Stable workflow identifier. Use lowercase snake_case. Exactly one of:

- `web_research` — live-web search/browse on a topic (default actor `apify/rag-web-browser`).
- `site_crawl` — crawl a site or list of URLs for page content (default actor `apify/website-content-crawler`).
- `structured_extract` — extract structured records from a known source set (actor discovered via `search-actors`).

### `query_params`

The effective retrieval parameters actually used. Always include the caps you set,
because they materially affect the result and the cost.

Examples:

```json
{
  "query": "EU AI Act enforcement timeline 2026",
  "maxResults": 10,
  "timeoutSecs": 120
}
```

```json
{
  "start_urls": ["https://example.com/docs"],
  "maxCrawlPages": 20,
  "timeoutSecs": 300
}
```

### `results`

Workflow-specific records only. Keep one stable record shape per workflow; do not
mix unrelated shapes in one array unless a shared discriminator field is present.

Every result record carries, at minimum:

- `source` — the actor or origin (`"apify/rag-web-browser"`, the crawled domain, …)
- `url` — the canonical URL of the item
- `retrieved_at` — ISO-8601 timestamp of retrieval
- `content_evidence` (when you quote text) — see "Content evidence objects" below

### `metadata`

Everything that is not a primary result record:

- `tool_calls` — the Apify MCP tools you called, in order
- `returned_count` — number of records in `results`
- `warnings` — empty datasets, truncation, auth issues, skipped pages
- `assumptions` — any inference you made (e.g. picked a non-curated actor)
- `apify` — the run provenance + cost note:

```json
{
  "actor": "apify/website-content-crawler",
  "run_id": "abc123",
  "dataset_id": "def456",
  "caps": {"maxCrawlPages": 20, "timeoutSecs": 300},
  "est_cost_note": "≈ $0.40 at the actor's per-result price (advisory; client's Apify account). No live-usage tool exists; the console spend cap is the backstop."
}
```

Rich source-native `metadata` is useful for traceability, but treat it as optional
depth, not the minimum stable contract.

## Minimal examples

### Web research

```json
{
  "workflow_type": "web_research",
  "query_params": {
    "query": "EU AI Act enforcement timeline 2026",
    "maxResults": 5,
    "timeoutSecs": 120
  },
  "results": [
    {
      "source": "apify/rag-web-browser",
      "title": "EU AI Act: key dates",
      "url": "https://example.org/ai-act-timeline",
      "retrieved_at": "2026-06-16T10:00:00Z",
      "content_evidence": {
        "quote": "General-purpose AI obligations apply from 2 August 2025.",
        "url": "https://example.org/ai-act-timeline",
        "retrieved_at": "2026-06-16T10:00:00Z"
      }
    }
  ],
  "metadata": {
    "tool_calls": ["fetch-actor-details", "call-actor", "get-actor-output"],
    "returned_count": 1,
    "warnings": [],
    "apify": {
      "actor": "apify/rag-web-browser",
      "run_id": "abc123",
      "dataset_id": "def456",
      "caps": {"maxResults": 5, "timeoutSecs": 120},
      "est_cost_note": "≈ $0.05 (advisory; billed to the client's Apify account)."
    }
  }
}
```

### Site crawl

```json
{
  "workflow_type": "site_crawl",
  "query_params": {
    "start_urls": ["https://example.com/blog"],
    "maxCrawlPages": 10,
    "timeoutSecs": 300
  },
  "results": [
    {
      "source": "example.com",
      "url": "https://example.com/blog/post-1",
      "retrieved_at": "2026-06-16T10:05:00Z",
      "title": "Post 1",
      "text": "…cleaned page text…"
    }
  ],
  "metadata": {
    "tool_calls": ["fetch-actor-details", "call-actor", "get-actor-output"],
    "returned_count": 1,
    "warnings": [],
    "apify": {
      "actor": "apify/website-content-crawler",
      "run_id": "ghi789",
      "dataset_id": "jkl012",
      "caps": {"maxCrawlPages": 10, "timeoutSecs": 300}
    }
  }
}
```

### Structured extract

```json
{
  "workflow_type": "structured_extract",
  "query_params": {
    "start_urls": ["https://directory.example/listings"],
    "maxItems": 25
  },
  "results": [
    {
      "source": "directory.example",
      "url": "https://directory.example/listings/acme",
      "retrieved_at": "2026-06-16T10:10:00Z",
      "record": {"name": "Acme Ltd", "category": "Software", "city": "Brussels"}
    }
  ],
  "metadata": {
    "tool_calls": ["search-actors", "fetch-actor-details", "call-actor", "get-actor-output"],
    "returned_count": 1,
    "warnings": [],
    "assumptions": ["No curated extract actor fit; selected via search-actors and verified pricing with fetch-actor-details."],
    "apify": {
      "actor": "<actor-selected-at-runtime>",
      "run_id": "mno345",
      "dataset_id": "pqr678",
      "caps": {"maxItems": 25}
    }
  }
}
```

## Content evidence objects

When you quote crawled or searched **text**, attach a `content_evidence` object to
the result:

```json
{
  "quote": "General-purpose AI obligations apply from 2 August 2025.",
  "source": "apify/rag-web-browser",
  "url": "https://example.org/ai-act-timeline",
  "retrieved_at": "2026-06-16T10:00:00Z"
}
```

**Rules for content evidence:**

- Only quote from the actor's returned page **content/text** — never from a search
  snippet, a title, or your own summary.
- Always include `source`, `url`, and `retrieved_at`.
- If the crawl was truncated (cap hit), note in `metadata.warnings` that content
  may continue beyond what was fetched.
- If a page failed to fetch, report it in `metadata.warnings` — do not pretend it
  was read.

## Contract rules

- Keep `results` primary and `metadata` explanatory.
- Preserve Apify MCP warnings/errors verbatim where possible.
- Do not hide missing data. Put the gap in `metadata.warnings` or
  `metadata.assumptions`.
- Keep provenance fields (`run_id`, `dataset_id`, `actor`) so a downstream
  deliverable can cite where each record came from.
- Quote only from returned page content, never from titles or snippets.
- Record the caps you used in both `query_params` and `metadata.apify.caps` — they
  are the audit trail for spend on the client's account.
