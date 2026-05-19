# AGENTS.md

Route card for `schemas/support-objects/`.

## Purpose

This district owns support-object schemas that help memory objects preserve
source, lineage, and core-contract structure.

## Source

`core-memory-contract.schema.json` and `provenance_thread.schema.json` are
source contracts. Meaning routes to `docs/memory/NARRATIVE_CORE_CONTRACT.md`
and `docs/posture/PROVENANCE_THREADS.md`.

## Route

- Up: `schemas/AGENTS.md`, then `AGENTS.md`.
- Across: `examples/support-objects/`.
- Downstream: `generated/memory/` registry surfaces.

## Validate

```bash
python scripts/memory/validate_memo.py
```
