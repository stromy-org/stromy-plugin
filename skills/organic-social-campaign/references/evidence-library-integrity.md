<!-- since: 2026-07-28 -->

# Evidence library integrity — verification state across stages

The [Evidence Discipline](../SKILL.md) gates govern a **claim in a deliverable**.
This file governs the **library those claims are drawn from**, because a
multi-stage engagement reuses evidence and reuse is where verification silently
lapses.

The originating failure: a six-week campaign's strategy stage built an evidence
library, the content-plan stage cited it by ID, and a verification round at
content-plan time found **six figures that could not be traced to any findable
source at all** — including two that had reached a client-facing deck. Every
Evidence Discipline gate had nominally been satisfied. None of them caught it,
for reasons worth naming precisely.

## 1 · Why the per-claim gates were not enough

| What the gate checks | What slipped past it |
|---|---|
| "Every stated number carries a named, dated source" | The source was named, real and findable — **the number simply was not in it**. A named source is not a verified source. |
| Close-out verification runs "before the deliverable is marked ready" | The figures entered the library at *strategy* stage and were inherited into the content plan by ID. Nothing re-ran at the boundary; the second deliverable trusted the first. |
| Citations resolve to a real publication | The content plan cited `[digital-78-end-user-devices]` — an internal pointer that **looks like a citation** to a reader and a reviewer, and resolves for neither. |
| Source tiering (peer-reviewed → journalistic) | Several bad figures came from **the client's own brochures**, a tier the ladder does not name and the one an engagement trusts most uncritically. |

The structural lesson: **an evidence library is a persistent asset that crosses
stage boundaries, so verification must be a property of the entry, not an event
in a deliverable's close-out.**

## 2 · Verification state lives on the entry

Every library entry carries its own verification state. Downstream stages
inherit **state**, never trust.

```json
{
  "id": "oko-co2-5x",
  "claim": "A paper leaflet emits up to 5x less CO2 than the digital alternative",
  "stat": "642 kg vs 3,360 kg CO2 per million impressions",
  "source": "Öko-Institut e.V., 'Vergleichende Bewertung…' (Köhler & Gröger)",
  "sourceUrl": "https://www.oeko.de/fileadmin/oekodoc/2025-PCF_Print_vs_Digital_Werbung.pdf",
  "publishedDate": "2025-11-05",
  "commissionedBy": "bvdm, Austropapier, dpsuisse, Jorcon b.v.",
  "independence": "industry-funded, ISO 14071 critical review by a named reviewer",
  "geography": "DE/AT/CH/NL",
  "verification": "VERIFIED 2026-07-27 — Tabelle 4-7 p.48, read from the primary PDF",
  "doNotUse": "Always name the commissioning party. …"
}
```

Six fields are load-bearing and none is optional for an externally-usable figure:

- **`sourceUrl`** — a working link. Without it nobody, including the next agent,
  can check the claim. A source name alone is a claim about a claim.
- **`publishedDate`** — a figure's scope is bounded by its date.
- **`commissionedBy`** — who paid for it. Disclosed every time it is used.
- **`independence`** — the honest tier, including "industry-funded but externally
  reviewed" where that is the truth.
- **`geography`** — the population it measured. A German figure used for a Dutch
  audience is labelled or dropped.
- **`verification`** — verdict, date, and **where in the source it was found**
  (page, table, verbatim line). "Checked" is not a verification record.

An entry missing `verification` is **unverified**, regardless of how confident
its prose sounds. It may inform internal thinking; it may not reach a
client-facing artifact.

## 3 · The verification ladder

Each rung is a distinct check, and each has failed in practice at exactly the
rung above the one people stop at:

1. **The source exists.** A real publication, not a plausible-sounding title.
2. **The source is findable.** A working URL a reviewer can open today.
3. **The source contains the number.** Open it and find the figure. This is the
   rung most often skipped, and it is where four of the six failures sat.
4. **The number means what we say it means.** Scope check — see §4.
5. **The number is about the population we imply.** Population check — see §4.

Stop below rung 3 and you have verified a bibliography, not a fact.

## 4 · Two failure classes the per-claim gates do not name

