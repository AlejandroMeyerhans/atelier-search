# Building Topical Maps

> Part of [The Atelier](https://alejandromeyerhans.com/atelier/) by Alejandro Meyerhans
> **Stage 3 of 4** · Topical Mapping Pipeline

Assembles SERP-clustered page groups into a hub-and-spoke topical map with gap analysis and priority scoring. Grounded in siteFocusScore/siteRadius patents and Koray Tuğberk GÜBÜR methodology.

## Quick Start

1. Download this folder into your agent's skills directory
2. Ensure you have `serp-clusters.json` from [Stage 2](../clustering-serp-intent/)
3. Tell your agent: *"Build the topical map from the SERP clusters"*

## Core Principle

A topical map is NOT a list of keywords. It's a **structure** that mirrors how Google evaluates topical authority (`siteFocusScore`). Every page must tighten the site's semantic radius around the core topic — never widen it.

## When to Use

- After running [Clustering SERP Intent](../clustering-serp-intent/) (Stage 2)
- You have `serp-clusters.json` with 20+ page clusters
- You need to organize clusters into topic groups, identify hubs, and find content gaps

## Prerequisites

- `serp-clusters.json` from Stage 2
- Understanding of the site's core topic / niche
- Optional: `keyword-universe.json` for volume reference

## Workflow

- [ ] **Stage 1:** Identify the site's core topic and sub-topics
- [ ] **Stage 2:** Group page clusters into 5-10 topic clusters
- [ ] **Stage 3:** Identify hub and spoke roles
- [ ] **Stage 4:** Gap analysis — missing hubs, missing spokes, rebuild candidates
- [ ] **Stage 5:** Priority scoring and output `topical-map.json`

---

## Stage 1: Identify Core Topic

### Automated Detection
From the keyword universe, determine the core topic by:
1. **Entity frequency:** Which noun/entity appears most across ALL keywords?
2. **Existing page themes:** What topics do the existing URLs cover?
3. **Highest volume cluster:** Which topic cluster has the most total volume?

### Manual Override
Ask the user: "What is this site primarily about?" Use their answer as the core topic anchor. Everything in the topical map must orbit this anchor.

---

## Stage 2: Group Page Clusters into Topic Clusters

### Grouping Logic
Page clusters from Stage 2 share a SERP. Now group them by **semantic theme**:

1. **Extract the primary entity** from each page cluster's H1 keyword
2. **Semantic grouping rules:**
   - Clusters sharing the same core entity → same topic cluster
   - Clusters with modifier variations (how/what/why/types/best) → same topic cluster
   - Clusters with distinct entities → different topic clusters

### Typical Topic Cluster Count
| Site Size | Recommended Clusters |
|---|---|
| Small (< 50 keywords) | 3-5 clusters |
| Medium (50-200 keywords) | 5-8 clusters |
| Large (200+ keywords) | 7-12 clusters |

---

## Stage 3: Assign Hub and Spoke Roles

### Hub Page (1 per topic cluster)
The hub is the **broadest, most authoritative** page in the cluster. Selection criteria:

1. **Highest total cluster volume** (sum of H1 + all H2/H3 keywords)
2. **Broadest coverage** — the keyword that encompasses all spoke topics
3. **Intent match** — for money sites, commercial intent hubs are preferred for commercial clusters
4. **Usually the "what is" or "guide to" page**

### Spoke Pages (All other page clusters)
Spokes are supporting content that:
- Answer specific questions within the topic
- Target long-tail or modifier keywords
- Link UP to the hub (implemented in Stage 4)

### Hub Status Classification
| Status | Meaning |
|---|---|
| `exists` | Page exists, ranking, and adequate |
| `exists_needs_rebuild` | Page exists but isn't ranking well or is thin |
| `gap` | No page exists — must be created |
| `exists_wrong_cluster` | Page exists but is currently orphaned or misassigned |

---

## Stage 4: Gap Analysis

### Types of Gaps

#### Missing Hubs (Critical Priority)
A topic cluster exists but has no hub page. Spokes have nothing to link up to.

#### Missing Spokes (High Priority)
Keywords/clusters that SHOULD exist based on competitor coverage, keyword demand, or topical coverage requirements, but the site has no content.

#### Rebuild Candidates (Medium Priority)
Existing pages that:
- Rank position 20+ (lost significant positions)
- Have < 500 words (thin content)
- Target keywords now assigned to a different cluster
- Lost traffic in an algorithm update

#### Orphan Pages
Existing pages that don't fit into ANY topic cluster. These either:
1. Need to be integrated into the map (assigned to a cluster)
2. Should be consolidated/merged with another page
3. Should be pruned (if truly off-topic — harms `siteFocusScore`)

### Gap Detection Sources
1. **Competitor comparison:** Competitors rank for clusters the target doesn't have
2. **Keyword coverage:** High-volume keywords with no existing page
3. **Entity coverage:** Sub-entities of the core topic not addressed on any page

---

## Stage 5: Priority Scoring & Output

### Priority Formula
```
Priority = (volume_potential × 0.30) + (kd_feasibility × 0.25) + 
           (intent_value × 0.25) + (structural_importance × 0.20)

Where:
  volume_potential = total_cluster_volume / max_cluster_volume (normalized 0-1)
  kd_feasibility = 1 - (avg_cluster_kd / 100) (lower KD = higher score)
  intent_value = {"transactional": 1.0, "commercial": 0.8, "informational": 0.5, "navigational": 0.3}
  structural_importance = {"missing_hub": 1.0, "missing_spoke": 0.6, "needs_rebuild": 0.4, "exists": 0.1}
```

### Priority Tiers
| Score | Tier | Action |
|---|---|---|
| 0.70+ | **P0** | Create/rebuild immediately |
| 0.50–0.69 | **P1** | Create within 30 days |
| 0.30–0.49 | **P2** | Create within 90 days |
| < 0.30 | **P3** | Backlog — create when resources allow |

### Output File
Save as `topical-map.json` in the working directory. See `resources/topical-map-schema.json` for the complete schema.

### Patent Grounding Reference

| Signal | Application in Topical Map |
|---|---|
| `siteFocusScore` | Every page must tighten focus. Prune off-topic content |
| `siteRadius` | Keep page embeddings within the site's semantic centroid |
| `normalizedTopicality` | Each page has a fixed entity budget. Hub = broad entity. Spoke = specific sub-entity |
| `headVolumeRatio` | Pages should have high topical concentration — don't spread thin |
| **Koray Tuğberk GÜBÜR** | Cover every entity and sub-entity related to core topic for comprehensive authority |

---

## Handoff

The output `topical-map.json` is the input for the next pipeline skill: **[Designing Site Architecture](../designing-site-architecture/)**, which designs the reverse silo internal linking structure and content calendar.
