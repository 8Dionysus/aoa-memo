# Memory operational readouts stay memo-owned and source-owner bounded

## Memory

`aoa-memo` owns memo-side operational readouts for access-plane currentness,
source-intake wave coverage, and workspace memo-port status.

Those readouts help a distant agent inspect whether reviewed memory surfaces,
MCP access-plane expectations, local source intake, and workspace port status
line up. They do not move MCP runtime ownership out of `abyss-stack`, and they
do not move workspace topology ownership out of `8Dionysus`.

## Source Route

- `docs/decisions/0069-memory-operational-readouts.md`
- `generated/memory/access_plane_currentness.min.json`
- `generated/memory/source_intake_wave.min.json`
- `generated/memory/workspace_memo_port_status.min.json`
- `scripts/memory/build_memory_operational_readouts.py`
- `docs/memory/MEMORY_OPERATION_CYCLE.md`
- `docs/memory/LIVING_MEMORY_TOPOLOGY.md`

## Review Posture

This is a confirmed decision memory. It may be used for recall and routing, but
live MCP status still requires the live readout path and stronger runtime truth
from `abyss-stack`.

## Next Routes

- Use `python scripts/memory/build_memory_operational_readouts.py --check` for
  checked-in shape.
- Use `python scripts/memory/build_memory_operational_readouts.py --check --live`
  when live MCP currentness is the question.
- Use `8Dionysus` workspace memory map for source workspace topology.
