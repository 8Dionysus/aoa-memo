# AGENTS.md

Route card for `generated/memory-objects/`.

## Purpose

This district holds generated object-facing catalog, capsule, and section
surfaces.

## Source

Reviewed corpus objects live under `memo/objects/**/object.json`.
Teaching fixtures live under `examples/memory-objects/`, `examples/phase-alpha/`,
`examples/lifecycle/`, mechanic example homes, and
`examples/generated-surfaces/memory_object_surface_manifest.json`.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `schemas/generated-surfaces/`.
- Downstream: consumers inspect compact catalog first, then open the source path.
  Use `source_kind` to distinguish reviewed corpus from teaching fixtures.

## Validate

```bash
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
```
