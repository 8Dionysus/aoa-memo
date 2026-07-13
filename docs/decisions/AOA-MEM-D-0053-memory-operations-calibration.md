# Memory Operations Calibration

- Decision ID: AOA-MEM-D-0053

## Status

Accepted on 2026-05-19.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: memory doctrine
- Mechanic parents: none
- Guard families: memory surface
- Memory object classes: none
- Posture: active rationale

## Context

The strategic calibration plan in
`/home/dionysus/Документы/PLANS_TMP/2026-05-19-aoa-memo-memory-ops-calibration`
identified several missing practical surfaces: write-path guardrails against
poisoned memory, one compact memory operation cycle, consolidation and
forgetting as an operation, operation modes, wider eval handoff cases,
KAG/temporal graph bridge refs, reviewed runtime and host intake, and a living
topology for local memory ports.

The repository already had mechanics, docs districts, schemas, examples,
generated indexes, and AGENTS route cards. The missing piece was not another
flat plan; it was a calibrated operational layer that agents can use during
real OS Abyss work.

## Decision

Land memory operations as bounded, validated surfaces:

- general cycle and topology docs live in `docs/memory/`
- write-path boundary language lives in `docs/boundaries/`
- operation modes live in `docs/posture/`, with schema and example under
  `schemas/recall-posture/` and `examples/recall/`
- poisoned or untrusted writes are handled by a new
  `mechanics/operational-gate/parts/write-path-guardrails/` part
- consolidation, supersession, archive, retraction, and freeze are handled by a
  new `mechanics/retention/parts/consolidation-and-forgetting/` part
- KAG temporal graph edges extend the existing KAG/ToS bridge handoff part
- reviewed runtime and host intake extends the existing writeback runtime and
  temperature part
- `scripts/memory/validate_memory_operations.py` becomes the machine-checkable
  gate for this operational layer

## Consequences

- `aoa-memo` now has a practical memory cycle instead of only separate
  doctrine fragments.
- Untrusted input, prompt-injected text, sleeper memory, poisoned experience,
  derivation lineage, and action-safety separation are visible before memory is
  written.
- Forgetting is not silent deletion; it is a reviewed lifecycle operation with
  audit refs.
- Local `memo/` ports can exist across the system without becoming second
  canons, because promotion routes through reviewed intake.
- Graph edges can help recall while preserving backward refs to authored memory
  objects, provenance threads, lifecycle, and stronger owner routes.
- Runtime and host layers send reviewed packets, not raw streams.

## Affected Surfaces

- `docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md`
- `docs/memory/MEMORY_OPERATION_CYCLE.md`
- `docs/memory/LIVING_MEMORY_TOPOLOGY.md`
- `docs/memory/LOCAL_MEMO_PORT_STANDARD.md`
- `docs/posture/MEMORY_OPERATION_MODES.md`
- `mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md`
- `mechanics/operational-gate/parts/write-path-guardrails/`
- `mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md`
- `mechanics/retention/parts/consolidation-and-forgetting/`
- `mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/`
- `mechanics/writeback/parts/runtime-and-temperature/`
- `schemas/recall-posture/memory_operation_mode.schema.json`
- `examples/recall/memory_operation_modes.example.json`
- `scripts/memory/validate_memory_operations.py`
- `tests/memory/test_memory_operations.py`
- `config/mechanics/memo_mechanics.json`
- `config/root-topology/root_technical_districts.json`
- `generated/memory/memo_registry.min.json`

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
