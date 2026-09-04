# VALIDATION.md

On-demand human procedure for `config/AGENTS.md`.

## On-demand procedure

### Preserved route from `config/AGENTS.md`

Shared executable routes remain owned by [`docs/memory/VALIDATION.md`](../docs/memory/VALIDATION.md), [`docs/root/VALIDATION.md`](../docs/root/VALIDATION.md), [`docs/validation/VALIDATION.md`](../docs/validation/VALIDATION.md), [`generated/agents/VALIDATION.md`](../generated/agents/VALIDATION.md), [`generated/root-topology/VALIDATION.md`](../generated/root-topology/VALIDATION.md), [`mechanics/VALIDATION.md`](../mechanics/VALIDATION.md), [`scripts/agents/VALIDATION.md`](../scripts/agents/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python -m pytest -q tests/root-topology/test_validation_lanes.py tests/root-topology/test_validator_topology.py tests/root-topology/test_ci_gate.py tests/root-topology/test_release_check.py
```
