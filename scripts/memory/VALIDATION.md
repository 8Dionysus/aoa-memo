# VALIDATION.md

On-demand human procedure for `scripts/memory/AGENTS.md`.

## On-demand procedure

### Preserved route from `scripts/memory/AGENTS.md`

Shared executable routes remain owned by [`docs/boundaries/VALIDATION.md`](../../docs/boundaries/VALIDATION.md), [`docs/memory/VALIDATION.md`](../../docs/memory/VALIDATION.md), [`examples/memory-ports/VALIDATION.md`](../../examples/memory-ports/VALIDATION.md), [`memo/VALIDATION.md`](../../memo/VALIDATION.md), [`tests/memory/VALIDATION.md`](../../tests/memory/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python scripts/memory/validate_memo.py --profile handoff-boundary
python scripts/memory/validate_memo.py --profile eval-boundary
```

## Landing usage

Run this first as a dry-run plan; add `--write` only after review accepts the
target object id, kind, title, and lifecycle posture.

```bash
python scripts/memory/land_reviewed_memo_intake.py --port <repo>/memo --export <packet>.aoa-memo-intake.json --object-kind <kind>
```
