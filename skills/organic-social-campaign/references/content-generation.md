<!-- since: 2026-06-01 -->

# Phase 8 — Edition-batched content generation

Generate branded, coherent assets **one edition at a time with human review**,
per-platform configurable, consuming the `media-gen` MCP. This skill *mentions*
`media-gen`, `chart`, `diagram`, `pdf`, `pptx`, and the voice cascade as
context — it never invokes another skill.

The config + media taxonomy live in
[platform-content-config.md](platform-content-config.md). The post objects this
phase consumes/mutates are defined in
[post-object-schema.md](post-object-schema.md).

## Coherence is two things

- **Narrative coherence** (storyline, series arc) lives in the planning agent's
  context — the `concept` and `series_id` carried on each post.
- **Visual coherence** is either **identity** (Track A: media-gen reference
  conditioning — pass the approved anchor as a `subject`/`first_frame`
  reference) or **family resemblance** (fallback: reuse the locked prompt block
  verbatim). State the expectation to the user explicitly.

## Batch renders demonstrate; production is one at a time

<!-- since: 2026-08-18 -->

Producing a family of sibling assets in one batch run yields visible
cross-item repetition — the same layout beats, the same transitions, the same
phrasing rhythm — because a single generation context converges. That is
acceptable when the point is to demonstrate a format family (a test pack),
and it must be said out loud when it is. Production assets are made **one at
a time, each reviewed before the next starts** (originating engagement,
2026-08-17: the batch repetition was the client-side reviewer's first
observation). The per-edition gate in §3 bounds *review*; this rule bounds
*generation* inside an edition too.

## 1. Gate

Phase 8 runs **only** if the user opts in **AND**
`content_generation.enabled == true`. Up front, state:

> Identity reuse (the same recurring subject across posts) requires `media-gen`
> reference conditioning (Track A, `PLAN_reference_conditioning.md`). If that is
> unavailable, assets will be **family-resemblance** (consistent style/palette),
> not identical subjects.

Get explicit acknowledgement before generating.

## 2. Lock the style block once (campaign-level)

Derive a verbatim prompt string (photography spec + palette) from
charter/tokens. Persist as
`{base}/social-media/organic/style-blocks/<ref>.txt` (the
`default_style_block_ref` from config). Reused across editions and by
`paid-social-campaign`.

<!-- since: 2026-08-28 -->

## 2b. Lock the campaign visual system (designed assets)

§2 locks *generated* imagery. The assets a campaign actually ships most of —
carousels, one-pagers, motion — are **designed, not prompted**, and have no
campaign-level lock at all, so every new post re-derives its look from the brand
folder and the set drifts apart over six weeks.

The moment the first assets of each track are approved, write
`campaigns/<slug>/VISUAL-SYSTEM.md` and have every later post inherit it. It
fixes: surface anatomy (and what each structural variant *means*), the type
scale, the signature marks with a rule each, the pictogram and diagram
vocabulary **including the diagram types already established by name**, so the
next post reuses one instead of inventing a fourth, the density rule, the motion
grammar where relevant, and the production constraints that shape all of it.

Two rules keep it alive rather than decorative:

- **The bar is brand smell, not pixel identity.** Recognisable as the same
  campaign at a glance in a feed — not built identically.
- **Deviation with a stated reason is fine; drift without one is not.**

Where the client's channel already exists, derive the system from their **real
feed** — a screenshot of the actual grid — not from the brand book. Continuity
with what the audience already sees is what makes a post look native instead of
like an ad dropped into someone's account.

<!-- since: 2026-08-28 -->

## 2c. Verify the delivered artifact, not the render intent

A render tool's `status: ok` is a statement about the *request*, not about the
file. Every one of these shipped green and was caught only by opening the bytes:
a page silently rasterized (fonts unembedded, file 10-25× larger) because one
decorative asset carried an alpha channel; a burn-in caption setting that emitted
a subtitle track and burned nothing, on a platform that autoplays muted; a
fallback typeface pulled in for a single glyph missing from the brand font; and
an artifact returned as a storage push with no bytes at all once the output
crossed the tool's inline size cap.

So before anything reaches a review gate: rasterize the pages and look at them,
list the embedded fonts, check duration and dimensions, and where text is burned
in, read it back **off the pixels**. Then look at the whole set together —
repetition and broken rhythm only show up side by side.

Two extensions, both learned the expensive way:

