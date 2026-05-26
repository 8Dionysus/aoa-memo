# Agon Part-Local Artifacts

- Decision ID: AOA-MEM-D-0045

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-19
- Legacy path: docs/decisions/2026-05-19-agon-part-local-artifacts.md
- Surface classes: mechanic package, mechanic part
- Mechanic parents: agon
- Guard families: mechanic topology, part and payload
- Memory object classes: none
- Posture: active rationale

## Context

The physical `parts/` layer made each active mechanic part reviewable, but
Agon still carried its runnable technical artifacts at package level:
`config/`, `examples/`, `generated/`, `schemas/`, `scripts/`, `tests/`, and
`manifests/`.

That was better than root sprawl, but weaker than the OS Abyss mechanics shape
used by `Agents-of-Abyss`, `aoa-skills`, and `aoa-techniques`, where parts can
own their own runnable companions when a sub-operation has enough technical
weight.

## Decision

Move Agon single-part technical artifacts into the nearest functioning part:

- `parts/prebinding-and-candidate-intake/` owns memo prebindings and
  retention-rank candidate intake companions.
- `parts/bridge-and-evidence-seams/` owns epistemic, KAG, SLC, Sophian, VDS,
  and mechanical-trial memo bridge companions.
- `parts/stage-landing-and-stop-lines/` owns stage recurrence manifests and hook
  bindings.

Extend `generated/mechanic_artifacts.min.json` so the inventory recognizes both
package-local and part-local homes. Extend readiness so part-local test
directories count as local mechanic validation routes.

## Consequences

- Agon parts are now runnable owner units, not only contract headings.
- Package-level Agon technical homes stop acting as a second owner layer for
  sub-operations that already have parts.
- Future artifact moves can use the same inventory/readiness contract rather
  than adding special-case validators.
- The change does not grant Agon proof, runtime, role authority, KAG truth,
  source doctrine, or owner acceptance inside `aoa-memo`.

## Validation

This decision is validated through:

```bash
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_memo_prebindings.py
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_retention_rank_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_epistemic_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_kag_memo_evidence_package_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_mechanical_trial_memo_intakes.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_slc_memo_bridge_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_sophian_memo_evidence_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_vds_memo_bridge.py
python -m pytest -q mechanics/agon/parts/prebinding-and-candidate-intake/tests mechanics/agon/parts/bridge-and-evidence-seams/tests mechanics/agon/parts/stage-landing-and-stop-lines/tests
python scripts/validate_mechanic_artifact_inventory.py
python scripts/validate_memo_mechanic_readiness.py
python scripts/release_check.py
```
