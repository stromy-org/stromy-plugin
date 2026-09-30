# Company Data Schema Reference

This reference documents the company data schemas used by the proposal skill. There are two layouts — the **deployed-plugin overlay** (what the skill reads at runtime in a client plugin) and the **canonical client-data** layout (operator-side source of truth, not accessible from deployed plugins).

## Deployed-Plugin Overlay (`companies/{client_slug}/`)

This is the layout the skill reads. `company_context.json` is the single source of company facts for deployed skills — `profile.json` and `people.json` are not present in public plugin overlays.

```
companies/{client_slug}/
├── company_context.json   # Redacted public company facts (replaces profile.json + people.json)
├── charter.json           # Visual identity (colors, fonts, logos, format settings)
├── logos/                 # Logo files referenced by charter
└── proposals/
    ├── case-studies.json
    ├── team-bios.json
    ├── methodologies.json
    ├── boilerplate.json
    ├── testimonials.json
    ├── differentiators.json
    └── partnerships.json
```

## Canonical Client-Data Layout (operator-side only)

> **Operator environment only.** The paths below exist in `client-data/clients/<company-name>/` on operator infrastructure. Deployed plugins have no `client-data/` directory — do NOT reference these paths in deployed skills.

```
client-data/clients/<company-name>/
├── profile.json          # Full company identity, services, pricing, credentials, legal (incl. PII)
├── people.json           # Full people registry — contact details, roles (incl. email, phone)
├── company_context.json  # Generated redacted export — distributed to plugin overlays
├── charter.json          # Visual identity
└── proposals/
    └── ...
```

## company_context.json

Redacted public company facts distributed to deployed plugin overlays. `schemaVersion: 1`.

### `company` (required)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Trading name |
| `legalName` | string | Legal entity name |
| `displayName` | string | Display name (marketing) |
| `shortName` | string | Abbreviated name |
| `description` | string | 2-3 sentence company description |
| `tagline` | string | One-line value proposition |
| `website` | string | Company website URL |
| `founded` | number | Year founded |
| `industry` | string | Primary industry |
| `headquarters.city` | string | City |
| `headquarters.region` | string | State / province |
| `headquarters.country` | string | Country |
| `services[]` | array | Services offered (id, name, description, industries, deliverables, typicalDuration, pricingModel) |
| `industries[]` | string[] | Industries served |
| `businessLines[]` | string[] | Business line categories |
| `positioning` | string | Strategic positioning statement |
| `values[]` | string[] | Company values |
| `stats` | object | Public metrics (key → value) |
| `publicContact.website` | string | Public website URL |
| `publicContact.email` | string | Public contact email |
| `publicContact.press` | string | Press / media contact (optional) |
| `publicContact.linkedin` | string | LinkedIn URL (optional) |

### `credentials` (optional)

Array or object with `certifications[]`, `awards[]`, `memberships[]` — same structure as `profile.json` credentials but limited to public-facing entries.

### `pricing` (optional)

| Field | Type | Description |
|-------|------|-------------|
| `publicModels[]` | array | Publicly shareable pricing models (id, name, description, rates?) |
| `paymentTerms` | string | Payment terms (e.g., "Net 30") |
| `discounts` | array | Publicly available discount types |

### `legal` (optional)

| Field | Type | Description |
|-------|------|-------------|
| `publicTerms` | object or array | Standard public engagement terms: `ip`, `confidentiality`, `liability`, `termination` |
| `insurances[]` | array | Insurance types (optional) |

### `people[]` (optional)

Public people profiles for document authoring and contact sections.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Shared ID (links to `team-bios.json`) |
| `name` | string | Full name |
| `title` | string | Job title |
| `publicRole` | string | Functional role label (e.g., `"author"`, `"spokesperson"`) |
| `publicBio` | string | Short public biography |
| `quoteStyle` | string | Preferred quote attribution format (optional) |

> **PII note:** `company_context.json` intentionally omits banking details, registration/VAT/KVK numbers, billing email, personal email, and personal phone. Those remain in canonical `profile.json` and `people.json` on the operator side and are **never distributed to deployed plugins**.

### `redactions[]`

Array of field-path strings documenting what was redacted from the canonical source (informational only).

---

## profile.json (operator-side only)

> **Operator environment only.** Not present in deployed plugin overlays.

Top-level company identity and operational data.

### `company` (required)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Legal or trading name |
| `tagline` | string | One-line value proposition |
| `description` | string | 2-3 sentence company description |
| `founded` | number | Year founded |
| `headquarters.city` | string | City name |
| `headquarters.country` | string | Country name |
| `website` | string | Company website URL |
| `email` | string | Proposals/contact email |
| `phone` | string | Main phone number |

