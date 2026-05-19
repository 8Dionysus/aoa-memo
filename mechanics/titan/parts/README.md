# Titan Parts Index

Functioning Titan memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Core memory posture](core-memory-posture/README.md) - keeps Titan recall and source refs explicit without granting write authority
- [Closeout and digest posture](closeout-and-digest-posture/README.md) - keeps bridge, closeout, and console memory proposals bounded
- [Specialized policy](specialized-policy/README.md) - keeps audit, personality, and swarm memory posture reviewable

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
