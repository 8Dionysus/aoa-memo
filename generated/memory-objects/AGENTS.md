# AGENTS.md

Route card for `generated/memory-objects/`.

## Purpose

This district holds generated object-facing catalog, capsule, and section
surfaces.

## Source

Source examples live under `examples/memory-objects/`, `examples/phase-alpha/`,
`examples/lifecycle/`, and `examples/generated-surfaces/`.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `schemas/generated-surfaces/`.
- Downstream: consumers inspect compact catalog first, then open source examples.

## Validate

```bash
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
```
