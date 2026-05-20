# Runtime and temperature

This active part belongs to `mechanics/writeback/` and materializes the matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- [RUNTIME_WRITEBACK_SEAM](../../docs/RUNTIME_WRITEBACK_SEAM.md)
- [WRITEBACK_TEMPERATURE_POLICY](../../docs/WRITEBACK_TEMPERATURE_POLICY.md)

## Function

keeps runtime writeback mapped without runtime ownership

## Local Artifacts

- `schemas/runtime-writeback-targets.schema.json`
- `schemas/reviewed_memory_intake_packet_v1.json`
- `examples/reviewed_memory_intake_packet.abyss-stack.example.json`
- `examples/reviewed_memory_intake_packet.abyss-machine.example.json`
- `generated/runtime_writeback_targets.min.json`
- `generated/runtime_writeback_intake.min.json`
- `generated/runtime_writeback_governance.min.json`
- `scripts/generate_runtime_writeback_targets.py`
- `scripts/generate_runtime_writeback_intake.py`
- `scripts/generate_runtime_writeback_governance.py`
- `tests/test_runtime_writeback_part.py`

## Next Route

Use `../../OWNER_MAP.md` for stronger owner routing and `../../PROVENANCE.md` for placement history.
