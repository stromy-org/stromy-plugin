<!-- since: 2026-07-24 -->

# Content Plan — Stage-2 production process

The second client-facing stage of the campaign deliverable ladder, sibling of
[strategy-deck-stage1.md](strategy-deck-stage1.md):

> **Stage 1 Strategy** (document + deck) → **Stage 2 Content plan** (the calendar
> werkdocument — this file) → **Stage 3 Roll-out** (week-by-week publication-ready
> posts + support).

Maps onto the skill workflow as: Stage 2 = Phases 4–5 plus the **structural half**
of Phase 7; Stage 3 = the creative half of Phase 7, plus Phase 8 and the weekly
loop. This file exists because the boundary between the two stages is the single
most commercially and operationally load-bearing line in a client engagement, and
a run that blurs it silently gives away the next phase's deliverable for free.

## 1 · The stage boundary: plan the post, don't write it

**The content plan contains everything needed to produce each post — except the
post itself.** Per planned slot it fixes:

- **Schedule** — date, week, platform/track, act/beat (campaign mode).
- **Format** — the concrete content format: reel / single image / carousel /
  video / text post / story.
- **Key-message allocation** — which of the week's pillar key messages this post
  carries. Work per week: take the key messages of that week's pillar/beat and
  **divide them across the week's posts**, so every message lands somewhere and
  no post carries all of them.
- **Evidence** — the specific figures/data points the post will cite, drawn from
  the engagement's research library, listed on the row **with its source and a
  working link, not an internal proof-point ID**. Evidence crossing into this
  stage gets a boundary re-verification first: [evidence-library-integrity.md](evidence-library-integrity.md) §6–7.
- **Concept idea** — a one-to-two-line creative direction (enough to brief from,
  not a caption), **ending in an explicit takeaway**: one line naming what the
  viewer should think or remember afterwards, tied back to the campaign
  message. Mood and craft posts need this most — "beautiful images of the
  process" without a stated takeaway is the single most common review finding
  (live client review, 2026-08): the post reads as random until its last card
  or closing line makes the connection the concept never wrote down.
- **Producer** — who makes the asset: in-house, creator, or production partner
  (§3). Every row's named producer must be a party that **exists and is in
  scope** — checked mechanically at §7, not assumed.

**Deliberately absent: publication-ready copy.** No captions, hooks, CTA copy, or
hashtags. Two reasons, and both should survive into any engagement's phase
design:

1. **Commercial.** The roll-out stage must remain a separately chargeable phase
   with **tangible outputs** (the finished posts), not "continuous guidance."
   Copy delivered inside the content plan hollows out the next phase's fee basis.
2. **Operational.** Calendar approval gates generation; posts are then produced
   **week-by-week** against live performance and feedback, so the plan can flex
   (formats swapped, messages re-weighted) without rewriting finished copy.

State the boundary in the deliverable itself (one line in the werkdocument's
intro): what this plan fixes, and that publication-ready development happens in
the roll-out phase per approved week.

## 2 · Calendar shape

- **One central working document** covering all tracks is the default (a track
  per tab/section); split into per-track documents only if the client's
  operating reality demands it, and say so. One document keeps the cross-track
  echo (same beat, per-audience dialect) visible.
- Tabular, spreadsheet-grade (XLSX via `format-xlsx`, or the client's
  collaborative equivalent) — it is a *working* document the client's own
  publisher/marketer will live in, not a slide.
- Columns: the required set in
  [editorial-calendar-template.md](editorial-calendar-template.md), which
  includes **Key messages**, **Data/evidence**, and **Producer** for exactly
  this stage.
- The strategy deck's per-track content formats (`tracks[].contentFormats[]`)
  seed the Format column — the plan instantiates what the strategy promised,
  never invents a new format mix silently.

## 3 · The three production lanes

Every row names its producer up front — discovering at roll-out that nobody
owns a video is the classic slip. The lanes carry different deliverables from
us and different lead-times:

