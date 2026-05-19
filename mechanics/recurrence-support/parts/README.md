# Recurrence Support Parts Index

Functioning Recurrence Support memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Route-return anchors](route-return-anchors/README.md) - preserves checkpoint continuity, relaunch anchors, return packs, and anti-`return_memory` stop-lines
- [Witness trace contract](witness-trace-contract/README.md) - keeps witness trace exports reviewable and maps later writeback into existing memo object kinds
- [Reviewed closeout recall landing](reviewed-closeout-recall-landing/README.md) - preserves owner-local recall survivors without becoming proof, playbook authority, or a second route ledger

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
