# Decision: Corpus-Backed Memory Read Models

## Status

Accepted.

## Context

`generated/memory-objects/` originally projected curated examples and mechanic
fixtures. That made the object-facing catalog useful for teaching and smoke
checks, but it left downstream recall without a machine-visible distinction
between examples and reviewed memory truth.

After adding `memo/` as the reviewed corpus district, the read-model builder
needed to consume `memo/objects/**/object.json` without losing the existing
teaching fixtures.

## Decision

Change `scripts/memory/generate_memory_object_surfaces.py` to build
object-facing read models from two source classes:

- `reviewed_corpus`: reviewed object bundles under `memo/objects/`
- `teaching_fixture`: examples listed by
  `examples/generated-surfaces/memory_object_surface_manifest.json`

Generated catalog, capsule, and section rows include `source_kind` so consumers
can filter reviewed corpus objects from examples.

The generated surface source id becomes `aoa-memo-object-read-models-v2`.
The example manifest keeps its own source id,
`aoa-memo-object-example-surfaces-v1`, because it still only owns teaching
fixture selection.

## Consequences

- `generated/memory-objects/*` now includes the reviewed corpus decision object
  from `memo/objects/decisions/2026/reviewed-corpus-district/object.json`.
- Existing examples remain available for docs, schemas, and regression
  coverage.
- MCP, KAG, eval, and recall consumers can prefer `source_kind:
  reviewed_corpus` without discarding fixture-based teaching material.
- Generated surfaces remain read models; `memo/objects/` remains reviewed
  object truth.

## Validation

```bash
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memory_object_surfaces.py
python -m pytest -q tests/memory/test_memo_corpus.py tests/memory/test_memo_validators.py
```
