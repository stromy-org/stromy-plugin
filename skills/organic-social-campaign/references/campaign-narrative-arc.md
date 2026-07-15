<!-- since: 2026-07-15 -->

# Campaign Narrative Arc — sequencing belief change over a time-boxed window

**Campaign mode only.** An always-on **program** compounds: pillars, cadence,
community, repetition. A **campaign** converges — it has a deadline and a job:
move a specific audience from believing X to believing Y by the end of the
window. That job needs *sequence*, not just slots.

This reference is the method behind Phase 3 Step 2b. The output is a table the
user approves before any content planning begins.

## Why arcs, not grids

The default failure of a repositioning campaign is a **flat grid**: eight weeks
of on-pillar posts, each defensible, that never accumulate into an argument. The
audience sees eight disconnected assertions and updates nothing. A grid is
optimised for *coverage*; belief change needs *order*.

Order matters because the beliefs are dependent. You cannot land "here is the
evidence" on someone who has not first noticed they hold an assumption worth
testing — the evidence reads as noise against a settled prior. And you cannot ask
for a decision from someone who has not yet accepted the evidence. Each act
**earns the right** to the next one.

Three practical consequences:

1. **Week 1 and week 8 are different jobs.** If a post could run in any week
   without loss, the campaign has no arc — it has a content calendar.
2. **Repetition inside an act is a feature; repetition across acts is drift.**
   Hammer one belief shift per act from multiple angles, then move.
3. **The arc is falsifiable.** "What should the audience believe in week 4 that
   they did not in week 1?" is answerable. If it isn't, the arc is decoration.

## The frame: audience-as-hero, brand-as-guide

The evidence-backed B2B framing is **not** brand-as-hero. The audience is the
hero with a problem; the brand is the guide with a plan. In a repositioning
campaign the shape is:

| Story role | Who | In practice |
|---|---|---|
| Hero | the audience (procurement lead, member company, consumer) | holds the assumption the campaign tests |
| Problem | the assumption itself | usually *inherited*, not chosen — this is why blame fails |
| Guide | the client (trade body, brand) | has evidence and standing, not superiority |
| Plan | the acts | what the hero does with the new belief |
| Stakes | what the hero loses by not updating | must be the *hero's* stakes, not the client's |

**The most common arc failure is casting the brand as hero** — "we commissioned
research, we are leading the conversation." The audience has no role in that
story, so there is nothing for them to do. Recast: *they* hold a belief formed by
reasonable-but-outdated inputs; the campaign gives them a better input.

**Corollary — never make the hero the villain.** If the arc's act 1 tells the
audience they were wrong/careless, it triggers defence, not curiosity. The
assumption was *reasonable given what they were told*. Disrupt the assumption,
never the person.

## Acts

Define **2–4 acts** across the window. Each act declares:

| Field | What it states |
|---|---|
| **Name** | short, internal — the act's job ("Disrupt the assumption") |
| **Belief shift** | explicit **from → to** ("paper = deforestation" → "paper = a managed renewable cycle") |
| **Pillar emphasis** | which editorial pillar(s) carry this act |
| **Hero asset** | the flagship the act's derivatives hang off (see [content-formats.md](content-formats.md) § Hero → derivative production (COPE)) |
| **Differentiation note** | one line: *what this audience already heard vs what is new this time* (grounded in the Phase 2 prior-wave inventory — see below) |

### 3-act default

The default for a repositioning campaign:

1. **Disrupt the assumption** — surface the belief and make it visible as a
   *belief* rather than a fact. Goal: curiosity, not agreement. Ends when the
   audience concedes the question is open.
2. **Evidence and proof** — land the substantive case. This is the act that
   needs documents/carousels and third-party credibility. Goal: acceptance.
3. **Invitation and choice** — convert acceptance into a decision or an action
   the hero takes. Goal: a behaviour, not a nod.

### Variants

| Window | Acts | Notes |
|---|---|---|
| < 4 weeks | **2 acts** (disrupt → invite) | evidence folds into act 1; the peak moment is optional |
| 6–8 weeks | **3 acts** (the default) | ~2–3 weeks per act |
| 10+ weeks | **4 acts** — split evidence into *category proof* then *client/member proof* | only when there is genuinely enough distinct evidence; a padded act reads as repetition |

**Do not add acts to fill time.** A 12-week campaign with three strong acts beats
one with four, where the fourth is act 3 restated.

## Beats

Break each act into **weekly beats** — one theme per week. A beat is expressed
**once per track**, not once in total (see cross-track echo). The beat table is
the artifact the user approves:

