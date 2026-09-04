# VALIDATION.md

On-demand human procedure for `generated/AGENTS.md`.

## On-demand procedure

### Preserved route from `generated/AGENTS.md`

Shared executable routes remain owned by `docs/VALIDATION.md`, `docs/memory/VALIDATION.md`, `docs/root/VALIDATION.md`, `examples/VALIDATION.md`, `generated/agents/VALIDATION.md`, `generated/memory/VALIDATION.md`, `generated/quests/VALIDATION.md`, `generated/root-topology/VALIDATION.md`, `mechanics/VALIDATION.md`, `schemas/memory-objects/VALIDATION.md`, `scripts/VALIDATION.md`; follow that on-demand lane for this surface.
```bash
python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py
python mechanics/writeback/parts/runtime-and-temperature/scripts/generate_runtime_writeback_governance.py
```

## Generated builders

Shared executable routes remain owned by `docs/memory/VALIDATION.md`; follow that on-demand lane for this surface.
```bash
python scripts/agents/build_agents_mesh_index.py
python scripts/root-topology/build_root_technical_districts_index.py
```
