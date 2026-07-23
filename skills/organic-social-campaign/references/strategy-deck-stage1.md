<!-- since: 2026-07-23 -->

# Strategy Deck (Stage 1) — production process

The Phase 3 Step 6 strategy document has a DOCX-first, always-produced twin: a
**client-presentable slide deck**. This file is the detailed, repeatable
production process for that deck — the reusable slide spine, the
source-attribution discipline for claim slides, the render path, and the
review loop that turns an approved strategy document into a signed-off deck.
The **Substitution Test** governs everything here exactly as it governs the
rest of this skill: every slide role and rule must make sense for a Belgian
fintech, a music festival, and a hospital system alike. Nothing client- or
engagement-specific lives in this file.

This file does not restate what is already defined elsewhere — it assumes and
cites:

- **The deck density budget** and **what belongs in the deck vs the content
  plan** — [strategy-document-template.md](strategy-document-template.md)
  § Deck density budget, § What belongs in the deck vs the content plan.
- **The campaign narrative arc** (acts, beats, revival ladder, peak moment) —
  [campaign-narrative-arc.md](campaign-narrative-arc.md).
- **The review-response ledger and PM-authority posture** —
  [strategy-document-template.md](strategy-document-template.md)
  § Review-response ledger; SKILL.md Phase 3 Step 7.
- **The Evidence Discipline gate** (tiering, cite-or-hedge, diversification) —
  SKILL.md § Evidence Discipline; [strategy-document-template.md](strategy-document-template.md)
  § Evidence & citations.

## Where the deck sits

This skill's own workflow already produces three tiers of deliverable, in
order: the **strategy document** (Phase 3 Step 6 — architecture, pillars,
distribution, arc, KPIs), the **content plan** (Phase 4/5 — the content
matrix and editorial calendar that instantiate the strategy into dated,
per-pillar production detail), and **rollout** (Phase 7/8 — frozen post
objects, generated assets, and the ongoing weekly production rhythm). The
strategy deck formalized here is the **client-presentable rendering of the
first tier**: not a fourth deliverable, and not a shortcut that skips the
document. Route it exactly like the DOCX — draft after Phase 3 is approved,
never before.

**When to use it.** Offer the deck whenever the strategy document will be
presented live or shared with a reviewer who skims rather than reads closely
(a client stakeholder, an agency PM, a board). A program (always-on, no
campaign manifest) or a single-audience engagement uses the same spine with
the per-track repeats collapsed to one pass — the shape degrades cleanly, it
does not need a different spine.

**What the deck is not.** It is not a place to re-litigate strategy (the deck
instantiates the approved document, same as the content plan does), and it is
not a substitute for the content plan's operational depth — per-pillar
messaging, the full evidence base, and format-level production detail stay
in the content plan (see the boundary table cited above).

## The reusable deck spine

A generic slide-by-slide structure abstracted to **roles**, not content. Every
role below is a *purpose*, not a fixed slide count or wording — an engagement
with three audiences repeats the per-track block three times; a single-track
program collapses the overview/timeline rows to one column and skips the
per-track divider.

