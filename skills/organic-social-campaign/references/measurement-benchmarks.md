# Measurement Benchmarks — B2B Organic Social

## Critical Caveat

**Benchmarks are directional, not prescriptive.** They vary dramatically by:

- Industry sector (tech vs. government vs. professional services)
- Company size (startup vs. enterprise)
- Audience size (1,000 followers vs. 100,000)
- Geography (regional vs. global)
- Content maturity (new channel vs. established presence)

**Always set targets based on your own baseline first.** Run 60-90 days of consistent posting, measure your actual performance, then set improvement targets from there. External benchmarks are useful only for initial sanity-checking and identifying which metrics are significantly below or above normal ranges.

## Attribution — measure the dark funnel

Most B2B influence now happens **off-platform and unlinked** — in private messages, Slack/WhatsApp groups, forwards, and closed communities ("dark social," an estimated ~84% of B2B sharing). UTM/last-click attribution therefore **systematically undercounts** organic social; deterministic tracking is estimated to miss the majority of the B2B buying journey. Measure the funnel you actually have:

- **Self-reported attribution (primary).** Ask "how did you hear about us?" on intake/demo/contact forms, with free-text and room to name a person ("saw our CEO's posts", "found you on r/…"). This is the single most reliable organic-social signal in a dark-funnel world — treat it as a primary KPI, not a footnote.
- **UTMs + assisted conversions (supporting).** Still tag every link; use multi-touch/assisted views, never last-click alone.
- **Correlation signals.** Spikes in direct/branded search and direct traffic after a content push are organic working, even when unattributable.
- **Brand/narrative lift.** Periodic surveys or share-of-voice on core topics — is the brand (and its executives) increasingly *associated* with the theme?
- **AI-citation share.** Whether AI answer engines name/cite the client on core buyer questions (see `aeo-geo-social.md`) — a slow, qualitative outcome measure.
- **Person-level attribution.** Which executive/advocate drove the signal, not just "the brand page." Person-led distribution needs person-level measurement.

**Rule of thumb:** if a metric can only be captured by pretending the buying journey is linear and trackable, it is undercounting. Pair every quantitative number with a qualitative, self-reported read.

## Engagement Rate Calculation

Different platforms calculate engagement rate differently. When reporting, always specify which formula you are using.

### LinkedIn

```
Engagement Rate = (Reactions + Comments + Shares + Clicks) / Impressions × 100
```

LinkedIn's native analytics show this as "engagement rate" in the content tab. Some tools exclude clicks (counting only reactions + comments + shares). Clarify which definition you are using.

### Instagram

```
Engagement Rate = (Likes + Comments + Saves + Shares) / Reach × 100
```

Note: Instagram uses **Reach** (unique accounts), not Impressions. This produces a higher number than impression-based calculations. Some benchmarks use followers as the denominator instead — this is less accurate but easier to calculate from public data.

### Facebook

```
Engagement Rate = (Reactions + Comments + Shares + Clicks) / Reach × 100
```

Similar to Instagram, Facebook uses Reach. Clicks include link clicks, photo clicks, and "see more" clicks.

### X (Twitter)

```
Engagement Rate = (Likes + Replies + Reposts + Quote Posts + Bookmarks + Clicks) / Impressions × 100
```

X includes all interactions. Bookmark rate is increasingly important as a quality signal.

### YouTube

YouTube does not have a single "engagement rate." Key engagement metrics:

- **Click-through rate (CTR)**: Impressions to views
- **Average view duration**: Total watch time / views
- **Engagement actions**: (Likes + Comments + Shares + Saves) / Views × 100

## Directional Benchmark Ranges

