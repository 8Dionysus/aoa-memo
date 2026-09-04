# VALIDATION.md

On-demand human procedure for `.agents/AGENTS.md`.

## On-demand procedure

### Preserved route from `.agents/AGENTS.md`

Shared executable routes remain owned by [`.agents/spark/VALIDATION.md`](spark/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python -m unittest discover -s .agents/spark/tests -p 'test*.py'
python -m pytest -q tests/root-topology/test_topology_spine.py
```