| # | Slide role | Carries | Density note |
|---|---|---|---|
| 1 | Cover | Deliverable title, campaign/program name, client + delivering-partner branding, date | Title only — no content density |
| 2 | Campaign vision | Problem/context (the Chapter 1 reframe — the *from → to* belief and the core insight), goal, approach (the one-frame, N-track framing) | 2–3 short blocks |
| 3 | One-message, N-tracks overview | Per-track comparison: channel/account, audience (label verbatim — see below), primary focus, tone, core argument, distribution, **and a content-formats row** (2–4 concrete examples per track) | One N-column comparison table beats prose; see M10 below |
| 4 | Timeline | One bar per track across the window; per-track phase labels; any client-named concurrent event or tentpole flagged **to-confirm** unless independently verified | One visual, optional callout |
| — | **Per-track block** (repeat once per audience/track) | | |
| 5a | Track divider | Section identity, colour-coded per track when the brand supports it | Chrome only |
| 5b | Track audience & goal opener | Who this track is for (audience label verbatim), what it's for, **concrete content-format examples for this track** | 2 blocks |
| 5c | Track distribution | Which account carries the track, the ecosystem/partner network if any (roster + the client heads-up gate — Phase 3 Step 4) | Diagram or 1 block |
| 5d | Track strategy / phasing | Cadence, phasing or beats (campaign mode: the arc's per-track beat — cite, don't restate, [campaign-narrative-arc.md](campaign-narrative-arc.md)), the revival ladder if the account is dormant/borrowed | Reference the arc file rather than re-deriving it |
| 5e | Content pillars | Per pillar: headline claim, why it matters to this audience, **one paired claim + source** citation | One table row per pillar — see Source-attribution discipline below |
| 5f | Track-specific extras | Whatever this track's engine needs load-bearing on-slide (an amplification-budget line + one compliance line for a paid/influencer track; a reach mechanic for an organic-revival track) | Only what's load-bearing; deeper detail routes to the content plan |
| 6 | Evidence / sources (optional client enhancement) | The claim-per-source extraction across pillars, offered as something the client can accept or decline | See "Evidence slide as an optional enhancement" below |
| 7 | Influencer / creator archetypes + profiles | Archetypes first (advice-only — [influencer-advisory.md](influencer-advisory.md)); named profiles only if the client/PM supplied them, each carrying name/handle, a verified & dated follower count, archetype fit, content angle, and **tone** | 3 archetype cards + N profile cards |
| 8 | KPIs | Split **per track** — never one merged funnel metric across tracks with different jobs | Two-panel or two-column table |
| 9 | Next steps | The sign-off ask, immediate per-track actions, the handoff to the content plan | 2–4 blocks |
| 10 | Closing (optional) | Thank-you/contact; an optional one-line pointer that deeper detail lives in the content plan | 1 line; cut first if the deck runs long |

### Per-track content formats and creator tone as standard elements

Two structured fields belong in the spine **by default**, not as review-round
additions: a **content-formats** row/line at the two-track overview (3) and
each track's opener (5b), and a **tone** field on every influencer/creator
profile (7). Both are read from the campaign's own format/tone definitions —
`campaign.json` → `tracks[].contentFormats` (see
[social-data-schema.md](social-data-schema.md)) or the client's own
input/intake, and the client/PM's own description of a named creator's
register — **never invented to sound plausible for the industry or
archetype**. Full mechanics: [content-formats.md](content-formats.md)
§ Declaring content formats per track; [influencer-advisory.md](influencer-advisory.md)
§ Presenting a candidate on a client-facing slide/page. A strategy artifact
that names pillars and channels but leaves the concrete formats implicit
reads as abstract to a reviewer — this is a recurring finding, not a one-off
preference, so it is now a default deck element for every engagement.

### Evidence slide as an optional enhancement

The claim-per-source extraction (pairing each cited source's key statements
with the pillar or claim they support) is genuinely useful, but it is not
mandatory content: present it to the client/reviewer as an **enhancement they
can accept or decline**, not a slide that ships unilaterally. Where every
pillar already carries its own paired claim+source on slide 5e, a dedicated
evidence slide adds the *extra* supporting statements a source offers beyond
what's already used — offer it, let the client decide whether it enters the
deck (and, downstream, content generation) or stays in the content plan's
reference list.

## Source-attribution discipline on claim slides

Every claim that appears under a source label must actually derive from that
source — this sounds obvious and is the most common way a claim slide goes
wrong under review. Two failure modes to guard against explicitly:

1. **Over-attribution under a shared header.** A column or section labeled
   generically (e.g. "supporting evidence", "what the research shows") that
   in fact pairs several different claims with several different sources
   implies a single source for all of them unless **each row carries its own
   source tag**. A shared header is chrome; the attribution lives at the row
   level, always.
