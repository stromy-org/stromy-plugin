<!-- since: 2026-07-16 -->

# Strategy document template — the Phase 3 Step 6 client-facing deliverable

This is the generic chapter list and mechanics for the strategy document every
engagement produces at the end of Phase 3, regardless of industry. It is the
DOCX-first artifact the client sees, and the baseline Phase 5 builds the
editorial calendar from. The **Substitution Test** governs everything in this
file: every chapter and rule must make sense for a B2B fintech, a consumer
festival, and a hospital system alike. Nothing client-specific lives here —
client facts live in `{base}/company_context.json`, `{base}/social-media/`, and
the campaign manifest.

## Chapter list

Not every chapter applies to every engagement — omit what the scope doesn't
need (e.g. no influencer chapter for a program with no B2C track), but keep the
order. A program (always-on, no campaign manifest) uses the same chapters minus
the campaign-only ones (arc, revival ladder, launch mechanics).

| # | Chapter | Feeds from |
|---|---------|-----------|
| 0 | Executive summary | Everything below, written last |
| 1 | Frame & positioning | Phase 3 Step 1 (pillars), the core insight, the reframe (from → to) |
| 2 | Audiences & the N × M matrix | Phase 1 Step 2 (audience type), Phase 2 Step 2 (ICP) |
| 3 | Core messages per pillar | Phase 3 Step 1, Evidence Discipline |
| 4 | The campaign arc (campaign mode) | Phase 3 Step 2b, [campaign-narrative-arc.md](campaign-narrative-arc.md) |
| 5 | Distribution model | Phase 3 Step 4 (launch-anchor, ecosystem tagging, revival ladder) |
| 6 | Boost / amplification strategy | Phase 3 Step 2b (when any track is non-`organic`) |
| 7 | Influencer advisory (if scoped) | Phase 3 Step 4b, [influencer-advisory.md](influencer-advisory.md) |
| 8 | Creative direction | Phase 4 |
| 9 | Measurement & KPIs | Phase 6 Step 1 |
| 10 | Next steps & timeline | Handoff sequencing to the client and to the content plan |
| — | Legal & claims compliance (embedded per-chapter, not a single chapter) | Evidence Discipline |
| — | Validation appendix | Every open confirmation item, gated before external send |
| — | Reference list | Every cited source, mandatory |

### Chapter 0 — Executive summary

One page. States the reframe (from → to belief), the core insight in one
sentence, the audience(s) and channel(s), the campaign duration (if time-boxed),
and the single most differentiating element of this engagement versus anything
the client has run before. Written last, read first.

### Chapter 1 — Frame & positioning

The reframe this engagement argues for, stated as an explicit **from → to**
belief shift. The core insight that makes the *old* belief understandable
rather than foolish — a good core insight explains *why* the audience holds the
assumption, not just that it's wrong. State the per-audience goal (what each
audience should do differently once the reframe lands) and, if relevant, the
**design gap**: does the audience have an obvious action to take once
convinced, or does the strategy need to manufacture one (a mechanic, a choice,
a participation moment)? Name that gap explicitly rather than assuming the
persuasion alone closes the loop.

### Chapter 2 — Audiences & the N × M matrix

The explicit table: N audiences (rows) × the frame's narrative pillars
(columns), each cell stating what the pillar means for that audience — tone,
proof type, format affinity, CTA style. This chapter is the one that must read
as generic architecture, not a client instance: two audiences sharing one frame
is one shape of the matrix; three audiences with divergent frames is another;
a single-audience program with three pillars collapses the matrix to one row.
Never hardcode "B2B/B2C" as if it were structural — state the client's actual
audiences and let the matrix take whatever shape they require.

### Chapter 3 — Core messages per pillar

Per pillar: the headline claim, its evidence (tiered per Evidence Discipline
below), the tone/posture per audience, and the banned constructions for this
pillar specifically (beyond the standing voice-cascade bans). Every claim here
has already passed the Evidence Discipline gate before it appears in this
chapter — this chapter presents the *outcome* of that gate, not the place where
tiering happens for the first time.

### Chapter 4 — The campaign arc (campaign mode only)

The acts/beats table from [campaign-narrative-arc.md](campaign-narrative-arc.md),
the peak moment, and — critically — the **differentiation-vs-prior-waves**
section: what previous campaigns on this evidence/theme said, and what this one
adds. A campaign that repeats a prior wave without an honest answer to "what's
new" reads to the client as a copy-paste.

### Chapter 5 — Distribution model

Which layer (page, executive, employee/member advocacy) carries which content,
the **launch-anchor decision** (page vs. person, and why), the **ecosystem
tagging plan** (roster + the client heads-up gate — tagging never precedes
confirmed heads-up), and — where a track's account is dormant or borrowed — the
**revival ladder**: organic → paid boost → one collaboration, in that order,
with account revival stated as its own KPI and a dated baseline snapshot taken
before the revival phase starts.

### Chapter 6 — Boost / amplification strategy

