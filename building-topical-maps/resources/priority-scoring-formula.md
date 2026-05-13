# Priority Scoring Formula

## Formula

```
Priority = (volume_potential × 0.30) + (kd_feasibility × 0.25) + 
           (intent_value × 0.25) + (structural_importance × 0.20)
```

## Component Definitions

### Volume Potential (30% weight)
```
volume_potential = total_cluster_volume / max_cluster_volume
```
- Normalized 0-1 across all clusters
- Uses total cluster volume (H1 + all H2/H3)

### KD Feasibility (25% weight)
```
kd_feasibility = 1 - (avg_cluster_kd / 100)
```
- Lower difficulty = higher score
- Average across all keywords in the cluster

### Intent Value (25% weight)
| Intent | Score |
|---|---|
| Transactional | 1.0 |
| Commercial | 0.8 |
| Informational | 0.5 |
| Navigational | 0.3 |

Uses the dominant intent of the cluster.

### Structural Importance (20% weight)
| Status | Score |
|---|---|
| Missing hub | 1.0 |
| Missing spoke | 0.6 |
| Needs rebuild | 0.4 |
| Exists (optimization only) | 0.1 |

## Priority Tiers

| Score | Tier | Timeline |
|---|---|---|
| 0.70+ | P0 | Immediate |
| 0.50–0.69 | P1 | 30 days |
| 0.30–0.49 | P2 | 90 days |
| < 0.30 | P3 | Backlog |

## Customization

For **money sites** (e-commerce, SaaS landing pages):
- Increase intent_value weight to 0.35
- Decrease volume_potential weight to 0.20

For **content/media sites** (blogs, publishers):
- Increase volume_potential weight to 0.40
- Decrease intent_value weight to 0.15