- **Check delivered *affordances*, not only delivered text.** A calendar cell
  listing three sources carried a hyperlink on only the first, because a
  spreadsheet cell holds one link — so the reviewer read "that source is
  missing" while its label sat there unlinked. The failure is silent precisely
  because the text looks right. Links, downloads, playable audio, alt text: a
  thing the reader cannot *act on* is not delivered. (Render one row per cited
  item, figure beside its own link, rather than stacking them in one cell.)
- **Re-rendering an approved set to change one item is a regression risk.**
  Brand data, tokens and the renderer itself move underneath an approved
  deliverable. When a reviewer's edit touches one card of seven, re-render the
  set, then **diff every unchanged item against the committed output** before
  publishing, and publish only what actually differs. Two things follow: a
  silent restyle of the six approved cards becomes impossible to miss, and the
  untouched files keep a clean version history instead of collecting empty
  versions. If a sibling comes back byte-identical, that is the proof — do not
  re-upload it.

**A verifier that fails a correct artifact is worse than no verifier**, because
the next person learns to ignore it. When an automated check disagrees with what
you can see, confirm the artifact by eye **first**, then fix the check — never
the other way round, and never by loosening it until it passes. (Worked example:
an OCR caption check cropped a fixed band and read it as "a single text line";
new drawn objects appeared inside that band and the read turned to garbage while
the caption was plainly legible. The fix was a tighter crop plus a second
segmentation mode — not a lower threshold.)

## 3. Per edition (default one week), in order

### a. Select + partition
Select the edition's posts from `posts.json` where `media_spec.type != none`,
capped at `max_assets_per_edition` (`log()` any deferred — never silently
truncate). Partition by `media_spec.producer`:
- `media-gen` posts (`image`/`carousel`/`reel`/`short`) → steps b–c.
- `chart`/`diagram`/`pdf`/`pptx` posts (`infographic`/`document`) → step c2.

### b. Anchor-select loop (media-gen posts)
Per recurring subject/series:
1. Build the `brand_context` dict (step 4) and call `media-gen` `generate_image`
   for **3–4 candidates**.
2. **Human picks ONE anchor.**
3. Persist the anchor + its rendered prompt block; set `anchor_asset_ref` on
   sibling posts that share the subject.

### c. Generate siblings & video (media-gen posts)
- **With Track A** → pass the approved anchor bytes as a `subject` reference to
  `generate_image_variants` (aspect fan-out) and as a `first_frame` reference to
  `generate_video` → true identity.
- **Without Track A** → reuse the anchor's locked prompt block verbatim via
  `generate_image_variants` + `generate_video` → family resemblance.
- `carousel` → N × `generate_image` sharing the anchor; `reel`/`short` →
  `generate_video` at 9:16.

### c3. Designed motion graphics (`reel`/`short` with `producer: video-hd`)

<!-- since: 2026-08-19 -->

A `video-hd` row is **not** a media-gen asset and does not enter the anchor loop. Route it
to the branded-video skill and hold it to that skill's short-form rules. Three properties
make the difference between a cut that ships and one that gets re-made:

1. **The plan row owes a shape, not just a topic.** Before authoring, name which
   rhetorical shape the piece uses — explainer arc, false-assumption-then-reveal,
   zoom-out scale reveal, iceberg proportion, one-gesture-retargeted — and what the
   viewer is supposed to believe differently at the end. "Opener video introducing X" is
   a slot, not a brief, and a slot gets a storyline invented at render time.
2. **Review frames before the render, not after.** Storyboard the key beats as still
   frames and look at them (composition, subject scale, whether anything moves in the
   first two seconds). A finished async render is the most expensive place to discover a
   static hook.
3. **Verify the delivered file before it reaches the client gate (e).** Muted autoplay
   makes burned captions the primary channel, and a caption *setting* is not a caption on
   the pixels. Confirm the real duration and the on-screen text on the delivered frames —
   not from the render job's status block.

Where a row's message would be undercut by the obvious visual cliché (an image that
argues the opposite of the campaign's position), name the banned visuals at plan time and
carry them on the row. That check costs nothing on paper and is invisible once rendered.

### c2. Brief non-media-gen posts (infographic/document)
Emit a structured brief (data points, layout intent, brand refs) into the post
object and **flag the producer skill** (`chart`/`diagram` for infographics,
`pdf`/`pptx` for documents) for the user to run separately. Phase 8 does **not**
invoke those skills and does **not** call `media-gen` for these.

