# Mechanic-local technical contracts Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/lineage-harvest/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- `mechanics/lineage-harvest/schemas/pattern_lineage_memory_entry_v1.json`
- `mechanics/lineage-harvest/examples/pattern_lineage_memory_entry.example.json`
- `mechanics/lineage-harvest/tests/test_lineage_harvest_mechanic.py`

## Contract

keeps the lineage-harvest schema, example, and regression boundary package-local

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
