---
name: proposal
description: "Build production-quality consulting proposals, executive briefs, and bid documents. Supports 5 proposal archetypes (Corporate, Consultant, Entrepreneur, Creative, Minimal) with quick-setup and full intake workflows. Format-agnostic — handles proposal strategy, content assembly, and quality validation, then produces the final document in the requested output format (DOCX, PPTX, PDF). Use when creating new proposals, revising existing ones, merging sections, or condensing documents."
license: Proprietary. LICENSE.txt has complete terms
---

# Consulting Proposal Builder

## Inputs from client-data

- `companies/{client_slug}/brand_context.json` — resolved brand; read `expression` (`principles`, `signatureElements`, `antiPatterns`) for compact brand direction and `identity.positioning`. **Reference, never bind** — prose guidance, not hard rules.
- `companies/{client_slug}/company_context.json` — redacted public company facts: `company` (name, description, services, industries, positioning, values, stats, publicContact), `credentials`, `pricing.publicModels` (+ `paymentTerms`, `discounts`), `legal.publicTerms`, `people` (id, name, title, publicRole, publicBio, quoteStyle)
- `companies/{client_slug}/logos/` (optional) — logo files (paths resolved from `brand_context.logo`)
- `companies/{client_slug}/proposals/` (optional) — proposal content library (case studies, prior proposals)
- `companies/{client_slug}/proposals/methodologies.json` (optional) — methodology library
- `companies/{client_slug}/boilerplate.json` (optional) — boilerplate sections, including `sign_off` (closing salutation, locale/register-keyed: `default_en`/`default_nl`/`formal_en`/`formal_nl`) and `contact_block` (signer + firm + contact lines, locale-keyed)
- `companies/{client_slug}/voice/voice-profile.md` (optional) — entity voice profile (L2)
- `companies/{client_slug}/voice/voice-anchors.md` (optional) — entity voice anchors (L2)

## Voice

A proposal is client-facing prose, so run the org voice cascade before writing the
narrative sections (context, approach, scope, pricing rationale, next steps).

1. **Read the L1 baseline.** When the `stromy-format` MCP is connected, read
   `voice://baseline` (anti-AI-smell rules) and `voice://review` (the pre-output
   review checklist) via `ReadMcpResourceTool`.
2. **Read the local L2 profile when present.** Resolve the company slug as in
   "Company Data Integration" and read `companies/<slug>/voice/voice-profile.md` and
   `voice-anchors.md` if they exist.
3. **Apply, then disclose.** Review the draft against L1 + L2; if neither is
   reachable, say so explicitly rather than letting a silent skip read as a pass.
   L2 may add bans but never relax L1.

## Deliverable canvas (prerequisite)

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

This skill produces polished consulting proposals, executive briefs, capability statements, and bid documents. It is **format-agnostic** — it owns the proposal domain logic (structure, content strategy, quality gates) and hands signed-off render work to `format-prepare-document`.

**This skill provides the *what*** — proposal structure, content assembly from company data, interactive intake, and quality gates.
**`format-prepare-document` provides the render-path handoff** — structure packaging, substrate-aware planning, and routing to the final `format-*` renderer.

Use this skill when a user asks to:
- Write or generate a consulting proposal
- Create an executive brief or capability statement
- Revise, update, or refresh an existing proposal
- Merge content from multiple proposal sources
- Condense a full proposal into a shorter format
- Build a bid document or statement of work
- Respond to a client brief with a formal proposal

## Company Data Integration

> **No overlay → STOP.** If this plugin has no `companies/` directory, do not fabricate a brand, default to a self/Stromy brand, or attempt to produce a proposal. Surface: "no client overlay found — I cannot produce a proposal without company data." Only the user can supply the missing overlay.

> **Empty `people`/`credentials` → ask or omit, never fabricate.** The overlay can be present yet incomplete — a present-but-empty data field is still missing data, not a license to improvise a real person's profile. If `company_context.people[]` is empty or absent, do **not** write team bios or assign roles/titles to named individuals from the service catalogue, `business-cards/`, or inference — ask the user which team to feature, or omit the **Team & Qualifications** section. Likewise if `credentials` is empty: omit or flag it, never synthesize certifications, awards, or positioning presented as credentials. Names, titles, and contacts from `business-cards/` may be listed verbatim, but **no bio or specialism may be attributed to a named person without a `publicBio` source** (in `company_context.people[]` or `proposals/team-bios.json`). This is the within-overlay twin of the no-overlay STOP above.

