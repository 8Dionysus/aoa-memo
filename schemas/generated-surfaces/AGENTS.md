# AGENTS.md

Route card for `schemas/generated-surfaces/`.

## Purpose

This district owns schemas for generated memory-object companion surfaces.

## Source

`memory_object_catalog.schema.json` anchors the generated object catalog shape.
Schemas here validate generated mirrors. Reviewed object sources live in
`memo/objects/`; teaching fixtures remain in `examples/generated-surfaces/`,
`examples/memory-objects/`, and mechanic example homes. Generated rows use
`source_kind` to distinguish the source class.

## Route

- Up: `schemas/AGENTS.md`, then `AGENTS.md`.
- Across: `generated/memory-objects/`.
- Downstream: `scripts/memory/generate_memory_object_surfaces.py`.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
