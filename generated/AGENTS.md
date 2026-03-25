# AGENTS.md

This file applies to checked-in artifacts under `generated/`.

## Important split

`generated/` contains three different memo surface classes:

- `memo_registry.min.json` is the compact machine-readable registry surface for the layer
- the doctrine family consists of `memory_catalog.json`, `memory_catalog.min.json`, `memory_capsules.json`, and `memory_sections.full.json`
- the object family consists of `memory_object_catalog.json`, `memory_object_catalog.min.json`, `memory_object_capsules.json`, and `memory_object_sections.full.json`

Do not treat every file here as the same kind of artifact.

## Source and derivation map

Keep this split explicit:

- `generated/memo_registry.min.json` is a source-authored registry contract validated by `scripts/validate_memo.py`
- the doctrine family is a checked-in router-facing memo surface family validated by `scripts/validate_memory_surfaces.py`
- the object family is generator-backed and is rebuilt by `scripts/generate_memory_object_surfaces.py` and checked by `scripts/validate_memory_object_surfaces.py`

The object family is derived from curated examples in `examples/memory_object_surface_manifest.json` and the referenced memory-object examples.

## Editing posture

For `memo_registry.min.json`:

- edit carefully because it is canonical memory-layer registry metadata
- preserve stable ids, schema refs, doc refs, and validation command listings unless semantics truly changed

For the doctrine family:

- keep `memory_catalog.json`, `memory_catalog.min.json`, `memory_capsules.json`, and `memory_sections.full.json` aligned as one readable family
- preserve stable surface ids and source paths unless the underlying doctrine changed
- do not turn router-facing surfaces into workflow policy or proof verdicts

For the object family:

- Do not hand-edit `memory_object_catalog.json`, `memory_object_catalog.min.json`, `memory_object_capsules.json`, or `memory_object_sections.full.json`
- regenerate the family from curated examples
- keep object-facing exports deterministic and reviewable

## Validation

When this directory changes, run the matching checks:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
```

If the object family changed, also run:

```bash
python scripts/generate_memory_object_surfaces.py
```
