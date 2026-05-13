# Clustering SERP Intent

> Part of [The Atelier](https://alejandromeyerhans.com/atelier/) by Alejandro Meyerhans
> **Stage 2 of 4** · Topical Mapping Pipeline

Analyzes SERP overlap to determine which keywords belong on the same page, assigns heading hierarchy, and validates intent coherence. Uses Ahrefs `serp-overview` (primary) or DataForSEO SERP API (batch).

## Quick Start

1. Download this folder into your agent's skills directory
2. Ensure you have `keyword-universe.json` from [Stage 1](../extracting-keyword-universe/)
3. Tell your agent: *"Cluster the keywords by SERP overlap"*

## Core Principle

**If Google ranks the same URLs for two keywords, those keywords belong on the SAME page.**

This is not opinion — it's reverse-engineering Google's own query clustering logic (Patent US8775409B1: queries producing similar result sets are treated as the same informational need).

## When to Use

- After running [Extracting Keyword Universe](../extracting-keyword-universe/) (Stage 1)
- You have `keyword-universe.json` with 100+ keywords
- You need to determine which keywords should be targeted on the SAME page vs separate pages
- You need to assign heading hierarchy (H1, H2, H3) within page clusters

## Prerequisites

- `keyword-universe.json` from Stage 1
- Ahrefs MCP connected (preferred) OR DataForSEO API key
- Target country code (default: `US`)

## Workflow

- [ ] **Stage 1:** Select priority keywords for SERP analysis (sampling strategy)
- [ ] **Stage 2:** Pull SERP data for each priority keyword
- [ ] **Stage 3:** Build the SERP overlap matrix
- [ ] **Stage 4:** Cluster keywords by overlap threshold
- [ ] **Stage 5:** Assign heading hierarchy within clusters
- [ ] **Stage 6:** Validate intent coherence and output `serp-clusters.json`

---

## Stage 1: Sampling Strategy

Pulling SERP data for every keyword is expensive and unnecessary. Use this tiered strategy:

### Tier 1: Primary Keywords (ALWAYS analyze)
- All keywords with volume ≥ 200
- All keywords where the site currently ranks (has `current_url`)
- All keywords with commercial or transactional intent
- **Cap:** 100 keywords maximum

### Tier 2: Inferred Keywords (DO NOT pull SERP)
- Keywords with volume < 200 that are clear long-tail variants of Tier 1 keywords
- Assign these to clusters using **keyword structure matching** instead of SERP analysis:
  - "types of backlinks" is Tier 1 → "different types of backlinks" is automatically assigned to the same cluster
  - Match by: shared 2+ word phrases, modifier patterns (how to, what is, best, vs, etc.)

### Selection Logic
```
From keyword-universe.json:
1. Sort by volume DESC
2. Filter: volume >= 200 OR current_position IS NOT NULL OR is_commercial = true OR is_transactional = true
3. Take top 100 (or fewer if the universe is small)
4. These are your "SERP analysis candidates"
5. Everything else → Tier 2 (inferred assignment later)
```

---

## Stage 2: Pull SERP Data

### Option A: Ahrefs `serp-overview` (Preferred — already paid for)

```
Tool: serp-overview
Parameters:
  keyword: "{keyword}"
  country: "{country_code}"
  select: "position,title,url,domain_rating,backlinks,traffic"
  top_positions: 10
```

Run this for each Tier 1 keyword. Extract only the **URLs** from the top 10 positions.

**Cost:** Each call uses API units. For 100 keywords, this is manageable within most Ahrefs plans.

### Option B: DataForSEO SERP API (Better for large batches)

```
POST https://api.dataforseo.com/v3/serp/google/organic/live/regular/
Headers:
  Authorization: Basic {base64_encoded_credentials}
  Content-Type: application/json
Body:
[
  {
    "keyword": "{keyword}",
    "location_code": 2840,
    "language_code": "en",
    "depth": 10
  }
]
```

**Cost:** $0.002/keyword (live) or $0.0006/keyword (standard queue).

### What to Extract
For each keyword, store only the top 10 result URLs (domains, not full paths — for overlap analysis).

> **⚠️ SERP Dedup Rule:** Ahrefs `serp-overview` returns **multiple URLs per position** (sitelinks, carousel items, FAQ jump links). You MUST deduplicate:
> 1. Group results by `position` number
> 2. Take only the **first URL** per unique position
> 3. Extract the domain from that URL
> 4. Deduplicate domains — keep only unique domains
> 5. This gives you the clean 10-domain SERP for overlap analysis
>
> Without this, overlap scores will be inflated by duplicate domain entries.

---

## Stage 3: Build the SERP Overlap Matrix

For every pair of keywords (A, B), calculate:

```
overlap_score = |SERP_A ∩ SERP_B| / min(|SERP_A|, |SERP_B|)
```

This is the **Jaccard-like overlap coefficient**. Using `min()` in the denominator instead of union ensures that if one SERP has fewer results, overlap is measured proportionally.

### Threshold Rules
| Overlap Score | Interpretation | Action |
|---|---|---|
| ≥ 0.40 | **Same page** — Google treats these as the same topic | Cluster together |
| 0.25–0.39 | **Related** — same topic cluster but may warrant separate pages | Flag for manual review |
| < 0.25 | **Different pages** — distinct topics | Assign to different clusters |

> These thresholds are starting defaults. Adjust per niche: broader niches (finance, health) may need higher thresholds; narrow niches (specific SaaS tool features) may work with lower ones.

---

## Stage 4: Cluster Keywords by Overlap

### Algorithm: Greedy Clustering

```
1. Start with the highest-volume keyword as Cluster Seed 1
2. For all remaining keywords, calculate overlap with Seed 1
3. Any keyword with overlap ≥ 0.40 → add to Cluster 1
4. Take the next highest-volume keyword NOT yet assigned → Cluster Seed 2
5. Repeat until all Tier 1 keywords are assigned
6. Assign Tier 2 keywords to existing clusters via keyword structure matching
```

### Handling Edge Cases
- **Keyword overlaps with multiple clusters equally:** Assign to the cluster whose seed has the highest volume
- **Keyword overlaps with NO cluster:** It becomes a new cluster seed (new page)
- **Very large clusters (10+ keywords):** These are likely hub page candidates. Flag them

---

## Stage 5: Assign Heading Hierarchy

Within each cluster, assign heading levels based on this hierarchy:

### H1 Assignment (Page Title/Primary Target)
- **Rule:** Highest search volume keyword in the cluster
- **Tiebreaker:** Lower KD wins (more achievable)
- **Validation:** Must be under 60 characters (title tag constraint)

### H2 Assignment (Major Section Headings)
- Keywords that modify the H1 with a distinct subtopic
- Patterns: "how to [H1 topic]", "[H1 topic] vs [alternative]", "best [H1 topic]", "types of [H1 topic]"
- Maximum 5-7 H2s per page

### H3 Assignment (Sub-section Headings)
- Long-tail variants that elaborate on an H2
- Patterns: "[H2 topic] for [audience]", "[H2 topic] examples", "[H2 topic] tools"
- These are supporting content, not separate ranking targets

### Patent Reference
Patent **US11409748B1** vectorizes the heading path (H1→H2→H3) into a single embedding and matches it against query intent. The heading hierarchy IS the ranking signal — not just a formatting choice.

---

## Stage 6: Validate & Output

### Intent Coherence Check
Every keyword in a cluster should share the same dominant intent. If a cluster mixes commercial and informational keywords:
- **If 80%+ share the same intent:** The outliers become H3s or FAQ items
- **If split 50/50:** The cluster likely needs splitting into two pages

### Orphan Detection
Keywords from the universe that couldn't be assigned to any cluster:
- Volume ≥ 100: Flag as potential new content opportunities
- Volume < 100: Deprioritize or assign as long-tail supporting terms

### Output File
Save as `serp-clusters.json` in the working directory. See `resources/serp-clusters-schema.json` for the complete schema.

---

## SERP Source Decision Tree

```
Q: How many Tier 1 keywords need analysis?

  ≤ 50 keywords  → Use Ahrefs serp-overview (already paid for)
  51-200 keywords → Use DataForSEO standard queue ($0.03-$0.12)
  200+ keywords   → Use DataForSEO standard queue + increase Tier 2 inference
```

---

## Cost Summary

| Source | Per Keyword | 50 Keywords | 100 Keywords |
|---|---|---|---|
| Ahrefs `serp-overview` | ~2-5 API units | ~100-250 units | ~200-500 units |
| DataForSEO Live | $0.002 | $0.10 | $0.20 |
| DataForSEO Standard | $0.0006 | $0.03 | $0.06 |

---

## Handoff

The output `serp-clusters.json` is the input for the next pipeline skill: **[Building Topical Maps](../building-topical-maps/)**, which groups page clusters into topic clusters and performs gap analysis.
