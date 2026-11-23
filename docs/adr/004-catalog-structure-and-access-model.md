# ADR-004: Catalog structure and access model

Status: Accepted
Date: 2026-11-23

## Context
Several personas need different views of the same data, including PII-like
identifiers. Access must be auditable and easy to review.

## Options considered
1. One catalog per environment, one schema per layer.
2. One catalog per domain, with layers inside.
3. A single shared catalog with table-level grants to individuals.

## Decision
Option 1 as the target (shopnova_dev, shopnova_test, shopnova_prod, with bronze,
silver and gold schemas). This repo runs it in the single `workspace` catalog
because Free Edition provides one. Access is granted to groups per schema.
Masks sit on PII columns at Silver. Row filters sit on Gold serving tables.

## Evidence
[Add your before/after mask screenshots and the grants output.]

## Consequences
**Positive**
- Easy to review: who can read each layer.
- Environment isolation is clear in the target design.

**Negative**
- Domain ownership is not expressed. At scale, teams may need domain catalogs.
- Masks that hash identifiers keep them linkable.

## Revisit when
More domains onboard, or access rules need to depend on data tags instead of schemas.