2. **Unhedged contested scope.** A claim whose public scope is contested,
   partially sourced, or measured differently than it is being used (see the
   skill's "never merge incompatible statistics" rule) must be hedged on the
   slide itself — a footnote a reviewer has to hunt for does not satisfy the
   gate.

**Enforcement.** This is exactly the class the skill's own **Evidence
Discipline** gate already targets (cite-or-hedge, tier every source, never
merge incompatible statistics) — apply that gate mechanically to every deck
row before the deck is rendered, not only to prose in the document. A claim
slide is not exempt from the gate just because it is terser than a paragraph.

## The render path

The deck is authored as slide content (HTML/structured slide objects with
per-slide `notes`) and handed off to the org's branded PPTX render skill
(server-side, brand-gated) — this skill authors the content and mentions the
render skill as context; it never invokes another skill directly.

- **Single-line discipline at authoring time.** Write every slide title, and
  every dense-table cell or diagram-node label, to fit on one line. Some
  HTML→PPTX render paths silently corrupt multi-line text elements (a
  wrapped heading, a wrapped cell, an overlapping node label) in ways a
  render-back preview can miss. The definitive guardrail for this lives on
  the render skill itself — mention it, do not restate its mechanics here.
- **Client-language deck + working-language twin.** The deck follows the same
  twinning convention already defined for the strategy document (see
  [strategy-document-template.md](strategy-document-template.md)
  § Internal → external twinning and its language-twin note): the
  client-facing deck ships in the client's own language, typically
  **notes-free**; a **working-language twin** (the team's shared working
  language) carries the same slides **with full speaker notes** for internal
  review and handoff. Keep both twins at the same slide count, same order,
  same claims — never let content drift between them.
- **PDF export for the client; the editable deck stays internal.** The
  default client deliverable is a **paginated PDF export** of the signed-off
  deck — a fixed, review-ready artifact. The editable deck (the working
  substrate) stays on whatever internal or shared collaboration surface the
  team iterates on; it crosses to the client only as the PDF, never as the
  editable source file, unless the client explicitly asks to co-edit.

## The review loop (shared collaboration surface)

When the working deck lives on a shared collaboration surface (a client or
partner's document workspace) rather than only in chat, apply the same
discipline any shared-surface production run should:

- **Fetch the latest version first, every run.** A reviewer's own direct
  small edits, or new comments, can land on the shared file between runs —
  never process a locally-cached or previously-fetched copy as if it were
  current.
- **Comments are directional, not verbatim insertions.** Interpret and
  integrate a reviewer's comment into the deck's own structure and voice;
  do not paste comment text onto the slide unedited.
- **Publish revisions in place.** Replace the same file/link's content
  rather than uploading a new version under a different name — the shared
  surface's own version history is the audit trail; a `-v2` filename
  destroys it.
- **Watch the file-lock gotcha.** An open viewer session on the file can
  silently block a re-publish from landing. Close viewer sessions before
  republishing, and verify the upload actually took (re-fetch and check)
  rather than assuming success.

## Review → response ledger, and PM authority

When a reviewer (a client-side PM, an agency partner, the client themselves)
marks up the deck, this is the **same** review discipline the strategy
document already uses — not a separate deck-specific process:

- **The reviewer's editorial call governs.** The skill's job is to justify
  the original reasoning and comply, not to defend research-maximalism
  against an explicit cut instruction.
- **Produce a review-response ledger** — per comment: decision, the
  original grounded rationale (traceable to a source or a prior decision;
  never reconstructed from imagination), and the action (stays on the deck /
  moves to the content plan / moves to a briefing / dropped / open
  question). Full ledger format:
  [strategy-document-template.md](strategy-document-template.md)
  § Review-response ledger.
- **Collect genuinely open questions into one clarification message**, after
  first answering everything self-researchable — never ask a reviewer
  something verifiable independently.

## Audience-label discipline

Every audience-facing slide in the spine (the N-tracks overview row, each
track's opener, the KPI panel) states the audience using the **exact label
already defined in client-data or the campaign manifest**
(`messaging/audiences.json`, or the campaign manifest's resolved
`tracks[].audience_id` definition) — never a paraphrase, and never a generic
stand-in ("decision-makers", "consumers") invented at deck-authoring time. A
reviewer who already has their own defined audience language will read a
paraphrase as a fidelity gap, not a wording nit. See
[strategy-document-template.md](strategy-document-template.md) Chapter 2 for
the same rule applied to the strategy document.
