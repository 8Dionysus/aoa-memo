# AGENTS.md

Route card for `docs/memory/`.

## Purpose

This district owns current memory doctrine: the memory model, memory object
profiles, operation cycle, living topology, local memo ports, and
narrative/core support-object contract.

## Source

Source truth lives in `MEMORY_MODEL.md`, `MEMORY_OBJECT_PROFILES.md`,
`MEMORY_OPERATION_CYCLE.md`, `LIVING_MEMORY_TOPOLOGY.md`,
`LOCAL_MEMO_PORT_STANDARD.md`, `MEMO_PORT_INDEXING_VOCABULARY.md`, and
`NARRATIVE_CORE_CONTRACT.md`. Generated memory companions must route back here
instead of authoring doctrine.

## Route

- Up: `docs/AGENTS.md`, then `AGENTS.md`.
- Across: `docs/posture/` for trust, lifecycle, temperature, operation modes,
  and provenance.
- Downstream: `schemas/memory-objects/`, `schemas/support-objects/`,
  `schemas/memory-ports/`, `examples/memory-objects/`,
  `examples/memory-ports/`, `examples/recall/`, and `generated/memory/`.

## Validate

```bash
python scripts/memory/validate_memo.py --profile schema
python scripts/memory/validate_memo.py --profile memory-context
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_local_memo_port.py --path examples/memory-ports/example-port
```
