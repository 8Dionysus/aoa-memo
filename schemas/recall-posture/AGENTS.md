# AGENTS.md

Route card for `schemas/recall-posture/`.

## Purpose

This district owns recall, lifecycle, trust, operation-mode, and decay-posture
schemas used by memo recall contracts.

## Source

`recall_contract.schema.json` is the shared recall contract.
`memory_operation_mode.schema.json` binds task-level memory access posture.
Schemas here bind recall posture. Doctrine lives in `docs/posture/` and
`docs/memory/MEMORY_MODEL.md`.

## Route

- Up: `schemas/AGENTS.md`, then `AGENTS.md`.
- Across: `examples/recall/` and `docs/posture/`.
- Downstream: validators in `scripts/memory/`.

## Validate

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_memory_surfaces.py
```
