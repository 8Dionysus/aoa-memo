# Retention Provenance Bridge

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

Retention technical contracts now live under the nearest functioning part:

- `parts/cross-repo-and-governance-retention/` owns cross-repo retention result
  and governance retention check artifacts.
- `parts/office-markers/` owns first-office and multi-office marker artifacts.
- `parts/post-release-retention/` owns post-release retention memory and watch
  artifacts.
