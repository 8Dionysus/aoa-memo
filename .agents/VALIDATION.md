# VALIDATION.md

On-demand human procedure for `.agents/AGENTS.md`.

## On-demand procedure

### Root validation route

Shared executable routes remain owned by the repository root validation and
configuration lanes; follow those on-demand lanes for this surface.
```bash
python -m pytest -q tests/root-topology/test_topology_spine.py
```