| Lane | Our deliverable | Who makes the final content | Lead-time reality |
|---|---|---|---|
| **In-house (text/visual posts)** | Publication-ready copy (+ optional visuals) in Stage 3, week-by-week | Us | Weekly cycle |
| **Creator (influencer-seeded)** | **Briefing + concept ideas only** (concept ideas may sit in the content plan); advice-only boundary per [influencer-advisory.md](influencer-advisory.md) | The creator — that is the point of the lane (their voice, their telling) | Client-side sourcing/negotiation/contracting must **complete during the content-plan window**, before roll-out |
| **Production partner (studio video)** | **Talking points + a short briefing** by default; a full word-for-word script **only on explicit client ask** | The client's studio/production partner | Production must fit inside the pre-launch window; clarify the client↔partner working mode at content-plan sign-off, not during roll-out |

The briefing-tier default (talking points first, escalate only on request) is
deliberate: start with the lightest artifact that lets the partner work, and
give more only when they ask — over-specifying a partner's craft is the same
failure as scripting a creator.

**Creator-lane placement decisions belong in Stage 2, "the sooner the better."**
Whether creators are used at all is the client's call (their budget, their
contracts); the plan's job is to make the decision unavoidable now — because the
contracting lead-time sits on *their* critical path, not ours.

**Cross-posting + boost pattern (creator lane).** Default recommendation: the
creator's content publishes on **both** the creator's channel and the campaign's
own track account, and paid boost runs **from the campaign account** — so spend
and analytics stay on a surface the client controls. For message-led campaigns
(no product to show), prefer **short video/reel** over static or stories: a
message needs a telling, and stories are too ephemeral/short for one.

## 4 · Production-window feasibility gate (before sign-off)

Count **backward from go-live** before the plan is signed off:

1. Client review rounds on the content plan (there will be back-and-forth to
   full alignment — budget ≥ a week).
2. Creator sourcing → negotiation → contracting (client-side; fast when lucky,
   weeks when not).
3. Production-partner filming/production for every non-creator video row.
4. Any concurrent client campaign competing for the same people/attention.

If the chain does not fit, **advise moving go-live** (a month is the natural
unit) rather than compressing — framed as quality protection: "you want a good
campaign, not a rushed one." This is doubly true when steps 2–3 depend on third
parties the client, not we, must mobilize. A slipped go-live recommendation made
*at content-plan sign-off* is advice; the same recommendation mid-roll-out is an
apology.

### 4b · Publishing capacity — the gate's twin, and the one that gets skipped

The window gate asks whether the content can be *made* in time. It says nothing
about whether the client can **post** it. Cadence is capped by two client-side
facts, and both have to be asked for — neither is derivable from reach maths:

- **The publisher's own throughput** on that account. Whoever actually posts has
  a schedule of their own; a campaign is one item on it, not the whole channel.
- **The audience's tolerance on that channel.** A frequency the audience reads
  as repetitive is a cost, not a reach gain, and it is the client — who has
  watched their own audience for years — who knows where the line is.

Ask both **at intake**, alongside the window, and treat the answer as a ceiling
the calendar is designed under. A cadence discovered to be unpublishable *after*
the calendar exists does not shrink gracefully: it re-cuts pillar coverage, the
per-week key-message allocation and the arc's beat spacing all at once. In the
originating engagement a three-a-week track met a one-a-week ceiling at review
and cost a full replan of calendar, pillars and both language workbooks.

Asymmetric ceilings across tracks are normal and fine — declare them
(one track weekly, another three times a week) rather than averaging to a
cadence neither channel wants.

## 5 · Structural freeze now, creative fill per week

Run the Phase 7 builder at content-plan stage in **structural mode**: emit
`calendar.json`, run `build_posts.py`, persist `posts.json` with the creative
fields (`hook`, `body`, `thread_parts`, `hashtags`, `cta`) **left empty**. The
builder's structure/copy seam maps exactly onto the stage boundary — structure
is a Stage-2 artifact, copy is Stage-3 work.

In Stage 3, per weekly edition: fill that week's creative fields through the
voice cascade (from the row's key-message allocation + cited figures — the
calendar is the brief), run `validate_posts.py` to exit 0 for the edition, and
hold the edition-review gate before the next week starts. Never fill all weeks'
copy up front: that reintroduces the boundary violation with extra steps.

## 6 · Matched-spend amplification experiment (optional, propose when both lanes run)

