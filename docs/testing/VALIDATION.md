# VALIDATION.md

On-demand human procedure for `docs/testing/AGENTS.md`.

## On-demand procedure

### Preserved route from `docs/testing/AGENTS.md`

This surface owns only the focused or composite invocations shown here; linked parent routes own wider/shared lanes.
```bash
python -m pytest -q tests/root-topology/test_test_topology.py
python -m pytest -q tests/root-topology/test_validation_lanes.py
python -m pytest -q tests/root-topology/test_validator_topology.py
```
