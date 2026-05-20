# AGENTS.md

Route card for `examples/recall/`.

## Purpose

This district owns recall contract examples and operation-mode examples for
router-facing, object-facing, and task-facing memory access.

## Source

Examples here bind inspect, capsule, expand, scope, source-route, and
operation-mode posture. Doctrine routes to `docs/memory/MEMORY_MODEL.md` and
`docs/posture/MEMORY_OPERATION_MODES.md`.

## Route

- Up: `examples/AGENTS.md`, then `AGENTS.md`.
- Across: `schemas/recall-posture/`.
- Downstream: `generated/memory/` and `generated/memory-objects/`.

## Validate

```bash
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python scripts/memory/validate_memory_operations.py
```
