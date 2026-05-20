# AGENTS.md

Route card for `schemas/memory-ports/`.

## Purpose

This schema district defines local `memo/` port contracts.
It validates port metadata, local candidates, receipts, exports, and generated
local port indexes before any reviewed intake route reaches `aoa-memo`.

## Route

- Up: `schemas/AGENTS.md`, then root `AGENTS.md`.
- Doctrine: `docs/memory/LOCAL_MEMO_PORT_STANDARD.md`.
- Vocabulary: `docs/memory/MEMO_PORT_INDEXING_VOCABULARY.md`.
- Examples: `examples/memory-ports/`.
- Validation: `scripts/memory/validate_local_memo_port.py`.

## Boundary

These schemas validate local memory packet shape. They do not define durable
reviewed memory objects and do not authorize direct writes into `aoa-memo`.