### `services[]` (required)

Array of services the company offers.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., `"svc-001"`) |
| `name` | string | Service name |
| `description` | string | What the service includes |
| `industries` | string[] | Target industries |
| `deliverables` | string[] | Typical outputs |
| `typicalDuration` | string | Expected engagement length |
| `pricingModel` | string | Reference to `pricing.models[].id` |

### `pricing` (required)

| Field | Type | Description |
|-------|------|-------------|
| `models[]` | array | Available pricing models |
| `models[].id` | string | Unique identifier (e.g., `"price-001"`) |
| `models[].name` | string | Model name (e.g., "Time & Materials", "Fixed Fee") |
| `models[].rates[]` | array | Rate card (for T&M models) |
| `models[].rates[].role` | string | Role title |
| `models[].rates[].amount` | number | Rate amount |
| `models[].rates[].currency` | string | Currency code |
| `models[].rates[].per` | string | Rate unit (e.g., "hour", "day") |
| `models[].description` | string | Description for non-rate models |
| `paymentTerms` | string | Payment terms (e.g., "Net 30") |
| `discounts[]` | array | Available discounts |
| `discounts[].type` | string | Discount trigger |
| `discounts[].description` | string | Discount details |

### `credentials` (optional)

| Field | Type | Description |
|-------|------|-------------|
| `certifications[]` | array | Formal certifications |
| `certifications[].name` | string | Certification name |
| `certifications[].issuer` | string | Issuing body |
| `certifications[].validTo` | string | Expiry date (YYYY-MM) |
| `awards[]` | array | Awards and recognitions |
| `awards[].name` | string | Award name |
| `awards[].issuer` | string | Awarding body |
| `awards[].year` | number | Year awarded |
| `memberships[]` | array | Professional memberships |
| `memberships[].organization` | string | Organization name |
| `memberships[].status` | string | Membership status |

### `legal` (optional)

| Field | Type | Description |
|-------|------|-------------|
| `standardTerms.ip` | string | IP ownership terms |
| `standardTerms.confidentiality` | string | Confidentiality provisions |
| `standardTerms.liability` | string | Liability limitations |
| `standardTerms.termination` | string | Termination provisions |
| `insurances[]` | array | Insurance coverage |
| `insurances[].type` | string | Insurance type |
| `insurances[].coverage` | number | Coverage amount |
| `insurances[].currency` | string | Currency code |

---

## brand/charter.json

Unified visual identity covering all output formats.

### `colors` (required)

| Field | Type | Description |
|-------|------|-------------|
| `primary` | string | Primary brand color (hex) — headings, accents |
| `secondary` | string | Secondary color (hex) — subheadings, borders |
| `accent` | string | Accent color (hex) — highlights, CTAs |
| `background` | string | Background color (hex) |
| `backgroundAlt` | string | Alternate background (hex) — tables, cards |
| `text` | string | Primary text color (hex) |
| `textLight` | string | Secondary text color (hex) |
| `success` | string | Success/positive color (hex) |
| `warning` | string | Warning color (hex) |
| `error` | string | Error/negative color (hex) |

### `fonts` (required)

| Field | Type | Description |
|-------|------|-------------|
| `heading.family` | string | Heading font (must be web-safe for PPTX) |
| `heading.fallback` | string | Fallback font stack |
| `heading.weight` | string | Font weight |
| `body.family` | string | Body font |
| `body.fallback` | string | Fallback font stack |
| `body.weight` | string | Font weight |
| `mono.family` | string | Monospace font |
| `mono.fallback` | string | Fallback font stack |
| `mono.weight` | string | Font weight |

### `logo` (required)

| Field | Type | Description |
|-------|------|-------------|
| `primary` | string | Primary logo filename (relative to `brand/`) |
| `white` | string | White/reversed logo filename |
| `icon` | string | Icon/favicon (optional) |
| `maxWidth` | string | Maximum logo width (e.g., "120pt") |
| `maxHeight` | string | Maximum logo height (e.g., "50pt") |

### `document` (optional — DOCX-specific)

| Field | Type | Description |
|-------|------|-------------|
| `margins.top` | string | Top margin (e.g., "1in") |
| `margins.bottom` | string | Bottom margin |
| `margins.left` | string | Left margin |
| `margins.right` | string | Right margin |
| `header.content` | string | Header template (supports `{{company.name}}`, `{{project.title}}`) |
| `header.logo` | boolean | Show logo in header |
| `footer.content` | string | Footer text (e.g., "Confidential") |
| `footer.pageNumbers` | boolean | Show page numbers in footer |
| `headingColor` | string | Key from `colors` to use for headings (e.g., "primary") |
| `tableHeaderColor` | string | Key from `colors` for table headers |

