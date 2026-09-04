# Adoption Provenance Bridge

Use active surfaces first:

- [README](README.md)
- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [parts](parts/)
- [OWNER_MAP](OWNER_MAP.md)
- [docs](docs/)

Former staging material is historical only; recover it from the pinned baseline
in [AOA-MEM-D-0090](../../docs/decisions/AOA-MEM-D-0090-retire-spark-and-legacy-mechanics.md).

## Active Placement

Adoption technical contracts now live under the nearest functioning part:

- `parts/adoption-boundary/` owns boundary, forgetting, duplicate-cluster, and
  generic adoption-memory writeback candidate artifacts.
- `parts/revision-and-retention-pressure/` owns adoption retention memory and
  revision ledger artifacts.
- `parts/scar-and-routing-adoption/` owns agonic scar writeback and
  router-facing adoption validation.