When a campaign runs **both** paid boost and creator collaboration, propose
structuring comparable spend as an explicit experiment: the same budget unit
(e.g. €2k vs €2k) into boosting organic posts vs a creator collab, same window,
per-lane KPIs (reach, engagement, follows, cost-per-result). The campaign then
doubles as a **benchmark instrument** — the client (and the agency) gain numbers
to size future campaigns with, which is itself a sellable outcome. Frame as
"and, not or": the experiment needs both lanes live. Record the design in the
Phase 6 measurement spec; the lanes' dark-funnel caveats
([measurement-benchmarks.md](measurement-benchmarks.md)) apply per lane.

## 7 · Production-route completeness (mechanical, before freeze)

§3 says every row names its producer. That is necessary and not sufficient: a
named producer can be a party that does not exist for this engagement, or one
whose lane the contract excludes. Run this as a **count, not an impression**:

1. **Group the rows by format and producer.** Print the matrix. A plan that
   looks fine row-by-row is where the imbalance hides.
2. **For each row, ask whether the named producer can actually make that
   format.** The in-house lane is *text and visual* posts (§3). A row that says
   in-house and *video* is already a contradiction — and it is the exact shape
   the failure takes, because the format was chosen for the story and the
   producer column was filled in afterwards by default.
3. **Reconcile against scope.** If video production sits outside the engagement's
   scope, then every video row belongs to the creator lane, the production
   partner, or a format that is not video. There is no fourth option, and
   "we'll figure it out" resolves to the agency absorbing out-of-scope work.
4. **Reconcile against capacity, not just scope.** A client with an in-house
   designer can carry animated infographics; one without cannot. Ask before
   assuming either way.

**Conversion is the normal remedy, not a compromise.** A video row with no
producer has three honest resolutions:

| Resolution | When it fits |
|---|---|
| **Route to a lane that exists** — creator or production partner | The story genuinely needs a filmed telling, and there is budget/time |
| **Convert to an animated format** — a motion graphic delivered as a video file, built from the same design system as the static assets | The point is a message, a number, or a comparison. No camera, no location, no crew, and it still reads as video in-feed |
| **Convert to a still format** — carousel or single image | The idea leaned on footage a sequence carries just as well |

In a message-led campaign — no product to show — the animated route covers more
rows than teams expect, and it is the one that keeps a video-shaped feed
achievable inside an agency's actual scope.

**The check passes when zero rows name a producer who cannot make that row.**
State the resulting format mix in the deliverable so the client sees what they
are agreeing to.

### The shoot-day upside, marked as an option

When the plan already sends **two or more** rows to a production partner, a
filming day is happening regardless — crew, location, and a day are already
committed. At that point the marginal cost of filming more on the same day is
low, while other rows may be sitting in a converted format precisely *because*
there was no filming capacity.

Surface this as a marked **option**, never a dependency: a column flagging which
rows would be upgraded if the shoot happens, plus a short concept for what one
day yields (a longer hero piece, cut-downs for the flagged rows, stills for the
carousels, and reserve footage for the roll-out stage). The calendar must stand
completely without the shoot; the option only says what improves if it lands.
This is a high-value, low-cost proposal to put in front of a client and it is
invisible unless someone counts the partner rows.

## 8 · Conformance to the agreed scope document (line by line)

The engagement has a signed scope document. Before the plan is presented, walk
its component-2 bullets **one at a time** against the deliverable and record a
verdict per bullet. Not a general impression — a list.

This catches the omission that a good-looking plan hides: in the originating
engagement the scope named "captions, visual directions and calls-to-action". The
call had (correctly, §1) moved *captions* to the roll-out stage — and **visual
directions and CTAs quietly went with them**, unmentioned by anyone, absent from
the deliverable. One bullet, three sub-items, two silently dropped.

Also check the format list. Scope naming "reels, carousels **and stories**" and a
calendar containing no stories is a gap that needs a decision — add them as a
rhythm or drop them deliberately — not an oversight discovered at roll-out.

Where the plan intentionally departs from scope, say so in the deliverable with
the reason. An agreed departure is fine; a silent one is a dispute waiting.

## 9 · Column discipline — what earns a column

A working document's credibility comes from every column carrying information.
Two anti-patterns, both from real builds:

**A column with one value per group is noise.** A Status column reading `idea`
for every row on one track and `planned` for every row on the other tells the
reader nothing except that it was filled in. Either populate it with real state
or drop it. The same applies to approval-tier columns copied from a governance
model the client has not actually adopted.

