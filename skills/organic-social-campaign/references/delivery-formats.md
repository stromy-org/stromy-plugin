# Delivery formats — what file each channel actually takes

**When to load:** Phase 8 step "gate the file", and every handover of a rendered
asset to a client or a scheduler. Also whenever a new channel or surface enters
a campaign, because that means adding a row rather than editing a build script.

The table below is **generated** from `scripts/delivery_formats.py` — regenerate
it with `python3 scripts/delivery_formats.py --markdown` rather than editing it
here, or the prose and the gate will disagree and only one of them runs.

---

## Why this exists at all

Phase 7 validates a **post object**. Nothing validated the **file**.

On the KVGO / indruk.nu campaign the rule *"the final Instagram deliverable is
per-slide images (JPEG/PNG), not PDF"* was:

- decided on a client call on **2026-08-17**,
- written into the campaign's own briefing as rule 9,
- repeated in that campaign's `VISUAL-SYSTEM.md`, in the B2C column of its
  format table,
- agreed by everyone, and disputed by nobody.

Every B2C asset was published to the client as a PDF anyway, for five weeks,
until the client asked for PNG **by hand** on 2026-09-21. She was doing a gate's
job.

The rule was never wrong. It had no measurement at the seam where it applies, so
it survived as prose while the builds shipped the intermediary. When the
producer side was then fixed, it was fixed in the two assets the complaint had
landed on, and the other two producers kept emitting the wrong frame — which is
how, on 2026-09-22, a sweep found **eight live client-facing files at
1080×1351** for a 1080×1350 format: seven carousel cards and a LinkedIn
one-pager, all published four days earlier and all looking perfectly fine.

**The rule this file encodes: a delivery-format rule is enforced where the file
is produced or handed over, never where it is designed.** A rule with no
measurement is a preference, and a preference is what you are left defending
when a client notices first.

---

## The contract

<!-- generated: python3 scripts/delivery_formats.py --markdown -->

| key | takes | one file per | frame | pages / length | severity | evidence |
|---|---|---|---|---|---|---|
| `instagram/carousel` | .png, .jpg, .jpeg | card | 1080x1350 | -- | **blocks** | engagement |
| `instagram/image` | .png, .jpg, .jpeg | post | 1080x1350 | -- | **blocks** | engagement |
| `instagram/reel` | .mp4 | post | 1080x1920 | 5-90s | **blocks** | engagement |
| `instagram/story` | .mp4, .png, .jpg | post | 1080x1920 | -- | warn | inferred |
| `linkedin/document` | .pdf | post | 1080x1350 | 2-20 pages | **blocks** | engagement |
| `linkedin/carousel` | .pdf | post | 1080x1350 | 2-20 pages | **blocks** | engagement |
| `linkedin/image` | .png, .jpg, .jpeg | post | 1080x1350 | -- | **blocks** | engagement |
| `linkedin/infographic` | .png, .jpg, .jpeg | post | 1080x1350 | -- | **blocks** | engagement |
| `linkedin/video` | .mp4 | post | 4:5 | -- | warn | inferred |
| `print/leavebehind` | .pdf | post | A4 | 1-12 pages | **blocks** | engagement |
| `internal/review` | .pdf, .png, .jpg, .mp4, .docx, .xlsx, .pptx | post | -- | -- | advisory | engagement |

Open choices a content plan may carry, and what they resolve to:

| plan says | candidates |
|---|---|
| `document of carousel` | document, carousel -- the delivered file decides, and the check records which |
| `document or carousel` | document, carousel -- the delivered file decides, and the check records which |
| `carousel of document` | carousel, document -- the delivered file decides, and the check records which |

<!-- /generated -->

---

## The four things a row carries, and why it carries them

Modelled on stromy-org's `scripts/delivery_limits.py`, which exists because a
bare number next to the code that needs it has no record of where it came from —
so a conservative internal choice becomes folklore and is later quoted back as a
platform requirement.

| field | question it answers |
|---|---|
| `kind` | does breaking this **block** a delivery, or only warn? |
| `evidence` | is this a platform fact, this engagement's decision, or a guess? |
| `source` | the call, email or first-party URL it came from |
| `checked_on` | the date a human last read that source |

**The invariant, asserted by `validate_registry()`: a row may only BLOCK if its
evidence is `documented` or `engagement`.** An inferred or community-reported
number may warn; it may never refuse a delivery.

That is not squeamishness. A gate that blocks on folklore gets switched off, and
a switched-off gate gates nothing at all — which is strictly worse than no gate,
because the team believes it is covered.

### `engagement` is the honest label for most rows

