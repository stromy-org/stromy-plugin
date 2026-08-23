<!-- since: 2026-07-31 -->

# Co-produced deliverables — when a generated artifact is also edited by a reviewer

Both client-facing deliverables this skill produces — the Stage-1 strategy deck
and the Stage-2 content plan — are **generated from a source** *and* handed to a
reviewer who edits and comments on the rendered file. That combination has its
own failure mode, and it is severe: **a rebuild silently reverts every edit it
did not author.** This file is the single home for that discipline;
[strategy-deck-stage1.md](strategy-deck-stage1.md) and
[content-plan-stage2.md](content-plan-stage2.md) both cite it rather than
carrying half of it each.

> **Scope split — read this first.** This file covers the *deliverable*
> semantics: what a reviewer's edit means, where it has to land, and how to
> reconcile it with their comments. It deliberately does **not** cover the
> *substrate* mechanics — fetching the live version, reading version history,
> file locks, publishing in place, keeping the pickup→republish window short.
> Those are identical for every artifact on a shared workspace, belong to the
> workspace layer, and are defined once in the org's **`workspace-cowork`**
> protocol. Follow that protocol for the surface; follow this file for the
> content. Never restate its mechanics here — a copy rots the moment the
> substrate changes.

## 1 · Two channels, two meanings

A review round arrives on two channels at once, and they mean different things:

| Channel | What it is | How to treat it |
|---|---|---|
| **Comments** | Directional intent — "make this shorter", "add the formats" | Interpret and integrate into the deliverable's own structure and voice. Never paste comment text onto the artifact unedited. |
| **Direct edits** | Literal, already-decided wording | Adopt as written. The reviewer stopped asking and did it. |

**On any overlap, the file wins on anything the comments do not mention** — and
the reviewer's wording wins over ours wherever both address the same line.

Feedback also arrives on surfaces the artifact itself never sees: a call, a
message, a document the reviewer wrote for their own client. **Ask what else
landed since the last round rather than assuming the file and its comments are
the whole input** — the point is to arrive open to more than one channel, not to
maintain a checklist of channels that will always be incomplete.

## 2 · Every edit lands in the build source, never in the output

An edit folded into the rendered file survives exactly until the next build.

1. **Diff the live copy against what you last published**, before changing
   anything. That diff — not the comment thread — is the record of what they
   actually changed.
2. **Fold each surviving edit into the build source**, then rebuild.
3. **Say which of their edits you kept**, so a reviewer can tell folded-in from
   overwritten, and can challenge a judgment call.

### The diff must be mechanical, and sanity-checked

Extract the text of **every part on both sides programmatically** — every slide,
every notes page, every sheet and cell — and compare. Then state the count.

**If the reviewer says they made edits and your diff finds almost none, your
diff is wrong, not the reviewer.** In the originating engagement a round
reported "four changes" on a file carrying forty-six; the deliverable was
rebuilt on that number and thirty-four of their edits died. A count that
contradicts the collaborator's own account of their work is a bug to
investigate before a single line is rebuilt.

### Their intent is not their artifact

A hand-edit made in a web editor routinely leaves the layout broken — text
running together, a lost line break, a card that no longer fits. That breakage
is not a request to reproduce it; it is usually the very thing their comment
asks you to fix. Adopt the *intent*, repair the *artifact*.

### Some of their edits are superseded by their own later instruction

An edit from an earlier batch can be overtaken by a comment in a later one (a
cadence they themselves then changed, a box they later asked to delete). Do not
restore it, and **list what you deliberately did not restore, with the reason** —
an unexplained absence reads as another lost edit.

## 3 · A label change is a scope instruction

When a reviewer renames something structural — a pillar, a track, a section,
a column — **re-check its contents against the new name in the same pass**. A
renamed element whose body still argues the old scope ships a promise the
deliverable does not keep, and it is invisible in a diff because the diff shows
only the rename.

In the originating engagement a content pillar was renamed from one machine to
the whole industry chain; the body kept comparing the same two materials for
another full round, in a client-facing deck.

## 4 · Provenance: who originated the instruction

Record, per instruction, **who it came from** — the reviewer themselves, their
own client, or our earlier draft. This is not bookkeeping: it decides who has
to agree when an instruction cannot be executed as given.

The Evidence Discipline rule for an instruction that fails verification
([evidence-library-integrity.md](evidence-library-integrity.md) § When a client
instruction fails verification) ends in "let the client decide, and record the
decision" — which is meaningless if nobody recorded *which* client. A correction
delivered only to the intermediary leaves the person actually holding the wrong
belief uncorrected, and they will ask for the same thing again next round.

When the originator is a step removed, hand back both the objection and the
verified alternatives **in a form the intermediary can forward** — they, not
you, are in the room.

## 5 · The round is not closed until the record says so

Close every round with the **review-response ledger** the strategy document
already defines ([strategy-document-template.md](strategy-document-template.md)
§ Review-response ledger): per comment, the decision, the grounded rationale,
and the action (stays / moves to the content plan / moves to a briefing /
dropped / open question). Add to it, for a co-produced artifact:

- the **edits folded in**, and the ones deliberately not restored, with reasons;
- the **version identifiers** you diffed, so the next round can audit the claim
  rather than trust it;
- genuinely open questions, collected into **one** clarification message after
  everything self-researchable has been answered.

## 6 · Keep the reviewer's own words

Two classes of reviewer wording are load-bearing and must not drift back on the
next rebuild:

- **Their audience labels**, verbatim — see
  [strategy-document-template.md](strategy-document-template.md) Chapter 2.
- **Their lexicon** — the term their market uses for a role, a channel, a
  format. A reviewer who sweeps one word across an entire deliverable by hand
  has told you the vocabulary was wrong, not the sentence. Record the resolved
  term in the client's voice profile
  ([voice-integration.md](voice-integration.md) § Client lexicon) so the next
  build cannot regress it.

## 7 · Standalone deliverables carry no trace of the process

<!-- since: 2026-08-18 -->

The co-edit loop generates process residue — reviewer names, round numbers,
"per feedback of <date>" notes, version labels, open-point cross-references.
That residue belongs in the ledger (§5) and the internal working documents,
and **nowhere in a client-facing deliverable**: an artifact that cites its own
feedback trail reads as a draft to the exact reader it was cleaned up for, and
shows the client their agency's kitchen (live review, 2026-08: a rendered plan
cell citing the reviewer's own mail note, spotted by the reviewer).

Enforce it mechanically, not by eyeball — the same principle as the voice
gate's literal count. Before publishing, lint every rendered cell/paragraph of
the client-facing artifact against a trigger list: reviewer and colleague
names, "feedback"/"review", round and version numbers, internal file names,
and dates coupled to process events rather than content. Zero hits or it does
not ship; wire the lint into the build so a rebuild cannot regress it. Working
documents — the internal twin, the ledger — keep the full trail deliberately:
the lint separates the two postures, it never sanitizes the record.