This skill draws from structured company data in the invoking plugin's `companies/{client_slug}/` overlay.

### Discovery

1. List `companies/` to find available client overlays (`{client_slug}` directories)
2. Zero entries → STOP (see guard above)
3. One entry → use it directly; state which client you resolved
4. Multiple entries → ask the user which company is proposing; do not guess
5. After resolving `{client_slug}`, read `company_context.json` for all company facts; check `company_context.people[]` for "Prepared by" and contact sections (filter by `publicRole` containing `"author"`, auto-select if the array has exactly one such person)

> **Note on PII:** `company_context.json` carries only the **public** subset — no banking details, registration/VAT/KVK numbers, billing email, personal email, or personal phone. Those fields are operator-side only in canonical `client-data` and are intentionally not available in deployed plugins. The skill works from the public subset.

### Loading Company Data

```
companies/{client_slug}/company_context.json  → Company facts: name, services, pricing, credentials, legal, people
companies/{client_slug}/brand_context.json    → Resolved brand: expression, identity, colors, fonts, logo
companies/{client_slug}/proposals/             → Proposal content library:
  ├── case-studies.json      → Past performance
  ├── team-bios.json         → Key personnel with bio variants
  ├── methodologies.json     → Standard approaches/frameworks
  ├── boilerplate.json       → Assumptions, disclaimers, legal terms
  ├── testimonials.json      → Client quotes
  ├── differentiators.json   → Win themes and competitive positioning
  └── partnerships.json      → Technology and strategic partnerships
```

For full schema documentation, see [company-data-schema.md](references/company-data-schema.md).

### Content Library Assembly

Map library items to proposal sections by matching tags, service IDs, and industry relevance:

| Proposal Section | Content Source | Selection Criteria |
|------------------|---------------|-------------------|
| Client Context | Manual (from brief/RFP) | — |
| Approach & Methodology | `methodologies.json` | Match by `applicableServices` or tags |
| Team & Qualifications | `team-bios.json` | Match by `expertise` tags; use `executive` or `technical` variant based on audience |
| Relevant Experience | `case-studies.json` | Match by `tags` (industry, service type); use `short` or `long` variant based on depth |
| Pricing & Investment | `company_context.json` → `pricing.publicModels` | Match by service's `pricingModel` reference |
| Risk Management | `boilerplate.json` → `assumptions` | Standard assumptions + engagement-specific ones |
| Terms & Conditions | `boilerplate.json` → `legalTerms` | Standard terms from `company_context.json` → `legal.publicTerms` |
| Proof Points (inline) | `testimonials.json` | Match by `tags` and `caseStudy` reference |
| Win Themes (inline) | `differentiators.json` | Match by `applicableServices` or tags; thread throughout proposal |
| Partnership Proof (inline) | `partnerships.json` | Match by `relevantServices`; use in Team & Qualifications or Credentials |
| Closing salutation | `boilerplate.json` → `sign_off` | Pick the variant matching the proposal's language + register (`formal_*` for first-contact / public-sector; `default_*` otherwise) |
| Next Steps contact block | `boilerplate.json` → `contact_block` | Pick the variant matching the proposal's language; emit verbatim in the Next Steps / closing section |

## Interactive Intake Workflow

The proposal process begins with a structured conversation to gather requirements before writing.

### Phase 1 — Signal

User provides:
- Client brief, RFP, or verbal description of the opportunity
- Which company is proposing (if multiple profiles exist)

### Phase 2 — Smart Interview

For common B2B scenarios, a quick-setup path can shortcut configuration using proposal archetypes. See [archetypes.md](references/archetypes.md) for presets.

Ask **only questions that genuinely add value** — skip anything deducible from the brief. Aim for 3-5 focused questions, adapting based on what's already known.

