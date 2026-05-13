# Designing Site Architecture

> Part of [The Atelier](https://alejandromeyerhans.com/atelier/) by Alejandro Meyerhans
> **Stage 4 of 4** · Topical Mapping Pipeline

Designs the internal linking architecture using Kyle Roof's reverse silo principles with both virtual (linking) and physical (URL structure) silos. Grounded in siteFocusScore, Seed Distance PageRank, and phrase-based indexing patents.

## Quick Start

1. Download this folder into your agent's skills directory
2. Ensure you have `topical-map.json` from [Stage 3](../building-topical-maps/)
3. Tell your agent: *"Design the site architecture from the topical map"*

## Core Principles

1. **Supporting pages link UP to the money page** — never the reverse in isolation
2. **Virtual silo through linking > physical silo through URL structure** — use BOTH
3. **No cross-silo leakage from spokes** — spokes ONLY link within their silo
4. **Daisy-chain between spokes** — sequential PageRank flow
5. **Hub-to-hub strategic bridges** — the ONLY acceptable cross-silo links
6. **Contextual body links** — all internal links in body content, NOT nav/footer/sidebar

## Workflow

- [ ] **Stage 1:** Design physical silo (URL structure)
- [ ] **Stage 2:** Design virtual silo (linking rules per cluster)
- [ ] **Stage 3:** Plan cross-silo bridges
- [ ] **Stage 4:** Assign anchor text strategy
- [ ] **Stage 5:** Generate content calendar
- [ ] **Stage 6:** Output `site-architecture.json`

---

## Stage 1: Physical Silo (URL Structure)

```
/{cluster-slug}/                    → Hub page
/{cluster-slug}/{spoke-slug}        → Spoke page
```

### Migration Rules
- Check if existing URLs have backlinks (use Ahrefs backlinks-stats)
- If URL has backlinks: implement 301 redirect
- If no backlinks: redirect or canonical
- **Never break existing equity**

---

## Stage 2: Virtual Silo (Linking Rules)

### Rule 1: Spoke → Hub (MANDATORY)
Every spoke links to its hub. First 3 paragraphs. Exact H1 keyword or variant.

### Rule 2: Hub → Spokes (STRATEGIC)
Hub links down to ALL spokes via body content or "Related Topics" section.

### Rule 3: Spoke ↔ Spoke Daisy Chain
Spokes link to the next spoke sequentially (circular). Bottom of body content.

### Rule 4: NO Cross-Silo Spoke Links (FORBIDDEN)
```
❌ /link-types/authority-links → /strategies/outreach
✅ /link-types/authority-links → /link-types/dofollow-vs-nofollow
```

### Rule 5: Hub → Hub Bridges (LIMITED)
Hub pages CAN link to other hubs. Max 2-3 bridges per hub.

---

## Stage 3: Cross-Silo Bridge Planning

Score potential bridges by: `semantic_relevance × user_flow × equity_balance`

---

## Stage 4: Anchor Text Strategy

| Link Type | Strategy |
|---|---|
| Spoke → Hub | Hub's H1 keyword (50%) or variant (50%) |
| Hub → Spoke | Spoke's H1 keyword (70%) or phrase (30%) |
| Spoke → Spoke | Next spoke's H1 (80%) or contextual (20%) |
| Hub → Hub | Other hub's H1 or descriptive phrase |

**Forbidden:** "click here", "read more", "this article", naked URLs.

---

## Stage 5: Content Calendar

1. **Hubs first, then spokes**
2. **Highest-priority cluster first** — complete P0 before P1
3. **Within cluster:** Hub → P0 spokes → P1 → P2
4. **All internal links added at publication time**

---

## Stage 6: Output

Save as `site-architecture.json`. See `resources/site-architecture-schema.json` for schema.

### Patent Grounding

| Patent / Signal | Application |
|---|---|
| `siteFocusScore` | Silo keeps pages in the same semantic neighborhood |
| **US9953049B1** — Seed Distance PageRank | Hub = seed page; shorter distance = more authority |
| **US7536408B2** — Phrase-Based Indexing | Exact-match internal anchors create co-occurrence |
| **US11409748B1** — Heading Hierarchy | Heading path vectorized as ranking signal |
| **US8775409B1** — Query Clustering | Silo mirrors Google's query-to-cluster mapping |

---

## Post-Architecture Checklist

- [ ] Implement 301 redirects for URL migrations
- [ ] Update robots.txt and XML sitemap
- [ ] Add BreadcrumbList schema to all pages
- [ ] Verify no orphan pages remain
- [ ] Set up GSC tracking for new URL structure
