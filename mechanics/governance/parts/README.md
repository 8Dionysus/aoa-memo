# Governance Parts Index

Functioning Governance memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Governance boundary](governance-boundary/README.md) - memo-side governance and runtime-governance memory stop-lines
- [Federation boundary](federation-boundary/README.md) - cross-repo pattern memory, forgetting, and harvest gates without promotion authority
- [Install and certification boundary](install-and-certification-boundary/README.md) - install/certification memory facts without release approval or proof
- [Precedent and stay order](precedent-and-stay-order/README.md) - recallable policy precedent and stay-order memory without forced adoption

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