**Always ask:**
- What depth: executive brief (2-4 pages) or full proposal (15-25 pages)?
- Which pricing model? (present options from `company_context.json` → `pricing.publicModels`)

**Ask if not clear from brief:**
- What's the primary pain point to emphasize?
- Which team members to highlight or exclude?
- Any sections to skip or emphasize?
- Target audience: technical evaluators, executives, or mixed?
- Competitive context: sole-source or competitive bid?

**Never ask:**
- Questions answered in the brief/RFP
- Generic questions that don't change the output
- Questions about the company's own capabilities (that's in the data layer)

For detailed guidance, see [intake-workflow.md](references/intake-workflow.md).

### Phase 3 — Strategy

Present a content plan for user approval before writing:

1. **Proposed sections** — which sections from the skeleton to include, with rationale
2. **Content selections** — which case studies, team members, and methodology to feature (with reasons)
3. **Pricing structure** — proposed pricing model and breakdown approach
4. **Key differentiators** — 3-5 win themes to thread through the proposal
5. **Output format** — DOCX, PPTX, or PDF (confirm with user)
6. **Archetype** — which proposal archetype best fits (Corporate, Consultant, Entrepreneur, Creative, Minimal). See [archetypes.md](references/archetypes.md)

Wait for user approval before proceeding to Phase 4.

### Phase 4 — Production

Execute the proposal workflow (Steps 1-7 below). All drafting happens **in the deliverable canvas** (see "Deliverable canvas" above) — open it now if not already open.

### Phase 5 — Review

Present the draft canvas to the user with a quality gate summary. Run the checklists from [quality-gates.md](references/quality-gates.md) and flag any issues. Iterate in the canvas until the user signs off — only then proceed to document production (Step 3 Assembly onward).

## Editing Modes

Choose the correct mode based on what the user needs:

### Create New
Start from a brief, template, or verbal description and produce a complete proposal.
→ Run intake workflow (Phases 1-3), then workflow Steps 1-7 below.

### Revise Existing
Update scope, pricing, staffing, case studies, or other sections in an existing proposal without breaking formatting.
→ Edit the existing document in place, or use the redlining workflow if tracked changes are needed.

### Merge Sections
Combine content from multiple source documents (e.g., prior proposals, boilerplate library, SME drafts) into a single cohesive proposal.
→ Extract content from sources, then follow Create New workflow with pre-written section content.

### Condense
Shorten a full proposal to N pages (e.g., produce a 2-page executive brief from a 40-page proposal).
→ Read the full proposal, identify key messages per section, then Create New with a reduced skeleton (see condensed format mapping in [sections.md](references/sections.md)).

**Decision tree:**
1. Does a proposal document already exist? → **Revise** or **Condense**
2. Are there multiple source documents to unify? → **Merge**
3. Starting from scratch or a brief? → **Create New**

## Standard Proposal Skeleton

The canonical section order for a full consulting proposal. Not every proposal needs every section — adapt based on scope and formality.

| # | Section | Purpose |
|---|---------|---------|
| 1 | Cover Page | First impression — client name, project title, date, firm branding |
| 2 | Table of Contents | Navigation — auto-generated from heading styles |
| 3 | Executive Summary | The pitch — written *last*, distills scope + differentiators + key proof points |
| 4 | Client Context | Shows understanding — restate the client's situation, challenges, and goals |
| 5 | Objectives | Alignment — what success looks like, measurable where possible |
| 6 | Approach & Methodology | The "how" — phased approach, frameworks, tools, techniques |
| 7 | Work Plan & Timeline | The schedule — phases, milestones, dependencies, Gantt or table format |
| 8 | Deliverables | What the client receives — tangible outputs with descriptions |
| 9 | Team & Qualifications | Who delivers — key personnel, roles, relevant credentials |
| 10 | Relevant Experience | Proof — case studies, past performance, client references |
| 11 | Pricing & Investment | The ask — fee structure, payment terms, what's included/excluded |
| 12 | Risk Management | Confidence — identified risks, mitigation strategies, assumptions |
| 13 | Terms & Conditions | Legal — engagement terms, IP, confidentiality, liability |
| 14 | Appendices | Supporting detail — resumes, detailed methodologies, certifications |
| 15 | Next Steps | Call to action — what happens after acceptance, contact information |

