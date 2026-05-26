# Decision: Memory operational readouts stay memo-owned and source-owner bounded

- Decision ID: AOA-MEM-D-0069

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-25
- Surface classes: memory doctrine, generated/readout
- Mechanic parents: none
- Guard families: generated/read-model, memory surface
- Memory object classes: decision
- Posture: active rationale

## Context

The memory-organ foundation identified two immediate operational gaps:
access-plane currentness and workspace memo-port status. A distant agent needs
a small, inspectable route from `aoa-memo` to answer whether the MCP access
plane, reviewed read models, local ports, and workspace memory map currently
line up.

The strongest source owners are split. `abyss-stack` owns the `aoa_memo` MCP
runtime. `8Dionysus` owns the workspace memory overlay map. Source
repositories own raw local memory candidates and acceptance. `aoa-memo` owns
reviewed memory posture, object recall, lifecycle, and consumer handoff
contracts.

## Decision

Add a generated operational readout family under `generated/memory/`:

- `access_plane_currentness.min.json`
- `source_intake_wave.min.json`
- `workspace_memo_port_status.min.json`

The family is rebuilt by
`scripts/memory/build_memory_operational_readouts.py`. In a live workspace it
can run MCP probes with `--live`; in release or CI it validates checked-in
shape and source-owner boundaries without requiring the external MCP checkout
or workspace map to be present.

The readouts belong to `aoa-memo` as memory interpretation and route evidence,
not as authority over MCP runtime or workspace topology.

## Alternatives

- Put all status in `8Dionysus`. Rejected because a distant memory consumer
  entering through `aoa-memo` still needs a memo-side inspect surface.
- Move MCP currentness into `abyss-stack` only. Rejected because the runtime
  owner can prove service behavior, but memo still needs to state whether the
  output aligns with reviewed memory surfaces and recall boundaries.
- Make `aoa-memo` generate the workspace map directly. Rejected because that
  would move workspace topology authority out of `8Dionysus`.
- Add another prose-only status document. Rejected because the goal is a
  repeatable readout that agents and validators can inspect.

## Consequences

- Agents can inspect access-plane currentness, source-lane intake wave
  coverage, and workspace memo-port status from `aoa-memo`.
- The release gate can protect the shape and owner-boundary contract without
  requiring live workspace services in CI.
- A live workspace should run
  `python scripts/memory/build_memory_operational_readouts.py --check --live`
  when MCP currentness is the question.
- Known gaps, such as fresh source-doc terms not yet appearing in reviewed
  corpus search, are routed as gaps rather than hidden or treated as proof.
- `AOA-MEM-Q-0010`, `AOA-MEM-Q-0011`, and `AOA-MEM-Q-0015` close as
  operational readout slices, not as claims that all future object population,
  lifecycle, or eval loops are done.

## Affected Surfaces

- `generated/memory/access_plane_currentness.min.json`
- `generated/memory/source_intake_wave.min.json`
- `generated/memory/workspace_memo_port_status.min.json`
- `scripts/memory/build_memory_operational_readouts.py`
- `docs/memory/MEMORY_OPERATION_CYCLE.md`
- `docs/memory/LIVING_MEMORY_TOPOLOGY.md`
- `config/root-topology/root_technical_districts.json`
- `generated/root-topology/root_technical_districts.min.json`
- `quests/memo/done/AOA-MEM-Q-0010.yaml`
- `quests/memo/done/AOA-MEM-Q-0011.yaml`
- `quests/memo/done/AOA-MEM-Q-0015.yaml`

## Verification

Use:

```bash
python scripts/memory/build_memory_operational_readouts.py --check --live
python scripts/memory/build_memory_operational_readouts.py --check
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python scripts/release/release_check.py
```