**Invented precision is worse than no precision.** A per-post boost trigger like
"boost when engagement exceeds 2x the track median within 24 hours" reads as
rigour and is fabrication: nobody has that baseline before a campaign starts on a
channel with no history. Mark **boost candidates** — the posts that carry the
story — and state the real rule plainly: *we boost what works.* Precision that
cannot be sourced is the amplification-plan twin of an unsourced statistic.

Keep a column when it changes what someone does. Drop it when it does not.

## 10 · Blocked, never fabricated

Rows waiting on client input — a named case study, a creator not yet contracted,
a decision above the day-to-day contact — stay in the calendar **visibly
blocked**, with what is missing and who owns it. They are not quietly filled with
a plausible substitute, and they are not deleted to make the plan look complete.

A blocked row is doing useful work: it makes the dependency legible at review,
which is exactly when the client can still resolve it. The same row silently
invented becomes a fabricated case study in a client-facing artifact.

Use one blocker column, populated only where something genuinely blocks. Blank
means nothing is in the way — which is only true if the §7 check passed.

## 11 · Multi-language plans are generated, never hand-maintained

When the engagement runs in more than one language, **derive** the second version
from the first at build time. A hand-maintained twin drifts: fields get
translated on the first pass and forgotten on the second, and the reader who
needs that language is the one least able to notice.

Two properties make it reliable, and both are mechanical:

- The generator **reports every string it has no translation for**, and that
  count is meant to read zero. Silent fallback to the source language is the
  exact failure it exists to prevent.
- Judgement calls — a quotation, a study title, a legal term, a proper noun —
  are recorded per unit, not re-decided each run, so output is reproducible.

Never overwrite a shared-space copy without checking whether someone edited it
there; a target that diverged is reported, not regenerated over.

## 12 · Revision rounds that change the campaign, not the document

<!-- since: 2026-07-30 -->

Most feedback rounds refine wording. Occasionally one changes a campaign
parameter — the dates, the cadence, the channel mix — and then every artifact
downstream is wrong in ways no reviewer will read for. Four things go wrong
quietly.

**A cadence cut is a recount, not a delete.** "B2B goes to one post a week" over
six weeks means 18 posts become 6. The other 12 are finished, sourced content, and
which 6 survive is an editorial call the client may want to revisit. Move them to a
named reserve and surface it as its own tab — a silent deletion reads as a plan that
was always this size, and destroys the cheapest source of replacements.

**A date shift must preserve the weekday rhythm.** A calendar with a deliberate
Mon/Wed/Fri cadence, shifted by the literal number of days to the new start date,
lands on Sun/Tue/Thu — no error, no warning, just a plan that quietly publishes on
weekends. **Shift by a multiple of 7** and adjust the start to match, rather than
shifting to an exact date and losing the pattern.

**A date shift invalidates every event tie-in.** Posts anchored to a conference,
a sector week or a seasonal moment are now anchored to nothing. Re-anchor them
explicitly and say what changed; leaving the copy in place means the deliverable
asserts a connection that no longer exists. Whether to chase the event again is a
*start-date* question, not a content one — surface it that way.

**Renaming rows breaks anything keyed on their identity.** Re-sequencing posts
after a cadence change and renaming them to their new slot (`b2b-w5-p1`) collides
with names already held by displaced posts. Anything keyed on the id — a
translation map above all — then attaches the wrong text to the wrong row, with no
error. Give every row a **stable id** written once at creation, keep the
sequence-based name as a display label only, and assert the stable ids are unique.

## 13 · When the reviewer also edits the plan directly

The content plan is generated *and* co-edited, so a rebuild silently reverts
every edit it did not author. That discipline — comments vs direct edits, the
mechanical diff and its sanity check, folding into the build source, intent vs
web-editor artifact, label changes as scope instructions, instruction
provenance, and what the closing ledger must record — is defined once for both
this deliverable and the strategy deck in
**[co-produced-deliverables.md](co-produced-deliverables.md)**. The workspace
mechanics it defers to (fetch-latest, version history, locks, publish in place)
belong to the org's `workspace-cowork` protocol.

Plan-specific consequence: a fold-in that changes a row's **cadence, week or
producer** is a campaign change, not a copy change — run it through §12 before
rebuilding, or the calendar and the campaign manifest drift apart.