**Key rule**: The Executive Summary is always written *last*, after all other sections are finalized. It synthesizes the final scope, differentiators, and strongest proof points.

For detailed guidance on each section, see [sections.md](references/sections.md).

## Workflow

### Step 1 — Document Plan

1. Select editing mode (Create / Revise / Merge / Condense)
2. Choose which sections from the skeleton are needed (full proposal vs. exec brief vs. capability statement)
3. Map content library items to sections:
   - Case studies → Relevant Experience (match by tags to client industry/service)
   - Team bios → Team & Qualifications (select `executive` or `technical` variant based on audience)
   - Methodologies → Approach & Methodology (match by `applicableServices`)
   - Boilerplate → Risk Management, Terms & Conditions
   - Pricing models → Pricing & Investment (from `company_context.json` → `pricing.publicModels`)
4. Identify gaps — content that needs to be written fresh vs. pulled from library
5. Note any client-specific formatting requirements (page limits, required sections, naming conventions)

### Step 2 — Section Drafting

Draft each section **in the deliverable canvas**, following the guidance in [sections.md](references/sections.md):

- **Pull from content library first** — reuse and adapt case studies, bios, and methodology descriptions before writing new content
- **Substantiate every claim** — each assertion needs a proof point (case study reference, metric with source, certification)
- **Maintain the unsourced ledger as you draft** — record each section's `basis` in an in-canvas ledger *when you write it* (not reconstructed at the end): `client_data` (every claim/bio traces to the overlay), `inferred` (extrapolated from real data), or `fabricated` (no client-data source). Any named person's bio/role with no `publicBio` source, or any claim with no proof point, is `fabricated` — which means you must revisit the empty-`people`/`credentials` guard (ask or omit). This ledger seeds `asset-feedback.unsourced_content` at close-out (Step 7).
- **Write for the evaluator** — lead with the answer, then provide supporting detail
- **Maintain consistent voice** — same tense, same level of formality, same terminology throughout
- **Skip the executive summary** — it gets written in Step 4
- **Apply brand expression (if present) — reference, never bind.** Read `expression` from `brand_context.json`. If present, use as prose guidance — not hard layout rules:
  - `expression.principles` — let these inform tone and emphasis (e.g., "measured authority" → lead with evidence, not assertion)
  - `expression.signatureElements` — weave into structure where natural (e.g., a brand that uses "indexed rules" may benefit from numbered evidence citations)
  - `expression.antiPatterns` — avoid these constructions in the prose and section framing
  - `identity.positioning` — use to sharpen the executive summary angle and differentiation framing
  - If `expression` is absent, fall back to the voice profile only (soft note; no hard failure — output-tier brands may legitimately omit it)
  - **Voice-cascade rule:** `expression` is additive to the L1 baseline + L2 profile bans, never a relaxation. Expression principles may sharpen tone but must not reintroduce a banned construction. Where a Brand Context API narrative is attached (`candidate.context`), treat it as input evidence for expression principles, not a voice source that overrides the cascade.
- **Emit the authored closing (if present).** Read `companies/{client_slug}/boilerplate.json`. If it carries `sign_off` and/or `contact_block`, use them instead of inventing a closing:
  - `sign_off` → the closing salutation (e.g. a cover-letter sign-off, or the line before the contact block in Next Steps). Select the locale + register variant — `formal_en`/`formal_nl` for first-contact or public-sector proposals, `default_en`/`default_nl` otherwise; match the proposal's language.
  - `contact_block` → emit verbatim in the **Next Steps** section (section 15) as the firm's contact details; select the variant matching the proposal's language.
  - These are locale/register-keyed maps, not bare strings — never emit the raw JSON or a key name; resolve to the chosen variant's value.
  - **Absence is not failure.** A client whose `boilerplate.json` lacks `sign_off`/`contact_block` (or has no `boilerplate.json`) simply omits the authored closing — fall back to a plain "Next steps" call-to-action and do **not** fabricate a signer, salutation, or contact details.

### Step 3 — Assembly

