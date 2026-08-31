# VALIDATION.md

On-demand human procedure for `mechanics/governance/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/governance/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/governance/parts/governance-boundary/tests tests/mechanics/test_memo_mechanics.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/governance/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
