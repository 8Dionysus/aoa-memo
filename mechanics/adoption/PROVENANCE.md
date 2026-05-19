# Adoption Provenance Bridge

Use active surfaces first:

- [README](README.md)
- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [parts](parts/)
- [OWNER_MAP](OWNER_MAP.md)
- [docs](docs/)

Use [legacy/INDEX](legacy/INDEX.md) only to audit the former flat docs-root
placement. Legacy paths are historical receipts, not active contracts.

## Active Placement

Adoption technical contracts now live under the nearest functioning part:

- `parts/adoption-boundary/` owns boundary, forgetting, duplicate-cluster, and
  generic adoption-memory writeback candidate artifacts.
- `parts/revision-and-retention-pressure/` owns adoption retention memory and
  revision ledger artifacts.
- `parts/scar-and-routing-adoption/` owns agonic scar writeback and
  router-facing adoption validation.