**Gate: do not start this step until the user has signed off on the canvas** (see "Deliverable canvas" Step 5 — pending feedback or placeholders block assembly).

Produce the document in the chosen output format. Pass the following context to `format-prepare-document`:

- **Brand**: `companies/{client_slug}/brand_context.json` (resolved expression + identity + colors/fonts/logo)
- **Logo**: `companies/{client_slug}/logos/` (path in `brand_context.logo`)
- **Drafted sections**: the content from Step 2
- **Tone and archetype**: from intake Phase 2/3
- **Brand expression**: include `expression` (if resolved from `brand_context.json`) and `deliverable_genre: "proposal"` in the envelope so the downstream renderer applies the same compact direction

`format-prepare-document` then routes to the terminal renderer:
- DOCX output → `format-docx`
- PPTX output → usually `format-pptx-hd`
- PDF output → usually `format-pdf-hd`

### Step 4 — Executive Summary

Write the executive summary last — in the canvas, as the final section before the sign-off gate — synthesizing:
- **The opportunity** — 1-2 sentences on the client's situation and need
- **The solution** — what you're proposing, at the highest level
- **Key differentiators** — why this firm, why this team, why this approach (2-3 bullets)
- **Proof points** — strongest evidence (metrics, case studies, credentials)
- **The investment** — total cost and timeline at a glance
- **Call to action** — next step to move forward

Target length: 1-2 pages. An executive should be able to read only this section and make an informed decision.

### Step 5 — Layout Validation

Before quality gates, verify visual presentation:
- Cover page renders correctly with branding
- Table of contents is generated and accurate
- Page breaks fall before major sections
- Tables don't split across pages awkwardly
- Headers and footers appear consistently
- No orphan headings (heading at bottom of page, content on next)
- Consistent spacing between sections

Convert DOCX to images (DOCX → PDF via LibreOffice → images via pdftoppm) to visually inspect output.

### Step 6 — Quality Gates

Run the quality checklist. See [quality-gates.md](references/quality-gates.md) for the full detailed checklists.

**Quick reference:**

| Gate | Check |
|------|-------|
| Content completeness | Every required section exists with substantive content; no TBD, placeholders, or lorem ipsum |
| Claim substantiation | Every claim has a proof source (case study ID, metric source, internal reference) |
| Section coherence | No contradictions between sections; pricing matches scope; timeline matches deliverables |
| Visual consistency | Cover page present, TOC generated, heading styles consistent, page numbers present |
| Formatting hygiene | All formatting via styles (no manual), no orphan headings, tables don't split badly |
| Cross-references | All "see Section X" references point to actual sections; all appendix references valid |

### Step 7 — Packaging

Produce final deliverables:
1. **Final document** — in the requested format via `format-prepare-document`
2. **PDF export** (if requested) — via the renderer selected on that handoff path
3. **Email summary** (if requested) — 10-bullet summary suitable for forwarding to the client as a cover email

After handoff, *mention* (never auto-activate) that the user can capture feedback on the proposal with `asset-feedback`, and file your own `source: agent` retrospective there if the run hit an instruction gap or tool-call failure worth fixing.

**Close-out grounding (file a truthful retrospective).** Before filing the `asset-feedback` retrospective, inspect the overlay you actually used — inspecting an artifact you already loaded is itself an `external_signal`, not a judgement call:

- If `company_context.people[]` was empty/absent **and** you nonetheless produced a Team & Qualifications section, record `{section: "Team & Qualifications", basis: inferred|fabricated}` in `unsourced_content`.
- If `credentials` was empty **and** you presented credentials, record that section in `unsourced_content` likewise.
- For every explicit ask you could not satisfy from client-data (e.g. "include real credentials" with none present), add an `unmet_asks` entry (`reason: no_data`, `resolution` = what you actually did: `stopped` / `asked_user` / `flagged_in_output` / `improvised`).
- Carry the in-canvas unsourced ledger (Step 6) straight into `unsourced_content`; a section you filled by inference or fabrication is the highest-value signal and is **always** reported.

Use `category: data-shortfall` when the deliverable improvised under a data gap. A run that correctly STOPped or asked still files the `unmet_asks` it hit — the honest retrospective is the point.

