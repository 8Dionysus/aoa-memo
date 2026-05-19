# AGENTS.md

Route card for `examples/generated-surfaces/`.

## Purpose

This district owns source manifests for generated memory-object companion
surfaces.

## Source

`memory_object_surface_manifest.json` is source-authored and drives
`generated/memory-objects/`.

## Route

- Up: `examples/AGENTS.md`, then `AGENTS.md`.
- Across: `schemas/generated-surfaces/`.
- Downstream: `scripts/memory/generate_memory_object_surfaces.py`.

## Validate

```bash
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
```
