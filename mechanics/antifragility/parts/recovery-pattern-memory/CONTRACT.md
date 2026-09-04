# Recovery pattern memory Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/antifragility/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and historical placement is recorded in `../../PROVENANCE.md`.

## Source Surfaces

- [RECOVERY_PATTERN_MEMORY](../../docs/RECOVERY_PATTERN_MEMORY.md)
- [RECOVERY_PATTERN_RECALL](../../docs/RECOVERY_PATTERN_RECALL.md)
- [ROLLBACK_FOLLOWTHROUGH_PATTERN](../../docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md)
- `schemas/recovery_pattern_memory_v1.json`
- `examples/recovery_pattern_memory.example.json`
- `examples/recovery_pattern_memory.lineage.example.json`
- `examples/recovery_pattern_memory.rollout.example.json`
- `examples/recovery_pattern_memory.rollback_followthrough.example.json`
- `examples/recovery_pattern_memory.component_refresh.example.json`
- `examples/pattern.antifragility-stress-recovery-window.example.json`
- `tests/test_antifragility_recovery_patterns.py`

## Contract

keeps reviewed recovery windows recallable without authorizing rollback or route behavior

## Artifact Contract

The part keeps the recovery pattern contract, recovery examples,
rollback-followthrough and component-refresh examples, native pattern source,
and local regression together. The native pattern example stays here because it
feeds recovery-pattern generated object surfaces without making this part a
router, proof layer, or rollback authority.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
