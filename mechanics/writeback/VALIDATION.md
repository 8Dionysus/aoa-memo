# VALIDATION.md

On-demand human procedure for `mechanics/writeback/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/writeback/AGENTS.md`

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/generate_memory_object_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_targets.py --check
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_intake.py --check
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py --check
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_growth_refinery_writeback_lanes.py --check
python mechanics/writeback/parts/growth-and-continuity/scripts/generate_phase_alpha_writeback_map.py --check
python -m pytest -q mechanics/writeback/parts/runtime-and-temperature/tests mechanics/writeback/parts/quest-and-chronicle/tests mechanics/writeback/parts/revision-ledgers/tests mechanics/writeback/parts/rollback-and-recovery/tests mechanics/writeback/parts/growth-and-continuity/tests mechanics/writeback/parts/receipt-publication-regression/tests mechanics/consumer-handoff/parts/downstream-feed-regression/tests tests/mechanics/test_cross_mechanic_operational_contracts.py
```
```bash
python scripts/release/release_check.py
```

<!-- Preserved on-demand procedure from `mechanics/writeback/docs/VALIDATION.md`. -->
# VALIDATION.md

On-demand human procedure for this route.

## On-demand procedure
