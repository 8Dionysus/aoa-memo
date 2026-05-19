# AGENTS.md

Route card for `schemas/memory-objects/`.

## Purpose

This district owns shared memory object schemas and the per-kind object profile
contract.

## Source

Schemas here are source contracts for root memory-object examples and generated
object surfaces.
Start from `memory_object.schema.json` before editing kind-specific schemas.

## Route

- Up: `schemas/AGENTS.md`, then `AGENTS.md`.
- Across: `docs/memory/MEMORY_OBJECT_PROFILES.md`.
- Downstream: `examples/memory-objects/`, `examples/phase-alpha/`, and
  `generated/memory-objects/`.

## Validate

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_object_surfaces.py
```
