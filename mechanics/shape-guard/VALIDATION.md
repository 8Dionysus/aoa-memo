# VALIDATION.md

On-demand human procedure for `mechanics/shape-guard/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/shape-guard/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/shape-guard/parts/via-negativa-checklist/tests/test_shape_guard_mechanic.py tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/shape-guard/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
