<!-- since: 2026-06-01 --><!-- updated: 2026-07-15 campaign namespace + campaign.json -->

# `social-media/*` shared data schema (v1.0)

The persisted files under `{base}/social-media/` are the contract shared between
`organic-social-campaign` (writer) and `paid-social-campaign` (reader of
`config.json`). Every file carries a top-level `"schema_version": "1.0"` so the
two skills can detect drift. **When `schema_version` is absent on read, treat the
file as `"1.0"`** (back-compat: pre-versioning files remain valid).

All additions to these schemas are **additive** — consumers ignore unknown keys.
Never repurpose or remove a documented key without bumping `schema_version`.

```
{base}/social-media/
├── config.json                      # shared by BOTH modes and by paid-social-campaign
├── organic/                         # PROGRAM state (always-on — the default mode)
│   ├── pillars.json
│   ├── series.json
│   ├── community-playbook.json
│   ├── advocacy.json
│   ├── posts.json                   (Phase 7 — see post-object-schema.md)
│   └── style-blocks/<ref>.txt       (Phase 8 — locked visual prompt blocks)
└── campaigns/<campaign-slug>/       # CAMPAIGN state (time-boxed — campaign mode only)
    ├── campaign.json                # manifest (see below)
    └── organic/                     # identical shapes to the program organic/ above
```

## `config.json`

Platform, tracking, and compliance settings. Read by **both** skills.

```json
{
  "schema_version": "1.0",
  "platforms": ["linkedin", "instagram"],
  "utm": {
    "source": "linkedin",
    "medium": "organic_social",
    "campaign_pattern": "{pillar}-{yyyymm}"
  },
  "hashtags": {
    "core": ["#PublicAffairs"],
    "per_platform": { "linkedin": ["#B2B"], "instagram": ["#BehindTheScenes"] }
  },
  "compliance": {
    "posture": "conservative-eu",
    "consent_required": true,
    "prohibited_topics": []
  },
  "content_generation": { "...": "see platform-content-config.md" }
}
```

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| `schema_version` | string | yes (on write) | `"1.0"`; absent ⇒ treat as `"1.0"` |
| `platforms` | string[] | yes | platform slugs the program targets |
| `utm` | object | optional | UTM taxonomy; `paid-social` reads this |
| `hashtags` | object | optional | `core` + `per_platform` |
| `compliance` | object | optional | posture, consent, prohibited topics; `paid-social` reads this |
| `content_generation` | object | optional | Phase 8 config — full schema in [platform-content-config.md](platform-content-config.md) |

`content_generation` is **additive and optional**: `paid-social-campaign` ignores
it. It is documented separately because it is large and Phase-8-specific.

## `organic/pillars.json`

```json
{
  "schema_version": "1.0",
  "pillars": [
    {
      "id": "regulatory-radar",
      "name": "Regulatory Radar",
      "covers": "EU policy shifts relevant to the ICP",
      "proof_types": ["data", "methodology"],
      "format_affinity": ["carousel", "document"]
    }
  ]
}
```

`id` is a stable kebab-case slug — it is the `source_pillar_id` foreign key that
`posts.json` references (see [post-object-schema.md](post-object-schema.md)).

## `organic/series.json`

```json
{
  "schema_version": "1.0",
  "series": [
    {
      "id": "3-minute-methodology",
      "name": "3-Minute Methodology",
      "pillar_id": "regulatory-radar",
      "format": "carousel",
      "structure": "Hook → 3 steps → CTA",
      "cta_type": "engage",
      "funnel_intent": "consideration"
    }
  ]
}
```

## `organic/community-playbook.json`

```json
{
  "schema_version": "1.0",
  "response_slas": { "question": "4h", "complaint": "1h" },
  "tone_rules": { "praise": "...", "complaint": "...", "crisis": "..." },
  "escalation_matrix": [{ "category": "legal", "owner": "..." }],
  "prohibited_topics": [],
  "after_hours": "..."
}
```

## `organic/advocacy.json`

```json
{
  "schema_version": "1.0",
  "level": "pilot",
  "advocates": [],
  "content_queue_url": null,
  "recognition_model": "..."
}
```

