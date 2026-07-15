<!-- since: 2026-06-01 -->

# Voice cascade integration

Every copy-producing step in this skill runs a **draft → review → rewrite** pass
against the org voice cascade. This is the dominant lever against AI-slop in
social copy. The cascade is mentioned here as context — this skill never invokes
another skill.

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
what the audience already recognises as the client.

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
4. **Rewrite.** Revise until the draft passes. Only then present it to the user.

## Where it applies in this skill

| Step | Copy artifact |
|------|---------------|
| Phase 5 | Sample post copy / concept hooks carried in calendar rows |
| Phase 7 | The creative fields the agent fills on `posts.json` (`hook`, `body`, `thread_parts`, `cta`) |
| Phase 8 | Per-edition captions, hooks, CTAs |

## Anti-slop quick checklist (always, even headless)

- No em-dash-as-drama, no "It's not just X, it's Y" antithesis frames.
- No filler openers ("In today's fast-paced world…", "Let's dive in").
- **No engagement-bait** ("Comment YES below", "Tag someone who…", "Drop a 🔥").
- No overused LLM vocabulary (delve, leverage as a verb, robust, seamless,
  tapestry, testament, landscape-as-metaphor, "in the realm of").
- Match the L2 `voice-anchors.md` register if anchors exist.
- Platform tone notes still apply — cross-check the relevant
  `references/platforms/<platform>.md` for channel-specific register.

## Fallback when the voice MCP is unreachable (headless / no network)

If `voice://*` resources cannot be fetched:

1. Use **L2-only** (`{base}/voice/*`) if present.
2. Apply the anti-slop quick checklist above as the L1 floor.
3. `log()` the degradation ("voice L1 resources unreachable — applied L2 + inline
   checklist only") so the user knows the pass ran in fallback mode.

Never fail the copy step on an unreachable voice MCP — degrade and log.