| Week | Act | Beat | Belief shift | B2B expression | B2C expression | Hero / derivative |
|---|---|---|---|---|---|---|
| 1 | 1 | The number everyone quotes | "the stat is settled" → "the stat is 20 years old" | LinkedIn document: provenance of the figure | Reel: "where did this number come from?" | Hero A → doc + reel |
| 2 | 1 | Who actually plants the trees | "paper destroys forests" → "demand sustains them" | Carousel: the managed-forest cycle | Carousel: 4 slides, no jargon | Hero A → 2 carousels |

`Week`, `Act`, and `Beat` map **directly** onto the Phase 5 calendar's `act`/`beat`
columns and flow through Phase 7 onto every post object (see
[editorial-calendar-template.md](editorial-calendar-template.md) and
[post-object-schema.md](post-object-schema.md)).

**One beat per week.** Two beats in a week means neither lands — the audience
sees fragments, and the arc's causality breaks.

## Cross-track echo (multi-audience campaigns)

A two-track campaign (e.g. B2B LinkedIn + B2C Instagram) must read as **one
story told twice**, not two campaigns sharing a hashtag.

The rule: **same beat, per-audience dialect, never cross-posted verbatim.**

- **Same beat** — both tracks express the *same* belief shift in the same week.
  This is what makes the campaign feel coherent to anyone who sees both, and it
  is what lets a peak moment work.
- **Per-audience dialect** — the *expression* differs completely: evidence
  register and professional stakes on the B2B track; concrete, human, visual on
  the B2C track. The B2C track is not a simplified B2B post; it answers a
  different question the same fact settles.
- **Never verbatim.** Beyond reading as lazy, recycled content is **algorithmically
  down-ranked** — Instagram suppresses visibly reposted/watermarked assets (see
  [platforms/meta.md](platforms/meta.md)). Cross-posting the same file is a reach
  penalty, not a shortcut.

**Single-track campaigns:** the echo rules collapse to one dialect. The arc still
applies unchanged — acts, beats, and the peak moment are not multi-track
features.

**Asymmetric tracks are normal.** A B2B track may carry all three acts while a
B2C track carries only acts 1 and 3 (awareness and invitation), skipping the
evidence act because the audience will not read a provenance document. Declare
the asymmetry in the table rather than faking coverage.

## Differentiation vs prior waves

A repositioning campaign rarely lands on virgin ground. The client has usually
run the *same evidence* before — and adjacent channels they borrow or partner
with may be running it **right now**. Repeating a wave the audience already saw
is not just weak; the client will recognise it as a copy-paste and lose
confidence in the whole plan.

### Inventory method (feeds from Phase 2)

Before writing the arc, inventory:

1. **The client's own channels** — what did they publish on this theme, when, in
   what format, and how did it perform?
2. **Adjacent/borrowed channels** — a sector platform, partner, or member body
   whose account the campaign will post on (see the `borrowed` account contract
   in [social-data-schema.md](social-data-schema.md)). What has *it* run?
3. **Live influencer/partner work** — anything currently in-market on the same
   evidence, including work the client did not commission.

For each: **what did that wave assert, to whom, and what did it leave unsaid?**

### The "different angle, not copy-paste" test

For every act, answer in one line: *what has this audience already heard, and
what is new this time?* If the honest answer is "the same thing, better
designed", the act is not differentiated — change the **angle**, not the
polish. Legitimate angles on identical evidence:

| Angle | Shift |
|---|---|
| **New frame** | same fact, different question it answers ("is paper bad?" → "what replaces it?") |
| **New protagonist** | same fact, told by a member company / a consumer rather than the association |
| **New stakes** | same fact, different consequence ("environmental" → "supply-chain cost") |
| **New surface** | same fact, a format/channel that reaches people the last wave missed |

### Continuity vs competition

An adjacent live campaign is a judgement call, not automatically a conflict:

- **Continuity** (usually right) — the new wave *builds on* the live one:
  reference it, pick up where it stopped, let the audience feel a developing
  story. Best when the live wave is credible and on-message.
- **Competition** (rare) — the live wave is off-message or exhausted, so the new
  campaign deliberately re-frames. This needs an explicit decision, because it
  can read as the client contradicting itself.

State which you chose, and why, in the act's differentiation note.

## Peak moment

Place **one peak moment** in the arc — a concentrated multi-channel burst where
every track, advocate, and (if scoped) influencer lands on the same beat in the
same short window. Everything before it builds; everything after it converts.

Placement: usually the **start of the final act** — late enough that the evidence
has landed, early enough that there is runway to convert attention. Never week 1
(nothing to peak on) and never the last week (no time to use it).

