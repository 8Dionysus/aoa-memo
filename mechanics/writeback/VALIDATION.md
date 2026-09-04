# VALIDATION.md

On-demand human procedure for `mechanics/writeback/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/writeback/AGENTS.md`

Shared executable routes remain owned by [`examples/VALIDATION.md`](../../examples/VALIDATION.md), [`mechanics/VALIDATION.md`](../VALIDATION.md), [`schemas/memory-objects/VALIDATION.md`](../../schemas/memory-objects/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py --check
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py --check
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py --check
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_growth_refinery_writeback_lanes.py --check
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_phase_alpha_writeback_map.py --check
python -m pytest -q mechanics/writeback/parts mechanics/consumer-handoff/parts/downstream-feed-regression/tests tests/mechanics/test_cross_mechanic_operational_contracts.py
```
This surface owns only the focused or composite invocations shown here; linked parent routes own wider/shared lanes.
