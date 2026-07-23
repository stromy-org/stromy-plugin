---
name: organic-social-campaign
description: "Build organic B2B social media campaigns: editorial strategy, content pillars, editorial calendars, content matrices, executive & founder-led thought-leadership programs, employee advocacy, community-building and community-management playbooks, AEO/GEO (getting content cited by AI answer engines), and dark-funnel measurement specs. Interactive multi-phase process from discovery through governance. Person-led and community-anchored by default (company-page organic reach has collapsed; executives, employees, and communities carry distribution). Models any engagement as an N-audience × M-narrative-pillar matrix under one shared frame (e.g. a B2B and a B2C audience sharing a core insight, expressed through several narrative pillars) so the same architecture runs across any industry. Produces a DOCX-first client-facing strategy document with evidence-tiered citations that becomes the baseline for the downstream editorial calendar. Integrates with company profiles, messaging libraries, and brand data for consistent voice and positioning. Runs as an always-on program (default) or a time-boxed, story-driven campaign with a narrative arc. Use this skill whenever the user asks to build an organic social strategy, plan a time-boxed social media campaign, design a campaign narrative arc, sequence a multi-week advocacy or repositioning campaign, create a content calendar, plan social media content, develop editorial pillars, build a community-management or community-building playbook, set up employee advocacy or an executive/founder LinkedIn program, build a member advocacy or member activation kit for a trade association or membership org, advise on influencer use (archetypes, briefing, disclosure; advice only, never sourcing), optimize content to be cited by AI answer engines, plan organic LinkedIn or Reddit content, create a social content program, or anything involving 'what should we post and how do we build an audience'; even if they just say 'we need a social presence', 'help me plan our LinkedIn content', or 'we're running a campaign for the next six weeks.'"
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-local-skills.py (operator-run: ./scripts/sync.sh local-skills)
  Source:      workspace-studio/.claude/skills/organic-social-campaign/SKILL.md
  This file is a mirror of its canonical source. A local edit here will be
  overwritten by the next mirror run. Edit the source, then:
    ./scripts/sync.sh local-skills
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# Organic Social Campaign

## Inputs from client-data

- `companies/{client_slug}/brand_context.json`: resolved brand (expression, colors, fonts, logo); read `expression` (`principles`, `signatureElements`, `antiPatterns`) for compact brand direction and `identity.positioning`. **Reference, never bind**; prose guidance, not hard rules. (Image catalog lives in `images/manifest.json`.)
- `companies/{client_slug}/company_context.json`: redacted public company facts (name, positioning, values, services, publicContact) and public people (SMEs, spokespersons). PII such as banking, registration, VAT, billing, and personal contact details is intentionally absent from deployed overlays.
- `companies/{client_slug}/messaging/pillars.json` (optional): reusable messaging pillars
- `companies/{client_slug}/messaging/proof-points.json` (optional): evidence library
- `companies/{client_slug}/messaging/audiences.json` (optional): audience profiles / ICP seeds
- `companies/{client_slug}/messaging/narratives.json` (optional): core narratives, positioning
- `companies/{client_slug}/voice/voice-profile.md` (optional): L2 voice profile
- `companies/{client_slug}/voice/voice-anchors.md` (optional): L2 reference passages
- `companies/{client_slug}/voice/voice-extensions.json` (optional): L2 additive bans
- `companies/{client_slug}/social-media/config.json` (optional): platforms, UTM, compliance, content_generation
- `companies/{client_slug}/social-media/claims-to-avoid.json` (optional): banned claims/figures and off-limits framing; load before drafting any evidence-bearing pillar (see Evidence Discipline)
- `companies/{client_slug}/social-media/organic/pillars.json` (optional): editorial pillars from a prior run
- `companies/{client_slug}/social-media/organic/series.json` (optional): repeatable content series
- `companies/{client_slug}/social-media/organic/community-playbook.json` (optional): response SLAs, tone, escalation
- `companies/{client_slug}/social-media/organic/advocacy.json` (optional): employee advocacy config
- `companies/{client_slug}/tokens.css` (optional): design tokens for branded output
- `companies/{client_slug}/logos/` (optional): logo variant files

### Path resolution (`{base}`)

Throughout this skill, `{base}` is the single resolved root for all the inputs
above. Resolve it **overlay-first** (per `skill-data-loading.md` §2):

