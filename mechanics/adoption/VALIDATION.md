# VALIDATION.md

On-demand human procedure for `mechanics/adoption/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/adoption/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/adoption/parts/adoption-boundary/tests mechanics/adoption/parts/revision-and-retention-pressure/tests mechanics/adoption/parts/scar-and-routing-adoption/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/adoption/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
