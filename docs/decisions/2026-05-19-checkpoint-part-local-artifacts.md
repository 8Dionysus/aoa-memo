# Checkpoint Part-Local Artifacts

## Status

Accepted on 2026-05-19.

## Context

Checkpoint already had functioning `parts/` nodes, but its technical contract
was still parked at the package level. The inquiry checkpoint schema and
examples, checkpoint-to-memory schema and example, approval/health/improvement
examples, Phase Alpha checkpoint examples, and checkpoint regression test lived
under `mechanics/checkpoint/{schemas,examples,tests}`.

That kept checkpoint usable but not cleanly shaped for OS Abyss. The carry
packet, writeback mapping, approval/health record preservation, and package
boundary regression are different operations with different consumer routes.
Keeping them in one package bucket made the parts descriptive instead of fully
functional.

## Decision

Move checkpoint technical artifacts to the nearest functioning part:

- `inquiry_checkpoint` schema and examples under
  `mechanics/checkpoint/parts/checkpoint-carry-contract/`
- checkpoint-to-memory schema and example under
  `mechanics/checkpoint/parts/checkpoint-to-memory-mapping/`
- approval, health, improvement-thread, and checkpoint review examples under
  `mechanics/checkpoint/parts/approval-and-health-records/`
- the package boundary regression under
  `mechanics/checkpoint/parts/checkpoint-memory-boundary/tests/`

Keep recurrence-support and writeback as consumers of checkpoint artifacts, not
owners. Their refs point to the part-local surfaces, while checkpoint remains
the source owner for the checkpoint artifact and mapping.

## Consequences

- The checkpoint artifact inventory now reports checkpoint artifacts as
  `scope: part`, not package-owned.
- Writeback runtime target and intake generation read the part-local
  checkpoint-to-memory contract.
- Recurrence-support and consumer-handoff tests assert the new part-local
  checkpoint paths.
- The old package-level `mechanics/checkpoint/schemas`,
  `mechanics/checkpoint/examples`, and `mechanics/checkpoint/tests` paths are
  provenance only, not active homes.
- `aoa-memo` still does not execute checkpoints, own runtime state, grant role
  rights, dispatch return routes, prove checkpoint success, choreograph
  playbooks, or accept source-owner outcomes.

## Verification

Expected verification:

- `python -m pytest -q mechanics/checkpoint/parts/checkpoint-memory-boundary/tests tests/test_memo_validators.py mechanics/consumer-handoff/parts/downstream-feed-regression/tests/test_downstream_feed_contracts.py mechanics/consumer-handoff/parts/playbook-scope-handoff/tests/test_playbook_memory_scopes.py mechanics/recurrence-support/tests/test_recurrence_support_mechanic.py mechanics/writeback/parts/runtime-and-temperature/tests/test_runtime_writeback_part.py`
- `python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py --check`
- `python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py --check`
- `python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py --check`
- `python scripts/validate_memo_mechanics.py`
- `python scripts/validate_memo_mechanic_parts.py`
- `python scripts/validate_mechanic_artifact_topology.py`
- `python scripts/validate_memory_object_surfaces.py`
- `python scripts/validate_memo.py`
- `python scripts/release_check.py`