Mandatory whenever any track's amplification is non-organic. Budget allocation
across the arc (or across the always-on cadence for a program), boost triggers,
and expectation-setting for a cold or low-reach account — never sell a cold
account's first weeks as a reach guarantee.

### Chapter 7 — Influencer advisory (if scoped)

Archetype × mode recommendations, concept directions, and the disclosure
baseline for the client's jurisdiction, per
[influencer-advisory.md](influencer-advisory.md). Restate the advice-only
boundary explicitly in this chapter — the client reads this document without
the skill's guardrails in view, so the boundary has to be visible on the page,
not just enforced upstream.

### Chapter 8 — Creative direction

The visual/creative system (Phase 4), the content matrix summary, and — if
relevant — the fallback options (e.g. a data-visualization fallback when a
bespoke visual system is out of budget).

### Chapter 9 — Measurement & KPIs

The KPI table from Phase 6 Step 1, with the account-revival KPI (if scoped)
stated against the pinned baseline, and the review cadence.

### Chapter 10 — Next steps & timeline

The concrete sequence from this document to the next deliverable (typically:
internal review → client-facing send → client sign-off → content-plan draft →
example content). State who owns each step and roughly when.

## Evidence & citations

The mechanical gate is defined in the skill's Evidence Discipline section; this
is the **document-facing convention** — how the gate's output looks on the
page.

### Evidence tiers

| Tier | What qualifies | How to cite it |
|---|---|---|
| Peer-reviewed | Published, reviewed academic research | Author(s)/institution, publication, year |
| Institutional / official | Government agencies, official statistics bureaus, regulators, international bodies | Agency name, dataset/report title, year |
| Industry-funded | Trade-association or company-commissioned research (even when methodologically sound) | Name the funder explicitly alongside the researcher — never present as independent |
| Journalistic | Reputable press reporting a fact or figure | Outlet, date |

A pillar's citation mix should be visible at a glance: never let a whole
pillar's proof rest on one industry-funded source with no independent anchor
(the diversification gate).

### `claimsToAvoid` schema (client-data)

Loaded from `{base}/social-media/claims-to-avoid.json` before any pillar is
drafted. Additive, optional, and — like every client-data file — never
fabricated; absence means no known banned claims, not license to assume
anything is safe.

```json
{
  "schema_version": "1.0",
  "banned_claims": [
    {
      "claim": "digital advertising is always greener than print",
      "reason": "contradicted by the client's own commissioned research on device-side emissions",
      "added_by": "client",
      "date": "2026-07-10"
    }
  ],
  "banned_figures": [
    {
      "figure": "a single merged reuse-count number",
      "reason": "two credible figures measure different scopes (practice average vs. technical ceiling) and must never be collapsed into one"
    }
  ],
  "sensitive_topics": ["named competitor comparisons"]
}
```

A banned claim or figure is never used even if independently verified true in
some other context — flag it to the user and ask, rather than silently
substituting a nearby permitted figure.

### Never merge incompatible statistics

The recurring failure mode: two credible sources state different numbers for
what looks like "the same" fact because they measure different things (a
practical-average figure vs. a technical-ceiling figure; a national figure vs.
an international one used as an indicative comparison; pre- vs. post- a
structural change in the underlying market). The document must **show both,
scoped**, never merge them into one convenient number and never silently pick
the more favorable one.

### Counter-argument chapter (adversarial rebuttal)

For each pillar with a live, credible counter-argument (surfaced in Phase 2's
"Adversarial check" and Evidence Discipline step 6), the strategy document
states: the counter-argument, its source and scope, and a sourced rebuttal that
acknowledges what the counter-argument gets right within its own scope before
showing the fuller picture. Publishing the rebuttal as active client-facing
content is a client sign-off decision — mark it as a validation-ledger item,
never publish unilaterally.

### Reference list (mandatory, every client-facing document)

The final section of every client-facing strategy document. One row per cited
source:

| Source | Tier | Date | Scope note |
|---|---|---|---|
| e.g. national statistics agency, dataset name | Institutional | 2025-12 | what it measures; note if used as an international indicator rather than a local figure |

No client-facing strategy document ships without this section, even a short
one.

## Validation appendix (client-facing gate)

The client-facing **concept** document (see the skill's Phase 3 Step 6
internal → external twinning) always ends with a Validation Ledger — the
generic form of the same discipline the `internal-draft` `gaps.md` uses
internally. Both share this structure; the difference is audience and gate:
`gaps.md` is an operator/collaborator working document, the Validation Ledger
is the one section of the client-facing document itself that names what still
needs confirming.

### Shared structure (`gaps.md` and the Validation Ledger)

- **Severity key** — 🔴 blocking (document cannot be sent until resolved), 🟠
  important (should resolve before send, but not sending-blocking on its own),
  🟡 nice-to-confirm (improves precision, not required to send).
- **Categories** — people (spokesperson names, mandates), channels (account
  ownership, access, governance), evidence (contested figures, prior
  collaborations whose content is unconfirmed), prior-wave (unresolved
  adjacency questions), voice (uncalibrated tone), assets (missing imagery,
  unconfirmed rights), measurement (unset baseline, unconfirmed anchor date).