**Scope-widening.** A figure is real, correctly cited, and quietly generalised
past what it measured. A study found 78% of a *banner ad's* emissions come from
the end-user device; the same study puts a PDF brochure at 9%. Written as "78%
of online advertising", the citation still resolves and the claim is now false.
*Rule: the claim sentence must carry the scope the source measured, not the
scope we wish it measured. When the scope makes the line clumsy, the line
changes — not the scope.*

**Population conflation.** Two true numbers about **different populations**
welded into one sentence. "Over 600 companies and more than 20,000 people" — the
600 was the trade association's *membership*, the 20,000 was the *whole sector*
(~3,190 companies). Both numbers true, the sentence false, and every citation
check passes because each half resolves. *Rule: one population per sentence,
named. If two populations are genuinely needed, two sentences with two sources.*

Both classes are invisible to citation resolution, which is why they need their
own named check rather than trust in the existing gate.

## 5 · Client-supplied collateral is a source tier — the most dangerous one

Add to the tier ladder, **below journalistic**:

> **Client collateral** — the client's own brochures, one-pagers, decks and
> website copy.

It ranks lowest for a reason that has nothing to do with the client's honesty:
collateral is *already* a secondary rendering, produced under marketing
pressure, often uncited, and sometimes internally contradictory. In the
originating engagement the client's own materials carried the same comparison
framed two different ways, attached a distributor's advertorial figure to a
research institute, and welded an unsourced equivalence onto a regulator's
statistic.

**Treat a figure arriving via client collateral as a lead, not a source.** Trace
it to the primary publication before it goes anywhere external. When the trace
fails, say so to the client — a trade body publishing an unsourceable number
carries more risk than the missing number costs, and clients generally want to
know.

The same applies to figures arriving through a **briefing chain** with no
attribution. If nobody can say where a number came from, it did not come from
anywhere.

## 6 · Stage-boundary re-verification

When evidence crosses a stage boundary (strategy → content plan → roll-out),
run a **boundary check** on the entries the next stage will actually use:

1. List the entries the downstream deliverable cites.
2. For each, read its `verification` field. Missing, older than the engagement's
   staleness window, or marked provisional → re-verify now.
3. Re-verified → update the field. Fails → **retire the entry** and record why.

Retirement is a first-class outcome, not a failure of the run. Keep retired
entries with their reason:

```json
{"id": "folder-winkelbezoek-38",
 "retired": "NOT FOUND 2026-07-27 — neither '38% visits a shop' nor '54% would
 miss the folder' appears in the primary study or any secondary source.
 Independent research gives a different, lower figure. Replaced by …"}
```

A retired entry with its reason stops the figure returning next quarter through
someone's memory. A silently deleted entry does not.

## 7 · An internal ID is not a citation

Citing `[proof-point-id]` in a client-facing artifact is a pointer, not a
citation: the reader cannot follow it and the reviewer cannot check it.

**Any artifact leaving the team resolves IDs to source + date + working link at
build time.** Where the artifact is generated (a rendered calendar, a document),
make that resolution a **build-time gate**:

- Resolve every referenced ID against the library.
- An ID that does not resolve, or resolves to an entry with no `sourceUrl`,
  **fails the build** and names the offending row.
- Print the count of unlinked entries on every build. It is meant to read zero.

This is the mechanical twin of cite-or-hedge: the discipline is not "remember to
cite", it is "the artifact cannot be produced without a resolvable citation".

## 8 · Publish what argues against you — as a decision, not a reflex

Counter-argument discovery is already a gate. Two additions from practice:

- **Look for the counter-evidence inside your own strongest source.** The
  academic paper carrying the campaign's best retail finding had an earlier,
  peer-reviewed companion by the same authors reaching a more inconvenient
  conclusion. Citing only the flattering half is the kind of omission a
  journalist finds first. Cite both or expect to be asked why not.
- **Whether to publish stays the client's call**, and it usually needs sign-off
  at a level above the day-to-day contact. Draft the rebuttal, mark the row
  blocked on that decision, and never publish an "honest reckoning" post
  autonomously.

## 9 · Close-out digest

The verification round emits a digest carried into the deliverable's own
documentation, so the next stage inherits state instead of assumptions:

| Line | Meaning |
|---|---|
| Entries cited | How many library entries the deliverable uses |
| Verified / unverified | With the unverified named |
| Retired this round | With reasons |
| Scope or population corrections | The claims whose wording changed and why |
| Open verification items | What still needs a human, and who owns it |

