# Retention Provenance Bridge

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

Retention technical contracts now live under the nearest functioning part:

- `parts/cross-repo-and-governance-retention/` owns cross-repo retention result
  and governance retention check artifacts.
- `parts/office-markers/` owns first-office and multi-office marker artifacts.
- `parts/post-release-retention/` owns post-release retention memory and watch
  artifacts.
