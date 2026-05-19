# Antifragility Provenance Bridge

Use active surfaces first:

- [README](README.md)
- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [parts](parts/)
- [OWNER_MAP](OWNER_MAP.md)
- [docs](docs/)

Antifragility docs were moved from flat `docs/*.md` placement into
`mechanics/antifragility/docs/` because the family has mechanic shape:
repeatable inputs, outputs, owner split, stop-lines, validation, schemas,
examples, generated surfaces, and tests.

On 2026-05-19 the active antifragility schemas, examples, and tests moved from
package-level artifact homes into functioning parts:

- `parts/failure-lesson-memory/` owns failure lesson and shared lesson schemas,
  examples, and regression tests.
- `parts/recovery-pattern-memory/` owns recovery pattern schema, recovery
  examples, the native antifragility stress/recovery pattern example, and
  regression tests.

Use [legacy/INDEX](legacy/INDEX.md) only to audit former placement. Legacy
paths are historical receipts, not active contracts.
