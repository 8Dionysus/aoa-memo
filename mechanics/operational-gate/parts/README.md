# Operational Gate Parts Index

Functioning Operational Gate memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Deployment incident gate](deployment-incident-gate/README.md) - admits deployment incident memory only with evidence, owner route, review posture, and future effect
- [Office incident gate](office-incident-gate/README.md) - keeps office/service incident memory governed by upstream office law and local memo admission
- [Service revision ledger](service-revision-ledger/README.md) - preserves service revision recall without becoming live service state or release approval
- [Post-release boundaries](post-release-boundaries/README.md) - names what post-release material memo may preserve and what stays with release/runtime owners

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
