# VALIDATION.md

On-demand human procedure for `mechanics/retention/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/retention/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/validate_memory_operations.py
python -m pytest -q mechanics/retention/parts/consolidation-and-forgetting/tests mechanics/retention/parts/cross-repo-and-governance-retention/tests mechanics/retention/parts/office-markers/tests mechanics/retention/parts/post-release-retention/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/retention/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
