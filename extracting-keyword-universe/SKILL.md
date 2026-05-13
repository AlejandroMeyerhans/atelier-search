# Extracting Keyword Universe

> Part of [The Atelier](https://alejandromeyerhans.com/atelier/) by Alejandro Meyerhans
> **Stage 1 of 4** · Topical Mapping Pipeline

Extracts the complete keyword universe for any website using the Ahrefs MCP. Pulls organic keywords, discovers competitors, expands with matching/related terms, and classifies by intent.

## Quick Start

1. Download this folder into your agent's skills directory
2. Ensure the [Ahrefs MCP server](https://docs.ahrefs.com/docs/api/reference/introduction) is connected
3. Tell your agent: *"Extract the keyword universe for example.com"*

## When to Use

- Building a topical map for any website (Stage 1 of the 4-skill pipeline)
- Comprehensive keyword research for a site or niche
- Pre/post algorithm update keyword comparison
- Content gap analysis at the keyword level

## Prerequisites

- Ahrefs MCP server connected (`ahrefs_remote`)
- Target site URL **OR** a `keyword-seeds.json` file (for greenfield sites — see Mode B below)
- Target country code (default: `US`)
- Optional: pre-update date for comparison analysis

> **Date handling:** Ahrefs data lags by 3-5 days. Always use a date at least 4 days in the past. Never use today's date — it will return an error.

---

## Mode Detection

This skill operates in one of two modes:

### Mode A: Live Site Mode (Default)
**Trigger:** User provides a domain/URL to analyze.
**Flow:** Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 (all stages below)

### Mode B: Codex-Seeded Mode (Greenfield)
**Trigger:** User provides a `keyword-seeds.json` file with seed keywords and competitor domains.
**When to use:** The site doesn't exist yet. There are no organic keywords to pull. You have niche research to work from.

**How it works:**
1. Prepare a `keyword-seeds.json` file containing `seed_keywords`, `topic_seeds`, and `competitor_domains`
2. The skill reads this file and adapts the stages:

| Standard Stage | Codex-Seeded Adaptation |
|---|---|
| **Stage 1:** Extract site's own keywords | ⏭️ **SKIP** — site doesn't exist yet |
| **Stage 2:** Discover competitors | 🔄 **REPLACE** — use `competitor_domains` from keyword-seeds.json |
| **Stage 3:** Extract competitor keywords | ✅ **SAME** — pull organic keywords from identified competitors |
| **Stage 4:** Expand with matching/related | 🔄 **ADAPT** — use `seed_keywords` + `topic_seeds` as seed input |
| **Stage 5:** Deduplicate, classify, output | ✅ **SAME** — identical processing |

#### Codex-Seeded Stage 2: Load Competitors

Instead of running `site-explorer-organic-competitors`, read the `competitor_domains` array from `keyword-seeds.json`:

```
Read: keyword-seeds.json → competitor_domains
Select: top 5 by fact_count
These become the competitor targets for Stage 3.
```

#### Codex-Seeded Stage 4: Expand from Entity Seeds

Instead of using the site's own top keywords as seeds, use two seed sets:

**Seed Set A — Entity Keywords:**
```
Read: keyword-seeds.json → seed_keywords (top 15)
Use as: input to keywords-explorer-matching-terms and keywords-explorer-related-terms
```

**Seed Set B — Topic Compound Keywords:**
```
Read: keyword-seeds.json → topic_seeds
Generate compound seeds: "{niche} {topic_name}" for each topic
E.g., "olive oil chemistry", "olive oil health", "olive oil production"
Use as: additional input to keywords-explorer-matching-terms
```

> [!IMPORTANT]
> In codex-seeded mode, the `existing_pages` array in the output will be empty (the site doesn't exist yet). All keywords will be tagged with `source: "codex-competitor:{domain}"` or `source: "codex-expansion:{tool}"` to distinguish from live-site extractions.

---

## Workflow

- [ ] **Stage 1:** Extract the site's own organic keywords *(skip in codex-seeded mode)*
- [ ] **Stage 2:** Discover organic competitors *(or load from keyword-seeds.json)*
- [ ] **Stage 3:** Extract competitor keywords (top 3-5 competitors)
- [ ] **Stage 4:** Expand keyword universe with matching/related terms
- [ ] **Stage 5:** Deduplicate, classify intent, and produce `keyword-universe.json`

---

## Stage 1: Extract Site's Organic Keywords

Pull ALL keywords the site currently ranks for. Use a high limit and include full intent flags.

```
Tool: site-explorer-organic-keywords
Parameters:
  target: "{site_domain}"
  mode: "subdomains"
  date: "{current_date}"        # YYYY-MM-DD format
  country: "{country_code}"     # e.g., "US"
  select: "keyword,volume,best_position,best_position_url,sum_traffic,cpc,keyword_difficulty,is_commercial,is_informational,is_navigational,is_transactional,is_branded,is_local,serp_features,best_position_kind"
  order_by: "sum_traffic:desc"
  limit: 1000
```

**If doing a pre/post comparison** (e.g., algorithm update analysis), run this TWICE:
- Once with `date: "{pre_update_date}"` and `date_compared: "{post_update_date}"`
- Capture `best_position_prev`, `sum_traffic_prev`, `volume_prev` fields

### Key Fields to Preserve
| Field | Why |
|---|---|
| `keyword` | The keyword string |
| `volume` | Monthly search volume |
| `best_position` | Current ranking position |
| `best_position_url` | Which URL ranks for this keyword |
| `sum_traffic` | Estimated monthly traffic from this keyword |
| `cpc` | Cost per click (USD cents — divide by 100 for dollars) |
| `keyword_difficulty` | KD score 0-100 |
| `is_commercial` | Intent flag |
| `is_informational` | Intent flag |
| `is_navigational` | Intent flag |
| `is_transactional` | Intent flag |
| `is_branded` | Is this a branded query? |
| `serp_features` | What SERP features appear (snippet, ai_overview, etc.) |

---

## Stage 2: Discover Organic Competitors

Find domains that rank for similar keywords.

```
Tool: site-explorer-organic-competitors
Parameters:
  target: "{site_domain}"
  mode: "subdomains"
  country: "{country_code}"
  date: "{current_date}"
  select: "competitor_domain,keywords_common,keywords_competitor,traffic"
  order_by: "keywords_common:desc"
  limit: 10
```

### Selection Criteria
From the results, select the **top 3-5 competitors** based on:
1. Highest `keywords_common` count (most keyword overlap)
2. Reasonable `traffic` (not too large — would drown signal with noise)
3. Same niche focus (manually verify the first few domains)
4. Skip mega-sites (ahrefs.com, semrush.com, moz.com, fiverr.com) — too broad to be useful competitors

---

## Stage 3: Extract Competitor Keywords

For each selected competitor, pull their keywords that the TARGET site does NOT rank for.

```
Tool: site-explorer-organic-keywords
Parameters:
  target: "{competitor_domain}"
  mode: "subdomains"
  date: "{current_date}"
  country: "{country_code}"
  select: "keyword,volume,best_position,sum_traffic,cpc,keyword_difficulty,is_commercial,is_informational,is_navigational,is_transactional,serp_features"
  order_by: "volume:desc"
  limit: 200
  where: '{"field":"volume","is":["gte",50]}'
```

**Filter strategy:**
- Only keywords with volume ≥ 50 (skip zero-volume long-tail noise)
- Cap at 200 per competitor to avoid API cost explosion
- Tag each keyword with `source: "competitor:{domain}"`

---

## Stage 4: Expand with Matching/Related Terms

Take the **top 10-15 seed keywords** from Stage 1 (highest volume, most representative of the niche) and expand:

> **⚠️ Column Name Difference:** `keywords-explorer` tools use DIFFERENT column names than `site-explorer` tools:
> - Difficulty: `difficulty` (not `keyword_difficulty`)
> - Intent: `intents` nested object (not individual `is_*` flags)
> - The `intents` object contains: `informational`, `commercial`, `transactional`, `navigational`, `branded`, `local`

### 4a. Matching Terms
```
Tool: keywords-explorer-matching-terms
Parameters:
  keywords: "{seed_keyword_1},{seed_keyword_2},..."
  country: "{country_code}"
  select: "keyword,volume,difficulty,cpc,intents,traffic_potential"
  order_by: "volume:desc"
  limit: 200
  where: '{"and":[{"field":"volume","is":["gte",30]},{"field":"difficulty","is":["lte",50]}]}'
```

### 4b. Related Terms ("Also Rank For")
```
Tool: keywords-explorer-related-terms
Parameters:
  keywords: "{seed_keyword_1},{seed_keyword_2},..."
  country: "{country_code}"
  select: "keyword,volume,difficulty,cpc,intents,traffic_potential"
  order_by: "volume:desc"
  limit: 200
  view_for: "also_rank_for"
```

Tag all expanded keywords with `source: "expansion:{tool_name}"`.

---

## Stage 5: Deduplicate, Classify & Output

### Deduplication Rules
1. Lowercase all keywords
2. Merge duplicates, keeping the record with the most metadata
3. If a keyword appears from multiple sources, preserve all source tags
4. Prefer the site's own ranking data over competitor data for position/URL fields

### Intent Classification
Ahrefs provides native intent flags. Classify each keyword's **dominant intent**:

```
Priority order for dominant intent:
1. transactional (if is_transactional = true)
2. commercial (if is_commercial = true AND is_transactional = false)
3. navigational (if is_navigational = true AND no commercial/transactional)
4. informational (if is_informational = true — default)
5. branded (if is_branded = true — separate flag, not mutually exclusive)

Note: Keywords can have MULTIPLE intent flags. Capture all, but assign one dominant.
```

### Existing Pages Inventory
From Stage 1, extract the unique `best_position_url` values to build the site's existing page inventory.

### Output File
Save the final output as `keyword-universe.json` in the working directory. See `resources/keyword-universe-schema.json` for the complete schema.

---

## API Cost Awareness

| Tool | Cost per Call | Typical Calls | Estimated Total |
|---|---|---|---|
| `organic-keywords` (target) | 10 units/row | 1 call × 1000 rows | 10,000 units |
| `organic-competitors` | 10 units/row | 1 call × 10 rows | 100 units |
| `organic-keywords` (competitors) | 10 units/row | 3 calls × 200 rows | 6,000 units |
| `matching-terms` | 10 units/row | 1 call × 200 rows | 2,000 units |
| `related-terms` | 10 units/row | 1 call × 200 rows | 2,000 units |
| **Total** | | | **~20,100 units** |

> Before running, check available units with `subscription-info-limits-and-usage`.

---

## Handoff

The output `keyword-universe.json` is the input for the next pipeline skill: **[Clustering SERP Intent](../clustering-serp-intent/)**, which analyzes SERP overlap to determine which keywords belong on the same page.
