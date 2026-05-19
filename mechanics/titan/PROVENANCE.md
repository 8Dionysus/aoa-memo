# Titan Provenance Bridge

Use active surfaces first:

- [README](README.md)
- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [OWNER_MAP](OWNER_MAP.md)
- [docs](docs/)

Titan docs were first moved from flat `docs/TITAN_*.md` files into the
transitional `mechanics/titan/docs/` district. They now live under
`mechanics/titan/docs/` because Titan memory posture has mechanic shape:
repeatable inputs, outputs, owner split, stop-lines, validation, and legacy
routing.

Titan single-mechanic schemas, examples, and tests were later moved from
package-level `schemas/`, `examples/`, and `tests/` into the nearest
`parts/<part>/` homes. Active artifact ownership now follows:

- `parts/core-memory-posture/` for recall, writeback, and remembrance records
- `parts/closeout-and-digest-posture/` for bridge, closeout, console, and digest
  candidates
- `parts/specialized-policy/` for audit-memory candidates

Use [legacy/INDEX](legacy/INDEX.md) only to audit former placement. Legacy
paths are historical receipts, not active contracts.
