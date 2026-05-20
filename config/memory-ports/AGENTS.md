# AGENTS.md

Route card for `config/memory-ports/`.

## Purpose

This district owns source vocabularies for local `memo/` ports.
The files here name indexing terms that validators and generated read models
may use when inspecting candidate, receipt, export, and local port index
packets.

## Route

- Up: `config/AGENTS.md`, then root `AGENTS.md`.
- Doctrine: `docs/memory/LOCAL_MEMO_PORT_STANDARD.md` and
  `docs/memory/MEMO_PORT_INDEXING_VOCABULARY.md`.
- Schemas: `schemas/memory-ports/`.
- Builders and validators: `scripts/memory/`.

## Validate

```bash
python scripts/memory/build_memo_port_vocabulary.py --check
python scripts/memory/validate_local_memo_port.py --path examples/memory-ports/example-port
```

