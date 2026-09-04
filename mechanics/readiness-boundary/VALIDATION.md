# VALIDATION.md

On-demand human procedure for `mechanics/readiness-boundary/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/readiness-boundary/AGENTS.md`

Shared executable routes remain owned by [`docs/VALIDATION.md`](../../docs/VALIDATION.md), [`generated/agents/VALIDATION.md`](../../generated/agents/VALIDATION.md), [`mechanics/VALIDATION.md`](../VALIDATION.md), [`scripts/agents/VALIDATION.md`](../../scripts/agents/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python -m pytest -q mechanics/readiness-boundary/parts tests/memory/test_memo_memory_context_boundaries.py tests/root-topology/test_current_direction_routes.py tests/root-topology/test_mechanic_artifact_topology.py tests/mechanics/test_memo_mechanics.py
```
This surface owns only the focused or composite invocations shown here; linked parent routes own wider/shared lanes.
