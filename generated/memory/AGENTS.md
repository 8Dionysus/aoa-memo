# AGENTS.md

Route card for `generated/memory/`.

## Purpose

This district holds generated doctrine and registry companions for memory
recall.

## Source

Files here are checked-in companions. Source truth routes to `docs/memory/`,
`docs/boundaries/`, and `docs/posture/`.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `examples/recall/` for recall contract entrypoints.
- Downstream: consumers may inspect compact JSON, then hydrate source docs.

## Validate

```bash
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
```