- **Rows** — 4 columns: `# | topic | what's unresolved | what's needed`.
- **Ranked-for-review agenda** — the rows sorted by severity, presented first;
  this is the deliverable's spine for the reviewer, not an afterthought
  appendix.
- **Change log** — a running list of what closed, when, and how (so a
  reviewer returning after a week sees what moved).

`gaps.md` additionally carries the `internal-draft` run-mode machinery (draft
watermark, `-DRAFT` suffix, phase blocks) documented in the skill's Run Mode
section and [social-data-schema.md](social-data-schema.md). The Validation
Ledger inside the client-facing document does not need those internal-mode
mechanics — it needs only the shared row structure above, because its job is
narrower: tell the client (or the reviewing collaborator) exactly what to
confirm before the document is treated as final.

## Internal → external twinning (posture, not just content)

Two artifacts, two postures, produced from the same underlying work:

| | Internal working document | Client-facing concept document |
|---|---|---|
| Audience | Operator + collaborator(s) | The client (or the client via a reviewing partner) |
| Banner | None required | **CONCEPT / DRAFT — not for client distribution** until sign-off |
| Open items | May carry inline TBDs / open questions anywhere | Consolidated into the Validation Ledger appendix, not scattered inline |
| Editing posture | Iterated freely, versioned informally | Frozen once shared for review; changes tracked as a new version, not silent edits |
| Send gate | None | Never sent externally while a 🔴 blocking Validation Ledger row is open |

A language twin (when the project language differs from a collaborator's or
client's shared working language) is a **third dimension**, not a substitute
for the internal/external distinction — a translated document still needs its
own posture (internal vs. concept) applied.

## Deck density budget (slide follow-on)

The slide deck derived from an approved strategy document has a different job
than the document: it is presented and skimmed, not read. LLM generation
naturally over-produces, so the budget is set **before** any slide is written:

- **Slide-count target up front** (~15–20 for a full two-track strategy;
  fewer for single-track). Agree it with the reviewer before generating.
- **One idea per slide.** A slide's headline states the idea; the body carries
  at most **5 supporting lines or one visual/table** — never both a dense
  table and a paragraph.
- **Two-column comparison tables beat prose** wherever two tracks, options, or
  audiences are being contrasted.
- **Speaker notes carry the density.** Everything a presenter needs beyond the
  visible slide — full sourcing, nuance, the "why", anticipated questions —
  goes into per-slide speaker notes (renderers such as `format-pptx-hd` accept
  a `notes` field per slide). The client sees a lean slide; the presenter
  keeps the depth.
- **No internal markers client-facing.** Provenance legends, source-tags
  (e.g. "[E]/[R]"), watermark shorthand, and pipeline metadata never appear on
  client-facing slides; they live in the build plan and speaker notes only.
- **Expect iterations.** Reviewers converge fastest when shown a 1–2 slide
  density prototype of the densest slides first, then the full deck calibrated
  to the accepted density.

## What belongs in the deck vs the content plan

The strategy deck and the content plan are two tiers of the same work. Cutting
depth from the deck is a **routing** decision, not a deletion:

| Artifact | Carries | Does NOT carry |
|---|---|---|
| Strategy deck (client-facing) | Vision, audience/track structure, timeline, pillars at headline depth, distribution model, budget table, KPI table, next steps | Per-pillar messaging detail, full evidence base, alternative/extra narrative lines, legal analysis, counter-evidence, operational governance detail |
| Content plan (working doc) | Per-pillar key messages + proof points, post concepts/formats, the full reference list, extra narrative lines as content inspiration, evidence tiers | Strategy re-litigation — it instantiates the approved deck, never contradicts it |
| Briefings (creator / compliance) | Disclosure rules and format requirements, platform ad-targeting constraints, claim guardrails per jurisdiction, do/don't lists | Anything the client must approve strategically |

When a reviewer says "this is too detailed for the deck," the content moves
down a tier with a pointer — it is never silently lost.

## Review-response ledger

When a client-side reviewer (client, agency PM) returns comments on the
strategy document, respond with a **ledger**, not an edit-and-hope pass. One
row (or entry) per comment:

- **Comment** — verbatim or faithfully condensed, with its anchor (what text
  it was attached to).
- **Decision** — agreed / agreed-with-note / validate-with-reviewer. The
  reviewer's editorial calls govern; disagreement is expressed as a note plus
  compliance, not as quiet non-implementation.
- **Why it was there** — the original, *grounded* rationale (traceable to a
  source, a prior decision, or research done; never reconstructed from
  imagination — if the rationale cannot be recovered, say so).
- **Action** — where the content goes: stays in deck / moves to content plan /
  moves to a briefing / dropped (with reason) / open question.

Close the ledger with: (a) a short summary (how many agreed / flagged), and
(b) the open questions collected into ONE clarification message — after first
answering everything that can be self-researched (dates, public facts,
regulatory scope): never ask the reviewer something you can verify yourself.
The ledger is shareable with the reviewer by default; it is the record that
nothing useful was silently lost.
