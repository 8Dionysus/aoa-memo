# Writeback Part-Local Artifacts

- Decision ID: AOA-MEM-D-0061

## Status

Accepted on 2026-05-19.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: local port/writeback, mechanic package, mechanic part
- Mechanic parents: writeback
- Guard families: mechanic topology, part and payload, local port/writeback
- Memory object classes: local_candidate
- Posture: active rationale

## Context

Writeback had functioning `parts/` nodes, but the runnable contracts still
lived at the package level: schemas, examples, generated companions, scripts,
tests, and the receipt publication fixture were all grouped under
`mechanics/writeback/{schemas,examples,generated,scripts,tests}`.

That was too blunt for OS Abyss use. Runtime target maps, quest chronicles,
revision ledgers, rollback memory, growth/continuity writeback, and receipt
publication have different owner boundaries and different validation routes.
A package-level bucket made those differences harder for agents and validators
to inspect.

## Decision

Move writeback technical artifacts to the nearest functioning part:

- runtime target schema, generated target/intake/governance surfaces, and
  builders under `mechanics/writeback/parts/runtime-and-temperature/`
- quest chronicle schema, example, and test under
  `mechanics/writeback/parts/quest-and-chronicle/`
- assistant/release/revocation ledger schemas, examples, and tests under
  `mechanics/writeback/parts/revision-ledgers/`
- rollback memory and rollback revision ledger schemas, examples, and tests
  under `mechanics/writeback/parts/rollback-and-recovery/`
- continuity examples, growth-refinery generated lanes, Phase Alpha writeback
  map, builders, and tests under `mechanics/writeback/parts/growth-and-continuity/`
- receipt publication helper, fixture, and regression test under
  `mechanics/writeback/parts/receipt-publication-regression/`

Move the cross-mechanic operational-contract regression out of the writeback package and into
root `tests/` because it protects a cross-mechanic contract set. Register it in
the root technical district test-family contract rather than letting writeback
pretend it owns governance, operational-gate, retention, and writeback at once.

## Consequences

- The writeback artifact inventory now reports writeback artifacts as
  `scope: part`, not package-owned.
- Runtime and growth generated companions keep generator-backed checks at their
  owning parts.
- The object-surface manifest schema allows curated memory-object examples
  under `mechanics/<slug>/parts/<part>/examples/`.
- Local live receipt refs must follow the new growth-lane generated path.
- `aoa-memo` still does not run a live ledger, runtime worker, route dispatch,
  proof verdict, playbook choreography, stats truth, role authority, KAG
  substrate, source-owner acceptance, or release authority.

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
