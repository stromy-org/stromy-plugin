#!/usr/bin/env python3
"""The channel x surface DELIVERY-FORMAT contract, and the gate that measures it.

WHY THIS MODULE EXISTS
----------------------
Phase 7 of this skill already validates a PLAN: `validate_posts.py` checks that
`media_spec.aspect_ratio` sits in the producer's Literal set before anything is
rendered. Nothing then checks the FILE. Between the renderer and the moment an
asset is handed to a client there was no seam that asked "is this the thing the
channel takes?", so a format rule could be written down, agreed by everyone,
repeated in two places, and violated by every build for five weeks.

That is not hypothetical. On the KVGO/indruk.nu campaign the rule "the final
Instagram deliverable is per-slide images (JPEG/PNG), not PDF" was decided on a
client call on 2026-08-17, written into the campaign briefing as rule 9 and into
its visual system's own B2C table row -- and every B2C asset was published to
the client as a PDF until the client asked for PNG by hand on 2026-09-21. The
rule was never wrong and nobody ever disagreed with it. It had no gate at the
seam where it applies, so it survived as prose while the builds shipped the
intermediary.

The generic lesson, and the whole design of this file: a delivery-FORMAT rule is
enforced where the file is PRODUCED or HANDED OVER, never where it is designed.
A rule with no measurement is a preference.

WHAT A ROW CARRIES, AND WHY
---------------------------
Modelled on stromy-org's `scripts/delivery_limits.py`, for the same reason it
was built: a bare number next to the code that needs it has no record of where
it came from, so a conservative internal choice becomes folklore and gets quoted
back as a platform requirement. Every row here therefore carries:

  * `kind`      -- does breaking this BLOCK, or is it a preference?
  * `evidence`  -- documented by the platform, decided by this engagement, or
                   unknown. `unknown` is not zero and never blocks.
  * `source`    -- the call, email, or first-party URL it came from.
  * `checked_on`-- the date a human last read that source.

The invariant that makes this worth the ceremony, asserted in
`validate_registry()`: **a row may only BLOCK if its evidence is `documented` or
`engagement`.** An inferred or community-reported number may warn; it may never
refuse a delivery. A gate that blocks on folklore gets switched off, and then it
gates nothing at all.

EITHER/OR IS FIRST-CLASS
------------------------
Two different "either this or that" shapes show up in real campaigns and a
registry that models neither pushes both back onto prose:

  1. **Either extension.** Instagram takes JPEG or PNG for a feed image. So
     `extensions` is an ordered tuple: every member is accepted, the first is
     what a producer should emit absent a reason.
  2. **Either SURFACE.** A content plan is allowed to leave a post's surface
     open -- the KVGO plan carries a literal `"document of carousel"` for
     b2b-w6-p1, because that choice belongs to the week it is built, not to the
     day the calendar was frozen. `resolve()` returns every candidate row and
     `check_file()` passes if the file satisfies ANY of them, then REPORTS WHICH
     ONE it satisfied. That report is how an open choice becomes a closed one:
     the delivered file is the decision, and it is written down by being made.

USAGE
-----
    python3 delivery_formats.py --markdown          # the table, generated
    python3 delivery_formats.py --check             # validate the registry
    python3 delivery_formats.py --verify instagram/carousel card1.png card2.png

    from delivery_formats import resolve, check_file, measure
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any, Literal

Kind = Literal["block", "warn", "advisory", "unknown"]
Evidence = Literal["documented", "engagement", "observed", "inferred", "unknown"]

# Every row that may BLOCK must carry one of these. See validate_registry().
BLOCKING_EVIDENCE = ("documented", "engagement")

# CSS reference pixel. A PDF page rect is in points; a page authored at 1080px
# CSS comes back as 810pt. This is the only conversion in the file and it is
# named rather than inlined, because getting it wrong turns every PDF row into a
# false failure.
PT_PER_PX = 72.0 / 96.0


@dataclass(frozen=True)
class Format:
    """One (channel, surface) delivery contract."""

    key: str                      # "instagram/carousel"
    channel: str
    surface: str
    extensions: tuple[str, ...]   # accepted, in preference order
    unit: str                     # what ONE file is: "card" | "post" | "page"
    pixels: tuple[int, int] | None = None   # exact frame, or None
    aspect: str | None = None     # "4:5" -- checked when `pixels` is None
    pages: tuple[int, int] | None = None    # (min, max) for paged formats
    duration_s: tuple[float, float] | None = None
    kind: Kind = "block"
    evidence: Evidence = "engagement"
    source: str = ""
    checked_on: str | None = None
    note: str = ""

    @property
    def blocking(self) -> bool:
        return self.kind == "block" and self.evidence in BLOCKING_EVIDENCE


# --------------------------------------------------------------------------- registry
#
# SCOPE NOTE. The rows below are the ones this skill has actually delivered
# against and can therefore defend. Their `evidence` says which kind of fact
# each one is, and that distinction is the point:
#
#   `engagement` -- THIS campaign decided it, on a call or in an email. It is
#                   binding on this campaign and on nothing else. Most rows are
#                   this, and that is correct: 1080x1350 is not a platform
#                   requirement, it is the frame the work was designed in, and a
#                   file that is not the frame it was designed in has been
#                   resampled or cropped by something nobody reviewed.
#   `documented` -- a first-party platform statement, with a URL and a date.
#   `unknown`    -- we have not checked. Carries NO number and never blocks.
#
# Adding a channel means adding a row, not editing a build script.

FORMATS: tuple[Format, ...] = (
    # ---------------------------------------------------------------- instagram
    Format(
        key="instagram/carousel",
        channel="instagram", surface="carousel",
        extensions=(".png", ".jpg", ".jpeg"),
        unit="card",
        pixels=(1080, 1350),
        kind="block", evidence="engagement",
        source="KVGO client call 2026-08-17 (briefing rule 9); restated by "
               "Emma van Gelder 2026-09-21: 'can we have the output as 3 "
               "separate cards and as png files?'",
        checked_on="2026-09-21",
        note="ONE FILE PER CARD. A multi-page PDF is an internal review "
             "artifact here and is never the handover. Every card in one "
             "carousel must share the frame exactly -- Instagram crops the "
             "whole set to the first card's aspect, so a single odd card "
             "silently crops its siblings.",
    ),
    Format(
        key="instagram/image",
        channel="instagram", surface="image",
        extensions=(".png", ".jpg", ".jpeg"),
        unit="post",
        pixels=(1080, 1350),
        kind="block", evidence="engagement",
        source="Same decision as instagram/carousel; a beeldpost is a "
               "one-card carousel as far as the frame is concerned.",
        checked_on="2026-09-21",
        note="Named after the post, never '-card1': a single image has no "
             "card number, and a file called card1 invites the question "
             "where card 2 is.",
    ),
    Format(
        key="instagram/reel",
        channel="instagram", surface="reel",
        extensions=(".mp4",),
        unit="post",
        pixels=(1080, 1920),
        duration_s=(5.0, 90.0),
        kind="block", evidence="engagement",
        source="Campaign briefing, Tooling section: 'Instagram reels 9:16 "
               "(1080x1920)'. The duration band is this campaign's own: the "
               "plan specs 15-20s motion graphics.",
        checked_on="2026-09-21",
        note="Burned-in captions are mandatory on this campaign (most "
             "viewing is muted), which is a CONTENT gate, not a format one "
             "-- see the per-asset OCR verifier, not this table.",
    ),
    Format(
        key="instagram/story",
        channel="instagram", surface="story",
        extensions=(".mp4", ".png", ".jpg"),
        unit="post",
        pixels=(1080, 1920),
        kind="warn", evidence="inferred",
        source="Not used on any delivered asset to date; the 9:16 frame is "
               "carried over from the reel row rather than checked.",
        checked_on=None,
        note="WARNS, never blocks: inferred evidence may not refuse a "
             "delivery. Promote to `engagement` the first time a story is "
             "actually specced, and put the decision in `source`.",
    ),
    # ----------------------------------------------------------------- linkedin
    Format(
        key="linkedin/document",
        channel="linkedin", surface="document",
        extensions=(".pdf",),
        unit="post",
        pixels=(1080, 1350),
        pages=(2, 20),
        kind="block", evidence="engagement",
        source="Campaign briefing, Tooling section: 'LinkedIn carousel "
               "documents: PDF pages at 1080x1350 (4:5)'.",
        checked_on="2026-09-21",
        note="THE ONE PLACE PDF IS THE DELIVERABLE, not an intermediary. "
             "A page rect is measured in points and compared at "
             "PT_PER_PX with a half-point tolerance: a page authored at "
             "1080x1350 CSS comes back as 810x1012.5pt and Chromium rounds "
             "it to 1013, which is not a defect.",
    ),
    Format(
        key="linkedin/carousel",
        channel="linkedin", surface="carousel",
        extensions=(".pdf",),
        unit="post",
        pixels=(1080, 1350),
        pages=(2, 20),
        kind="block", evidence="engagement",
        source="Same as linkedin/document. On LinkedIn a 'carousel' IS a "
               "document post; the two plan words name one surface.",
        checked_on="2026-09-21",
        note="Kept as its own key so a plan that says 'carousel' resolves "
             "without a human translating it first.",
    ),
    Format(
        key="linkedin/image",
        channel="linkedin", surface="image",
        extensions=(".png", ".jpg", ".jpeg"),
        unit="post",
        pixels=(1080, 1350),
        kind="block", evidence="engagement",
        source="VISUAL-SYSTEM.md B2B column: 'PDF (document post) or PNG "
               "one-pager'. The one-pagers are authored at 1080x1350.",
        checked_on="2026-09-21",
        note="The PNG is the deliverable; a PDF beside it is the review "
             "copy. Both may be published, only the PNG is the post.",
    ),
    Format(
        key="linkedin/infographic",
        channel="linkedin", surface="infographic",
        extensions=(".png", ".jpg", ".jpeg"),
        unit="post",
        pixels=(1080, 1350),
        kind="block", evidence="engagement",
        source="Same as linkedin/image: the plan's 'infographic' is a "
               "single-image post whose content happens to be a data "
               "graphic.",
        checked_on="2026-09-21",
        note="",
    ),
    Format(
        key="linkedin/video",
        channel="linkedin", surface="video",
        extensions=(".mp4",),
        unit="post",
        pixels=None, aspect="4:5",
        kind="warn", evidence="inferred",
        source="No LinkedIn video has been delivered on this skill yet.",
        checked_on=None,
        note="WARNS only. Aspect rather than an exact frame, because no "
             "engagement has chosen one.",
    ),
    # -------------------------------------------------------------------- print
    Format(
        key="print/leavebehind",
        channel="print", surface="leavebehind",
        extensions=(".pdf",),
        unit="post",
        pixels=None, aspect="A4",
        pages=(1, 12),
        kind="block", evidence="engagement",
        source="Campaign briefing, Tooling section: 'A4 portrait for the B2B "
               "leave-behind documents'.",
        checked_on="2026-09-21",
        note="A4 portrait is 595x842pt. Landscape A4 is a DIFFERENT thing "
             "and fails here on purpose -- a leave-behind that opens "
             "sideways was not designed as a leave-behind.",
    ),
    # ------------------------------------------------------------------ internal
    Format(
        key="internal/review",
        channel="internal", surface="review",
        extensions=(".pdf", ".png", ".jpg", ".mp4", ".docx", ".xlsx", ".pptx"),
        unit="post",
        kind="advisory", evidence="engagement",
        source="Briefing rule 9: 'PDF stays an internal-review/intermediary "
               "format only'.",
        checked_on="2026-09-21",
        note="THE ESCAPE HATCH, and it is deliberately explicit. Anything "
             "routed here is declared NOT to be a channel deliverable, so "
             "nothing about it is measured. A file lands here because "
             "someone said so in data, never because the resolver could not "
             "work out what it was -- an unresolved file is reported as "
             "unresolved, which is the finding.",
    ),
)

BY_KEY: dict[str, Format] = {f.key: f for f in FORMATS}

# Plan vocabulary -> surface. The left-hand side is what a `content-plan.json`
# actually says, including the Dutch words and the open choices; the right-hand
# side is this registry's vocabulary. Keep the raw strings verbatim: a plan is
# a client-facing artifact and is not rewritten to suit a lookup table.
SURFACE_ALIASES: dict[str, tuple[str, ...]] = {
    "carousel": ("carousel",),
    "document": ("document",),
    "infographic": ("infographic",),
    "image": ("image",),
    "single-image post": ("image",),
    "beeldpost": ("image",),
    "reel": ("reel",),
    "animatie": ("reel",),          # a motion graphic ships as a reel
    "animation": ("reel",),
    "video": ("reel",),
    "story": ("story",),
    # --- the open choices: every candidate, in the plan's own order ---
    "document of carousel": ("document", "carousel"),
    "document or carousel": ("document", "carousel"),
    "carousel of document": ("carousel", "document"),
}


class Unresolved(Exception):
    """The plan named a surface this registry does not know.

    Raised rather than defaulted, on purpose. A resolver that quietly picks a
    plausible row turns an unknown surface into a silent pass, which is the
    exact failure this module exists to stop.
    """


def resolve(channel: str, plan_format: str) -> list[Format]:
    """(channel, plan word) -> every format row that could satisfy it.

    Returns a LIST because a plan is allowed to leave the surface open. One
    entry means the choice is closed; several mean the delivered file decides.
    """
    word = " ".join(plan_format.strip().lower().split())
    surfaces = SURFACE_ALIASES.get(word)
    if surfaces is None:
        raise Unresolved(
            f"content plan says format {plan_format!r}, which is not in "
            f"SURFACE_ALIASES. Add it there with the surface(s) it means -- do "
            f"not rename it in the plan to fit this table.")
    rows = [BY_KEY[f"{channel}/{s}"] for s in surfaces if f"{channel}/{s}" in BY_KEY]
    if not rows:
        raise Unresolved(
            f"no row for channel {channel!r} x surface(s) {surfaces}. Add a "
            f"Format() for it with its evidence, or route the file to "
            f"internal/review explicitly.")
    return rows


# ------------------------------------------------------------------- measurement


@dataclass
class Measurement:
    path: str
    ext: str
    pixels: tuple[int, int] | None = None
    pages: int | None = None
    duration_s: float | None = None
    points: tuple[float, float] | None = None
    error: str | None = None
    # INCONCLUSIVE IS NOT WRONG. If the reader itself is missing -- no ffprobe
    # on this PATH, no Pillow in this interpreter -- we have learned nothing
    # about the file, and reporting that as a format failure is the exact
    # anti-pattern this campaign already hit once: publish_sharepoint.sh used
    # to print a confident MISMATCH whenever its readback came back as an auth
    # error, which trains everyone to wave the failure through, and the day it
    # fires for real it is ignored. So an unavailable reader sets this flag,
    # the file is reported UNMEASURED, and the run is not green.
    unmeasurable: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


def measure(path: str) -> Measurement:
    """Read a produced file's real geometry. Never trusts a render result.

    The heavy readers are imported lazily so this module stays importable (and
    `--markdown`/`--check` stay runnable) on a machine with none of them.
    """
    ext = os.path.splitext(path)[1].lower()
    m = Measurement(path=path, ext=ext)
    if not os.path.exists(path):
        m.error = "file does not exist"
        return m
    try:
        if ext in (".png", ".jpg", ".jpeg"):
            from PIL import Image
            with Image.open(path) as im:
                m.pixels = (im.width, im.height)
        elif ext == ".pdf":
            import pymupdf
            with pymupdf.open(path) as doc:
                m.pages = doc.page_count
                r = doc[0].rect
                m.points = (round(r.width, 2), round(r.height, 2))
                m.pixels = (round(r.width / PT_PER_PX), round(r.height / PT_PER_PX))
        elif ext == ".mp4":
            out = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height:format=duration",
                 "-of", "json", path],
                capture_output=True, text=True, check=True).stdout
            j = json.loads(out)
            s = j["streams"][0]
            m.pixels = (int(s["width"]), int(s["height"]))
            m.duration_s = round(float(j["format"]["duration"]), 2)
    except FileNotFoundError as exc:
        # The FILE's own absence is checked above, so this is the READER's:
        # ffprobe is not on PATH.
        m.unmeasurable = (f"the reader is not available ({exc.filename or exc}); "
                          f"install it or run this where it exists")
    except ImportError as exc:
        m.unmeasurable = f"the reader is not importable ({exc})"
    except Exception as exc:  # noqa: BLE001 - any other reader failure is a finding
        m.error = f"{type(exc).__name__}: {exc}"
    return m


def _aspect_ok(pixels: tuple[int, int], aspect: str) -> bool:
    if aspect == "A4":
        # compared in POINTS by the caller; here we only see px
        w, h = pixels
        return abs(w / h - 595 / 842) < 0.01
    a, b = (float(x) for x in aspect.split(":"))
    w, h = pixels
    return abs(w / h - a / b) < 0.01


@dataclass
class Result:
    path: str
    satisfied: str | None            # the key it matched, if any
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    measurement: dict[str, Any] = field(default_factory=dict)
    unmeasured: str | None = None

    @property
    def ok(self) -> bool:
        """Passing means MEASURED AND CLEAN. `unmeasured` is neither."""
        return not self.failures and not self.unmeasured


def _check_one(fmt: Format, m: Measurement) -> list[str]:
    """Every way this one file fails this one row. Empty list means it passes."""
    bad: list[str] = []
    if m.error:
        return [m.error]
    if m.unmeasurable:
        return []  # handled by check_file, which reports it as UNMEASURED
    if fmt.extensions and m.ext not in fmt.extensions:
        bad.append(f"extension {m.ext} is not one of {', '.join(fmt.extensions)}")
    if fmt.pixels and m.pixels and tuple(m.pixels) != tuple(fmt.pixels):
        want = f"{fmt.pixels[0]}x{fmt.pixels[1]}"
        got = f"{m.pixels[0]}x{m.pixels[1]}"
        if m.ext == ".pdf" and m.points:
            # Half a point of rounding on a page rect is Chromium, not a defect.
            wpt, hpt = fmt.pixels[0] * PT_PER_PX, fmt.pixels[1] * PT_PER_PX
            if abs(m.points[0] - wpt) <= 0.6 and abs(m.points[1] - hpt) <= 0.6:
                return bad
        bad.append(f"frame is {got}, the format is {want}")
    if fmt.pixels is None and fmt.aspect and m.pixels:
        if fmt.aspect == "A4" and m.points:
            if not (abs(m.points[0] - 595) <= 2 and abs(m.points[1] - 842) <= 2):
                bad.append(f"page is {m.points[0]:.0f}x{m.points[1]:.0f}pt, "
                           f"A4 portrait is 595x842pt")
        elif not _aspect_ok(tuple(m.pixels), fmt.aspect):
            bad.append(f"aspect is {m.pixels[0]}:{m.pixels[1]}, "
                       f"the format is {fmt.aspect}")
    if fmt.pages and m.pages is not None and not (fmt.pages[0] <= m.pages <= fmt.pages[1]):
        bad.append(f"{m.pages} pages, the format takes {fmt.pages[0]}-{fmt.pages[1]}")
    if fmt.duration_s and m.duration_s is not None:
        lo, hi = fmt.duration_s
        if not (lo <= m.duration_s <= hi):
            bad.append(f"runs {m.duration_s:.1f}s, the format takes {lo:g}-{hi:g}s")
    return bad


def check_file(path: str, candidates: list[Format]) -> Result:
    """Measure one file against every candidate row; pass on ANY of them.

    With one candidate this is an ordinary check. With several -- the open
    `document of carousel` case -- passing is also a RECORD: `satisfied` names
    the row the file chose, which is how the plan's open question gets its
    answer written down.
    """
    m = measure(path)
    res = Result(path=path, satisfied=None, measurement=m.as_dict())
    if m.unmeasurable:
        res.unmeasured = m.unmeasurable
        res.warnings.append(
            f"NOT MEASURED against {candidates[0].key}: {m.unmeasurable}. "
            f"This is not a pass -- nothing was checked.")
        return res
    per_row: list[tuple[Format, list[str]]] = []
    for fmt in candidates:
        bad = _check_one(fmt, m)
        if not bad:
            res.satisfied = fmt.key
            if fmt.kind == "advisory":
                res.warnings.append(f"{fmt.key}: not measured (advisory row)")
            return res
        per_row.append((fmt, bad))

    # Nothing matched. A row may only REFUSE if its evidence permits it;
    # everything else is reported as a warning and the file passes.
    for fmt, bad in per_row:
        line = f"{fmt.key}: " + "; ".join(bad)
        (res.failures if fmt.blocking else res.warnings).append(line)
    if not res.failures and per_row:
        res.satisfied = per_row[0][0].key
    return res


def check_set(paths: list[str], candidates: list[Format]) -> list[Result]:
    """Check files that ship together, plus the rules that are about the SET.

    A per-file loop cannot see the one that bites hardest in practice: a
    carousel whose cards disagree with each other. Instagram crops the whole
    set to the first card's aspect, so one odd card silently crops its
    siblings, and every individual card can still be a perfectly valid image.
    """
    results = [check_file(p, candidates) for p in paths]
    frames = {tuple(r.measurement.get("pixels") or ()) for r in results
              if not r.unmeasured}
    frames.discard(())
    if len(frames) > 1 and any(c.unit == "card" for c in candidates):
        shown = ", ".join(f"{w}x{h}" for w, h in sorted(frames))
        for r in results:
            r.failures.append(
                f"the cards in this set do not share one frame ({shown}); "
                f"the channel crops the whole set to the first card")
    return results


# -------------------------------------------------------------------- registry QA


def validate_registry() -> list[str]:
    """The invariants that keep this table honest. Run in CI and by --check."""
    problems: list[str] = []
    seen: set[str] = set()
    for f in FORMATS:
        if f.key in seen:
            problems.append(f"{f.key}: duplicate key")
        seen.add(f.key)
        if f.key != f"{f.channel}/{f.surface}":
            problems.append(f"{f.key}: key does not match channel/surface")
        if f.kind == "block" and f.evidence not in BLOCKING_EVIDENCE:
            problems.append(
                f"{f.key}: kind='block' with evidence={f.evidence!r}. Only "
                f"{BLOCKING_EVIDENCE} may refuse a delivery -- a gate that "
                f"blocks on folklore gets switched off and then gates nothing.")
        if not f.source:
            problems.append(f"{f.key}: no source. Every row says where it came from.")
        if f.evidence in BLOCKING_EVIDENCE and not f.checked_on:
            problems.append(f"{f.key}: evidence={f.evidence!r} with no checked_on date")
        if f.evidence == "unknown" and (f.pixels or f.aspect or f.pages or f.duration_s):
            problems.append(
                f"{f.key}: evidence='unknown' but carries a number. Unknown is "
                f"not zero and is not a measurement.")
        if f.pixels and f.aspect:
            problems.append(f"{f.key}: has both an exact frame and an aspect; pick one")
    for word, surfaces in SURFACE_ALIASES.items():
        for s in surfaces:
            if not any(f.surface == s for f in FORMATS):
                problems.append(f"alias {word!r} -> surface {s!r}, which no row defines")
    return problems


def markdown() -> str:
    rows = ["| key | takes | one file per | frame | pages / length | severity | evidence |",
            "|---|---|---|---|---|---|---|"]
    for f in FORMATS:
        frame = (f"{f.pixels[0]}x{f.pixels[1]}" if f.pixels
                 else (f.aspect or "--"))
        extent = "--"
        if f.pages:
            extent = f"{f.pages[0]}-{f.pages[1]} pages"
        if f.duration_s:
            extent = f"{f.duration_s[0]:g}-{f.duration_s[1]:g}s"
        sev = "**blocks**" if f.blocking else f.kind
        rows.append(f"| `{f.key}` | {', '.join(f.extensions) or 'any'} | {f.unit} "
                    f"| {frame} | {extent} | {sev} | {f.evidence} |")
    rows.append("")
    rows.append("Open choices a content plan may carry, and what they resolve to:")
    rows.append("")
    rows.append("| plan says | candidates |")
    rows.append("|---|---|")
    for word, surfaces in SURFACE_ALIASES.items():
        if len(surfaces) > 1:
            rows.append(f"| `{word}` | {', '.join(surfaces)} -- "
                        f"the delivered file decides, and the check records which |")
    return "\n".join(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--markdown", action="store_true", help="print the table")
    ap.add_argument("--json", action="store_true", help="print the registry as JSON")
    ap.add_argument("--check", action="store_true", help="validate the registry itself")
    ap.add_argument("--verify", metavar="CHANNEL/SURFACE",
                    help="check FILES against this row (or a plan word, e.g. "
                         "'linkedin/document of carousel')")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()

    if a.markdown:
        print(markdown())
        return 0
    if a.json:
        print(json.dumps([f.__dict__ for f in FORMATS], indent=1, default=list))
        return 0
    if a.check:
        problems = validate_registry()
        for p in problems:
            print("FAIL", p)
        print("registry OK" if not problems else f"{len(problems)} problem(s)")
        return 1 if problems else 0
    if a.verify:
        channel, _, word = a.verify.partition("/")
        try:
            cands = resolve(channel, word)
        except Unresolved as exc:
            print("UNRESOLVED", exc)
            return 2
        results = check_set(a.files, cands)
        bad = 0
        for r in results:
            tag = "OK  " if r.ok else "FAIL"
            geom = r.measurement.get("pixels")
            geom = f"{geom[0]}x{geom[1]}" if geom else "?"
            print(f"{tag} {geom:>11s}  {os.path.basename(r.path)}"
                  + (f"  [{r.satisfied}]" if r.satisfied else ""))
            for f_ in r.failures:
                print("       FAIL", f_)
                bad += 1
            for w in r.warnings:
                print("       warn", w)
        return 1 if bad else 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
