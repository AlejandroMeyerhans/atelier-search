# atelier-search

> Part of [The Atelier](https://alejandromeyerhans.com/atelier/) by Alejandro Meyerhans

Search intelligence skills for building topical maps, analyzing SERPs, and optimizing content through NLP. These four skills form a complete **Topical Mapping Pipeline** (Stages 1–4), plus a standalone NLP optimization analyzer.

## Skills

| Skill | Description | Pipeline Stage |
|---|---|---|
| [Extracting Keyword Universe](./extracting-keyword-universe/) | Pulls the complete keyword universe from Ahrefs MCP | Stage 1 of 4 |
| [Clustering SERP Intent](./clustering-serp-intent/) | Groups keywords by SERP overlap into page clusters | Stage 2 of 4 |
| [Building Topical Maps](./building-topical-maps/) | Assembles clusters into hub-and-spoke topic groups | Stage 3 of 4 |
| [Designing Site Architecture](./designing-site-architecture/) | Designs reverse silo internal linking structure | Stage 4 of 4 |
| [Analyzing NLP Optimization](./analyzing-nlp-optimization/) | Runs Google NLP API entity/salience analysis | Standalone |

## Quick Start

1. Download or clone this repository
2. Place the skill folders in your AI agent's skills directory
3. Ensure you have the [Ahrefs MCP server](https://docs.ahrefs.com/docs/api/reference/introduction) connected for pipeline skills
4. For NLP analysis, you'll need a [Google Cloud Natural Language API](https://cloud.google.com/natural-language) key

## Pipeline Flow

```
keyword-universe.json → serp-clusters.json → topical-map.json → site-architecture.json
     (Stage 1)              (Stage 2)            (Stage 3)            (Stage 4)
```

Each stage produces a JSON artifact that feeds into the next. You can also run any stage independently if you already have the required input file.

## Requirements

- An AI coding agent (Claude Code, Cursor, Windsurf, or similar)
- Ahrefs API access with MCP server configured
- Python 3.9+ (for NLP analysis script)

## License

[MIT](./LICENSE)
