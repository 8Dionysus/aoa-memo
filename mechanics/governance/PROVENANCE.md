# Governance Provenance Bridge

Use active surfaces first:

- [README](README.md)
- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [OWNER_MAP](OWNER_MAP.md)
- [docs](docs/)
- [parts](parts/)

Governance docs were moved from flat `docs/*.md` placement into
`mechanics/governance/docs/` because the family has mechanic shape:
repeatable route signals, authority checks, owner consent, gate outcomes,
forgetting and expiry posture, source-owner stop-lines, and stronger-owner
handoffs.

`VIA_NEGATIVA_CHECKLIST.md` now lives in `mechanics/shape-guard/docs/` because
it is a general memory-shape pruning operation, not governance authority
memory.

The active technical artifacts now live under the nearest functioning part:

- governance decision/writeback contracts and governance regression:
  `parts/governance-boundary/{schemas,examples,tests}/`
- federation gate and forgetting contracts:
  `parts/federation-boundary/{schemas,examples}/`
- installation and certification contracts:
  `parts/install-and-certification-boundary/{schemas,examples}/`
- policy precedent contract:
  `parts/precedent-and-stay-order/{schemas,examples}/`

Former package-level `schemas/`, `examples/`, and `tests/` homes are placement
history only after the 2026-05-19 part-local artifact move.

Use [legacy/INDEX](legacy/INDEX.md) only to audit former placement. Legacy
paths are historical receipts, not active contracts.
