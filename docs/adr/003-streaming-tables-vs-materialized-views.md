# ADR-003: Streaming tables for Bronze and Silver, materialized views for Gold

Status: Accepted
Date: 2026-11-22

## Context
The pipeline has three layers with different workloads:
- Bronze and Silver receive new files that are only ever appended
  (orders and order items arriving in a landing volume).
- Gold is a set of business aggregates (daily sales) that join and
  summarize Silver tables for BI users.

Lakeflow Spark Declarative Pipelines offers two main dataset types for this:
streaming tables (`@dp.table`) and materialized views (`@dp.materialized_view`).
We need to choose per layer, balancing correctness, cost and simplicity for a
team of 10-15 engineers.

## Options considered
1. **Streaming tables everywhere:** every layer processes only new data.
2. **Materialized views everywhere:** every layer is a declared query over
   its upstream tables, with no streaming state to manage.
3. **Streaming tables for Bronze/Silver, materialized views for Gold.**

## Decision
Option 3.

- **Bronze (streaming table):** Auto Loader reads each new file once, so raw
  data is appended without reprocessing history.
- **Silver (streaming table):** cleaning and typing are row-level and
  append-oriented, so processing only new rows is a natural fit.
  Expectations drop invalid rows on key columns.
- **Gold (materialized view):** aggregates and joins are expressed as a
  query over Silver. The platform decides how to refresh the result and
  handles late or corrected data without custom merge logic.

## Evidence from the first run
On the first pipeline run (Olist public dataset, about 99K orders and 113K
order items), the Gold `daily_sales` view produced 614 rows and the pipeline
graph reported a **full recompute** rather than an incremental refresh.

At this data size this is cheap, so it does not change the decision. It does
mean we must not assume Gold refreshes incrementally. The reason has not yet
been established; it is logged as a follow-up (see below).

## Consequences
**Positive**
- Bronze and Silver ingestion cost grows with new data, not total history.
- Gold logic is plain SQL/DataFrame code with no hand-written merge or
  state handling.
- Clear mental model for the team: streaming for append-only data,
  materialized views for derived business tables.

**Negative**
- Streaming tables are best suited to append-only sources. If a source
  system starts updating or deleting rows in Bronze, Silver needs a
  different pattern (for example change data capture).
- Deduplicating with `dropDuplicates` on a stream keeps state, which can grow
  without a watermark or a bounded key window. This needs review before
  production-scale volumes.
- Gold refresh cost depends on whether the engine can refresh it
  incrementally. At large scale a full recompute on every run could be
  expensive.

## Follow-ups
- Check the pipeline event log to see why Gold used a full recompute
  and whether the query can be rewritten so it refreshes incrementally.
- Revisit Silver deduplication (watermark or merge-based approach)
  once the volume assumptions in the requirements are fleshed out.
- Compare Gold refresh cost at larger synthetic volumes in the cost study.

## Revisit when
Source systems start sending updates or deletes, Gold refresh time or
cost becomes significant, or the platform's refresh behavior for
materialized views changes.