# VALIDATION.md

On-demand human procedure for `mechanics/consumer-handoff/docs/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/consumer-handoff/docs/AGENTS.md`

Shared executable routes remain owned by [`docs/VALIDATION.md`](../../../docs/VALIDATION.md), [`docs/memory/VALIDATION.md`](../../../docs/memory/VALIDATION.md), [`mechanics/VALIDATION.md`](../../VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python -m pytest -q mechanics/consumer-handoff/parts/downstream-feed-regression/tests mechanics/consumer-handoff/parts/playbook-scope-handoff/tests/test_playbook_memory_scopes.py tests/memory/test_memo_handoff_boundaries.py
```
