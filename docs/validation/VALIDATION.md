# VALIDATION.md

On-demand human procedure for `docs/validation/AGENTS.md`.

## On-demand procedure

### Preserved route from `docs/validation/AGENTS.md`

This surface owns only the focused or composite invocations shown here; linked parent routes own wider/shared lanes.
```bash
python scripts/root-topology/validate_validator_topology.py
python -m pytest -q tests/root-topology/test_validator_topology.py tests/root-topology/test_validation_lanes.py
```