1080×1350 is **not** an Instagram requirement — Instagram accepts a range. It is
the frame the work was designed in. A file that is not the frame it was designed
in has been resampled or cropped by something nobody reviewed, and that is worth
refusing on its own terms. Labelling it `engagement` rather than `documented`
keeps the claim true and keeps the row blocking.

### `unknown` carries no number

An `unknown` row records that a constraint exists and has not been checked. It
must not carry a value — unknown is not zero, and a zero that means "we never
looked" reads identically to a measured zero.

---

## Either/or is first-class, in two different shapes

Both show up in real campaigns, and a registry that models neither pushes both
back onto prose — where the last failure lived.

**1. Either extension.** `extensions` is an ordered tuple. Every member is
accepted; the first is what a producer emits absent a reason. `instagram/image`
takes `.png`, `.jpg` or `.jpeg`.

**2. Either surface.** A content plan is allowed to leave a post's surface open.
The KVGO plan carries a literal `"document of carousel"` for its week-6 B2B
post, because that choice belongs to the week it is built, not to the day the
calendar was frozen.

`resolve()` returns **every** candidate; `check_file()` passes if the file
satisfies **any** of them, and reports which one in `Result.satisfied`.

That report is the point. The delivered file is the decision, and the check is
where the open question gets its answer written down — instead of the choice
being made silently by whoever rendered it first.

Adding a new plan word means one line in `SURFACE_ALIASES`. **Never rewrite the
plan to fit the table**: a content plan is a client-facing artifact, and the
Dutch and the loose phrasing are the client's, not a lookup key.

---

## What a check actually measures

| extension | reader | measures |
|---|---|---|
| `.png` `.jpg` | Pillow | pixel frame |
| `.pdf` | PyMuPDF | page count, first page rect **in points** |
| `.mp4` | `ffprobe` | frame, duration |

**PDF pages are measured in points, with a half-point tolerance.** A page
authored at 1080×1350 CSS comes back as 810×1012.5pt, and Chromium rounds that
to 1013. Treating the rounding as a defect makes every correct PDF fail; that
same 0.04pt is exactly what made the PNG exports 1080×1351, so the rounding
matters in one direction and not the other.

**A carousel is checked as a SET.** `check_set()` refuses a set whose cards do
not share one frame, because Instagram crops the whole carousel to the first
card's aspect — so a single odd card silently crops its siblings while remaining
a perfectly valid image on its own. No per-file loop can see that.

---

## Inconclusive is not a pass, and it is not a failure either

If the **reader** is missing — no `ffprobe` on PATH, no Pillow in this
interpreter — nothing has been learned about the file. `Measurement.unmeasurable`
records that, `Result.ok` is False, and the file is reported `NOT MEASURED`
rather than either green or red.

Collapsing those two states is a known way to break a gate in both directions:

- report it as a **failure**, and people learn to wave the failure through; the
  day it fires for real it is ignored. The KVGO publish script hit exactly this
  when its readback returned an auth error and it printed a confident
  `MISMATCH` on a byte-perfect upload.
- report it as a **pass**, and an unmeasured deliverable ships under a green
  check, which is the original failure wearing a badge.

So: measured-and-clean is a pass. Everything else says which of the other two it
is.

---

## Wiring it into a campaign

Two seams, and both are needed:

1. **Production.** The render script exports through a helper that takes the
   frame from an explicit clip rectangle and asserts the result, rather than
   taking whatever the page rect gives it. KVGO's is
   `test-run/instagram_export.py`; it also refuses a PDF page with no embedded
   fonts, because a rasterized page still exports a good-looking PNG and that
   check has to happen while the PDF is still open.
2. **Handover.** The publish script refuses a file that is not what its channel
   takes. KVGO's `build/check_delivery_formats.py` resolves each published path
   through the campaign's own publish registry → content plan → this registry,
   and `build/publish_sharepoint.sh` calls it before the PUT.

**Fix it at both, and fix it everywhere at once.** Round 31 of that campaign
fixed the producer for the two assets the client had named and left the other
two alone; four days later a sweep found eight live files carrying the same
one-pixel defect. Fixing a rule only where it was noticed is how it stays broken
everywhere else.

---

## The frame is the ceiling; the quality inside it is yours to lose

A second question arrived the night after the format gate shipped: *"can we
improve png quality? text is pixelised."* The screenshot was a delivered card
at roughly 7x zoom.

Three separate answers, and only one of them was a defect.

### 1. The frame is right, and bigger is worse

