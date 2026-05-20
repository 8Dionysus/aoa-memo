# AGENTS.md

Route card for `scripts/memory/`.

## Purpose

This district owns memory-object, recall, lifecycle, operation-cycle, local
memo port, and generated memory surface validators and builders.

## Source

Scripts here execute checks; they do not author doctrine. Source routes to
`docs/memory/`, `docs/posture/`, `schemas/`, and `examples/`.

## Route

- Up: `scripts/AGENTS.md`, then `AGENTS.md`.
- Across: `tests/memory/`.
- Downstream: generated outputs in `generated/memory/` and
  `generated/memory-objects/`.

## Validate

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_local_memo_port.py --path examples/memory-ports/example-port
python -m pytest -q tests/memory
```