### `presentation` (optional — PPTX-specific)

| Field | Type | Description |
|-------|------|-------------|
| `slideMargin` | string | Slide content margin |
| `titleMargin` | string | Title area margin |
| `contentMargin` | string | Content area margin |
| `aspectRatio` | string | Aspect ratio (e.g., "16:9", "4:3") |

### `video` (optional — `format-video-hd`/`render_video`)

| Field | Type | Description |
|-------|------|-------------|
| `resolution` | string | Video resolution (e.g., "1920x1080") |
| `fps` | number | Frames per second |

---

## people.json (operator-side only)

> **Operator environment only.** Not present in deployed plugin overlays — use `company_context.json` → `people[]` instead.

Top-level people registry — structured contact and role data for document authoring, spokesperson selection, and approval workflows. Links to `team-bios.json` (rich narrative bios) and `spokespersons.json` (quote style, topic expertise) via shared `id`.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `id` | Yes | string | Shared with `team-bios.json` and `spokespersons.json` |
| `name` | Yes | string | Full name |
| `title` | Yes | string | Job title |
| `email` | Yes | string | Direct email |
| `phone` | No | string | Direct phone |
| `roles` | Yes | string[] | `"author"`, `"spokesperson"`, `"approver"`, `"mediaContact"` |
| `default` | No | boolean | Auto-select for document authoring if `true` |

### Author Discovery (deployed plugin)

1. Check `company_context.json` → `people[]` → filter by `publicRole` containing `"author"`
2. Exactly one matching person → auto-select, confirm with user
3. Multiple matches, none unambiguously default → ask user
4. No people with `publicRole: "author"` → ask user to provide "Prepared by" details manually

---

## proposals/case-studies.json

Array of past performance case studies.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., `"CS-001"`) |
| `title` | string | Case study title |
| `client.name` | string | Client name (or "Confidential") |
| `client.industry` | string | Client's industry |
| `client.namePublic` | boolean | Whether the client name can be used publicly |
| `tags` | string[] | Searchable tags for matching |
| `challenge` | string | Client's challenge/problem statement |
| `approach` | string | What the firm did |
| `results.summary` | string | Overall results narrative |
| `results.metrics[]` | array | Quantified outcomes |
| `results.metrics[].measure` | string | What was measured |
| `results.metrics[].value` | number | Numeric value |
| `results.metrics[].unit` | string | Unit of measurement |
| `timeframe.start` | string | Start date (YYYY-MM) |
| `timeframe.end` | string | End date (YYYY-MM) |
| `budget` | string | Engagement budget (free text) |
| `team` | string[] | References to `team-bios.json` → `[].id` |
| `services` | string[] | References to `company_context.json` → `company.services[].id` |
| `short` | string | 50-word version for inline references |
| `long` | string | 500-word version for dedicated sections |
| `lastReviewed` | string | Date last reviewed (YYYY-MM) — optional, for content freshness tracking |

---

## proposals/team-bios.json

Array of key personnel with role-variant biographies.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., `"person-001"`) |
| `name` | string | Full name |
| `title` | string | Job title |
| `photo` | string | Photo path (relative to company dir) |
| `expertise` | string[] | Expertise tags for matching |
| `certifications[]` | array | Professional certifications |
| `certifications[].name` | string | Certification name |
| `certifications[].issuer` | string | Issuing body |
| `certifications[].current` | boolean | Is certification current |
| `education[]` | array | Educational background |
| `education[].degree` | string | Degree name |
| `education[].institution` | string | Institution name |
| `yearsExperience` | number | Total years of relevant experience |
| `executive` | string | Executive-audience bio (2-3 sentences, emphasis on business impact) |
| `technical` | string | Technical-audience bio (2-3 sentences, emphasis on skills and tools) |
| `short` | string | One-line bio for tables and lists |
| `lastReviewed` | string | Date last reviewed (YYYY-MM) — optional, for content freshness tracking |

### Bio Variant Selection

- **Executive audience** → use `executive` bio in Team & Qualifications section
- **Technical audience** → use `technical` bio
- **Condensed format** → use `short` bio

---

## proposals/methodologies.json

Array of standard approaches and frameworks.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., `"meth-001"`) |
| `name` | string | Methodology name |
| `tags` | string[] | Searchable tags |
| `summary` | string | One-sentence description |
| `phases[]` | array | Methodology phases |
| `phases[].name` | string | Phase name |
| `phases[].description` | string | Phase activities and outputs |
| `differentiators` | string[] | What makes this approach unique |
| `applicableServices` | string[] | References to `company_context.json` → `company.services[].id` |
| `lastReviewed` | string | Date last reviewed (YYYY-MM) — optional, for content freshness tracking |

