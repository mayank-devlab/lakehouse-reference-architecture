# ADR-001: Use Medallion layers (Bronze, Silver, Gold)

Status: Accepted
Date: 2026-11-22

## Context
ShopNova ingests data from several source systems for analysts, engineers,
data scientists and compliance. We need replayable raw data, clear quality
boundaries, and curated tables that business users can trust.

## Options considered
1. **Single-layer tables:** load and transform in one step.
2. **Two layers (raw + curated):** simpler, fewer tables.
3. **Medallion (Bronze, Silver, Gold):** three layers with distinct purposes.

## Decision
Use three layers:
- **Bronze:** raw, append-only, minimal change, full history for replay and audit.
- **Silver:** cleaned, deduplicated, typed and conformed, with data quality
  expectations. PII is masked here for non-privileged users.
- **Gold:** business-level aggregates and marts for BI.

## Consequences
**Positive**
- Raw data can be reprocessed after logic changes without re-ingesting.
- Quality issues are isolated and visible per layer.
- Access can be granted per layer (analysts: Gold; data scientists: Silver).

**Negative**
- More tables and storage than a two-layer design.
- Extra pipeline hops add some latency.

## Revisit when
Streaming latency needs drop below what three hops can support, or the layer
count becomes a maintenance burden for the team.