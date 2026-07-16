# Client onboarding — BYOK web research via Apify (one-pager)

Setup steps for a client (or the agent walking a client through setup) to
enable the `research-apify` capability. Bring-your-own-key: **your Apify
account, your spend** — nothing is billed to or routed through Stromy.

## 1. Create (or reuse) an Apify account

Sign up at [apify.com](https://apify.com) — the free plan includes starter
credits and is enough to trial the capability. No card is required to start.

## 2. Set a console spend cap — required, do this before anything else

In the Apify console: **Settings → Limits → Maximum monthly usage**.

This cap is the **authoritative hard limit** on what research runs can ever
cost you in a month. The skill estimates and confirms costs before large pulls,
but those checks are advisory — the console cap is the only enforced ceiling.
A sensible starting cap is US$5–20/month; raise it later if your research
volume grows.

## 3. Add the Apify MCP connector to your workspace

Add a custom connector (Claude: Settings → Connectors → *Add custom
connector*) with this URL:

```
https://mcp.apify.com/?tools=actors,docs,runs,storage,apify/rag-web-browser,apify/website-content-crawler
```

Use this scoped URL rather than the bare `https://mcp.apify.com` — it exposes
exactly the tools the research skill uses and pins the two vetted default
actors (live-web search, site crawling) as first-class tools.

Complete the **OAuth sign-in** when prompted — you sign in to your own Apify
account in the browser. There is no API token to paste and nothing to put in a
`.env` file.

## 4. Verify with a small test run

Ask the agent for a small piece of web research, e.g.:

> "Using web research, find the 3 most recent announcements about &lt;topic&gt;."

Expect: the agent runs a capped query (~5 results, a few US cents), tells you
what it will cost *before* any larger pull, and cites what it found. Runs and
spend appear in your Apify console under **Actors → Runs** and **Billing**.

## Cost expectations

| Task shape | Typical cost |
|---|---|
| Web search, ~5 results | a few US cents |
| Site crawl, ~10 pages | usually well under US$1 |
| Larger pulls (>~25 items or >~US$1 estimated) | the agent stops and asks you first |

## Revoking access

Remove the connector from your workspace, and/or revoke the OAuth
authorization in the Apify console (**Settings → Integrations**). Your account
and data remain yours throughout — Stromy never holds a credential.
