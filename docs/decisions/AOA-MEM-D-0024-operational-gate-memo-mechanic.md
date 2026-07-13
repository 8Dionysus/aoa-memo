# 2026-05-18: Add Operational Gate as an Operation-First Memo Mechanic

- Decision ID: AOA-MEM-D-0024

## Index Metadata

- Original date: 2026-05-18
- Surface classes: mechanic package
- Mechanic parents: operational-gate
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

After consumer handoff landed, the remaining flat docs still included an
operational cluster:

- deployment incident memory gate
- office incident memory gate
- service revision ledger
- post-release memory boundaries

Leaving these files flat made them look like ordinary docs-root doctrine.
Putting them in governance, writeback, or retention would blur the operation.
Governance owns authority-boundary memory, writeback owns owner-return lanes,
and retention owns watches, markers, and outcomes. This cluster answers a
different question: when does an operational event deserve durable memo recall
at all?

## Decision

Add `mechanics/operational-gate/` as the memo mechanic for operational memory
admission.

Move these active docs from flat `docs/` into
`mechanics/operational-gate/docs/`:

- `DEPLOYMENT_INCIDENT_MEMORY_GATE.md`
- `OFFICE_INCIDENT_MEMORY_GATE.md`
- `POST_RELEASE_MEMORY_BOUNDARIES.md`
- `SERVICE_REVISION_LEDGER.md`

Keep their old flat paths only in `config/memo_mechanics.json`, this decision
record, and `mechanics/operational-gate/legacy/INDEX.md` as provenance.

The related schemas, examples, and tests were later moved into part-local
artifact lanes by
[2026-05-19-operational-gate-part-local-artifacts](AOA-MEM-D-0054-operational-gate-part-local-artifacts.md).

## Alternatives

- Leave the files flat. That would preserve path stability, but it would keep
  a repeatable operational admission mechanic in docs root after validated
  package routes exist.
- Move the files into governance. That would overstate the authority question
  and repeat the earlier via-negativa placement mistake.
- Move service revision surfaces into writeback or retention. Those mechanics
  own owner-return lanes and retention evidence, not the admission decision
  for operational memory.
- Create a generic `docs/operations/` district. That would group the topic but
  would not provide package cards, owner maps, legacy bridges, or mechanics
  validation.

## Consequences

- Operational-gate becomes the local entry route when deployment incidents,
  office/service incidents, service revisions, or post-release notes ask to
  enter durable memo.
- `aoa-memo` stays responsible for evidence/ref requirements, owner-route
  stop-lines, review posture, future-effect wording, and memory admission.
- Stronger owners still own release approval, runtime remediation, proof,
  service rights, route dispatch, stats truth, and source meaning.
- Deployment and post-release boundary docs now carry enough contract shape to
  be useful; they are no longer placeholder notes.
- Generated mechanics and AGENTS mesh indexes make the new route
  machine-checkable.

## Affected Surfaces

- `mechanics/operational-gate/`
- `mechanics/README.md`
- `config/memo_mechanics.json`
- `generated/memo_mechanics.min.json`
- `config/agents_mesh.json`
- `generated/agents_mesh.min.json`
- `README.md`
- `docs/README.md`
- `docs/ROOT_SURFACE_LAW.md`
- `AGENTS.md`
- `DESIGN.md`
- `DESIGN.AGENTS.md`
- `ROADMAP.md`
- `CHANGELOG.md`
- `mechanics/operational-gate/parts/deployment-incident-gate/tests/test_operational_gate_mechanic.py`
- `mechanics/operational-gate/parts/post-release-boundaries/tests/test_post_release_boundary_contracts.py`
- `tests/test_memo_mechanics.py`
- `tests/test_agents_mesh.py`

## Verification Route

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
