# Print-ready business cards (PDF/X-1a)

Each `*-eu-print.pdf` is a press deliverable: 2-page (front + back), EU 85×55 mm
trim, 3 mm bleed, crop marks, CMYK, fonts embedded, PDF/X-1a:2003.

| Card | Holder | Role |
|------|--------|------|
| `william-eu-print.pdf`  | William Masquelier | Founder |
| `corentin-eu-print.pdf` | Corentin Merlé     | Founder |

Shared back: `../source/back-eu.svg` (Stromy lockup + "Intelligence, orchestrated.").

## How it's built

From `client-data/clients/stromy/`, run the brand-builder converter on the vector
sources in `../source/`:

```bash
python <stromy-org>/.claude/skills/brand-builder/scripts/build-card-print-pdf.py \
    --front business-cards/source/william-eu-front.svg \
    --back  business-cards/source/back-eu.svg \
    --size eu --icc-target eu \
    --out business-cards/print/william-eu-print.pdf
```

The **`source/` SVGs are the editable master** — change the design there and
re-run the command to regenerate the PDF. Repeat per holder (swap the `--front`
and `--out`).

## ⚠️ Profile provenance — re-render before sending to a printer

The committed PDFs were rendered with the macOS **Generic CMYK** profile as a
proof — they are valid PDF/X-1a but **not colour-accurate for a press**. For
production, drop the EU press profile `PSOcoated_v3.icc` (FOGRA51, from eci.org)
into `<stromy-org>/.claude/skills/brand-builder/assets/icc/` and re-run with
`--icc-target eu`. Always confirm the standard/profile the chosen print house
prefers.

Phone numbers are placeholders (`+61 (0) — — —`) — fill in before printing.

Requires `brew install librsvg ghostscript` (native tools, operator-local).
