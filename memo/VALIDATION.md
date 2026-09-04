# VALIDATION.md

On-demand human procedure for `memo/AGENTS.md`.

## On-demand procedure

### Preserved route from `memo/AGENTS.md`

```text
memo/objects/<kind-dir>/<year>/<slug>/
  object.json
  MEMO.md
```
Shared executable routes remain owned by [`docs/root/VALIDATION.md`](../docs/root/VALIDATION.md), [`generated/memory-objects/VALIDATION.md`](../generated/memory-objects/VALIDATION.md), [`scripts/agents/VALIDATION.md`](../scripts/agents/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python scripts/memory/validate_memo_corpus.py
python -m pytest -q tests/memory/test_memo_corpus.py tests/memory/test_reviewed_intake_landing.py tests/agents/test_agents_mesh.py tests/root-topology/test_root_technical_districts_index.py
```
