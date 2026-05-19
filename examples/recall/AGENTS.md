# AGENTS.md

Route card for `examples/recall/`.

## Purpose

This district owns recall contract examples for router-facing and
object-facing memory access.

## Source

Examples here bind inspect, capsule, expand, scope, and source-route posture.
Doctrine routes to `docs/memory/MEMORY_MODEL.md`.

## Route

- Up: `examples/AGENTS.md`, then `AGENTS.md`.
- Across: `schemas/recall-posture/`.
- Downstream: `generated/memory/` and `generated/memory-objects/`.

## Validate

```bash
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
```
