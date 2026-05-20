# AGENTS.md

Route card for `examples/memory-ports/`.

## Purpose

This district holds public-safe examples for local `memo/` port contracts.
The example port demonstrates packet-first candidate, receipt, export, and
index surfaces without becoming durable reviewed memory.

## Route

- Up: `examples/AGENTS.md`, then root `AGENTS.md`.
- Schemas: `schemas/memory-ports/`.
- Doctrine: `docs/memory/LOCAL_MEMO_PORT_STANDARD.md`.
- Vocabulary: `docs/memory/MEMO_PORT_INDEXING_VOCABULARY.md`.

## Validate

```bash
python scripts/memory/validate_local_memo_port.py --path examples/memory-ports/example-port
python scripts/memory/build_local_memo_port_index.py --path examples/memory-ports/example-port --check
```

