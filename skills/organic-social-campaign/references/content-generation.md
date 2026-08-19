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

## Narrated video: the voice is a client decision

<!-- since: 2026-08-18 -->

Before any narrated cut goes to client review, send short samples of the
candidate TTS preset voices speaking one campaign-toned line **in the
campaign language**, and let the client pick. Record the pick in the brand
folder (e.g. `brand_context.video.tts.presetVoice`) so every subsequent
render uses it — a voice change mid-campaign is a brand break. A cloned voice
(a client spokesperson) is a client option with its own consent, cost and
recording requirements: note it, never default to it.

## Edge cases

| Situation | Response |
|-----------|----------|
| `media-gen` `QuotaExceeded` mid-edition | Stop, persist what succeeded, surface the dashboard URL, resume the edition later. |
| Track A absent, user insists on identity | Flag the dependency on `PLAN_reference_conditioning.md`; offer family-resemblance or stop. |
| Video cost (Veo ~600s/clip) | Keep video editions small; the per-edition gate + `max_assets_per_edition` bound spend. |
| Voice MCP unreachable | L2-only + inline anti-slop checklist, logged (see voice-integration.md). |