The originating engagement's digest read: 19 entries cited, 0 without a source
link, 6 retired, 2 rescoped, 3 sector facts corrected, 6 open items for the
client. That is a healthy result, not an embarrassing one — the embarrassing
version is the run that reports nothing because it checked nothing.

## 10 · Unit conflation, and the control value that catches it

<!-- since: 2026-07-30 -->

A third failure class, alongside the two in §4, and the one that survived longest
in practice: the figure is real, the source is real, the population is right —
and the **unit** is wrong.

A trade association's own library carried *"7,5 miljoen brievenbussen bereikt per
week — 92% van de Nederlandse huishoudens."* 7,5 million is the weekly
**circulation** of a medium: copies printed. Not letterboxes, not households,
not people. Every citation check passes, because the source really does say
7,5 million.

Media reach is where this concentrates, because one medium is routinely measured
four ways — copies distributed, households delivered to, people who receive, people
who read — and the four differ by a factor of two in both directions. Money, energy
and emissions data have the same property.

**The cheap catch is a control value: divide by the total.** The Netherlands has
~8,4 million households, so "7,5 million households reached weekly" claims **89% of
the entire country through one medium** — implausible on its face, and it takes one
division to see. Register the denominator as its own library entry, marked as a
control rather than a campaign claim, so the check is available instead of
remembered.

*Rule: state the unit in the claim sentence, every time — copies, households,
people, and the age floor if the research has one. A number whose unit is implied
is a number waiting to be misread. When a figure asserts coverage of a
population, divide by that population before it goes anywhere.*

## 11 · Promote the verdict, or the library re-infects the work

Verification usually runs **inside a deliverable**, and its verdicts get written
to whatever register that deliverable reads. If the canonical library lives
somewhere else, nothing propagates, and the retired figures sit there waiting.

In the originating engagement two rounds of verification retired five figures in
the campaign's register while the canonical client library kept all five — one of
them flagged `needs-source-check` and sourced to a footnote in a client brochure.
The next round, the client read that entry and asked for it on a slide. The
library had quietly re-issued a claim we had already killed.

- **A verdict is not landed until it reaches the canonical library.** Retiring a
  figure in a deliverable's local register is half the work; the promotion is the
  other half, and it belongs in the same unit of work.
- **`needs-source-check` is not a state a library can rest in.** It is a claim
  that has not been checked, sitting where colleagues and clients read it as
  established. Resolve it or retire it.
- **When the bad figure came from your own library, say so.** The client who asked
  for it was reading what you gave them. Owning that is what makes the correction
  land as rigour rather than as contradiction.

### Retiring a figure is a sweep, and it ends in a count

"Promote the verdict to the canonical library" is not one write. A retired
figure survives in every place it was ever copied to, and each of those places
is a live source for the next build:

- **Every surface of every deliverable** — not only the visible one. Slide
  bodies *and* speaker notes, both language twins, the content plan, the source
  register, any exported PDF still circulating.
- **Every file of the library**, not just the register the retirement was
  written in. A claim library is usually several files — proof points,
  narratives, pillars, audience descriptions — and a figure that lives in a
  narrative summary or a pillar's one-liner is exactly what a build reads
  first.

So: **grep the retired figure — and its rounded and reworded variants — across
every deliverable surface and every library file, and report the hit count in
the close-out digest.** Zero is the only passing number, and a number is what
makes the sweep auditable; "propagated" is not.

Two live instances, one engagement, two days apart: a withdrawn figure still
sitting in a published deck's *speaker notes* after the slides were corrected,
and the same figure live in three places in a narratives file plus one in a
pillars file while its own register carried a correct, dated retirement record.
Both were found by looking, not by the process.

## 12 · When a client instruction fails verification

An explicit instruction to publish a specific number, where that number does not
survive checking, is neither a licence nor a veto. Both silent responses are wrong:
complying ships a claim you know is false, and quietly substituting your own figure
overrides a decision that is not yours.

Do all four, in this order:

1. **Do not publish either version yet.** New information pauses an instruction;
   it never reverses it on your own authority.
2. **Bring the verified alternatives**, not just the objection. "That figure is a
   circulation count; here are three verified persons-based figures from the same
   research family, with links" is actionable. "That figure is wrong" is not.
3. **Name where the wrong figure came from**, especially if the answer is you.
4. **Get a decision from the person whose decision it is, and record it as
   theirs.** Not "flagged in the review sheet". Not "noted in the register". A
   named person, a date, and an answer.

