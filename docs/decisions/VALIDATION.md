# VALIDATION.md

On-demand human procedure for `docs/decisions/AGENTS.md`.

## On-demand procedure

### Preserved route from `docs/decisions/AGENTS.md`

This surface owns only the focused or composite invocations shown here; linked parent routes own wider/shared lanes.
```bash
python scripts/root-topology/build_decision_indexes.py --check
python -m pytest -q tests
```
