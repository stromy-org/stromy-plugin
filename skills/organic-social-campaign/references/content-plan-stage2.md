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
  the engagement's verified research library, listed on the row (source-mapped).
- **Concept idea** — a one-to-two-line creative direction (enough to brief from,
  not a caption).
- **Producer** — who makes the asset: in-house, creator, or production partner
  (§3).

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
