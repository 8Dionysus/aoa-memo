# AGENTS.md

Route card for `scripts/memory/`.

## Purpose

This district owns memory-object, recall, lifecycle, operation-cycle, local
memo port, reviewed corpus, and generated memory surface validators and
builders. The broad memo validator CLI is a compatibility router; boundary
logic lives under `scripts/memory/validators/`.

## Source

Scripts here execute checks; they do not author doctrine. Source routes to
`docs/memory/`, `docs/posture/`, `schemas/`, and `examples/`.
Reviewed corpus checks route to `memo/`.
Reviewed intake landing from a local memo port route uses
`land_reviewed_memo_intake.py`; the script prepares object bundles and landing
receipts, but only after an export packet explicitly allows `reviewed_write`.
Its implementation is split into path/schema input checks, landing-plan
synthesis, and write/summary helpers so the CLI remains an entrypoint rather
than a hidden policy body.

Object-surface and operational-readout builders follow the same boundary:
source loading, projection rendering, live probing, and CLI check/write
orchestration stay in separate helper modules. Generated builders may check
projection parity, but they must not become the source of memory meaning.

## Route

- Up: `scripts/AGENTS.md`, then `AGENTS.md`.
- Across: `tests/memory/`.
- Downstream: generated outputs in `generated/memory/` and
  `generated/memory-objects/`.
- Landing usage: run `python scripts/memory/land_reviewed_memo_intake.py
  --port <repo>/memo --export <packet>.aoa-memo-intake.json --object-kind
  <kind>` first as a dry-run plan; add `--write` only after review accepts the
  target object id, kind, title, and lifecycle posture.

## Validate

```bash
python scripts/memory/validate_memo.py --profile schema
python scripts/memory/validate_memo.py --profile memory-context
python scripts/memory/validate_memo.py --profile runtime-boundary
python scripts/memory/validate_memo.py --profile handoff-boundary
python scripts/memory/validate_memo.py --profile eval-boundary
python scripts/memory/validate_memo_corpus.py
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_local_memo_port.py --path examples/memory-ports/example-port
python -m pytest -q tests/memory
```
