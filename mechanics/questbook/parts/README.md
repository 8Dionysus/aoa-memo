# Questbook Parts Index

Functioning Questbook memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Public index](public-index/README.md) - compact list of open memo-facing obligations; not a second roadmap
- [Quest item store](quest-item-store/README.md) - lane-first lifecycle source files under `quests/<lane>/<state>/`
- [Source contract](source-contract/README.md) - reviewable YAML and Markdown source shape for memo quest objects
- [Generated views](generated-views/README.md) - root-published read models that never author quest meaning

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