**The Love Paper evidence.** A concentrated participation moment is how a
membership organisation turns its member base into distribution: nearly **400
organisations participated globally**, and — a **separate, non-overlapping**
figure — **500,000 people were reached in North America**. Keep the two
geographies distinct; they are not the same measurement. Sources:
https://lovepaper.org/love-paper-week/ ,
https://revistas.alborum.com/pdfs/lp_latam/lplatam77web.pdf , and
https://www.linkedin.com/posts/twosidesna_lovepaperweek-twosidesna-papersustainability-activity-7444760540125667328-OrkB
(all accessed 2026-07-14; directional, revisit annually).

What the mechanics teach:

- **Participation beats broadcast.** The moment worked because organisations
  *did something*, not because a page posted more.
- **Ship a kit, not a request.** Ready-to-share assets + copy variants + a date.
  See [employee-advocacy.md](employee-advocacy.md) § Variant: member &
  association advocacy.
- **A UGC/competition mechanic** gives participants a reason to post in their own
  voice — which is what buys reach the page cannot.
- **Amplification-ready.** If any track is `paid-boost` or `influencer-seeded`,
  the peak is where that budget concentrates.

**Never-fabricate applies.** Named member organisations, advocates, and
influencers in a peak plan must be real people/orgs from client data — or the
moment stays org-level and unaddressed. Do not invent participants.

## The reactive lane lives *inside* the arc

Phase 5 reserves ~15–25% of capacity for reactive/newsjacking content. In
campaign mode that lane is **not** arc-exempt: a reactive post still serves the
**current act's** belief shift, or it is off-story and dilutes the campaign. Plan
the slot and the fast approval path; let the act constrain the angle.

## How the arc feeds the rest of the workflow

| Consumer | What it takes |
|---|---|
| **Phase 4** (hero → derivative) | each act's **hero asset**; derivatives are planned per act |
| **Phase 5** (calendar) | `Week`/`Act`/`Beat` columns straight from the beat table; the reactive lane bounded by the current act |
| **Phase 7** (freeze) | `act`/`beat` pass through the builder onto every post object — narrative, not identity, so they never change `post_id` |
| **Phase 6** (measurement) | acts give a per-act read: did the belief shift move? |

## Worked example — sector-advocacy campaign (anonymised)

**Context.** A trade association representing a manufacturing sector. Its
category is widely assumed to be environmentally harmful, on evidence the
association believes is two decades stale. It commissioned fresh research.
8 weeks, two tracks.

- **Track A (B2B)** — LinkedIn, association-owned page + member/exec
  amplification, `organic`.
- **Track B (B2C)** — Instagram, **borrowed** sector-platform account,
  `paid-boost` + `influencer-seeded` (organic reach on a cold borrowed account is
  realistically ~zero; boost carries it).

**Prior-wave inventory (Phase 2).** The association posted the same research ~4
months ago to modest reach; the borrowed platform ran an explainer article and
currently has a live influencer campaign. → Differentiation is mandatory:
*continuity* with the live influencer work, *new frame* vs the association's own
earlier wave.

| Act | Weeks | Belief shift (from → to) | Pillar | Hero asset | Differentiation note |
|---|---|---|---|---|---|
| 1 — Disrupt the assumption | 1–3 | "the harm figure is settled fact" → "the figure is 20 years old" | Category truth | Research explainer (document) | Last wave *asserted* the new number; this wave interrogates the **old** one's provenance — new frame, same evidence |
| 2 — Evidence and proof | 4–6 | "the category harms the resource" → "demand sustains the managed cycle" | Evidence | Animated data story (MP4) | Last wave published a PDF nobody opened; same data, now a 40s visual — new surface |
| 3 — Invitation and choice | 7–8 | "nothing I do matters" → "my next specification decision matters" | Proof / action | Member factsheet + peak kit | Continuity with the live influencer campaign: picks up its consumer thread and gives it a professional ask |

**Beats (excerpt).**

| Week | Act | Beat | B2B expression | B2C expression |
|---|---|---|---|---|
| 1 | 1 | The number everyone quotes | Document: where the figure came from, and when | Reel: "who told you this?" — 30s, hook in 3 |
| 2 | 1 | Reasonable, and out of date | Text POV from a named exec: why we believed it too | Carousel: then vs now, 4 slides |
| 4 | 2 | Demand plants forests | Carousel: the managed cycle, sourced | Reel: the cycle in 20 seconds |
| 7 | 3 | **PEAK** — participation week | Member kit ships; execs + members post the same day | Influencer collabs + boosted UGC mechanic |

**Peak (week 7).** Members receive the kit (copy variants + co-brandable assets +
the date); influencers on Track B land in the same window; boost concentrates
here. Act 1 does not ask anyone to do anything — it has not earned it yet.

**Why this reads as one story:** week 4's B2B carousel and B2C reel carry the
*same* belief shift in *different* dialects, in the same week — the cross-track
echo. Neither is a repost of the other.
