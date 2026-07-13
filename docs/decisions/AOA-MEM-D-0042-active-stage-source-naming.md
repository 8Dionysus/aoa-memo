# Active Stage and Source Naming

- Decision ID: AOA-MEM-D-0042

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: memory doctrine, legacy/provenance
- Mechanic parents: none
- Guard families: docs route, memory surface
- Memory object classes: none
- Posture: active rationale

## Context

`aoa-memo` inherited active `wave` and `seed` wording from earlier Agon,
Dionysus, and migration-era surfaces. That made current mechanic topology look
like historical provenance, especially after `mechanics/` became the active OS
Abyss memory-mechanic surface.

Legacy snapshots still need their original language because they are evidence,
not current route law. Source-owned upstream refs such as Agents-of-Abyss wave
docs and Dionysus seed archive paths also must stay exact.

## Decision

Use `stage` for active memo-side Agon landing surfaces and `source` or
`candidate` for active memo-side intake inputs.

Keep legacy and upstream source refs literal:

- `mechanics/*/legacy/raw/` keeps historical filenames and prose.
- `mechanics/*/legacy/INDEX.md` may update only live active-route pointers
  when active docs move.
- Dionysus `seed_*` paths and Agents-of-Abyss `EXPERIENCE_WAVE*` refs stay
  exact because they are stronger-owner source vocabulary.

## Consequences

- Active Agon docs, configs, manifests, part slugs, validators, tests, and
  generated mirrors use stage/source naming.
- Active cross-mechanic examples and schemas avoid seed wording unless the
  value is a literal upstream source ref.
- Legacy provenance remains auditable instead of being rewritten into current
  terminology.
- The rename does not grant proof, runtime execution, source-owner acceptance,
  KAG truth, route authority, or role authority inside `aoa-memo`.

## Validation

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
