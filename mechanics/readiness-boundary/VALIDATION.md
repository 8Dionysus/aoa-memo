# VALIDATION.md

On-demand human procedure for `mechanics/readiness-boundary/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/readiness-boundary/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/readiness-boundary/parts/memory-readiness-boundary/tests/test_readiness_boundary_mechanic.py tests/memory/test_memo_memory_context_boundaries.py tests/root-topology/test_current_direction_routes.py tests/root-topology/test_mechanic_artifact_topology.py tests/mechanics/test_memo_mechanics.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/readiness-boundary/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