### d. Captions
Captions/hooks/CTAs for the whole edition pass the **voice cascade**
([voice-integration.md](voice-integration.md)).

### e. Human reviews the edition
Present tiles + briefs + captions side by side → approve → update each post
`status`:

For a video row, present a **contact sheet of frames from the delivered file** (not the
render job's own preview strip, which shows only the frames it chose) alongside the
caption — a reviewer cannot judge pacing, a static hook, or caption legibility from a
thumbnail. Say what the piece is trying to make the viewer believe, so the review is
about the argument and not only the finish.
- `media_ready` for generated media-gen assets,
- `brief_ready` for non-media-gen (infographic/document) posts.

Then **advance to the next edition**. **Never generate the next edition before
this gate.** Resume can re-enter mid-Phase-8 by edition.

## 4. Brand-context construction

Mirror `media_gen.brand.build_brand_context_from_charter` **exactly** and call
`validate_brand_context` before generating. Required fields (from
`media_gen.types.BrandContext`):

```
client_slug, display_name, tagline, industry, archetype, domain,
palette, palette_hex, fonts, image_descriptions, logo_paths,
token_variables, charter_version
```

Read these from `{base}/charter.json` (+ `{base}/tokens.css` for
`token_variables` / `charter_version`, `{base}/logos/` for `logo_paths`). The
MCP is client-agnostic — pass the resolved dict as a structured argument; never
expect the MCP to read `client-data/` itself (three-layer-clean).

## Asset output location

The MCP returns bytes (base64 + sha256), not filesystem paths — caller and MCP
share no filesystem in deployed mode. Write returned bytes to:

```
workspace/<client>/output/organic-social-campaign/assets/
```

## Narrated video: audio is a route decision, never a default

<!-- since: 2026-08-18, extended 2026-08-28 -->

**A preset TTS voice is a review placeholder, and it must be labelled as one.**
Expect this verdict pattern: the client likes the film and rejects the voice
("very AI"). It is not a wording problem and no amount of re-synthesis fixes it.

Put the audio route to the client as an explicit choice, with a fallback
designed for each: **studio-recorded voice-over** · **licensed music only** ·
**silent with burned-in captions** (plus a static fallback where the format
allows it). Burned-in captions stay in every route — most feed video plays
muted, so captions are the primary channel, not an accessibility extra.

**Ship the silent option as a file, not as a sentence.** Derive it from the
approved narrated cut by a stream copy that drops the audio track only
(`ffmpeg -an -c:v copy`), so the picture is bit-identical and the two cuts
cannot drift. Deliver it **beside** the narrated cut rather than in place of it:
the route is still open, and the silent cut is exactly what a studio voice-over
gets laid over later. Then make the filenames do the work — when two files
differ only in audio, a reader who clicks the wrong one concludes the work was
not done, so name the route in the filename and say in the covering note which
link is which.

Where a preset voice is still in play, send short samples of the candidates
speaking one campaign-toned line **in the campaign language** and let the client
pick; record the pick in the brand folder (e.g.
`brand_context.video.tts.presetVoice`) so every later render uses it — a voice
change mid-campaign is a brand break. A cloned voice (a client spokesperson) is
a client option with its own consent, cost and recording requirements: note it,
never default to it.

**Synthesized narration is not reproducible, and not only in length.** The same
text re-synthesized gives a different duration *and a different pause
structure* — the breath moves. Anything timed against it (caption windows, cuts)
must be re-measured from the delivered file after every render, never rescaled
from the previous one. When you map measured speech runs onto sentences, **count
the runs against the sentences before concluding a line is missing**: a run
count that exceeds the sentence count means one sentence breathes in the middle,
and assuming last render's split is what makes a complete narration look
truncated.

## Edge cases

| Situation | Response |
|-----------|----------|
| `media-gen` `QuotaExceeded` mid-edition | Stop, persist what succeeded, surface the dashboard URL, resume the edition later. |
| Track A absent, user insists on identity | Flag the dependency on `PLAN_reference_conditioning.md`; offer family-resemblance or stop. |
| Video cost (Veo ~600s/clip) | Keep video editions small; the per-edition gate + `max_assets_per_edition` bound spend. |
| Voice MCP unreachable | L2-only + inline anti-slop checklist, logged (see voice-integration.md). |
