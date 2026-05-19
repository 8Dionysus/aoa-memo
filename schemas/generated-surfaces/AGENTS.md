# AGENTS.md

Route card for `schemas/generated-surfaces/`.

## Purpose

This district owns schemas for generated memory-object companion surfaces.

## Source

`memory_object_catalog.schema.json` anchors the generated object catalog shape.
Schemas here validate generated mirrors. The source examples remain in
`examples/generated-surfaces/` and `examples/memory-objects/`.

## Route

- Up: `schemas/AGENTS.md`, then `AGENTS.md`.
- Across: `generated/memory-objects/`.
- Downstream: `scripts/memory/generate_memory_object_surfaces.py`.

## Validate

```bash
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
```
