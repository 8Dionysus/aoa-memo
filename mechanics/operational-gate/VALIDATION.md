# VALIDATION.md

On-demand human procedure for `mechanics/operational-gate/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/operational-gate/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_operations.py
python -m pytest -q mechanics/operational-gate/parts/deployment-incident-gate/tests mechanics/operational-gate/parts/write-path-guardrails/tests mechanics/operational-gate/parts/post-release-boundaries/tests tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/operational-gate/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
