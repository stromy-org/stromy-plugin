<!-- since: 2026-06-01 --><!-- updated: 2026-07-16 mechanical self-check as a distinct, non-skippable step -->

# Voice cascade integration

Every copy-producing step in this skill runs a **draft → review → rewrite →
verify** pass against the org voice cascade. This is the dominant lever against
AI-slop in social copy. The cascade is mentioned here as context — this skill
never invokes another skill.

## The two layers

| Layer | Where | Scope |
|-------|-------|-------|
| **L1 baseline** | `stromy-format-mcp` resources `voice://baseline` + `voice://rules.json` | Client-agnostic anti-AI-smell floor |
| **L2 profile** | `{base}/voice/voice-profile.md`, `voice-anchors.md`, `voice-extensions.json` | Per-client voice, additive on top of L1 |

**Precedence:** L2 may **add** bans (via `voice-extensions.json`
`additional_banned_phrases` / `additional_banned_substrings`); it may **never
relax** L1. If an L2 file appears to relax L1 (keys like `allow`, `unban`,
`remove`, `relax`, `override`, `disable`), ignore that directive and keep L1.

## Calibrating L2 from the client's prior content

**The client's previous content is the tone-of-voice baseline.** When the client
supplies prior posts or content — including partner/influencer content they
**endorse** — derive or calibrate the working voice profile from that corpus
*before* drafting. This is a standing method step, not a per-engagement
improvisation: a voice profile written from a brand adjective list will not match
what the audience already recognises as the client. It is also the primary
voice source in the skill's **Narrowed-intake mode** (Phase 1 Step 2), where a
full voice questionnaire isn't realistic — the corpus does the work a
heavyweight intake pass would otherwise do.

Read the corpus for:

| Dimension | What to extract |
|---|---|
| **Register** | formal ↔ colloquial; how much distance from the reader |
| **Sentence rhythm** | long and clausal vs short and punchy; how they open |
| **Warmth** | institutional vs personal; do they use "we"/"you" |
| **Emoji / hashtag habits** | how many, where, which — or none |
| **Language idiom** | NL/EN mix, sector jargon they do (and don't) use |

**Record deltas as *proposed* `voice-extensions` entries for the client to
confirm — never silently overwrite the L2 profile.** The corpus is evidence of
practice, not an approved standard: it may contain habits the client is actively
trying to leave behind. Propose, show the evidence, let them decide.

### AI-tell guardrails (standing ban candidates)

Prior-content calibration is the natural moment to propose the standing AI-tells
as **L2 bans**, since they are what makes generated copy fail to sound like the
client:

- **Em-dash-chain sentences** — multiple em-dashes stacked in one sentence.
- **"We are X, not Y" antithesis constructions.**
- **Catch-all AI phrasing** — the usual overused LLM vocabulary and filler
  openers (the L1 baseline already bans much of this; L2 may sharpen it).

Propose these as additions when the client confirms — they are candidates, not
automatic. Adding them is always safe under the cascade (L2 may **add** bans,
never relax L1).

### Edge cases

- **No prior content (cold brand)** → skip this step; author the L2 profile the
  normal way.
- **The corpus contradicts the client's stated voice profile** → **surface the
  contradiction; do not pick silently.** Show the mismatch ("your profile says
  concise and plain; the last 20 posts average three clauses and heavy jargon")
  and ask which is the target. Choosing for them buries a real strategic
  decision inside a formatting choice.
- **Running under `run_mode: internal-draft`** → an uncalibrated voice profile is
  itself a **gaps-ledger entry**.

## The loop (run at every copy step)

1. **Load.** Fetch L1 `voice://baseline` + `voice://rules.json` from
   `stromy-format-mcp`. Load any L2 files under `{base}/voice/`. If prior client
   content is available and the profile has not been calibrated against it, run
   the calibration step above first.
2. **Draft.** Write the copy (Phase 5 sample copy, Phase 8 hooks/captions/CTAs).
3. **Self-review.** Check the draft against the combined ruleset — flag every
   violation explicitly before rewriting.
4. **Rewrite.** Revise the draft until every flagged violation is fixed.
5. **Mechanical self-check (non-skippable — run every time, no exceptions).**
   Do not close the loop on an eyeballed re-read. Explicitly enumerate every L1
   + L2 banned construction as a checklist and **count matches against the
   final draft, one item at a time**:
   - Count every em-dash in the draft. If em-dashes are banned (L1 default, or
     an explicit L2 ban), the count must be **zero** — not "mostly clean," not
     "just a couple." A single missed instance is a failed gate.
   - Check each banned phrase / substring from `voice-extensions.json` and the
     anti-slop checklist individually — do not scan for "the vibe of" a
     banned phrase, check the literal string.
   - Any nonzero count → **go back to step 4**, fix, and re-run this checklist.
     Only present the copy to the user once every count is zero.

   This step exists because a self-review that "feels" clean is not the same
   check as a literal count: a run shipped dozens of em-dashes against an
   explicit client ban because the review was read-through rather than
   counted. Treat step 5 as a mechanical gate, not a second read of step 3.

## Where it applies in this skill

| Step | Copy artifact |
|------|---------------|
| Phase 5 | Sample post copy / concept hooks carried in calendar rows |
| Phase 7 | The creative fields the agent fills on `posts.json` (`hook`, `body`, `thread_parts`, `cta`) |
| Phase 8 | Per-edition captions, hooks, CTAs |
| Phase 3 Step 6 | The assembled strategy document's prose (executive summary, pillar copy, distribution/arc narrative) — the client-facing artifact with the highest cost of a missed ban |

## Anti-slop quick checklist (always, even headless)

- No em-dash-as-drama, no "It's not just X, it's Y" antithesis frames.
- No filler openers ("In today's fast-paced world…", "Let's dive in").
- **No engagement-bait** ("Comment YES below", "Tag someone who…", "Drop a 🔥").
- No overused LLM vocabulary (delve, leverage as a verb, robust, seamless,
  tapestry, testament, landscape-as-metaphor, "in the realm of").
- Match the L2 `voice-anchors.md` register if anchors exist.
- Platform tone notes still apply — cross-check the relevant
  `references/platforms/<platform>.md` for channel-specific register.

This checklist is the enumeration that step 5 above counts against — it is not
a separate, optional pass.

## Fallback when the voice MCP is unreachable (headless / no network)

If `voice://*` resources cannot be fetched:

1. Use **L2-only** (`{base}/voice/*`) if present.
2. Apply the anti-slop quick checklist above as the L1 floor.
3. `log()` the degradation ("voice L1 resources unreachable — applied L2 + inline
   checklist only") so the user knows the pass ran in fallback mode.

The mechanical self-check (step 5) still runs in fallback mode — losing the L1
MCP resource is not a reason to skip counting bans, since the anti-slop
checklist and any L2 bans are still fully enumerable offline.

Never fail the copy step on an unreachable voice MCP — degrade and log.
