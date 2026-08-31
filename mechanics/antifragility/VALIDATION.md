# VALIDATION.md

On-demand human procedure for `mechanics/antifragility/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/antifragility/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/antifragility/parts/failure-lesson-memory/tests mechanics/antifragility/parts/recovery-pattern-memory/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/antifragility/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