<!-- since: 2026-08-28 -->

### 12a · Only the asker can discharge the ask, and a repeat is a provenance signal

Step 4 is the one that fails, and it fails in a way that looks like diligence.
Two rules make it concrete, both learned the expensive way.

**An ask that needs someone's decision cannot be discharged by an internal
change.** Correcting your own register, rewriting your own rule and updating
your own plan feels like resolution and is not: the person who asked has seen
none of it and agreed to none of it. Before anything moves to "closed", answer
two questions — *does the person who asked know this is closed, and did they
agree?* If either answer is no, it is open. Worse, an internal rule written to
settle an open question **hardens against the client**, and the next artefact
built from it has to be retired.

> Measured on one engagement: a client asked three times across four weeks for a
> specific percentage. Each time it was flagged, recorded as "open, and theirs",
> and followed by a note saying not to re-litigate. On the third round the
> tracker showed the item under **Discharged** — closed on the strength of edits
> to two internal JSON files plus a new campaign rule the client had never seen.
> That rule then forbade what she was asking for. Cost: two retired
> deliverables, one rejected page, three rounds of the same conversation.

**When a client repeats an instruction you have already answered, stop
explaining and go find out where their version comes from.** A repeat is
evidence of an unexamined source, not of stubbornness. In the case above the
answer was in the intake folder the whole time: the client's own published
brochures printed the figure correctly once and with the direction reversed
twice, and the person kept reading the reversed ones. Three rounds of explaining
the arithmetic never touched the reason she kept asking, because the
disagreement was never about arithmetic. **Re-read their material — their
brochures, their site, their previous campaign — before you re-send your
objection.** §5 already treats client-supplied collateral as a source tier; this
extends it: read that collateral for FRAMINGS, not only for figures.

**When the decision goes against the arithmetic, record it as a decision.** The
client may knowingly choose their own house wording. That is theirs to choose.
What must not happen is the record quietly becoming "the figure is fine": keep
the arithmetic on the record, name who decided and when, write down the correct
alternative that was offered and declined, and write the honest answer to give
if someone challenges the number in public. A gate that enforces the chosen
wording stays a gate — it just enforces the new one, and says in its own
comments that it is doing so.

<!-- since: 2026-09-19 -->

## 12b · The library freezes between plan rounds

Once a content plan built from the library has been published, **the library is
frozen until the next plan round.** Production keeps verifying figures — that is
its job — but editing a register entry mid-production puts the published plan,
and any generated translation of it, out of step with its own sources for the
sake of a test asset.

Facts verified during production go to a **dated verification note** in the
project's research area, carrying the same fields the library entry would (exact
wording, publisher, commissioner, independence, date, URL, scope caution), and
are **proposed** as entries for the next round with their intended ids named.

The note also records the figures that did **not** survive verification. That
half is worth as much as the other: it stops the next production run
re-researching, and re-adopting, a circulating number that was already checked
and rejected.

<!-- since: 2026-08-28 -->

## 12c · Two conflicting figures: answer with both numbers *and* both addresses

"We are using conflicting percentages" is not actionable. A conflict note earns
its place only when it carries, for each figure: the number, **where it is
stated** (trade press, the client's own prior asset, our own deck, the primary
table), the arithmetic verdict, and a recommendation. Without the addresses the
note just re-schedules the same question for the next meeting.

Expect the awkward shape: the same true fact framed from opposite ends of one
fraction produces two honest numbers, and a third figure that is neither —
magnitude borrowed from one framing, direction from the other. That third one is
the only one a reader holding the report can catch, and it is usually the one in
widest circulation, because it travelled through syndicated coverage and into
the client's own earlier collateral. Name it as the one to avoid, and expect
whichever version is chosen to disagree with something the client has already
printed — say so, rather than letting them discover it.

<!-- since: 2026-08-28 -->

## 12d · A consistency sweep may correctly find nothing — report that, with evidence

When a figure is re-framed mid-campaign, the reflex is to sweep every asset and
"make them consistent". Run the sweep, but be ready for the honest outcome that
**nothing needed changing** — and report *that*, with what you searched and what
the assets actually carry, rather than quietly returning nothing or inventing an
edit to show work.

