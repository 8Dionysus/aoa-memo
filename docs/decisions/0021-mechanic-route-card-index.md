# Mechanic Route Card Index

- Decision ID: AOA-MEM-D-0021

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-mechanic-route-card-index.md
- Surface classes: generated/readout, mechanic package
- Mechanic parents: none
- Guard families: mechanic topology, generated/read-model
- Memory object classes: none
- Posture: active rationale

## Context

The memo mechanics tree now has package README cards for all active mechanics:
operation, trigger, memo-owned posture, stronger owner split, inputs, outputs,
stop-lines, validation, and next route.

The readiness matrix proves that package surfaces are present and ready, but it
does not expose the current route-card content as a compact object. That leaves
OS Abyss agents with two weak choices: scrape Markdown directly or rely on the
readiness matrix for a question it does not own.

Agents-of-Abyss uses machine-facing route-card companions for its mechanics.
`aoa-memo` needs the same discipline, adapted to memo's package README cards
and without turning generated output into source authority.

## Decision

Add `generated/memo_mechanic_cards.min.json` as a generated route-card mirror
built from current package README mechanic cards and checked against
`config/memo_mechanics.json`.

The package README cards remain the authored source. The generated card index
is a compact inspection and validation surface for OS Abyss, not a new doctrine
store.

## Alternatives

- Keep route-card content readable only in package README files. This avoids a
  generated file, but keeps machine inspection dependent on ad hoc Markdown
  reads.
- Extend `generated/memo_mechanics.min.json` with all route-card sections. This
  would overload the compact package index, whose current job is package and
  docs discovery.
- Extend the readiness matrix with full route-card text. This would blur
  readiness with route-card content and make readiness harder to scan.

## Consequences

- Every package README mechanic card now has a machine-readable companion.
- Release validation fails when card status, operation, required sections,
  stronger owner list, stop-lines, validation route, or next route drift.
- The readiness matrix can point to `generated/memo_mechanic_cards.min.json`
  without absorbing route-card content.
- Root generated, script, and test district contracts must list the new card
  builder, validator, generated output, and regression test.
- Generated card data must not claim proof, runtime, role, routing, KAG,
  source-owner, playbook, stats, or source doctrine authority.

## Affected Surfaces

- `generated/memo_mechanic_cards.min.json`
- `scripts/build_memo_mechanic_cards.py`
- `scripts/validate_memo_mechanic_cards.py`
- `scripts/memo_mechanic_cards_common.py`
- `tests/test_memo_mechanic_cards.py`
- `generated/memo_mechanic_readiness.min.json`
- `scripts/mechanic_readiness_common.py`
- `config/root_technical_districts.json`
- `scripts/release_check.py`
- `mechanics/README.md`
- `mechanics/AGENTS.md`

## Verification

Use:

```bash
python scripts/build_memo_mechanic_cards.py --check
python scripts/validate_memo_mechanic_cards.py
python scripts/build_memo_mechanic_readiness.py --check
python scripts/validate_memo_mechanic_readiness.py
python scripts/validate_mechanic_artifact_topology.py
python -m pytest -q tests/test_memo_mechanic_cards.py tests/test_memo_mechanic_readiness.py
python scripts/release_check.py
```
