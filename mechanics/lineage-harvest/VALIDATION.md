# VALIDATION.md

On-demand human procedure for `mechanics/lineage-harvest/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/lineage-harvest/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/lineage-harvest/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
