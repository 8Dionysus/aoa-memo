# Agon Parts Index

Functioning Agon memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Prebinding and candidate intake](prebinding-and-candidate-intake/README.md) - keeps candidate memory explicit before any stronger Agon write
- [Bridge and evidence seams](bridge-and-evidence-seams/README.md) - keeps evidence and bridge memory source-linked without owning downstream truth
- [Quest follow-through](quest-follow-through/README.md) - keeps Agon-specific follow-through in the public Questbook item store with owner-routed memo stop-lines
- [Wave landing and stop-lines](wave-landing-and-stop-lines/README.md) - keeps landing history reviewable without promoting it to source Agon law

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
