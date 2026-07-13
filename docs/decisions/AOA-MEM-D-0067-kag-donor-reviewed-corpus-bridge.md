# Decision: KAG donor bridge uses reviewed corpus object

- Decision ID: AOA-MEM-D-0067

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-24
- Surface classes: reviewed corpus, consumer handoff, boundary/runtime/sibling
- Mechanic parents: none
- Guard families: reviewed corpus/intake, sibling and boundary
- Memory object classes: decision
- Posture: active rationale

## Context

`aoa-memo` publishes a source-owned KAG donor export for the ToS lineage bridge.
The export object id was already stable, but the object-facing read-model row
came from the bridge teaching fixture. That kept the KAG path demonstrable, but
it weakened the reviewed-memory split: consumers could see the donor id without
being able to prefer `source_kind: reviewed_corpus`.

After corpus-backed read models landed, the KAG donor needed to become a real
reviewed memory object without changing KAG activation posture.

## Decision

Create `memo/objects/bridges/2026/tos-lineage-kag-candidate/` as the reviewed
corpus bundle for `memo.bridge.2026-03-23.tos-lineage-kag-candidate`.

The object-facing generated read models now take that id from the reviewed
corpus. The bridge teaching fixture remains in the consumer-handoff mechanic
for schema, guardrail, and bridge-face regressions, but it is removed from the
object-surface manifest so it no longer competes with the reviewed corpus row.

The source-owned `kag_export.min.json` direct relation now points at the corpus
object bundle. `aoa-kag` keeps this donor registry-visible only; graph
normalization, federation-spine activation, routing activation, and proof remain
outside `aoa-memo`.

## Alternatives

- Leave the donor sourced from the teaching fixture. This kept compatibility
  but forced consumers to treat a fixture as the donor row.
- Mint a new donor id for the reviewed object. This avoided duplicate-source
  tension but would break the existing KAG bridge id and envelope relationship.
- Promote the existing id into reviewed corpus and keep the fixture as a
  fixture only. This preserves the cross-repo id while making the source class
  honest.

## Consequences

- KAG-facing consumers can filter the donor through `source_kind:
  reviewed_corpus`.
- The bridge example remains useful as a public teaching and regression object,
  but generated object read models no longer treat it as the donor source.
- The memo donor still has `kag_lift_status: candidate`; this decision does not
  activate the live KAG federation spine or routing ABI.
- `aoa-kag` validators must expect the memo export's source-memory relation to
  point at `memo/objects/bridges/2026/tos-lineage-kag-candidate/object.json`.

## Validation

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
