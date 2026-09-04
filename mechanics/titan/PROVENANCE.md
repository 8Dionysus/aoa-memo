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

- `parts/recall-and-remembrance-posture/` for recall, writeback, and remembrance records
- `parts/closeout-and-digest-posture/` for bridge, closeout, console, and digest
  candidates
- `parts/audit-personality-and-swarm-policy/` for audit-memory candidates

Former staging material is historical only; recover it from the pinned baseline
in [AOA-MEM-D-0090](../../docs/decisions/AOA-MEM-D-0090-retire-spark-and-legacy-mechanics.md).
