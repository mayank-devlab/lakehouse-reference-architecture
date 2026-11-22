# Design rules of thumb

Starting points used in this repo. Adjust them to your own workload.

## Dataset type per layer
| Situation | Use |
|-----------|-----|
| Append-only source, each row processed once | Streaming table (Bronze, most of Silver) |
| Derived business table (join, aggregate) | Materialized view (Gold) |

## Data quality behavior
| Decorator | Behavior | Use for |
|-----------|----------|---------|
| `expect` | Record the violation, keep the row | Soft checks |
| `expect_or_drop` | Drop the row | Keys that must be valid |
| `expect_or_fail` | Stop the pipeline | Checks you cannot compromise on |

## Caveats
- Do not assume a materialized view refreshes incrementally. In this repo's first
  run, Gold did a full recompute (see ADR-003). Check the pipeline event log.
- Deduplicating a stream keeps state. Plan a watermark or merge strategy before
  volumes grow. This is a design risk, not something measured here.