## Quality Gates — Quick Reference

These are the high-level checks. For detailed per-section checklists and common failure modes, see [quality-gates.md](references/quality-gates.md).

**Content completeness**
- Every section in the document plan exists and has substantive content
- No "TBD", "[placeholder]", "[insert here]", or lorem ipsum text
- Word/page targets met for each section

**Claim substantiation**
- Every capability claim has a supporting reference (case study, metric, certification)
- No vague claims without evidence ("we are industry leaders" → needs proof)
- Metrics include source and timeframe
- **Emit the unsourced ledger** — produce a structured in-canvas list of every claim, bio, or section with no client-data proof source, each tagged `basis: inferred | fabricated` plus the section it appears in. An empty ledger is the goal; a non-empty one must be surfaced to the user, never silently shipped. This ledger is the source for `asset-feedback.unsourced_content` at close-out (see Step 7 "Close-out grounding").

**Section coherence**
- Pricing aligns with the scope described in Approach & Methodology
- Timeline aligns with deliverables and milestones
- Team composition matches the approach (right skills for the proposed methods)
- No contradictions between sections

**Visual consistency**
- Cover page has correct client name, project title, date, branding
- Table of contents is present and accurate
- Heading styles are consistent (all H1s look the same, all H2s look the same)
- Page numbers present in footer; headers have firm/project name

**Formatting hygiene**
- All formatting uses styles (no manual bold/italic/font-size for headings)
- No orphan headings at page bottoms
- Tables don't split across pages in confusing ways
- Consistent paragraph spacing throughout

## Customization

### Client Branding

Brand data is resolved from `companies/{client_slug}/brand_context.json` (the downstream renderer applies the per-format settings below; the `presentation` spacing block stays in `charter.json`, which is not compiled):

- **`document`** section → DOCX margins, headers, footers, heading colors
- **`presentation`** section → PPTX slide margins, aspect ratio
- **`video`** section → Remotion resolution, fps

If no company data exists, accept brand parameters as manual inputs:
- **Primary color** — used for headings, cover page accents
- **Secondary color** — used for subheadings, table headers
- **Fonts** — heading font, body font
- **Logo** — file path for cover page placement

### Tone & Voice

Accept tone parameters and apply consistently:
- **Formality**: formal / conversational (default: formal)
- **Audience**: technical / executive / mixed (default: executive)
- **Stance**: assertive / consultative / neutral (default: consultative)
- **Default voice**: Professional, confident, specific. Avoid jargon without explanation. Lead with outcomes, support with methods.

### Evidence Rules

Define what counts as proof and how to cite it:
- **Case study reference**: `[CS-ID]` with client name (if permitted), industry, outcome metric
- **Metric citation**: Number + source + timeframe (e.g., "reduced cycle time by 35% — ABC Corp engagement, 2024")
- **Certification reference**: Certification name + issuing body + current status
- **Client name usage**: Check `namePublic` flag in case study — use name only if `true`, otherwise use industry descriptor

## Output Location

Proposals follow the standard workspace project structure:

```
workspace/<client>/
├── build/<deliverable>/    ← build scripts and intermediates
└── output/<deliverable>/   ← final proposal files (docx, pptx, pdf)
```

**Override**: If the prompt specifies a target output directory, pass it through to the output format skill.



## Output Format Production

This skill owns proposal content strategy. Document production is handled by the appropriate format skill:

| Output | Skill | What it provides |
|--------|-------|-----------------|
| DOCX | `docx` | Word document creation with docx-js, OOXML editing, redlining |
| PPTX | `pptx` | Branded presentation creation with html2pptx workflow |
| PDF | `pdf` | PDF creation, conversion, merging |
| XLSX | `xlsx` | Spreadsheet creation for pricing models |

Brand context to carry forward:
- Brand location: `companies/{client_slug}/brand_context.json`
- Apply heading color from `colors.primary`, body font from `typography.body`, logo from `logos/` (path in `brand_context.logo`)
- Include resolved `expression` (if present) and `deliverable_genre: "proposal"` for downstream render direction
