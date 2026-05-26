# Decision Records Index

This directory is the durable decision surface for `aoa-memo`.

Use it when a future contributor needs the rationale for a route, topology,
source-of-truth split, validator, public contract, memory-object lane, or
workflow expectation.

## Operating Card

| Field | Route |
| --- | --- |
| role | durable decision rationale entrypoint and agent-facing index chooser |
| entry | use when a structural, topology, validation, public-contract, lifecycle, reviewed-corpus, generated-index, or agent-route change needs recoverable rationale |
| input | changed source surface, owner boundary, rejected option, validation guard, or cross-surface route pressure |
| output | canonical decision note, metadata-backed lookup index, and route back to the source surface |
| owner | `docs/decisions/AGENTS.md` for lane law; decision notes for rationale; generated indexes for lookup only |
| next route | source surface first, then nearest route card, `MEMORY_INDEX.md`, `docs/memory/MEMORY_MODEL.md`, generated lookup indexes, or the affected reviewed-corpus/mechanic owner |
| validation | `python scripts/root-topology/build_decision_indexes.py --check`, repo tests, and `python scripts/release/release_check.py` |

## Authority

Decision notes explain why a path was chosen.

They are weaker than the source surface they describe:

- memory doctrine stays in `docs/memory/`, `docs/boundaries/`, and
  `MEMORY_INDEX.md`;
- reviewed durable memory truth stays in `memo/`;
- mechanic shape stays in `mechanics/`, local route cards, and generated
  mechanic read models;
- generated readers stay derived from their builders;
- runtime, proof, routing, playbook, KAG, and role-contract owners keep their
  own stronger truth.

Generated decision indexes are weaker than the decision notes. They exist to
make lookup cheaper for agents, not to carry decision rationale.

## Index Shape

Each decision owns:

- a canonical `Decision ID: AOA-MEM-D-####`;
- an `## Index Metadata` block naming surface classes, mechanic parents, guard
  families, memory object classes, and posture.

The lookup indexes under [indexes](indexes/README.md) are generated from that
metadata:

- [Decisions by canonical ID and number](indexes/by-number.md)
- [Decisions by date](indexes/by-date.md)
- [Decisions by surface class](indexes/by-surface.md)
- [Decisions by mechanic parent](indexes/by-mechanic.md)
- [Decisions by validation or guard family](indexes/by-guard.md)
- [Decisions by memory-object class](indexes/by-memory-object-class.md)
- [Decision alias map](indexes/alias-map.md)

Use them in both directions:

- top down: repo route -> authority class -> operation -> mechanic parent ->
  guard family -> decision rationale;
- bottom up: changed source surface -> local route card or generated read model
  -> validator guard -> decision rationale -> stronger owner surface.

Regenerate the read models after decision metadata changes:

```bash
python scripts/root-topology/build_decision_indexes.py
```

## Dual Addressing

Current date-named decision paths remain live.

Canonical IDs are the stable handles. The alias map bridges old/current paths
to canonical IDs and reserves planned numbered paths for a later migration.

Do not rename decision files until a dedicated rename slice verifies the alias
and generated index layer protects all refs.

## Review Rule

Before adding a decision, ask whether the note explains a real choice. If the
answer is only "this file changed", the changelog or PR summary is enough.