---

## proposals/boilerplate.json

Reusable text blocks for standard proposal sections.

### `assumptions[]`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `category` | string | Category (General, Travel, Technical, etc.) |
| `text` | string | Assumption text |

### `disclaimers[]`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `category` | string | Category (Projection, Scope, Third Party, etc.) |
| `text` | string | Disclaimer text |

### `legalTerms[]`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `category` | string | Category (IP, Confidentiality, Liability, etc.) |
| `title` | string | Term title |
| `text` | string | Full legal text |

---

## proposals/testimonials.json

Array of client quotes and references.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `quote` | string | The testimonial quote |
| `attribution` | string | Who said it (title + company) |
| `caseStudy` | string | Reference to `case-studies.json` → `[].id` |
| `tags` | string[] | Searchable tags |
| `year` | number | Year of testimonial |
| `lastReviewed` | string | Date last reviewed (YYYY-MM) — optional, for content freshness tracking |

---

## proposals/differentiators.json

Array of reusable win themes and competitive positioning statements.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., `"diff-001"`) |
| `theme` | string | Win theme name (e.g., "Speed to Value") |
| `headline` | string | One-sentence positioning statement |
| `evidence` | string[] | References to `case-studies.json` → `[].id` |
| `applicableServices` | string[] | References to `company_context.json` → `company.services[].id` |
| `tags` | string[] | Searchable tags |
| `ghostStatement` | string | Optional competitive positioning (highlights strength without naming competitors) |
| `lastReviewed` | string | Date last reviewed (YYYY-MM) |

---

## proposals/partnerships.json

Array of technology and strategic partnerships.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., `"part-001"`) |
| `partner` | string | Partner organization name |
| `level` | string | Partnership tier (e.g., "Gold Partner", "Strategic Alliance") |
| `relevantServices` | string[] | References to `company_context.json` → `company.services[].id` |
| `proofPoint` | string | One-sentence credibility statement |
| `tags` | string[] | Searchable tags |
| `lastReviewed` | string | Date last reviewed (YYYY-MM) |

---

## Cross-Reference Map

IDs create a web of references across files (deployed-plugin overlay paths):

```
company_context.json              proposals/case-studies.json
  company.services[].id ────────→   [].services[]
  pricing.publicModels[].id          [].team[] ──→ proposals/team-bios.json → [].id

company_context.json
  people[].id ──────────────────→ proposals/team-bios.json → [].id

proposals/methodologies.json
  [].applicableServices[] ──────→ company_context.json → company.services[].id

proposals/testimonials.json
  [].caseStudy ─────────────────→ proposals/case-studies.json → [].id

proposals/differentiators.json
  [].evidence[] ────────────────→ proposals/case-studies.json → [].id
  [].applicableServices[] ──────→ company_context.json → company.services[].id

proposals/partnerships.json
  [].relevantServices[] ────────→ company_context.json → company.services[].id
```

When assembling a proposal:
1. Identify relevant services from the brief → `company_context.json` → `company.services[].id`
2. Find case studies that match → `case-studies.json` → filter by `services[]` or `tags[]`
3. Find team members from those case studies → `team-bios.json` → filter by `id` in case study's `team[]`
4. Find applicable methodology → `methodologies.json` → filter by `applicableServices[]`
5. Find testimonials for selected case studies → `testimonials.json` → filter by `caseStudy`
6. Find win themes → `differentiators.json` → filter by `applicableServices[]` or `tags[]`
7. Find partnership proof points → `partnerships.json` → filter by `relevantServices[]`

## Bootstrapping a New Company Profile

> **Operator environment only.** Run these steps in `client-data`; the plugin overlay (`companies/{client_slug}/`) is generated from it via the distribution pipeline.

1. Copy the example: `cp -r client-data/clients/_example client-data/clients/<name>`
2. Edit `profile.json` — fill in all company identity, services, and pricing
3. Edit `charter.json` — set your colors, fonts, and logo references
4. Add logo files to `logos/`
5. Run the brand compiler to generate `company_context.json` (the redacted public export) and distribute to plugin overlays
6. Replace example content in `proposals/`:
   - Add real case studies to `case-studies.json`
   - Add team members to `team-bios.json`
   - Add or modify methodologies in `methodologies.json`
   - Update boilerplate in `boilerplate.json` with your standard terms
   - Add testimonials to `testimonials.json`
   - Add win themes and differentiators to `differentiators.json`
   - Add technology and strategic partnerships to `partnerships.json`
7. Ensure all cross-references are valid (team IDs in case studies, service IDs in methodologies, case study IDs in differentiators)