## `campaigns/<campaign-slug>/`

The **campaign-mode** namespace. A campaign is time-boxed and story-driven; a
program is always-on. Both use identical `organic/*` shapes — only the **root**
differs. Namespacing exists because a client can run several campaigns against a
live always-on program, and a shared root would let each clobber the others.

### Slug validation (before the slug touches any path)

`campaign_slug` is **required** in campaign mode and MUST match
`^[a-z0-9]+(?:-[a-z0-9]+)*$` (lowercase kebab-case). Reject slashes, `..`,
whitespace, and empty values — the slug is interpolated into a filesystem path,
so a traversal-shaped slug is a path-traversal bug, not a naming nit. A slug that
collides with an existing campaign is a **resume** offer, never a silent
overwrite.

### Window normalization

Accept `start` + `end` **or** `start` + `weeks`. ISO-validate the dates, derive
the missing value, require `end >= start`, and **reject a supplied `weeks` that
contradicts the dates** (don't silently prefer one). If the user has no end date,
default to **8 weeks** from the confirmed start and mark the end **provisional**
in the scope summary.

### `campaign.json`

```json
{
  "schema_version": "1.0",
  "campaign_slug": "paper-is-not-the-problem",
  "name": "Paper Is Not The Problem",
  "objective": "Shift procurement decision-makers from 'paper = waste' to 'paper = renewable'",
  "window": { "start": "2026-09-07", "end": "2026-11-01", "weeks": 8 },
  "tracks": [
    {
      "platform": "linkedin",
      "audience_id": "b2b-procurement",
      "account": {
        "handle": "@kvgo",
        "ownership": "owned",
        "owner_org": "KVGO",
        "access_via": "Emma van Gelder"
      },
      "amplification": ["organic"]
    },
    {
      "platform": "instagram",
      "audience_id": "b2c-awareness",
      "account": {
        "handle": "@indruk.nu",
        "ownership": "borrowed",
        "owner_org": "Indruk (sector education platform)",
        "access_via": "Emma van Gelder"
      },
      "amplification": ["paid-boost", "influencer-seeded"]
    }
  ],
  "arc": { "acts": [{ "n": 1, "name": "Disrupt the assumption" }] },
  "status": "planned"
}
```

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| `schema_version` | string | yes (on write) | `"1.0"`; absent ⇒ treat as `"1.0"` |
| `campaign_slug` | string | yes | validated per **Slug validation** above; matches the directory name |
| `name` | string | yes | human-readable campaign title |
| `objective` | string | yes | the campaign's single business objective |
| `window` | object | yes | `{start, end, weeks}` — normalized per **Window normalization** above |
| `tracks[]` | object[] | yes | one entry per platform × audience — the account/amplification contract |
| `tracks[].platform` | string | yes | platform slug (`linkedin`, `instagram`, …) |
| `tracks[].audience_id` | string | yes | audience/ICP key this track speaks to |
| `tracks[].account` | object | yes | **which account posts** — see the sub-table below |
| `tracks[].amplification[]` | string[] | yes | one or more of `organic` \| `paid-boost` \| `influencer-seeded` — **what carries reach** |
| `arc` | object | optional | summary of the Phase 3 narrative arc (`acts[]`); full arc lives in the deliverable |
| `status` | string | yes | `planned` \| `live` \| `closed` — see **Status** below |
| `run_mode` | string | optional | `"internal-draft"` when the run is a draft on unverified data |

**`tracks[].account`:**

| Key | Type | Required | Notes |
|-----|------|----------|-------|
| `handle` | string | yes | the posting handle (`@kvgo`) |
| `ownership` | string | yes | `owned` (the client's own channel) \| `borrowed` (a **third party's** channel the client posts onto) |
| `owner_org` | string | yes | who owns the account — for `owned`, the client; for `borrowed`, the third party |
| `access_via` | string | yes | the **named person** who actually has posting access. Never assume access exists because the relationship does. |

**Borrowed-account semantics.** A `borrowed` account is not a cosmetic label — it
changes strategy structure three ways: (1) channel-access confirmation becomes a
tracked intake item (access runs through a named human, and that human is a
single point of failure); (2) Phase 3 MUST capture **co-branding/attribution
rules** — whose brand fronts the post, how the client is credited, who approves;
(3) the audience is the *owner's* audience, not the client's, so voice and
follower expectations follow the owner's channel, not the client's brand.

**Amplification semantics.** When **any** track's `amplification` is non-`organic`,
the Phase 3 strategy deliverable MUST include a boost-strategy section (budget
class, boost triggers, expectation-setting for a cold/low-reach account). A
paid-first track is strategy *structure*, not an advisory afterthought — the
common real case is a B2C track where organic reach is realistically ~zero and
boost plus influencer seeding carry the whole distribution.

### Status

| Status | Meaning | Transitions |
|--------|---------|-------------|
| `planned` | Strategy/calendar approved; nothing published | → `live` (first post ships) or → `closed` (cancelled) |
| `live` | Campaign is running inside its window | → `closed` (window ends or campaign stops) |
| `closed` | Window over; state kept read-only for the next campaign's prior-wave inventory | terminal |

`status` may only move to `live` when `run_mode` is **absent** — an
`internal-draft` run is never published (see **`run_mode`** below).

### `run_mode` + the gaps ledger

`run_mode: "internal-draft"` marks a campaign whose run leaned on unverified or
template-grade client data — the sanctioned "draft now, verify later" pattern.
It is **guard-preserving**: it defers only the *verified-data precondition*, and
never relaxes never-fabricate (a missing person/claim/number is `TBD (gap #n)`,
never a placeholder or invented value).

| Rule | Contract |
|---|---|
| Field | `run_mode: "internal-draft"` — optional; **absent** means a normal verified run |
| Publish interlock | `status` may move to `live` **only** when `run_mode` is absent. Clearing it requires a verified re-run of the affected phases, not an edit to the field |
| Ledger location | `gaps.md`, written **alongside the run's outputs** (campaign mode: beside the campaign's deliverables; program mode: beside the program's). It is not a JSON schema file — it is an operator-facing checklist |
| Ledger content | one entry per unverified claim, person, asset, right, or channel fact the run leaned on; each states **what would verify it** and **who owns the answer** |
| Ledger lifecycle | entries close individually as verification lands; the run stays `internal-draft` until **every load-bearing** entry is closed |
| Output labeling | every deliverable watermarked `DRAFT — INTERNAL / NIET PUBLICEREN` with a `-DRAFT` filename suffix |
| Blocked phases | Phase 7 freeze and Phase 8 generation — no `posts.json` is written and `validate_posts` is not run on draft data |

Clearing `run_mode` is therefore a **re-run**, not a field edit: flipping the key
without re-deriving the content from verified data is exactly the silent
promotion the mode exists to prevent.

### Resolution order (campaign mode)

1. Read `campaigns/<campaign_slug>/organic/*` — the campaign's own state wins.
2. If the campaign has **no** `pillars.json`, read root `organic/pillars.json`
   **read-only, as a seed**, and write the campaign's own copy into the campaign
   namespace. Never write back to the root.
3. Read root `config.json` for platforms/UTM/compliance — shared, never nested.
4. **Every** new write goes inside `campaigns/<campaign_slug>/`.

Program mode is unchanged: it reads and writes root `organic/` and never looks at
`campaigns/`.

### `paid-social-campaign` is unaffected

`paid-social-campaign` reads **only root `config.json`**. It does not read
`organic/` or `campaigns/` state, so the campaign namespace is invisible to it
and this addition cannot break it. If a paid leg ever needs campaign awareness
(reading `campaign.json` or calendar boost flags), that is a separate, explicit
contract change — not an implicit consequence of this namespace.

## Write convention

The skill's **"Offer to save reusable config"** step (Final Output Assembly) and
the Phase 7/8 persistence steps MUST write `"schema_version": "1.0"` into every
file they create or overwrite under `social-media/`. On read, missing
`schema_version` is treated as `"1.0"`.

In **campaign mode** every `organic/*` write is rooted at
`campaigns/<campaign_slug>/` instead of `{base}/social-media/`; root `config.json`
stays shared and root `organic/` is never written by a campaign run.