*Figures updated 2026-07. The ranges in this section are **account-level** — the performance band a given page/account sits in. The 2026-07 refresh added **format-level** averages (per-format engagement across a vendor's whole sample), which answer a different question and are recorded in the per-platform notes below rather than merged into these bands. Never read a format average as an account target, and never compare across platforms — LinkedIn engagement rate is **impression-based**, Instagram and Facebook are **reach-based** (see Engagement Rate Calculation above).*

### LinkedIn (Company Pages, B2B)

| Metric | Below Average | Average | Good | Excellent |
|--------|---------------|---------|------|-----------|
| Engagement rate | <1.5% | 1.5-3% | 3-5% | >5% |
| Follower growth (monthly) | <0.5% | 0.5-1.5% | 1.5-3% | >3% |
| Click-through rate | <0.5% | 0.5-1% | 1-2% | >2% |
| Video view rate (3s+) | <15% | 15-25% | 25-40% | >40% |
| Carousel avg. slides viewed | <3 | 3-5 | 5-7 | >7 |

**Context**: Smaller pages (<5,000 followers) typically show higher engagement rates because the audience is more concentrated and engaged. As follower count grows, engagement rate naturally decreases. A 50,000-follower page at 2% engagement is outperforming a 1,000-follower page at 4% in absolute terms.

**Format-level readings (2026-07 refresh — not account targets).** Socialinsider's ~1.3M-business-post sample reports **average engagement rate per impression** by format: native document **7.0%** (2025 full-year table), then Q1-2026 readings of multi-image **≈6.8%**, video **≈5.9%**, image **≈5.2%**, text **≈4.3%**. Same denominator as the account table above (impression-based), but a **different unit of analysis** — these are per-format averages across many accounts, so a 4.3% text post is not "below average" for *your* page. Use them to choose format mix, not to set a page KPI. Vendor-reported and directional; the 7.0% row and the Q1-2026 rows come from different tables. Source: https://www.socialinsider.io/social-media-benchmarks/linkedin (accessed 2026-07-14). Full hierarchy: `platforms/linkedin.md`.

**Company-page reach (vendor evidence).** Ordinal — a vendor reporting its own analysis, **not** LinkedIn-published data — reports page reach down **60–66% since 2024** and only **2–5% of followers** in a post's initial distribution test. This is why the "Organic reach (% of followers)" style bands keep drifting down, and why the person-led posture carries distribution. Source: https://www.tryordinal.com/blog/the-declining-reach-of-linkedin-company-pages (accessed 2026-07-14).

### Instagram (Business Accounts, B2B)

| Metric | Below Average | Average | Good | Excellent |
|--------|---------------|---------|------|-----------|
| Engagement rate (reach-based) | <1% | 1-3% | 3-5% | >5% |
| Follower growth (monthly) | <0.5% | 0.5-2% | 2-4% | >4% |
| Reels play rate | <10% | 10-20% | 20-35% | >35% |
| Save rate | <0.5% | 0.5-1.5% | 1.5-3% | >3% |
| Stories completion rate | <50% | 50-70% | 70-85% | >85% |

**Context**: B2B Instagram engagement is generally lower than B2C. Save rate is a meaningful utility signal for B2B — but as of the 2026-07 refresh, **sends/shares outrank saves** as the ranking signal, so track send rate alongside it (see `platforms/meta.md`).

**Format-level readings (2026-07 refresh — not account targets).** Buffer's *State of Social Media Engagement 2026* reports carousels at **6.9% median reach-based engagement**, **1.55×** the engagement rate of single images, and Reels at **2.25×** single-image **reach**. The first two are engagement-rate readings (same reach-based denominator as the account table above); the third is a **reach** ratio and must not be quoted as an engagement figure. Per-format averages across many accounts — a format-mix input, not a page KPI. Source: https://buffer.com/resources/state-of-social-media-engagement-2026/ (accessed 2026-07-14).

**No likes-multiple.** Sends/shares are top-signal, but no reliable source quantifies them as a fixed multiple of likes — do not put such a number in a client deliverable.

### Facebook (Business Pages, B2B)

| Metric | Below Average | Average | Good | Excellent |
|--------|---------------|---------|------|-----------|
| Engagement rate (reach-based) | <0.5% | 0.5-1.5% | 1.5-3% | >3% |
| Organic reach (% of followers) | <2% | 2-5% | 5-10% | >10% |
| Video avg. watch time | <5s | 5-15s | 15-30s | >30s |
| Link click-through rate | <0.5% | 0.5-1% | 1-2% | >2% |

**Context**: Facebook organic reach for business pages has declined significantly. These benchmarks reflect the current reality. If your reach is consistently below 2% of followers, paid amplification may be needed for key content.

### X / Twitter (B2B Accounts)

| Metric | Below Average | Average | Good | Excellent |
|--------|---------------|---------|------|-----------|
| Engagement rate | <0.5% | 0.5-1% | 1-2% | >2% |
| Follower growth (monthly) | <0.5% | 0.5-1% | 1-2% | >2% |
| Reply rate | <0.1% | 0.1-0.3% | 0.3-0.5% | >0.5% |
| Bookmark rate | <0.1% | 0.1-0.3% | 0.3-0.5% | >0.5% |
| Thread completion (last/first impressions) | <20% | 20-35% | 35-50% | >50% |

**Context**: Brand accounts typically underperform personal accounts on X. Executive accounts may show 2-5x higher engagement rates than the brand page.

### YouTube (B2B Channels)

| Metric | Below Average | Average | Good | Excellent |
|--------|---------------|---------|------|-----------|
| Click-through rate (CTR) | <2% | 2-5% | 5-8% | >8% |
| Avg. view duration (% of video) | <25% | 25-40% | 40-55% | >55% |
| Subscriber conversion (subs/views) | <0.5% | 0.5-1.5% | 1.5-3% | >3% |
| Shorts avg. view duration | <50% | 50-70% | 70-85% | >85% |

**Context**: YouTube CTR benchmarks assume the video is getting impressions (appearing in search/suggested). New channels with few subscribers will see highly variable CTR. Average view duration is the most important metric — YouTube's algorithm uses it as the primary ranking signal.

## How to Use Benchmarks Responsibly

### Do

- **Baseline first**: Measure your own performance for 60-90 days before comparing to benchmarks
- **Track trends, not snapshots**: A single month's data is noisy. Look at 3-month rolling averages
- **Compare like with like**: A 500-follower channel should not benchmark against industry averages that include 100,000-follower channels
- **Use benchmarks to identify outliers**: If you are significantly below average on one metric, investigate. If you are above, understand why (and whether it is sustainable)
- **Benchmark against yourself**: Month-over-month improvement matters more than industry comparison

### Do Not

- **Set benchmark numbers as KPI targets**: "We must achieve 3% engagement rate" is a recipe for gaming metrics
- **Compare across platforms**: 2% engagement on LinkedIn and 2% on Instagram mean very different things
- **Ignore denominator effects**: Engagement rate naturally decreases as audience grows — a declining rate with growing absolute numbers is usually healthy growth
- **Treat benchmarks as stable**: Platform algorithm changes shift benchmark ranges. Re-calibrate annually
- **Chase vanity metrics**: 10,000 impressions from the wrong audience is worth less than 500 impressions from ideal prospects

## Common Measurement Pitfalls in B2B Organic

### Pitfall 1: Conflating Reach with Impact

High impressions on a post about team drinks at Friday happy hour do not advance business objectives. Measure engagement quality (comments, saves, clicks, website traffic) not just quantity.

### Pitfall 2: Ignoring Attribution Complexity

A prospect who reads 5 LinkedIn posts, watches 2 YouTube videos, and attends 1 webinar before contacting sales will attribute to "direct" or "organic search" in most analytics. Organic social's contribution is systematically undercounted.

**Mitigation**: Use UTM parameters on all links. Ask "how did you hear about us?" in intake forms. Track assisted conversions, not just last-click attribution.

### Pitfall 3: Measuring Too Frequently

Weekly reporting on organic social creates noise-driven decisions. A post that underperforms in week 1 may catch algorithmic tailwind in week 2. Report monthly, review quarterly.

### Pitfall 4: Optimizing for Engagement at the Expense of Relevance

Posts that generate high engagement from peers and competitors (other agencies, other consultants) inflate metrics without reaching actual prospects. Track audience composition, not just engagement volume.

### Pitfall 5: No Control for Content Volume

If you doubled posting frequency and engagement doubled, that is not growth — it is proportional output. Track per-post metrics alongside aggregate metrics to separate volume effects from quality improvements.

### Pitfall 6: Treating All Engagement as Equal

A comment saying "Interesting perspective, we're facing this exact challenge" is worth 100 likes. Weight qualitative signals when assessing organic social performance. Build a simple comment quality rubric:

- **High value**: Questions, sharing own experience, tagging colleagues, requesting more information
- **Medium value**: Substantive agreement or disagreement with reasoning
- **Low value**: "Great post", emoji reactions, generic praise

## Recommended Metrics by Program Maturity

### Launch Phase (Months 1-3)

Focus on activity and baseline establishment:
- Posts published per week (consistency)
- Follower growth rate (audience building)
- Engagement rate by format (learning what works)
- Baseline metrics per platform (your starting point)

### Growth Phase (Months 4-9)

Focus on engagement quality and audience fit:
- Engagement rate trend (improving month over month)
- Save/bookmark rate (content utility)
- Website traffic from social (business impact)
- Audience demographics match (are you reaching the right people)

### Optimization Phase (Months 10+)

Focus on business outcomes:
- Self-reported attribution volume and quality (primary organic signal — see Attribution above)
- Website conversions from social traffic
- Lead quality from social-referred visitors
- Content efficiency (engagement per hour of production)
- Employee advocacy contribution (if applicable)
- Executive/creator authority (person-level) and AI-citation appearances
- Share of voice vs. competitors
