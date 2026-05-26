# Final Mechanic Part-Local Artifacts

- Decision ID: AOA-MEM-D-0049

## Status

Accepted on 2026-05-19.

## Index Metadata

- Original date: 2026-05-19
- Legacy path: docs/decisions/2026-05-19-final-mechanic-part-artifacts.md
- Surface classes: mechanic package, mechanic part
- Mechanic parents: none
- Guard families: mechanic topology, part and payload
- Memory object classes: none
- Posture: active rationale

## Context

Most memo mechanic packages had already moved their schemas, examples, tests,
scripts, generated companions, manifests, and config seeds into functioning
`parts/` homes. The remaining package-scope artifacts were small, but they
kept a two-layer model alive: active parts described the operation while the
executable contract still sat at the package root.

For OS Abyss, parts must be functional operation nodes, not labels over a
package-level technical bin.

## Decision

Move the remaining package-level artifacts to the nearest owning part:

- shape-guard regression to `parts/via-negativa-checklist/tests/`
- readiness-boundary schema, example, and regression to
  `parts/memory-readiness-boundary/{schemas,examples,tests}/`
- recurrence-support witness trace schema, example, and regression to
  `parts/witness-trace-contract/{schemas,examples,tests}/`
- lineage-harvest schema, example, and regression to
  `parts/pattern-lineage-memory-gate/{schemas,examples,tests}/`
- Questbook source validator and regression to
  `parts/source-contract/{scripts,tests}/`
- Questbook read-model projection builder to `parts/quest-read-model-projections/scripts/`

Remove the lineage-harvest `mechanic-local-technical-contracts` active part
because it named a file family rather than an operation. The
pattern-lineage-memory-gate part now owns its technical contract directly.

## Alternatives

Leaving the remaining files at package level would preserve shorter paths but
would keep package scope as a quiet artifact sink after the system had adopted
functional parts.

Keeping a `mechanic-local-technical-contracts` part in lineage-harvest would
avoid deleting a directory, but it would contradict the operation-first rule:
parts name work, not storage categories.

Moving root Questbook generated outputs under the package was rejected. Those
outputs are root-published read models over the public `quests/` item store;
their builder and validator are part-local, but the quest read-model projections remain
root surfaces.

## Consequences

`generated/mechanic_artifacts.min.json` should now report no `scope: package`
entries. Remaining root technical districts are shared, repo-wide, or
root-published by explicit exception rather than residual package convenience.

The move keeps `aoa-memo` below stronger owners. It does not create proof,
runtime execution, route dispatch, role rights, KAG substrate truth, playbook
choreography, stats truth, Tree-of-Sophia canon, source-owner acceptance, or
private memory.

## Affected Surfaces

- `mechanics/shape-guard/parts/via-negativa-checklist/`
- `mechanics/readiness-boundary/parts/memory-readiness-boundary/`
- `mechanics/recurrence-support/parts/witness-trace-contract/`
- `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/`
- `mechanics/questbook/parts/source-contract/`
- `mechanics/questbook/parts/quest-read-model-projections/`
- package `PARTS.md`, `PROVENANCE.md`, `LANDING_LOG.md`, and validation cards
- `mechanics/ARTIFACT_TOPOLOGY.md`
- `config/root_technical_districts.json`
- generated mechanics, readiness, landing, AGENTS mesh, and memo registry
  companions

## Verification

Expected verification:

- `python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py`
- `python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check`
- `python -m pytest -q mechanics/shape-guard/parts/via-negativa-checklist/tests mechanics/readiness-boundary/parts/memory-readiness-boundary/tests mechanics/recurrence-support/parts/witness-trace-contract/tests mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/tests mechanics/questbook/parts/source-contract/tests`
- `python scripts/build_mechanic_artifact_inventory.py --check`
- `python scripts/validate_mechanic_artifact_inventory.py`
- `python scripts/validate_memo_mechanic_parts.py`
- `python scripts/build_memo_mechanic_landing_logs.py --check`
- `python scripts/validate_memo_mechanic_landing_logs.py`
- `python scripts/build_memo_mechanic_readiness.py --check`
- `python scripts/validate_memo_mechanic_readiness.py`
- `python scripts/build_agents_mesh_index.py --check`
- `python scripts/validate_agents_mesh_index.py`
- `python scripts/validate_memo.py`
- `python scripts/release_check.py`
