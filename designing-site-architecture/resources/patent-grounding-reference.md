# Patent Grounding Reference — Site Architecture

## siteFocusScore (Google API Leak)
- **What it measures:** How focused a site is on a single topic
- **How it works:** Page embeddings are averaged to create a site centroid. Pages deviating from the centroid reduce the score
- **Architecture impact:** Silo structure ensures all pages within a cluster are semantically close, tightening the centroid around each topic
- **Source:** Codex Brand & Entity SEO, Google API Content Warehouse leak

## siteRadius (Google API Leak)
- **What it measures:** The semantic spread of a site's content
- **How it works:** Standard deviation of page embeddings from the site centroid
- **Architecture impact:** Cross-silo spoke isolation prevents pages from pulling the centroid in divergent directions
- **Source:** Codex Brand & Entity SEO

## US9953049B1 — Seed Distance PageRank
- **What it measures:** PageRank weighted by distance from trusted "seed" pages
- **How it works:** Authority decays with each hop from a seed page
- **Architecture impact:** Hub pages act as local seeds. 1-hop spoke-to-hub links transfer maximum authority. Daisy chains create additional 2-hop paths
- **Filed:** 2016 | **Granted:** 2018

## US7536408B2 — Phrase-Based Indexing
- **What it measures:** Co-occurrence of phrases across documents and links
- **How it works:** Anchor text containing topically relevant phrases creates co-occurrence signals that reinforce document relevance
- **Architecture impact:** Exact-match keyword anchors in internal links create the strongest co-occurrence signal between linked pages
- **Filed:** 2004 | **Granted:** 2009

## US11409748B1 — Heading Hierarchy Vectorization
- **What it measures:** The semantic path from H1 → H2 → H3 as a single embedding
- **How it works:** Google concatenates the heading hierarchy into a vector and matches it against query intent
- **Architecture impact:** Internal links between pages at the correct heading level reinforce the vectorized hierarchy. A spoke page about "H2-level topic" linking to the hub's "H1-level topic" mirrors the heading path
- **Filed:** 2021 | **Granted:** 2022

## US10235423B2 — Entity Metrics (S = aR + bN + cC + dP)
- **What it measures:** Entity strength across web presence
- **How it works:** R (express links/references), N (name mentions), C (citations), P (page quality)
- **Architecture impact:** Internal links are express links (R metric). More internal links to a page = higher entity metric score for that page's target entity
- **Filed:** 2017 | **Granted:** 2019

## US8775409B1 — Query Clustering by Result URLs
- **What it measures:** Which queries produce similar result sets
- **How it works:** Queries with ≥3 overlapping results are clustered together
- **Architecture impact:** Our silo structure mirrors Google's query clustering — keywords on the same page share SERP overlap (Skill 2), and silo grouping aligns with how Google groups related queries
- **Filed:** 2012 | **Granted:** 2014
