# AGENTS.md

Route card for `schemas/support-objects/`.

## Purpose

This district owns support-object schemas that help memory objects preserve
source, lineage, and core-contract structure.

## Source

`core-memory-contract.schema.json`, `provenance_thread.schema.json`, and
`reviewed_intake_landing_receipt.schema.json` are source contracts. Meaning
routes to `docs/memory/NARRATIVE_CORE_CONTRACT.md`,
`docs/posture/PROVENANCE_THREADS.md`, and `memo/OBJECT_SHAPE.md`.

## Route

- Up: `schemas/AGENTS.md`, then `AGENTS.md`.
- Across: `examples/support-objects/` and `memo/intake/receipts/`.
- Downstream: `generated/memory/` registry surfaces and reviewed corpus checks.

## Validate

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memo_corpus.py
```
