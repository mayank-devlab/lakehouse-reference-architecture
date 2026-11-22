# ADR-002: Lakeflow Declarative Pipelines for transformations, Lakeflow Jobs for orchestration

Status: Accepted
Date: 2026-11-22

## Context
We need declarative pipelines with built-in data quality and lineage,
maintainable by a team of 10-15 engineers, with a cost-aware compute model.
Lakeflow Spark Declarative Pipelines (formerly Delta Live Tables) is the
current Databricks product for this.

## Options considered
1. **Lakeflow Declarative Pipelines (SDP):** declarative, with expectations,
   lineage and automatic dependency handling.
2. **Lakeflow Jobs with custom notebooks:** maximum flexibility, more code to maintain.
3. **External orchestrator + Spark jobs:** powerful, but adds another platform to run.

## Decision
- Use **SDP** for Bronze to Silver to Gold transformations.
- Use **Lakeflow Jobs** to schedule pipelines and chain non-pipeline tasks.
- Do not introduce an external orchestrator at this scale.

(Keep the Consequences and Revisit sections as they are.)