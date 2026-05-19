# Lineage Harvest Parts Index

Functioning Lineage Harvest memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Pattern-lineage memory gate](pattern-lineage-memory-gate/README.md) - gates cross-repo recurring signals into reviewed pattern-lineage memory candidates without federation authority
- [Mechanic-local technical contracts](mechanic-local-technical-contracts/README.md) - keeps the lineage-harvest schema, example, and regression boundary package-local
- [Adjacent mechanic interfaces](adjacent-mechanic-interfaces/README.md) - routes stronger adjacent memory operations without absorbing their authority
- [Generated companions](generated-companions/README.md) - exposes compact mirrors while keeping lineage-harvest source truth in package docs and artifacts

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
