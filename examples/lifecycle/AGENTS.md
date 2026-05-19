# AGENTS.md

Route card for `examples/lifecycle/`.

## Purpose

This district owns lifecycle, supersession, retraction, current-entrypoint, and
audit-event examples.

## Source

Examples here demonstrate lifecycle posture. Doctrine routes to
`docs/posture/LIFECYCLE.md` and `docs/posture/AUDIT_EVENTS.md`.

## Route

- Up: `examples/AGENTS.md`, then `AGENTS.md`.
- Across: `schemas/recall-posture/` and `schemas/memory-objects/`.
- Downstream: `generated/memory-objects/`.

## Validate

```bash
python scripts/memory/validate_lifecycle_audit_examples.py
python scripts/memory/validate_memo.py
```
