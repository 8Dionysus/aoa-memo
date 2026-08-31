# VALIDATION.md

On-demand human procedure for `mechanics/checkpoint/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/checkpoint/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/checkpoint/parts/checkpoint-memory-boundary/tests/test_checkpoint_mechanic.py tests/memory/test_memo_schema_contracts.py tests/memory/test_memo_memory_context_boundaries.py mechanics/consumer-handoff/parts/downstream-feed-regression/tests tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py tests/root-topology/test_mechanic_artifact_topology.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/checkpoint/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
