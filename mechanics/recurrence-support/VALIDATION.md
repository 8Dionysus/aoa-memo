# VALIDATION.md

On-demand human procedure for `mechanics/recurrence-support/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/recurrence-support/AGENTS.md`

Shared executable routes remain owned by [`docs/VALIDATION.md`](../../docs/VALIDATION.md), [`generated/agents/VALIDATION.md`](../../generated/agents/VALIDATION.md), [`mechanics/VALIDATION.md`](../VALIDATION.md), [`scripts/agents/VALIDATION.md`](../../scripts/agents/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python -m pytest -q mechanics/recurrence-support/parts tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py tests/memory/test_memo_memory_context_boundaries.py mechanics/consumer-handoff/parts/playbook-scope-handoff/tests/test_playbook_memory_scopes.py tests/root-topology/test_roadmap_parity.py
```
This surface owns only the focused or composite invocations shown here; linked parent routes own wider/shared lanes.
