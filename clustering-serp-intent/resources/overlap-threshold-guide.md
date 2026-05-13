# SERP Overlap Threshold Guide

## Default Thresholds

| Score | Meaning | Action |
|---|---|---|
| ≥ 0.40 | Same page | Cluster together |
| 0.25–0.39 | Related | Flag for manual review |
| < 0.25 | Different | Separate pages |

## When to Adjust

### Lower the threshold (0.30) when:
- **Narrow niche** — fewer competing domains means less overlap naturally
- **Low search volume keywords** — SERPs can be volatile, less reliable
- **New/emerging topic** — Google hasn't settled on consistent results

### Raise the threshold (0.50) when:
- **Broad niche** (finance, health) — many domains rank across unrelated topics
- **High authority SERP** — domains like Wikipedia appear everywhere, inflating overlap
- **Multiple languages** — if analyzing multi-language SERPs

## Overlap Calculation

```
overlap_score = |SERP_A ∩ SERP_B| / min(|SERP_A|, |SERP_B|)
```

Using `min()` rather than union avoids penalizing keywords where one SERP returns fewer results.

## Domain-Level vs URL-Level

- **Domain-level** (recommended for clustering): `ahrefs.com` matches any page on ahrefs.com
- **URL-level** (use for validation): `/blog/authority-links` only matches that exact page

Domain-level is more forgiving and better matches how Google thinks about topical authority. URL-level can be used as a secondary validation to confirm that the same page (not just domain) ranks for both keywords.
