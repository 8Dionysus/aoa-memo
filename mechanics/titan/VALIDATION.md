# VALIDATION.md

On-demand human procedure for `mechanics/titan/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/titan/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/titan/parts/recall-and-remembrance-posture/tests mechanics/titan/parts/audit-personality-and-swarm-policy/tests
python -m pytest -q mechanics/titan/parts/recall-and-remembrance-posture/tests mechanics/titan/parts/closeout-and-digest-posture/tests mechanics/titan/parts/audit-personality-and-swarm-policy/tests
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/titan/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