1. **Plugin overlay (primary, steady state):** if a `companies/` directory
   exists, `{base}` = `companies/{client_slug}/`. Resolve `{client_slug}` from
   that overlay: zero entries → fail loud ("this plugin has no `companies/`
   overlay; client data unavailable"); one entry → use it; multiple → ask the
   user which client, never guess. Never accept `client_slug` as a parameter.
2. **Workspace Studio source fallback (development):** when running inside the Workspace Studio
   checkout with no `companies/` overlay, `{base}` = `client-data/clients/<slug>/`.

> **Operator environment only.** The `client-data/clients/<slug>/` fallback path is only reachable inside the Workspace Studio checkout. Deployed plugins have no `client-data/` directory: if the `companies/` overlay is absent, **STOP**: do not fabricate brand data, do not default to a Stromy brand, and do not attempt to read `client-data/` paths.

This skill is authored in Workspace Studio and synced into client plugin overlays (the
same distribution model as `proposal`, `messaging-framework`, `press-release`).
The plugin overlay is therefore the **primary, steady-state contract** (it is
what `validate-plugin-completeness.py` Invariant #3 enforces); the Workspace Studio
direct-read path is the development fallback. The `{base}` rule is correct in
both contexts. Missing **required** input (brand_context/company_context) → surface the full
resolved path and ask. Missing **optional** input → degrade per the Content
Assembly fallbacks below.

## Deliverable canvas (prerequisite for prose deliverables)

<!-- canvas-protocol:start v1 -->
This skill produces a multi-section deliverable. Collaborate through a single
chat artifact — the deliverable canvas. The canvas is the source of truth for
the in-progress draft; chat scroll-back is not.

1. **Resolve the section plan from this skill's own workflow.** Use the
   approved structure this skill already defines (or the prompt/resource it
   names). The canvas protocol does not invent sections.
2. **Choose the substrate.** Use `markdown` by default for strategic wording,
   plans, and other content where layout does not change meaning. Use `html`
   only when visual arrangement materially affects the user's decision. HTML is
   a **one-way display** surface only: never call back into an MCP from the
   artifact.
3. **Open the canvas.** Mint an 8-character hex `canvas_id`, then emit exactly
   one artifact with identifier `canvas-<canvas_id>-<deliverable_type>`. One
   chat = one canvas.
4. **Iterate in the canvas.** After every change, re-emit the **full** canvas
   as a new version of the same artifact. Never emit deltas. Never mint a
   second canvas mid-session.
5. **Self-check before handoff.** Every planned section exists, is substantive,
   and appears in the agreed order. No `TBD`, placeholders, or pending
   structural questions remain.
6. **Sign-off gate.** Ask the user to confirm the canvas is final before any
   render handoff or client-data write.
7. **Construct the envelope.** Hand off `{deliverable_type, title, client_id,
   sections:[{id, title, body}], meta:{canvas_id, substrate,
   methodology_version}}`, where `methodology_version` is `1`. The downstream
   formatter or terminal write step consumes the envelope — never raw chat
   history.
<!-- canvas-protocol:end -->

## Overview

This skill builds organic B2B social media campaigns as a systems design problem: not a creative exercise. The goal is to define objectives, editorial architecture, operating rhythms, and measurement so that every post is traceable to business outcomes. Organic social optimizes for compounding: reach via credibility, engagement via relevance, and distribution via *people and communities*; not the brand page.

**The generic shape.** Any engagement (a fintech, a festival, a hospital system, a trade association) reduces to the same architecture: **N audiences crossed with M narrative pillars, under one shared frame or core insight.** A two-audience B2B/B2C split sharing one insight expressed across several pillars is one instance of this matrix, not a special case; a single-audience program with three pillars is another. Phase 3 builds this **audience × narrative matrix** explicitly, and every downstream phase (creative system, calendar, measurement) is a per-cell instantiation of it; never a bespoke structure invented per client.

**Modern posture (2026).** B2B organic is now **person-led** (company-page organic reach has collapsed; executives, employees, and communities carry distribution), **citable** (content earns discovery by being quoted by AI answer engines, not only ranked in-feed), **community-anchored** (community over follower count; most B2B sharing is "dark social" the public feed never sees), and **video-first**. The strategic basis and evidence behind every phase live in [strategy-foundations.md](references/strategy-foundations.md): read it once to ground the approach; treat its figures as directional and revisit annually.

The skill is interactive and phase-gated. Each phase produces deliverables and includes a checkpoint where the user confirms direction before proceeding. The user can enter at any phase if they already have prior work to build on.

## Company Data Integration

### Discovery

Resolve `{base}` overlay-first (see **Path resolution** above):

1. If a `companies/` overlay exists → `{base}` = `companies/{client_slug}/`
   (one entry → use; multiple → ask which company; zero → **STOP**: "this plugin has no `companies/` overlay; client data unavailable. Do not fabricate brand or company data.").
2. **Operator environment only.** Else (Workspace Studio checkout only) → `{base}` = `client-data/clients/<slug>/`; if no client is in scope, ask, or gather company details manually during intake.

Do not list the central `client-data/clients/` repo and ask as the *primary*
discovery: the overlay-first rule above governs which client is in scope.

> **Empty `people` → never fabricate an SME, spokesperson, or advocate.** A present overlay can still lack public people. If `company_context.people[]` is empty or absent, do **not** attribute a quote, point of view, bio, or advocacy role to a named individual, and do **not** invent a spokesperson or employee advocate. Spokesperson visibility (Phase 3), employee advocacy (Phase 5), and any recurring on-camera subject (Phase 8) must use only real people from `company_context.people[]`; if there are none, ask the user who to feature or keep the content org/brand-level (no named individuals). A present-but-empty `people[]` is missing data, not a license to improvise a real person's identity: the within-overlay twin of the no-overlay STOP above.

### Run mode: `internal-draft` (provisional data)

> **`run_mode: internal-draft` is a guard-*preserving* mode, not a guard bypass.** Set it **only when the operator explicitly asks** for an end-to-end run on unverified or template-grade client data: the real kickoff pattern of "draft now, verify later", where an early draft is itself the instrument that tells the humans which inputs need work. It defers **one** thing: the *verified-data precondition*. Every guard above stays in force. In this mode:
> - **Label everything.** Every deliverable carries **`DRAFT: INTERNAL / DO NOT DISTRIBUTE`** (title-page/slide watermark) and a **`-DRAFT` filename suffix**. No exceptions; an unlabeled draft is how a provisional artifact reaches a client.
> - **Emit a gaps ledger.** Write `gaps.md` alongside the outputs listing every unverified claim, person, asset, right, and channel fact the run leaned on: each with **what would verify it** and **who owns the answer**. Structure (severity key, categories, columns, ranked agenda): [strategy-document-template.md](references/strategy-document-template.md) § Validation appendix. The ledger is the deliverable's other half.
> - **Phase 7 and Phase 8 are blocked.** No `posts.json`, no `validate_posts` run on draft data, no generated assets. Asked to freeze or publish while in draft mode → **refuse** and point at the open ledger.
> - **Never-fabricate is untouched.** A missing person, claim, or number is referenced as **"TBD (gap #n)"**: never a placeholder name, invented figure, or improvised identity. The no-overlay STOP and the empty-`people` guard apply exactly as written.
> - **Unverified brand assets** (logo rights, charter) may be used in **internal** renders only, and that use is itself a ledger entry.
> - **Draft → verified:** when verification lands, re-run the affected phases from the verified data using the ledger as the checklist. A draft artifact is **never** silently promoted to client-facing. Items close individually, but the run stays `internal-draft` until every load-bearing item is closed.
>
> Campaign mode records this as `run_mode: "internal-draft"` in `campaign.json`, which must be cleared before `status` may move to `live`. Program mode uses the same labeling + ledger rules with no campaign manifest involved.

### Loading Company Data

```
{base}/company_context.json      → Company identity, positioning, values, services, publicContact, public people (SMEs/spokespersons)
{base}/brand_context.json        → Resolved brand: expression, colors, fonts, logo (for branded output guidance)
{base}/messaging/                → Messaging content library (optional):
  ├── pillars.json         → Reusable messaging pillars (seed editorial pillars)
  ├── proof-points.json    → Evidence library (seed content proof)
  ├── audiences.json       → Audience profiles (seed ICP definition)
  └── narratives.json      → Core narratives, positioning
{base}/voice/                    → L2 voice profile (optional; see voice-integration.md)
{base}/social-media/             → Social media config and content (optional):
  ├── config.json          → Platforms, UTM taxonomy, hashtags, compliance, content_generation
  ├── claims-to-avoid.json → Banned claims/figures (optional; see Evidence Discipline)
  ├── organic/             → PROGRAM state (always-on; the default mode)
  │   ├── pillars.json     → Editorial pillars (if previous run exists)
  │   ├── series.json      → Repeatable content series
  │   ├── community-playbook.json → Response SLAs, tone, escalation
  │   ├── advocacy.json    → Employee advocacy program config
  │   ├── posts.json       → Frozen per-post objects (Phase 7, if previous run exists)
  │   └── style-blocks/    → Locked visual prompt blocks (Phase 8, if generated)
  └── campaigns/<campaign_slug>/   → CAMPAIGN state (time-boxed; campaign mode only)
      ├── campaign.json    → Manifest: window, tracks (account + amplification), arc, status
      └── organic/         → same shapes as the program organic/ above
```

**Mode decides the root.** Program mode reads and writes root `organic/`: unchanged. Campaign mode reads and writes `campaigns/<campaign_slug>/organic/`, and may read root `organic/pillars.json` **read-only as a seed** when the campaign has none; every campaign write stays inside the campaign namespace, so a client's always-on program is never clobbered by a campaign (or by a second campaign). Client-level `config.json` stays at the root and is shared by both. Full contract: [social-data-schema.md](references/social-data-schema.md).

**Resume mode** triggers when the mode's own state directory already exists: root `organic/` for program, `campaigns/<campaign_slug>/organic/` for campaign. Read the existing content and offer: continue from where they left off, rework a specific phase, or start fresh. Resume can re-enter mid-Phase-8 by edition (see Phase 8). A campaign-slug collision is a resume offer, never a silent overwrite.

### Content Assembly

| Component | Source | Fallback |
|-----------|--------|----------|
| Company identity | `{base}/company_context.json` → `company` | Ask user |
| Services/sectors | `{base}/company_context.json` → `company.services[]` | Ask user |
| Target audiences | `{base}/messaging/audiences.json` | Ask user to define ICP |
| Messaging pillars | `{base}/messaging/pillars.json` | Build editorial pillars from scratch |
| Proof points | `{base}/messaging/proof-points.json` | Ask user for evidence |
| Platform config | `{base}/social-media/config.json` | Ask user which platforms |
| Existing editorial pillars | `{base}/social-media/organic/pillars.json` | Build new |
| Banned claims/figures | `{base}/social-media/claims-to-avoid.json` | None assumed: ask if a claim looks contested |
| UTM taxonomy | `{base}/social-media/config.json` → `utm` | Propose defaults |
| Compliance posture | `{base}/social-media/config.json` → `compliance` | Default to conservative EU posture |

## Voice (prerequisite for every copy step)

Any step that produces copy: Phase 5 sample copy/hooks, the Phase 7 creative
fields on `posts.json`, Phase 8 captions/hooks/CTAs: runs a **draft → review →
rewrite → verify** pass against the org voice cascade. This is a **numbered,
non-skippable gate**: skipping the verify step is exactly how a banned
construction reaches a client (a past run shipped dozens of em-dashes against
an explicit client ban because the review step was eyeballed, not counted).

1. Load **L1** baseline: `voice://baseline` + `voice://rules.json` from
   `stromy-format-mcp`: and **L2** client voice from `{base}/voice/*`.
2. Draft the copy, self-review against the combined rules (L2 may add bans, never
   relax L1), then rewrite until it passes: only then show the user.
3. Ban engagement-bait, filler openers, antithesis frames, and overused LLM
   vocabulary. Cross-check the platform's tone notes.
4. **Mechanically verify, don't eyeball.** Before any client-facing copy is shown, run a literal count against every L1 + L2 banned construction (em-dash occurrences if banned, each banned phrase, filler-opener list) and confirm **zero** matches. One remaining instance is a failed gate: fix and re-scan. See [voice-integration.md](references/voice-integration.md) § Mechanical self-check for the checklist form.

**Maintain the unsourced ledger as you draft.** As you write each content item (pillar, series, sample copy, post, caption), record its `basis`: `client_data` (traces to the overlay), `inferred` (extrapolated from real data), or `fabricated` (no client-data source); *when you write it*, not reconstructed later. Any named SME/spokesperson/advocate, quote, or proof point with no client-data source is `fabricated` and means you must revisit the empty-`people` guard (ask or keep it org-level). This ledger seeds `asset-feedback.unsourced_content` at close-out (Final Output Assembly).

If `voice://*` is unreachable (headless), fall back to L2-only + the inline
anti-slop checklist and `log` the degradation: never fail the copy step. This
skill *mentions* the cascade as context; it never invokes another skill. Full
loop, precedence, and checklist: [voice-integration.md](references/voice-integration.md).

**Brand expression layer (additive to voice cascade): reference, never bind.** Before any copy step, read `expression` from `{base}/brand_context.json`. If present, apply as prose guidance alongside the cascade:
- `expression.principles`: inform the register of pillar copy, hook language, and CTAs (e.g., "measured authority" → factual hooks, evidence-first; "evidence before decoration" → data-led captions)
- `expression.signatureElements`: reflect where natural in copy style and series naming
- `expression.antiPatterns`: add to the ban-list alongside voice cascade bans
- `identity.positioning`: anchor the editorial strategy framing and the core message of content pillars
- If `expression` is absent, fall back to the voice profile only with a soft note; no hard failure (output-tier brands may legitimately omit expression)
- **Voice-cascade rule:** `expression` is additive to L1 + L2 bans, never a relaxation. Expression principles may sharpen tone but must not reintroduce a banned construction. Where a Brand Context API narrative is attached (`candidate.context`), treat it as input evidence for expression principles, not a voice source that overrides the cascade.

## Evidence Discipline (prerequisite for every fact-bearing claim)

Any step that states a statistic, cites a study, or asserts a fact as settled runs this gate before the claim reaches a Phase 3 pillar or the strategy document. Full mechanics, the `claimsToAvoid` schema, and the reference-list format: [strategy-document-template.md](references/strategy-document-template.md) § Evidence & citations.

1. **Tier every source**: peer-reviewed > institutional/official statistics > industry-funded > journalistic. Name the tier next to each claim in working notes so a pillar's citation mix is visible before it goes client-facing.
2. **Cite or hedge.** Every stated number carries a named, dated source. No source → hedge language ("directionally," "reported by X, unverified"): never state a number as settled fact without one.
3. **Never merge incompatible statistics.** Two credible numbers measuring different scopes (different year, geography, methodology, or definition) are **both shown, never averaged or silently picked**: say what each one measures.
4. **Evidence-diversification gate.** No pillar or narrative may rest on a single industry-funded source alone. Before a pillar goes client-facing, confirm at least one independent, peer-reviewed, or official/institutional anchor sits alongside any industry-funded figure.
5. **`claimsToAvoid` / banned figures.** Load `{base}/social-media/claims-to-avoid.json` (if present) before drafting any pillar. A banned claim or figure is never used even if independently verified true: flag it to the user instead of silently substituting.
6. **Counter-argument discovery.** For each narrative pillar, research the single strongest credible counter-argument (regulator, watchdog, competitor, academic) and draft a sourced rebuttal before the pillar is finalized: see Phase 2 Step 1 "Adversarial check" and Phase 3 Step 1. Publishing that rebuttal as active content is a client sign-off decision, not an autonomous one. Counter-evidence is internal calibration: surface it in working notes and the internal twin so the team is never blindsided, but never foreground opposing research in a client-facing persuasion deliverable unless the client asks.
7. **Mandatory reference list.** Every client-facing strategy document ends with a full reference list: every cited source, its tier, publication date, and a one-line scope note (what it measures, who funded it). No client-facing document ships without one.
8. **Recency preference: swap, don't drop.** Prefer the most recent credible source for every claim. When a reviewer flags a dated statistic, check the engagement's existing research library for a recent equivalent **before** deleting the claim or commissioning new research: replace dated with recent so the point survives, upgraded. Only drop a claim when no recent equivalent exists.
9. **Fact-verification gate (non-skippable close-out).** Before the deliverable is marked ready, run the mechanical recheck in `research://verification-gate` (`ReadMcpResourceTool(server="stromy-format", uri="research://verification-gate")`): recompute every derived number from its stated inputs, resolve every citation to a real, findable publication (via `research://capability-map`), and trace every non-obvious claim to a source — enforcing gates 2–5 mechanically instead of by eyeball. An **unresolved citation** or an **unreconciled arithmetic mismatch** means the deliverable is **NOT marked ready**: fix (replace/soften per gates 3 & 8) or ask, then emit the `{claims, unresolved_citations, recomputed_mismatches}` digest into the reference list.

## Workflow

The workflow has 6 phases. Phases 1-3 happen before any content planning begins: the most common organic social failures stem from posting without a system, not from bad creative.

Every phase is interactive: present options, ask questions, propose directions, and wait for confirmation before proceeding. Pull what you can from company data first, then fill gaps with the user.

### Phase 1: Intake & Scope

**Step 1: Understand the request and detect entry point**

If `social-media/organic/` exists, summarize what's there and ask:
- **Continue**: Pick up from where the last run left off
- **Rework phase N**: Jump to a specific phase with existing context
- **Start fresh**: Ignore existing and rebuild

If starting new, understand the brief. The user's input could range from "we need a LinkedIn presence" to a detailed brief with audiences and themes.

**Step 2: Gather scope**

Ask (unless already clear from context or company data):
- **Intake depth: Full vs Narrowed.** Default to full discovery (Phase 2). Switch to **Narrowed intake** when the client can realistically supply little: skip the heavyweight brief, extract the voice baseline from the client's own existing public posts (Phase 2 Step 1), and replace the full intake deliverable with a short **validation checklist**: spokesperson names plus the handful of input variables that actually gate quality. Reduce asset asks to essentials (e.g. logo only); ask for testimonials/case studies only if the content plan will actually use them. State which mode you're in before proceeding; never silently drop intake steps.
- **Engagement type?**: **Program** (always-on presence; the **default**) or **Campaign** (time-boxed, story-driven). Campaign mode needs `campaign_slug`, a window, tracks/audiences, and the campaign objective, and it activates: the Phase 2 prior-wave inventory, the Phase 3 narrative-arc step, the Phase 4 hero→derivative step, `act`/`beat` on the Phase 5 calendar, and persistence under `{base}/social-media/campaigns/<campaign_slug>/organic/`. A user saying "campaign" colloquially is not the signal; this question is. **Validate before using the slug in any path:** lowercase kebab matching `^[a-z0-9]+(?:-[a-z0-9]+)*$`; reject slashes, `..`, whitespace, and empty values; a collision with an existing campaign offers **resume**, never overwrite. **Normalize the window:** accept `start`+`end` or `start`+`weeks`; ISO-validate dates, derive the missing value, require `end >= start`, and reject a `weeks` that contradicts the dates. No end date → default to 8 weeks from the confirmed start and mark the end **provisional** in the scope summary.
- **Per track (campaign mode): which account posts, and what carries reach?** `account` = handle + `ownership` (`owned`, `borrowed` [posting the client's campaign on a third party's channel], or `co-owned` [a multi-party-governed channel, e.g. a joint sector initiative with no single owner]) + `owner_org` + `access_via` (the named person who actually has posting access). **Ambiguous ownership defaults to `borrowed`** (the stricter contract, since access, attribution, and co-branding all get confirmed); relaxing to `owned` is a confirmable correction, never the reverse, and `co-owned` needs all-party sign-off on co-branding. `amplification` = one or more of `organic` | `paid-boost` | `influencer-seeded`. A **borrowed** or **co-owned** account makes channel-access confirmation a tracked intake item and requires Phase 3 to capture co-branding/attribution rules (whose brand fronts the post, how the client is credited). **`config.json` stays campaign-agnostic**; never embed a campaign's `account`/`ownership`/attribution rules there; they live only in the campaign manifest's `tracks[].account`. Shapes + semantics: [social-data-schema.md](references/social-data-schema.md).
- What is the primary business objective? (thought leadership, lead generation, recruitment, partner visibility)
- Which services or sectors should the content focus on?
- Which platforms? (If `config.json` has platforms defined, confirm; if not, recommend based on B2B context)
- Current state? (Starting from zero vs. optimizing existing presence)
- Any partner constraints or co-marketing requirements?
- Geographic scope and language requirements?
- Audience type? (B2B decision-makers, B2C consumers, or hybrid: where B2B is the primary target but consumer awareness reinforces B2B credibility)

**Platform selection (2026).** Default the B2B set to **LinkedIn** (primary: but person-led; see Phase 3), plus, per fit: **YouTube** (long-form authority + AI-citation surface), **Reddit** (buyer research, niche community, and a top AI-citation source; a participation/community play, not a posting-cadence play; see [platforms/reddit.md](references/platforms/reddit.md) and [community-building.md](references/community-building.md)), **X**, and **Meta/Instagram**. Note emerging surfaces where the ICP is present; **TikTok** (rising for B2B), **Bluesky/Threads**; but don't spread thin: 1–2 primary platforms done well beat five neglected ones.

Present 2-3 objective options with rationale. Let the user pick.

**Audience-type calibration**

The audience type selection shapes downstream decisions across all phases:

| Dimension | B2B | B2C | Hybrid |
|-----------|-----|-----|--------|
| Tone | Professional, evidence-led, ROI-focused | Accessible, emotional, benefit-driven | Professional primary, with consumer-friendly proof points |
| Pillar emphasis | Commercial proof, industry authority, thought leadership | Lifestyle, values, social proof | B2B pillars anchored by consumer sentiment as social proof |
| Content formats | LinkedIn articles, case studies, data carousels, whitepapers | Short video, stories, UGC, infographics | LinkedIn-first with select consumer formats for cross-pollination |
| Platform priority | LinkedIn primary, X secondary | Instagram/Facebook primary, TikTok secondary | LinkedIn primary, Instagram/Facebook as B2B-reinforcing channel |
| CTA style | "Book a consultation", "Download the report" | "Shop now", "Learn more", "Join the community" | B2B CTAs on LinkedIn; awareness/credibility CTAs on consumer channels |
| Success metrics | MQLs, pipeline influence, share of voice among decision-makers | Reach, engagement rate, sentiment, conversions | B2B pipeline metrics primary; consumer engagement as leading indicator |

Default to **B2B** when no audience type is specified (consistent with the skill's B2B positioning). The hybrid model is particularly useful when consumer awareness creates market pressure that influences B2B buying decisions: e.g., sustainability campaigns where public sentiment drives corporate procurement.

**Step 3: Confirm scope**

Present a one-paragraph scope summary. Wait for confirmation.

**Phase 1 deliverable**: Campaign brief (organic), a **validation checklist** in Narrowed-intake mode or a full brief otherwise. Saved to workspace output.

### Phase 2: Discovery & Audit

**Step 1: Listen first (social intelligence)**

Lead discovery with listening, not self-report. Before defining the ICP or baselining, gather signal on:

- **What the ICP actually discusses**: the questions, language, objections, and jobs-to-be-done in their own words (feeds editorial pillars and AEO query framing; see [aeo-geo-social.md](references/aeo-geo-social.md)).
- **Where they gather**: the subreddits, niche Slack/Discord, forums, and voices worth participating in (feeds community-building; see [community-building.md](references/community-building.md)).
- **Competitor & category narrative**: who owns which topics, and the whitespace. For a deep quantitative read, the org's `sov-competitor-analysis` / `sov-sentiment-analysis` skills exist; *mention* them as context; never invoke another skill from here.
- **Live trends & timely hooks**: signals worth a reactive/newsjacking response (feeds the Phase 5 reactive lane).
- **Adversarial check.** What credible, sourced arguments (regulator, watchdog, competitor, academic) exist against the campaign's core claim or frame? Surface them here, before strategy is set: not after publish. Feeds the Evidence Discipline counter-argument step and the Phase 3 pillar map.

- **Voice baseline from prior content.** When the client has prior posts/content (including partner or influencer content they endorse), **that corpus is the tone-of-voice baseline**: calibrate the working voice profile against it (register, rhythm, warmth, emoji/hashtag habits, language idiom) **before** drafting, recording deltas as *proposed* `voice-extensions` for the client to confirm, never a silent overwrite. Cold brand → skip. Corpus contradicts the stated profile → surface it, don't pick silently. This is also the primary voice source in **Narrowed-intake mode** (Phase 1 Step 2), where a heavyweight voice questionnaire isn't realistic. See [voice-integration.md](references/voice-integration.md).
- **Prior-wave inventory (campaign mode).** Before any strategy, inventory previous campaigns/posts on the **same evidence or theme**: the client's own channels, *and* adjacent channels it borrows or partners with (including any **live** influencer work). For each: what did it assert, to whom, when, and what did it leave unsaid? **Record each wave's channel and format, not just its assertion**; a format mismatch (e.g. a prior wave ran in print, this one runs on LinkedIn) changes the differentiation math. **A shared channel or partner is not the same as a shared topic**; verify topical relevance before counting a candidate as a prior wave, and note exclusions explicitly. This inventory is what makes the arc's differentiation note real rather than asserted; see [campaign-narrative-arc.md](references/campaign-narrative-arc.md) § Differentiation vs prior waves.

Use available listening tools or manual scans; present a short intelligence brief. This is a continuous input, not a one-time step: refresh it each planning cycle.

**Step 2: Define the ICP**

If `messaging/audiences.json` exists, pull audience profiles and confirm relevance to social. If not, build the ICP interactively:
- Industry/firmographics
- Decision roles and seniority
- "Jobs-to-be-done" themes (what are they trying to accomplish?)

Present the ICP definition. Ask the user to confirm or adjust.

**Step 3: Baseline the current state**

Ask the user about their current social presence:
- Follower count and growth trajectory
- Posting frequency and formats used
- Top-performing content (if known)
- Current engagement patterns
- Traffic from social to website (if tracked)

If they have analytics access, note what to pull. If starting from zero, skip to gap analysis.

**Step 4: Assess governance readiness**

Check whether approval workflows, moderation rules, and escalation paths exist. If `config.json` has compliance settings, reference them. Otherwise, propose governance basics.

Present findings as a brief baseline report with gaps highlighted.

**Phase 2 deliverable**: Social-intelligence brief, baseline report, risk register.

### Phase 3: Strategy

This is the core architecture phase: build the **audience × narrative matrix** (N audiences crossed with M narrative pillars under one shared frame) and assemble it into the client-facing **strategy document** (Step 6). Everything here needs user approval before Phase 4.

**Step 1: Propose editorial pillars**

Build 3-5 editorial pillars aligned to the company's services and buyer problems. If `messaging/pillars.json` exists, use those as seeds: editorial pillars should extend messaging pillars into social-native themes, not duplicate them.

For each pillar, propose:
- Theme name (3-5 words)
- What it covers and why it matters to the ICP
- Proof types that support it (case evidence, data, methodology, POV): run every proof point through the **Evidence Discipline** gate (tiering, diversification, `claimsToAvoid`) before presenting
- Format affinity (which content formats work best for this theme)
- Citable claims (AEO/GEO lens): the sourced facts, statistics, and named-expert POVs within the pillar worth stating plainly enough to be quoted by AI answer engines (see [aeo-geo-social.md](references/aeo-geo-social.md))

Present as a table. Ask the user to confirm, add, or cut pillars.

**Step 2: Propose cadence and format mix**

Recommend a posting cadence using the walk/run/fly framework:
- **Walk**: 2-3 posts/week (building consistency)
- **Run**: 4-5 posts/week (established rhythm)
- **Fly**: Daily + real-time engagement (mature program)

Recommend a starting level based on the team's capacity. For each post frequency, suggest the format mix (text, image, carousel, video, document, poll). **Bias the mix toward video**: short-form for discovery, long-form for depth/credibility; video out-reaches static formats and long-form is resurging, while carousels remain strong for saves/dwell. See [content-formats.md](references/content-formats.md) for format guidance.

**Step 2b: Design the narrative arc (campaign mode only)**

A campaign converges on a deadline; a program compounds. Sequence the story **before** any content planning: a flat grid of on-pillar slots never accumulates into an argument. Full method, templates, and a worked example: [campaign-narrative-arc.md](references/campaign-narrative-arc.md).

- **Acts (2–4 over the window).** Each declares: name, **belief shift** (explicit *from → to*), pillar emphasis, hero asset, and a one-line **differentiation note** ("what this audience already heard vs what is new this time") grounded in the Phase 2 prior-wave inventory. Default 3 acts: *disrupt the assumption → evidence and proof → invitation and choice*. Frame the **audience as hero, the brand as guide**: never brand-as-hero (the audience gets no role), and never make the hero the villain (the assumption was reasonable given what they were told). Under 4 weeks → 2 acts; never add an act to fill time.
- **Beats (one theme per week).** Expressed **once per track**: the **cross-track echo**: same beat, same week, per-audience dialect, **never cross-posted verbatim** (recycled content is down-ranked). Asymmetric tracks are fine; declare them rather than faking coverage. Single-track campaigns collapse to one dialect; the arc still applies.
- **One peak moment.** A concentrated multi-channel burst, usually at the **start of the final act**; where boost/influencer budget concentrates. Ship a kit, not a request.
- **The reactive lane is not arc-exempt**: a reactive post still serves the current act's belief shift, or it dilutes the campaign.
- **Boost strategy is mandatory, not optional prose,** when **any** track's `amplification` is non-`organic`: budget class, boost triggers, and expectation-setting for a cold/low-reach account. A **borrowed** account additionally needs its **co-branding/attribution rules** captured here: whose brand fronts the post, how the client is credited, who approves.
- **Dormant/borrowed-account revival ladder.** When a track's account is cold or dormant, sequence amplification strictly: **organic first** (signs of life, no reach promise) → **paid boost** once it's breathing → **one influencer collaboration** last, never earlier. Treat **account revival itself as a KPI** (post frequency + engagement on the account's own content), and **pin the baseline with a dated, timestamped snapshot** taken immediately before the revival phase starts: a verbally-reported baseline drifts between stakeholders and breaks the KPI's zero point. Full method: [campaign-narrative-arc.md](references/campaign-narrative-arc.md) § Dormant/borrowed-account revival ladder.

Present the arc as a table. **User approval gates Phase 4.**

**Step 3: Propose the community strategy (building + management)**

Two distinct disciplines: decide both:

- **Community building** (proactive): where the brand and its people *participate* (subreddits, niche Slack/Discord, forums, LinkedIn/Facebook groups) and whether to run an owned community. Most B2B services firms should **participate before they build**. See [community-building.md](references/community-building.md).
- **Community management** (reactive): response SLAs, tone rules, and escalation categories for your own surfaces. See [community-management.md](references/community-management.md).

Present both for approval.

**Step 4: Propose the distribution model (person-led)**

Company-page organic reach has collapsed; **people carry distribution**. Propose the model as a system, not a single lever:

- **Executive & founder-led (primary engine)**: the highest-ROI organic play. Which real leaders (from `company_context.people[]` only; never fabricate one) run a thought-leadership program: profile-as-channel plus a capture → ghostwrite → approve content engine. See [executive-led-content.md](references/executive-led-content.md).
- **Employee advocacy (breadth)**: None → Pilot (8–15 advocates) → Structured program, tuned to company size and capacity. See [employee-advocacy.md](references/employee-advocacy.md).
- **Member advocacy (associations)**: for a membership org (trade body, alliance, franchise) the advocacy layer **is the member base**: member organisations and their people, activated with a ready-to-share kit rather than a mandate (members are independent legal entities; suggest, never require). See the variant in [employee-advocacy.md](references/employee-advocacy.md).
- **Brand Page (credibility anchor)**: the proof/legitimacy surface and paid-amplification origin, not the primary reach channel.
- **Launch-anchor rule.** Default the launch/kickoff post to the **brand page**, not an individual: an executive-led launch ties the message too closely to one person. Executive and member amplification are a same-day secondary layer that reinforces the page post; they never replace it. Override only when the client explicitly wants a named-founder launch and accepts that framing trade-off.
- **Ecosystem tagging.** Identify sector organizations, funds, unions, or partners worth tagging on the launch post, from a **client-supplied roster**: never self-generated; and confirm the client has given each organization a heads-up **before** the tag goes live. Tagging without that confirmed heads-up is never autonomous.

If capacity is scarce, fund the executive program first, then advocacy. Present the model for approval.

**Step 4b: Influencer advisory (optional, both modes; B2C/hybrid emphasis)**

Offer when a track is B2C/hybrid or `influencer-seeded`. **Advice-only**: this skill never sources, contacts, or negotiates; asked to pick named influencers, **decline** and produce archetype + criteria instead. Full method, brief template, and disclosure detail: [influencer-advisory.md](references/influencer-advisory.md).

- Propose **whether** influencers fit, then **archetype × mode** (B2B defaults to nano/micro: credibility with a narrow audience beats reach; mid-tier is a B2C awareness instrument), plus **2–3 content concept directions**. Constrain the **claim**, free the **telling**; a script removes the trusted voice you were buying.
- **State the advice-only boundary in the deliverable**, and carry the relevant national/regional disclosure baseline: a relevant paid/gifted relationship must be clearly recognisable, the advertiser holds a duty of care, and gifting counts. Platform labels are examples, not a safe harbour or a substitute for legal review. Regulated sectors → tier-3 QA. Never invent an influencer, follower count, or rate.

**Step 5: Cross-channel integration points**

Organic social rarely operates in isolation. Define how the social strategy connects to other channels the client uses or plans to use:

- **Owned media**: website/blog content social can link to or repurpose; email cross-promotion - **Offline touchpoints**: events, print materials, conferences social can amplify or be amplified by (report-tie-in posts, QR codes on print)
- **Paid media handoff**: which organic posts trigger paid amplification (threshold criteria: engagement rate > X%, topic alignment with active campaign) - **PR/media**: earned coverage amplified through social; spokesperson visibility

Present integration points as a brief table mapping channel → social touchpoint → direction (social amplifies channel / channel feeds social / bidirectional). This ensures the organic strategy doesn't exist in a vacuum, especially for clients whose business involves non-digital channels.

**Step 6: Assemble the strategy document (DOCX-first)**

Compile every Phase 3 output into ONE client-facing **strategy document**: the primary deliverable of this phase and the baseline Phase 5 builds the editorial calendar from. Chapter list, per-chapter guidance, and the validation-ledger/reference-list format: [strategy-document-template.md](references/strategy-document-template.md).

- **Format: DOCX first.** Route through `format-docx` (or `format-prepare-document` for a longer document: see Output Format Production). A slide-deck version is a possible follow-on once the DOCX is approved, never the first artifact.
- **Internal → external twinning.** Produce two distinct-postured artifacts, never one file wearing both hats: an **internal working document** (full detail, may carry open questions, no client banner required) and a **client-facing concept document** (a **CONCEPT / DRAFT: not for client distribution** banner until sign-off, ending in a **Validation Ledger** appendix; every point that must be confirmed before send, e.g. spokesperson names, account ownership/status, baseline snapshot, anchor date, asset rights, prior-collaboration content, publish mandate for counter-argument content). The client-facing document is never sent while the ledger has an operator-flagged blocking row open.
- **Compliance stays a briefing, not a chapter.** Legal/regulatory findings (disclosure rules, ad-targeting law, green-claims regimes) ship as a separate compliance/creator briefing; the client-facing strategy document or deck carries at most one operational line where it is load-bearing.
- **Language twin (optional).** When the project language differs from a collaborator's shared working language, produce both versions of the same document: never let the two drift into different content.

Present the full strategy package (including the assembled document). Wait for approval before proceeding.

**Step 7: Client review round (when a client-side reviewer marks up the document)**

A reviewer's editorial calls govern: justify the original reasoning and comply, never defend research-maximalism. Produce a **review-response ledger** (per comment: decision; why it was there, traceable to a source, never invented; action = deck / content plan / briefing / dropped / validate-with-client), route cut depth to the content plan or a briefing rather than deleting it, and collect genuinely open questions into one short clarification message instead of guessing. Never ask the reviewer anything you can verify yourself first. Ledger format: [strategy-document-template.md](references/strategy-document-template.md) § Review-response ledger.

**Phase 3 deliverables**: The **strategy document** (DOCX-first; Step 6) assembling editorial strategy, the audience × narrative matrix / content pillar map, distribution model (page/exec/advocacy + launch-anchor + ecosystem tagging), community strategy, campaign narrative arc (campaign mode, incl. revival ladder where scoped), boost strategy, influencer advisory (if scoped), the evidence/reference appendix, and, for a client-facing external send, the validation ledger.

### Phase 4: Creative System

**Step 1: Build the content matrix**

For each editorial pillar, define repeatable content series: the building blocks that make content production predictable and sustainable.

Matrix structure: pillar × format × funnel intent (awareness / consideration / conversion).

For each cell, define 1-2 series with:
- Series name (e.g., "Regulatory Radar," "3-Minute Methodology," "Client Proof")
- Format (carousel, video, text post, document, poll)
- Structure (what each post in the series looks like)
- CTA type (engage, click, subscribe, book)
- Production requirements (who provides input, typical turnaround)

Present the matrix. Ask the user to refine series definitions.

**Step 1b: Plan hero assets and derivatives (COPE)**

*Campaign mode: runs per act. Program mode: offer only when explicitly requested: it adds no default checkpoint.* A campaign needing 36–48 posts cannot produce 40 originals; it produces a few flagships and fans each out, which is also what keeps the posts coherent. Method + producer mapping: [content-formats.md](references/content-formats.md) § Hero → derivative production (COPE).

- **Per act, define 1–2 hero assets**: the flagship the act hangs off (research explainer, factsheet, mini-doc, animated data story).
- **Map each hero → 3–6 derivatives per track** (carousel slides → single images; video → clips + quote cards; document → text-post series). **A hero yields 4–6 derivatives before fatigue: refresh the hero, don't stretch it.** Every derivative is **native, never cross-posted verbatim** (recycled assets are down-ranked).
- **Output:** a hero/derivative table appended to the content matrix. No hero capacity (tiny team) → build the map from pillar-level evergreen assets and **flag the reduced coherence**. Formats out of scope (e.g. client excludes video) → map only permitted surfaces.

**Step 2: Define template needs**

Based on the series, recommend visual and copy templates to reduce production cycle time. Note which templates need brand assets (logo placement, color application).

**Step 3: Define QA process**

For each content risk tier:
- Tier 1 (low): educational, culture → standard brand review
- Tier 2 (medium): service POVs, outcome claims → SME review + brand
- Tier 3 (high): regulated topics, partner claims → legal + SME + brand

**Phase 4 deliverables**: Content matrix, template specs.

### Phase 5: Calendar & Execution Plan

The calendar instantiates the strategy document's audience × narrative matrix into dated, owned rows: it never re-derives strategy from scratch.

**Step 1: Generate the editorial calendar**

Produce an N-week calendar (default: 4 weeks). Each entry includes:

| Week | Pillar | Series | Concept | Format | CTA | Owner | UTM tags | Paid amplification trigger |
|------|--------|--------|---------|--------|-----|-------|----------|---------------------------|

**Campaign mode adds `Act` and `Beat` columns** (omit both in program mode): every row states which act it serves and which weekly beat it expresses, so no slot is orphaned from the arc. They flow through Phase 7 onto each post object. See [campaign-narrative-arc.md](references/campaign-narrative-arc.md).

The "paid amplification trigger" column defines when a post's performance warrants boosting: this is the handoff point to paid media. The `paid-social-campaign` skill handles the actual ad buying and optimization.

**Publish-from (person-led).** The Owner column should specify *who publishes*: brand Page, a named executive, or an advocate; reflecting the Phase 3 distribution model. Bias flagship POV to executive accounts (see [executive-led-content.md](references/executive-led-content.md)).

**Reserve a reactive lane.** Don't fill 100% of capacity with planned posts. Leave ~15–25% for **reactive / newsjacking** content driven by the Phase 2 listening loop: timely commentary while a topic is live. Plan the *slot and the fast approval path*, not the content.

Present the calendar. Ask the user to adjust assignments, swap concepts, or change cadence.

**Step 2: Build the community playbook (management + building)**

Expand Phase 3's community strategy into an operational playbook.

*Management (reactive):*
- Response time targets by message type
- Tone and voice rules per scenario (praise, question, complaint, crisis)
- Escalation matrix with named owners
- Prohibited engagement topics
- After-hours monitoring approach

*Building (proactive):* which communities to participate in, who participates (named people only), the value-first participation cadence, and any owned-community plan and owner. See [community-building.md](references/community-building.md).

**Step 3: Build the person-led activation plan (executive + advocacy)**

Activate the Phase 3 distribution model:

- **Executive & founder-led (if scoped)**: profile optimization, the capture → ghostwrite → approve cadence, per-leader topic lanes, and a fast approval SLA. Real leaders from `company_context.people[]` only. See [executive-led-content.md](references/executive-led-content.md).
- **Employee advocacy (if scoped)**: set goals and content strategy, select the employee audience (champions first), demonstrate the value to advocates, launch with enablement resources, sustain engagement (content queue, recognition, feedback loop), and measure results (shares, engagement, reach, site traffic). See [employee-advocacy.md](references/employee-advocacy.md) for the detailed program design.
- **Member advocacy (if scoped)**: build the **member-amplification kit** per beat (copy variants + co-brandable native assets + suggested personalisation + a date), distributed via the association's existing member channels; plan the concentrated participation moment against the arc's peak. Real member orgs only; an empty roster means a generic, unaddressed pack, never invented members.

**Phase 5 deliverables**: Editorial calendar (with reactive lane), community playbook (management + building), person-led activation plan (executive + advocacy).

### Phase 6: Measurement & Governance

**Step 1: Define the KPI framework**

Organize KPIs by category. For each, define the metric, measurement source, and baseline target (improvement-based, not absolute).

| Category | Metrics | Source |
|----------|---------|--------|
| Audience growth | Follower growth rate, subscriber growth | Platform analytics |
| Content performance | Impressions, engagement rate, saves, clicks to tagged URLs | Platform analytics + UTMs |
| Person-led authority | Executive/advocate follower growth, profile views, inbound connection quality, share of voice on core topics | Platform analytics + manual |
| AI visibility / citation | Whether the client/executives are named or cited by AI answer engines on core buyer questions; share of AI voice vs competitors | Manual engine checks (see [aeo-geo-social.md](references/aeo-geo-social.md)) |
| Community health | Response SLA adherence, sentiment themes, participation quality, community-sourced conversations | Manual + monitoring tool |
| Employee advocacy | Active advocates, shares, engagement by content type | Advocacy platform or manual |
| Account revival (if scoped) | Post frequency + engagement vs the dated baseline snapshot | Platform analytics vs the pinned baseline |
| Outcome & attribution | **Self-reported attribution** ("how did you hear about us?") as *primary*; consultation requests, event registrations, downloads, and assisted conversions as supporting | Intake forms + CRM + UTMs + site analytics |

**Measure the dark funnel, not the last click.** Most B2B influence now happens off-platform and unlinked, so UTM/last-click attribution systematically undercounts organic social. Make **self-reported attribution primary**, treat UTMs and assisted conversions as supporting, and read spikes in direct/branded traffic after a push as organic signal.

See [measurement-benchmarks.md](references/measurement-benchmarks.md) for directional benchmark ranges and the dark-funnel model: but set targets based on your own baseline, not industry averages.

**Step 2: Define reporting cadence**: **Weekly** content performance review (top posts, engagement, clicks); **Monthly** narrative and audience review (which pillars build followers and qualified traffic); **Quarterly** strategic reset (revalidate pillars, refresh templates, feed learnings into paid); **Annually** re-baseline benchmarks and revisit the modern posture ([strategy-foundations.md](references/strategy-foundations.md)).

**Step 3: Finalize governance**: compile the complete governance document: content approval tiers (Phase 4 QA), escalation matrix (Phase 5 community playbook), crisis protocol (pre-approved holding responses, legal escalation, monitoring protocol), and audit trail requirements (who approved what, retention policy).

**Phase 6 deliverables**: Measurement spec, governance doc.

### Final Output Assembly

After Phase 6, compile all deliverables and present a summary to the user. Then *mention* (never auto-activate) that the user can capture feedback with `asset-feedback`, and file your own `source: agent` retrospective there if the run hit an instruction gap or tool-call failure worth fixing.

**Close-out grounding (file a truthful retrospective).** Before filing the `asset-feedback` retrospective, inspect the overlay you actually used: inspecting an artifact you already loaded is itself an `external_signal`, not a judgement call:

- If `company_context.people[]` was empty/absent **and** you nonetheless named an SME, spokesperson, or advocate (or attributed a quote/POV to a named person), record `{section: "<where>", basis: inferred|fabricated}` in `unsourced_content`.
- For every explicit ask you could not satisfy from client-data, add an `unmet_asks` entry (`reason: no_data`, `resolution` = what you actually did: `stopped` / `asked_user` / `flagged_in_output` / `improvised`).
- Carry the in-canvas unsourced ledger straight into `unsourced_content`; an improvised identity or unsupported claim is the highest-value signal and is **always** reported.

Use `category: data-shortfall` when content improvised under a client-data gap.

**Offer to save reusable config** to `{base}/social-media/`: in campaign mode every `organic/*` path below is written under `campaigns/<campaign_slug>/` instead of the root:
- `config.json`: platform + UTM + compliance settings (if new or changed). **Always root-level and shared**; never nested under a campaign.
- `organic/pillars.json`: editorial pillar definitions
- `organic/series.json`: content series definitions
- `organic/community-playbook.json`: community management rules
- `organic/advocacy.json`: advocacy program config (if scoped)
- **Campaign mode only**: `campaigns/<campaign_slug>/campaign.json`, the manifest: `campaign_slug`, `name`, `window` {start, end, weeks}, `tracks[]` {platform, audience_id, `account` {handle, ownership, owner_org, access_via}, `amplification[]`}, `objective`, `arc` {acts[]} summary, `status` (`planned` | `live` | `closed`), optional `run_mode: "internal-draft"`, `counterArguments[]` (adversarial claims + sourced rebuttals from Evidence Discipline), `priorWaves[]` (the Phase 2 prior-wave inventory), `campaignInsight` (the one-line core insight anchoring the frame), `openConsiderations[]` (unresolved strategic questions, distinct from the gaps ledger), `schema_version: "1.0"`.

Write `"schema_version": "1.0"` into **every** file persisted here. The shapes
and the shared contract with `paid-social-campaign` are documented in
[social-data-schema.md](references/social-data-schema.md): keep additions
additive (consumers ignore unknown keys); never repurpose a key without bumping
the version. On read, a missing `schema_version` is treated as `"1.0"`.

This makes the content available for future runs and for the `paid-social-campaign` skill to reference when designing amplification strategies.

## Optional downstream phases

Phases 7–8 and Export are **optional extensions**: the strategy and editorial
calendar (Phases 1–6) are the product and remain fully valuable on their own.
Run these only when the user wants platform-correct per-post objects (Phase 7),
generated assets (Phase 8), or a published-calendar export.

### Phase 7: Freeze to post objects

At calendar approval, freeze the approved calendar into a validated,
graph-portable `posts.json`: the COPE expansion where one pillar atom fans out
into N native per-post objects. Three artifacts (full schemas in
[post-object-schema.md](references/post-object-schema.md)):

1. **Emit `calendar.json`**: the structured form of the Phase 5 calendar (rows
   of week / pillar_id / series_id / concept / format / cta / platforms / owner /
   utm, plus optional `act`/`beat` in campaign mode: the builder validates them
   per row and copies them onto every post it emits; they are not part of
   `post_id`, so arc metadata never re-keys a campaign's posts).
2. **Run the builder**:
   `uv run python scripts/build_posts.py calendar.json {base}/social-media/config.json -o posts.json`.
   This fills the **structural** fields deterministically (stable `post_id`,
   platform, surface, `media_spec`, utm, schedule) and leaves the **creative**
   fields (`hook`, `body`, `thread_parts`, `hashtags`, `cta`) empty. Builder =
   structure; agent = copy; validator = gate. A malformed row fails with the row
   index and writes no partial output.
3. **Fill the creative fields in chat**: run each through the voice cascade
   (see Voice section).
4. **Validate**: `uv run python scripts/validate_posts.py posts.json`. Rejects
   bad aspect ratios, `producer`↔`type` mismatches, and leftover empty
   placeholders, naming the offending `post_id`. Fix and re-run until it exits 0.
5. **Persist**: write to `{base}/social-media/organic/posts.json` with
   `"schema_version": "1.0"`.

The per-post object is a **superset** of the Phase 5 calendar columns: it
extends, never replaces, the calendar. The same `build_posts.py` /
`validate_posts.py` surfaces are exercised by the eval; the skill never carries
parallel expansion logic.

### Phase 8: Content generation (optional)

Generate branded, coherent assets **one edition at a time with human review**,
per-platform configurable, consuming the `media-gen` MCP. Full loop, brand-context
construction, and edge cases: [content-generation.md](references/content-generation.md);
config + media taxonomy: [platform-content-config.md](references/platform-content-config.md).

1. **Gate.** Runs only if the user opts in AND `content_generation.enabled`.
   State up front: identity reuse (same recurring subject across posts) requires
   `media-gen` reference conditioning (Track A, `PLAN_reference_conditioning.md`);
   if unavailable, assets are *family-resemblance* (consistent style/palette),
   not identical subjects: get explicit acknowledgement.
2. **Lock the style block once** (campaign-level): derive a verbatim prompt
   string from `brand_context.json`/tokens; persist to
   `{base}/social-media/organic/style-blocks/<ref>.txt`. Reused across editions.
3. **Per edition (default one week):** select + partition posts by
   `media_spec.producer` (media-gen vs non-media-gen); run the anchor-select loop
   for media-gen assets (build the `brand_context` dict, generate 3–4 candidates,
   human picks ONE anchor, siblings/video follow); brief non-media-gen posts for
   the user to run separately (chart/diagram/pdf/pptx); caption the edition
   through the voice cascade; human reviews the whole edition before the next one
   is generated. Never advance an edition before that gate.

Asset bytes (base64 + sha256 from the MCP) are written to
`workspace/<client>/output/organic-social-campaign/assets/`.

### Export: Planner / SharePoint / Excel

After Phase 7/8, offer to export `posts.json` (+ asset references) to a
human-publishable surface: an ms365 Planner board, a SharePoint list, or an
Excel calendar (tabular). Mention `m365-manager`'s safety rules (draft / confirm;
never delete) as context; do not invoke it. **No auto-publish** to LinkedIn /
Meta / X / TikTok: the publishing boundary is the exported calendar. (`reepl`
exists for LinkedIn only and is the user's separate choice.)

## Reference Files

Load these as needed: do not read all at once.

| File | When to Load |
|------|-------------|
| [strategy-foundations.md](references/strategy-foundations.md) | **Read once at the start.** The 2026 posture (person-led, citable, community-anchored, video-first, dark-funnel) and the evidence behind every phase. |
| [strategy-document-template.md](references/strategy-document-template.md) | Phase 3 Step 6: assembling the client-facing strategy document. Generic chapter list, evidence-discipline mechanics, `claimsToAvoid` schema, validation-ledger + gaps.md formats, reference-list convention. |
| [strategy-deck-stage1.md](references/strategy-deck-stage1.md) | Output Format Production / Phase 3 Step 6 slide follow-on: the Stage-1 strategy-deck production process — reusable slide spine (incl. per-track content formats + creator tone), source-attribution discipline, render path, and review loop. |
| [linkedin.md](references/platforms/linkedin.md) | When LinkedIn is a selected platform. Page optimization, analytics, formats, posting guidance. |
| [meta.md](references/platforms/meta.md) | When Meta/Instagram is a selected platform. Page setup, content formats, algorithm notes. |
| [twitter-x.md](references/platforms/twitter-x.md) | When X/Twitter is a selected platform. B2B usage patterns, formats, threads. |
| [youtube.md](references/platforms/youtube.md) | When YouTube is a selected platform. B2B video strategy, Shorts, SEO. |
| [reddit.md](references/platforms/reddit.md) | When Reddit is selected. B2B participation etiquette, AI-citation surface, community play (not a posting-cadence channel). |
| [campaign-narrative-arc.md](references/campaign-narrative-arc.md) | **Phase 3 Step 2b: campaign mode only.** Acts/beats, belief-shift sequencing, cross-track echo, differentiation vs prior waves, revival ladder, peak-moment design, worked example. |
| [influencer-advisory.md](references/influencer-advisory.md) | Phase 3 Step 4b: when influencers are in scope. Advice-only boundary, archetypes × modes, concept brief, disclosure baseline. |
| [content-formats.md](references/content-formats.md) | Phase 3: when designing cadence and format mix. Format taxonomy with B2B effectiveness notes, and the hero → derivative (COPE) production map. |
| [employee-advocacy.md](references/employee-advocacy.md) | Phase 3/5: when designing employee advocacy program. Step-by-step program design. |
| [executive-led-content.md](references/executive-led-content.md) | Phase 3/5: the executive/founder-led thought-leadership program (primary distribution engine). Profile-as-channel, ghostwriting engine, governance. |
| [aeo-geo-social.md](references/aeo-geo-social.md) | Phase 3 pillars + Phase 6 measurement: getting content cited by AI answer engines and found in social search. |
| [measurement-benchmarks.md](references/measurement-benchmarks.md) | Phase 6: when setting KPI targets. Directional benchmarks by platform (use cautiously). |
| [community-management.md](references/community-management.md) | Phase 5: when building community playbook. Response frameworks, crisis protocol, moderation. |
| [community-building.md](references/community-building.md) | Phase 3/5: proactive community *building* (owned/third-party communities, participation, dark social) vs the reactive management playbook. |
| [editorial-calendar-template.md](references/editorial-calendar-template.md) | Phase 5: when generating the calendar. Structure and examples. |
| [social-data-schema.md](references/social-data-schema.md) | When persisting to `social-media/` (Final Output, Phase 7/8). `config.json` + `organic/*` shapes, `schema_version`, the paid-social shared contract. |
| [voice-integration.md](references/voice-integration.md) | Any copy-producing step (Phase 5/7/8). The draft→review→rewrite→verify loop, L1/L2 precedence, mechanical self-check, headless fallback. |
| [post-object-schema.md](references/post-object-schema.md) | Phase 7: when freezing the calendar. `calendar.json` input + per-post object schema, the builder/validator seam, aspect Literal sets. |
| [platform-content-config.md](references/platform-content-config.md) | Phase 8: the `content_generation` config block + surface→producer→primitive media taxonomy (what media-gen renders vs what routes to chart/diagram/pdf/pptx). |
| [content-generation.md](references/content-generation.md) | Phase 8: the edition-batched generation loop, anchor-select, Track A vs family-resemblance, brand_context construction, asset output, edge cases. |

## Output Format Production

**Gate: prose deliverables require the deliverable canvas sign-off gate to have passed** (see "Deliverable canvas" above; tabular XLSX outputs are exempt).

This skill owns organic social campaign architecture: editorial strategy, content systems, community management, and measurement. Prose deliverables on the render path should go through `format-prepare-document`; tabular outputs stay on their direct format skill.

**Default sequencing: DOCX first.** The Phase 3 Step 6 strategy document always ships as DOCX first; a PPTX/slide version is an optional follow-on once the DOCX is approved: never generate the deck before the document is signed off.

**Deck density budget.** For the slide follow-on: set a slide-count target up front (~15-20), one idea per slide, at most 5 supporting lines or one visual/table; anything needing a paragraph moves to per-slide speaker notes and the content plan. Internal provenance legends or source tags never appear on client-facing slides: dense supporting content and sourcing live in the speaker notes. Full budget: [strategy-document-template.md](references/strategy-document-template.md) § Deck density budget. Full production process (reusable slide spine, render path, review loop): [strategy-deck-stage1.md](references/strategy-deck-stage1.md).

| Output | Routed renderer / skill | Recommended For |
|--------|-------------------------|-----------------|
| DOCX | `format-docx` | Strategy documents, playbooks, governance docs |
| PPTX | `format-pptx-hd` | Strategy presentations, stakeholder decks (follow-on to the DOCX) |
| PDF | `format-pdf-hd` | Distribution-ready strategy documents |
| XLSX | `format-xlsx` | Editorial calendars, content matrices, KPI dashboards |
**Default**: Produce markdown first; route prose through `format-prepare-document` when formatted output is wanted, keeping XLSX direct for calendars and matrices.

**Brand context to carry forward**: brand location `{base}/brand_context.json`; heading color from `colors.primary`, body font from `typography.body`; logo from `{base}/logos/`; include resolved `expression` (if present) and `deliverable_genre: "organic-social"` in the envelope for downstream render direction. **Diagram integration**: funnel/flow diagrams (content funnel, campaign architecture, editorial workflow) can be generated using the `diagram` skill for branded visual output.

## Output Location

Deliverables follow the standard workspace project structure:

```
workspace/<client>/output/organic-social-campaign/
├── campaign-brief.md
├── strategy-internal.md         # internal working document (Phase 3 Step 6)
├── strategy-CONCEPT.md          # client-facing twin, banner + validation ledger
├── content-matrix.md
├── editorial-calendar.md
├── community-playbook.md
├── employee-advocacy-plan.md    # if scoped
├── measurement-spec.md
└── governance.md
```

**Campaign mode** nests deliverables under the campaign slug: `workspace/<client>/output/organic-social-campaign/<campaign-slug>/` (adding `campaign-arc.md`, and `gaps.md` when `run_mode: internal-draft`); so multi-campaign clients keep separate outputs, mirroring the `campaigns/<campaign_slug>/` persistence namespace.

**Override**: If the prompt specifies a target output directory, use it.

## Error Handling

| Situation | Response |
|-----------|----------|
| No company data available | Gather essentials manually, note that a content library can be created from the output |
| No messaging pillars exist | Build editorial pillars from scratch using company services and audience pain points |
| User wants "just a calendar" | Explain that a calendar without a strategy behind it tends to produce inconsistent content: offer a lightweight strategy (Phase 3 only) as minimum viable structure |
| Too many platforms (4+) | Recommend focusing on 1-2 primary platforms first, then expanding after the system is proven |
| No capacity for community management | Reduce cadence recommendations and skip employee advocacy; flag that engagement drives organic distribution |
| Existing social-media/organic/ data conflicts with new brief | Surface the conflict, ask which takes priority, document the decision |
