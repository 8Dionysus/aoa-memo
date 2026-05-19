# Operational Gate Provenance Bridge

Use active surfaces first:

- [README](README.md)
- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [parts](parts/)
- [OWNER_MAP](OWNER_MAP.md)
- [docs](docs/)

The active route is now `mechanics/operational-gate/docs/` because these
surfaces share one repeatable memory-layer operation: decide whether an
operational event or service revision deserves durable memo recall without
moving release, runtime, proof, role, route, stats, or source authority into
`aoa-memo`.

Former flat docs-root surfaces were:

- `DEPLOYMENT_INCIDENT_MEMORY_GATE.md`
- `OFFICE_INCIDENT_MEMORY_GATE.md`
- `POST_RELEASE_MEMORY_BOUNDARIES.md`
- `SERVICE_REVISION_LEDGER.md`

On 2026-05-19 the active operational-gate schemas, examples, and tests moved
from package-level artifact homes into functioning parts:

- `parts/deployment-incident-gate/` owns deployment incident gate and
  deployment lesson candidate contracts plus the package boundary regression.
- `parts/office-incident-gate/` owns service incident memory entry contracts.
- `parts/service-revision-ledger/` owns service revision ledger entry
  contracts.
- `parts/post-release-boundaries/` owns train release memory entry contracts
  and the Wave 5 post-release seed regression.

Use root technical districts only for shared or cross-mechanic contracts.

Use [legacy/INDEX](legacy/INDEX.md) only to audit former placement. Legacy
paths are historical receipts, not active contracts.
