# Consumer Handoff Part-Local Artifacts

- Decision ID: AOA-MEM-D-0048

## Index Metadata

- Original date: 2026-05-19
- Surface classes: consumer handoff, mechanic part
- Mechanic parents: consumer-handoff
- Guard families: mechanic topology, part and payload
- Memory object classes: none
- Posture: active rationale

## Context

Consumer-handoff already had functioning parts, but its active schemas,
examples, generated KAG export, generator, and local regression tests still
lived at the package level.

That made `parts/` descriptive rather than operational for the surfaces that
neighboring owners actually consume.

## Decision

Move consumer-handoff technical artifacts to the nearest functioning part:

- bridge object chain, chunk face, and graph face under
  `parts/kag-tos-bridge-handoff/`
- source-owned KAG donor export, generator, and bridge-record source contract
  under `parts/kag-source-export/`
- eval guardrail pack schema and example under `parts/eval-guardrail-handoff/`
- playbook memory-scope regression under `parts/playbook-scope-handoff/`
- consumer feed and mechanic regression tests under
  `parts/downstream-feed-regression/`

Keep package docs as the authored handoff doctrine and keep generated root
companions as derived inspection surfaces.

## Alternatives

Leaving artifacts under package-level `schemas/`, `examples/`, `generated/`,
`scripts/`, and `tests/` would preserve shorter paths but leave the active
parts without the contracts they operate.

Moving everything into a generic package-local artifact directory would reduce
root sprawl but would still hide ownership from the part topology.

## Consequences

Consumer-handoff parts are now executable owner nodes: each runnable artifact
has a part-local home, and downstream validators point at the owning part.

The move keeps `aoa-memo` below stronger owners. It does not grant role policy,
playbook choreography, eval verdicts, KAG graph truth, ToS source meaning,
route dispatch, or runtime execution.

## Affected Surfaces

- `mechanics/consumer-handoff/PARTS.md`
- `mechanics/consumer-handoff/PROVENANCE.md`
- `mechanics/consumer-handoff/parts/*`
- `mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md`
- `mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md`
- `scripts/validate_memo.py`
- `generated/memo_registry.min.json`
- `generated/mechanic_artifacts.min.json`
- `generated/memo_mechanic_readiness.min.json`
- object-surface generated family

## Verification Route

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
