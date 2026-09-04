# VALIDATION.md

On-demand human procedure for `scripts/AGENTS.md`.

## On-demand procedure

### Preserved route from `scripts/AGENTS.md`

Shared executable routes remain owned by [`config/VALIDATION.md`](../config/VALIDATION.md), [`docs/validation/VALIDATION.md`](../docs/validation/VALIDATION.md), [`examples/VALIDATION.md`](../examples/VALIDATION.md), [`generated/VALIDATION.md`](../generated/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_growth_refinery_writeback_lanes.py
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_phase_alpha_writeback_map.py
```
