# 03. Security and Governance

## Personas and access
| Persona | Bronze | Silver | Gold | Sees raw IDs | Notes |
|---|---|---|---|---|---|
| Engineers | Read/write | Read/write | Read/write | Yes | Operate the pipeline and landing volume |
| Analysts | No | No | Read | n/a | Business reporting |
| Regional analysts (SP) | No | No | Read, SP rows only | n/a | Row filter on Gold |
| Data scientists | No | Read | Read | No (hashed) | Hash keeps joins and distinct counts working |
| Compliance | Read | Read | Read | Yes | Audit and investigation |

## Controls
- **Column masks** on `silver.customers` (`customer_unique_id`, `zip_prefix`)
- **Row filter** on `gold.sales_by_state`
- **Grants to groups**, never to individuals
- **Lineage** from Unity Catalog for impact analysis

## Status
| Control | Status |
|---|---|
| Masks and row filter | Designed |
| Group-based grants | Designed (Free Edition limits may apply) |
| Audit via system tables | Not yet |

## Known limitations
- Row filters on pipeline tables are Public Preview.
- Masks hash the ID, so it stays linkable across datasets. Consider that when judging re-identification risk.
- Free Edition restricts account-level group administration.