The likely reason is structural: an early week's assets often carry a *different*
comparison from the one under debate (a per-unit figure rather than the headline
ratio), so the contested framing simply is not on them. Saying so precisely —
"no week-1 item states that percentage at all; the only figure present is X,
which already matches your line" — is more useful than a diff, because it tells
the client where the decision *does* bite: in the plan's own note, at the next
round.

<!-- since: 2026-08-28 -->

## 12e · A partner-forwarded article is a lead, not a source

A client or partner forwarding an industry article is offering a lead. Register
it with **independence flagged** — who publishes it, and what they sell — and
use its company examples only as qualitative, provenance-named signals *beside*
(never instead of) a measured case. Then mine it: the studies it cites are often
already first-class entries in the register, and they get credited under their
own entries, not under the article's.

## 12f · A retired PHRASING is a sweep too, and it ends in a count

§11 already says that retiring a figure is a sweep across every artefact that
carries it, ending in a count. The same is true of a retired **wording** — a
banned attribution, a forbidden framing, a house term the client has changed —
and nobody applies it, because a phrase does not feel like a claim.

It is. When a client bans a form of words, or a house rule changes a term, sweep
every artefact already delivered, not only the ones named in the feedback, and
report the count. Two things fall out of this every time:

- **The instruction reaches further than the examples given.** A client naming
  two assets is naming the two they happened to look at. On one engagement a
  banned attribution line was named in two places and sat in five more — inside
  a copy workbook already delivered to the client, which their own feedback had
  not yet reached.
- **Rules added mid-engagement were never applied backwards.** The same sweep
  found a delivered caption still carrying a framing the campaign had banned by
  name three weeks earlier, because the ban was written for new work and no pass
  ever ran over the old.

Grep is the whole technique. The reason it does not happen is that nobody
schedules it, so schedule it: a phrasing change is not done until the sweep has
run and its count is in the record.

<!-- since: 2026-09-19 -->

## 12g · A quotation is a claim, and the number gates cannot see it

Every gate in this file is shaped around figures: cite or hedge, scope, units,
populations, commissioners, recomputation. A sentence in quotation marks carries
no number, so it passes all of them — and it is the single most damaging thing
that can be invented, because a reader treats quoted speech as reported fact and
a client's customer may be quoted back to them.

**The rule: a sentence in quotation marks on a client-facing asset must trace to
a real, named, verifiable utterance, or it does not go in quotation marks.** No
exception for an "archetypal" or "illustrative" objection. Write it as reported
experience instead — *"the question that comes up is…"*, *"the objection we hear
is…"* — which makes the same rhetorical move and claims nothing false.

*Measured case: a B2B factsheet designed to be forwarded by printers to their own
customers carried* "Just put the ad online, that saves paper" *under the heading*
"What a client says". *Nobody had said it. It cleared every gate on the build,
including an explicit no-fabrication rule, because that rule reads "a missing
figure or source" and a quotation is neither. The client caught it in review:
"we don't actually have a retailer saying this."*

**Extend the claims table accordingly.** The claims-and-citations table on a
review sheet is figure-shaped by default, which is precisely why these get
through. It covers:

- every **figure**, as it always did;
- every **quotation**, with who said it, when, and where it is recorded;
- every **source description** — "a comparative study" is a genre label, not a
  citation, any more than an internal proof-point id is (§7). Name the report;
- every **scope-bearing noun in a headline**, checked against what the figure
  under it actually measures.

<!-- since: 2026-09-19 -->

## 13 · Recent sources lead; old frameworks are cited as frameworks

Age is part of a figure's credibility, independent of its truth. An audience
that reads "2017" under the lead statistic concludes it was the best you could
find — and a reviewer will say exactly that ("a 2017 reference feels somewhat
outdated", live client review, 2026-08).

The rule, applied when allocating evidence to posts and again at the close-out
digest:

- **The newest national source that supports the claim leads.** If the library
  holds a recent domestic figure and an older international one for the same
  claim, the recent domestic figure is the headline; never the reverse.
- **An older international framework may still support the piece — cited AS a
  framework**, with its year and geography visible ("as a framework, not a
  <market> figure"), never presented as the lead statistic.
- **Review flag:** any lead figure older than ~3 years without a stated reason
  on the row. The reason can be good (a landmark study nothing newer replaces);
  it must be written down, or the reviewer writes it for you.
