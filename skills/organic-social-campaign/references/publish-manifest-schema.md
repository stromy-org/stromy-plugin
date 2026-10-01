<!-- since: 2026-10-01 -->

# Publish manifest — the optional LinkedIn handoff

`posts.json` is an editorial artifact and stays one. It is never published as-is:
its schedule is week-relative, its author is a display name, its LinkedIn link is
meant for a first comment, and nothing in it is an approval. When a reviewed
LinkedIn post should go out through the org's publish rail (`linkedin-publish` /
`linkedin-mcp`, ORG-PLAN-285), `scripts/build_publish_manifest.py` turns the
reviewed copy plus explicit **assignments** into a **publish manifest v1** — an
**unapproved** file. Approval happens later, over the stored bytes, by the
operator's own CLI. This step never publishes and never approves.

```bash
python3 scripts/build_publish_manifest.py posts.json assignments.json -o publish-manifest.json
linkedin-publish manifest validate publish-manifest.json   # canonical digest; still UNAPPROVED
```

## `assignments.json` (operator input)

```json
{
  "campaign_id": "stromy-autumn-2026",
  "defaults": {
    "binding_id": "bind-william-personal",
    "author_urn": "urn:li:person:<sub from account inspect>",
    "timezone": "Europe/Brussels",
    "visibility": "PUBLIC",
    "expiry_hours": 24
  },
  "posts": {
    "a41e61b8372c": {
      "scheduled_at": "2026-10-06T08:30",
      "link_disposition": "in_commentary"
    },
    "1bc3e31c768c": {
      "scheduled_at": "2026-10-08T08:30",
      "link_disposition": "none",
      "media": {"kind": "document", "asset": {"sha256": "<64 hex>"}, "title": "The ledger"}
    }
  }
}
```

| Field | Notes |
|---|---|
| `campaign_id` | Required. Chosen once and **reused across every export of this campaign**: post ids alone collide across campaigns. |
| `defaults.*` | Apply to every selected post unless the post overrides them. Unknown keys fail. |
| `posts.<post_id>` | **Only the posts named here are included** — the handoff is opt-in per post. Other LinkedIn posts are counted as not selected; non-LinkedIn posts are counted and excluded. |
| `scheduled_at` | Local wall time in `timezone` (`2026-10-06T08:30`), or with an explicit offset that zone actually uses. A time in a DST gap is refused; a time in a DST fold needs an explicit offset. Week/day alone is never turned into a date. |
| `expires_at` | Optional. Defaults to `scheduled_at` + `expiry_hours` (24). Shown for approval; a post that misses its window needs a new approval, not a late send. |
| `binding_id`, `author_urn` | The registered account binding and its **URN** — never a display name. An organization author cannot use `CONNECTIONS`. |
| `media` | Required when the surface carries media; refused when it does not fit (below). An `asset.sha256` is an asset-store handle, never a path, URL or base64. |
| `commentary` | Optional exact final text. Without it the builder assembles hook, body, CTA and hashtags (blank-line separated). The 3000 code-point cap applies to the **final** string. |
| `link_disposition` | Required for a `first_comment` post (every LinkedIn post by default): `in_commentary` (the link is in the approved text — checked) or `none`. The rail never writes comments, so a first-comment link is never silently lost. |
| any other key | Refused. In particular there is no `approved` field anywhere. |

## Surface → media

| `surface` | Rail media | Notes |
|---|---|---|
| `none` | none, or an `article` link preview | text post |
| `image`, `infographic` | `image` | one rendered image |
| `document` | `document` (PDF) | REST adapter capability |
| `carousel` | `document` (PDF) | LinkedIn has no organic carousel API; a carousel goes out as an approved PDF or not at all |
| `reel`, `short` | — | refused: video is a later rail capability |

## Output

Exactly the `linkedin-publish` manifest v1 contract: `schema_version`,
`campaign_id`, `source_posts_sha256` (SHA-256 of the canonical JSON of the
`posts.json` it was built from), and one `publications[]` entry per selected post
with `post_id`, `binding_id`, `author_urn`, `commentary`, `visibility`, `media`,
`scheduled_at`, `timezone`, `expires_at`. The library re-validates every rule on
import; the builder enforces them first so a refusal names the post while the
editorial context is still open.

Any refusal lists every offending post and **writes nothing**. The source
`posts.json` is never modified. Changing any field after approval — one character
of commentary, a minute of schedule, a different asset — changes the digest, and
the changed post needs a fresh approval.
