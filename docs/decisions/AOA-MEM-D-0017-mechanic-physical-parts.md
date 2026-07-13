# Mechanic Physical Parts

- Decision ID: AOA-MEM-D-0017

## Index Metadata

- Original date: 2026-05-18
- Surface classes: mechanic package, mechanic part
- Mechanic parents: none
- Guard families: mechanic topology, part and payload
- Memory object classes: none
- Posture: active rationale

## Context

Memo mechanics already had `PARTS.md` files, but for most packages those parts
were only rows in a table. That left the mechanic anatomy weaker than the
Agents-of-Abyss pattern, where functioning parts have physical nodes with
their own contract and validation surface.

The comparison pass also checked `aoa-skills` and `aoa-techniques`: their
parts become functional by carrying local route cards, source contracts, and,
where the part has technical load, local config, schemas, examples, generated
outputs, scripts, tests, manifests, or review/gate material. `aoa-memo` needs
the same growth path, but should first make every active part a stable
contractual node before deeper artifact moves.

For OS Abyss use, mechanics need more than topical grouping. A future agent
must be able to enter the package, identify the active part, read its contract,
and run the nearest validation route without reverse-engineering the table.

## Decision

Every active row in `mechanics/<slug>/PARTS.md` now materializes under:

```text
mechanics/<slug>/parts/<part-slug>/
  README.md
  CONTRACT.md
  VALIDATION.md
```

Each package also has:

```text
mechanics/<slug>/parts/
  AGENTS.md
  README.md
```

The existing Questbook quest-read-model-projections part remains specialized, but it now
participates in the same part validation contract.

## Alternatives Considered

- Keep `PARTS.md` as a table-only map. Rejected because table-only parts are
  not enough for active mechanic work.
- Move all source docs and artifacts into part directories immediately.
  Deferred because that would mix part topology with a much larger artifact
  migration. The safe first step is physical part contracts; deeper part-local
  artifact moves can happen one owner slice at a time.
- Create a generated-only parts index. Rejected because parts are active source
  contracts, not just generated inspection data.

## Consequences

- `scripts/validate_memo_mechanic_parts.py` now checks physical part nodes,
  part contracts, validation files, and local markdown links.
- Future `PARTS.md` edits must add or update the matching physical part.
- Part-local artifacts now have a stable destination before further root or
  package artifact migrations.

## Affected Surfaces

- `mechanics/*/parts/`
- `mechanics/AGENTS.md`
- `mechanics/README.md`
- `mechanics/ARTIFACT_TOPOLOGY.md`
- `scripts/validate_memo_mechanic_parts.py`
- `tests/test_memo_mechanic_parts.py`
- `config/agents_mesh.json`
- `generated/agents_mesh.min.json`

## Verification Route

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
