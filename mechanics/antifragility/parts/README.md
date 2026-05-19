# Antifragility Parts Index

Functioning Antifragility memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Failure lesson memory](failure-lesson-memory/README.md) - keeps repeated failure lessons recallable without becoming proof
- [Recovery pattern memory](recovery-pattern-memory/README.md) - keeps reviewed recovery windows recallable without authorizing rollback or route behavior

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
