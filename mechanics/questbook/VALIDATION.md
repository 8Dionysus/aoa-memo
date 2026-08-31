# VALIDATION.md

On-demand human procedure for `mechanics/questbook/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/questbook/AGENTS.md`

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/questbook/parts/source-contract/tests tests/memory/test_memo_questbook_boundaries.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/questbook/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