**Instagram downsizes anything wider than 1080 px**, and **LinkedIn skips its
own resize only when you hit the recommended size exactly**. So 1080x1350 is
not a compromise to be escaped by uploading 1440 or 2160 — going bigger hands
the re-encode to someone else's resampler. The registry rows stand.

Consequence worth saying plainly to a client: **a 1080 px asset shows pixels
when you zoom into it, and nothing can be done about that** at the delivery
frame. If someone needs an asset that survives inspection — for print, for a
pitch deck, for a poster — that is a *different deliverable*, not a better
export.

### 2. Supersampling the rasterization does nothing — measured, and rejected

The obvious idea is to rasterize at 3x and downsample. It was tried and
**dropped**, because MuPDF already rasterizes glyphs with proper area-coverage
antialiasing. On the KVGO headline, edge-ramp quality at supersample 2x, 3x and
4x with a box filter was **identical to 1x** (soft/abrupt ratio 0.61 → 0.63).
Lanczos moves the number (1.04) by adding a sharpening halo, which is a
different look, not a better edge.

A measured scan across a stem confirms it directly: paper → **one** partial
pixel at 11% coverage → ink. That is correct antialiasing, not a defect.

*If someone proposes supersampling again, this is the measurement that says no.*

### 3. The real defect: lossless container, lossy content

Every card is a PNG. Every card's pixels had been through **two JPEG
generations**. Counting distinct colours in one flat brand-yellow patch of the
composed artwork:

| stage | distinct colours |
|---|---|
| the composed pixels, as drawn | **302** |
| after the background composer wrote them at `quality=88`, 4:2:0 | 61 |
| in the delivered PNG, after Chromium re-encoded them into the PDF | **18** |

Peak error reached **141 levels** on single pixels along the torn paper edges;
8x8 block boundaries were readable across fields that are one colour by design;
and the brand's paper-fibre grain — the thing that makes the mark look printed
— was almost entirely gone. Nothing reported any of it. The frame was right,
the extension was right, the file opened fine.

**Two independent losses, two independent fixes:**

1. **Ours.** A pre-composed background saved as JPEG. 4:2:0 halves chroma on
   both axes, which is the worst available choice for flat brand colour meeting
   paper white — that edge lives entirely in the chroma plane. Fixed: the
   composer's `save()` writes lossless PNG and **owns the container**, so a
   caller cannot select a codec by naming a file.
2. **The renderer's.** `render_pdf` is Chromium `page.pdf()`, which
   **re-encodes every embedded raster to JPEG 4:2:0 regardless of what you send
   it** — verified by sending the same background as a lossless PNG and reading
   `ext='jpeg'`, `subsampling=2` back out of the returned PDF. Fixing our
   composer alone recovers only about 7% of the total error.

### The rule this gives you

**A PNG deliverable that is rendered through a PDF is not a lossless
deliverable.** For a channel whose handover is images — every Instagram row in
the table above — the PDF is an intermediary, and rule 9 already says so for
format reasons. It costs quality for the same reason: it is a JPEG round-trip
with extra steps.

Where the deliverable is images, produce them **from the HTML directly**
(Playwright `page.screenshot()` at the exact viewport) rather than from the
rendered PDF. Measured on the same patch: **302 of 302 distinct colours
survive**, against 18 through the PDF.

The trade is real and must be stated, not hidden: a direct screenshot skips the
server-side brand gate, the font handling and the render audits that
`render_pdf` runs. **Do not switch a live asset's delivery path to bypass a
gate.** The right shape is for the render service to grow a lossless image
output; until it does, this is a finding with a number attached, not a licence.

### What is NOT worth building

A JPEG-blockiness detector on the delivered PNG was written, measured and
**deleted**. It cannot separate: the PDF path rescales 810pt → 1080px, a 4:3
ratio that smears JPEG's 8-pixel lattice to a 10.67-pixel period, so the
lattice signature is gone by the time the file exists. Measured range on known
bad files +0.058 to +0.222, on known good files -0.076 to +0.106 — overlapping.

A check that cannot separate is worse than no check, because it looks like
coverage. The enforceable seam is the **input** (the composer owns its
container), not forensics on the output.

### The classification must be declared, never inferred

A handover gate has to know what each file *is*. Deriving that from the filename
or the folder is how the gate ends up agreeing with the bug — a rule like "PDFs
in a B2C folder are review copies" would have made the original five-week
failure invisible to the very check meant to catch it.

So the campaign declares it in data, one path at a time, and **a path the gate
cannot classify is a finding, not a pass**. Every run prints what it checked,
what it skipped and why, and the totals reconcile against the number of
published files or the run reports itself broken.
