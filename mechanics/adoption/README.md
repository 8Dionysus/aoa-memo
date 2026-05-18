# Adoption Mechanic

Adoption is the memo-side mechanic for making memory adoption candidates
reviewable without turning them into proof, automatic promotion, routing
authority, or runtime retention.

## Mechanic card

- Status: `landed`

### Trigger

Use when adoption, forgetting, revision, retention-adjacent adoption, scar
writeback, or routing-memory adoption must become an explicit memo surface.

### Memo owns

Memo owns the adoption memory posture, source refs, review boundaries,
forgetting and revision language, and candidate writeback framing.

### Stronger owner split

- `aoa-routing` owns dispatch behavior and router implementation.
- `aoa-evals` owns proof and adoption-quality verdicts.
- `aoa-agents` owns role rights and actor write authority.
- `aoa-playbooks` owns recurring adoption choreography.
- `abyss-stack` owns runtime storage or workers.
- Source repositories own authored meaning that memory may only cite.

### Inputs

Reviewed source refs, adoption candidates, forgetting pressure, revision notes,
scar writeback candidates, and routing consumption needs.

### Outputs

Bounded adoption memory docs, routeable source refs, review requirements,
candidate-only writeback posture, and owner handoff notes.

### Must not claim

- adoption has landed without reviewed evidence
- route correctness has proof status
- memory writes, scar writes, or retention execution have occurred
- `aoa-memo` owns runtime storage, role rights, dispatch policy, or source truth

### Validation

Use the validation lane in [AGENTS](AGENTS.md#validation).

### Next route

Route proof to `aoa-evals`, dispatch implementation to `aoa-routing`, role
rights to `aoa-agents`, runtime behavior to `abyss-stack`, and recurring
adoption choreography to `aoa-playbooks`.

## Active Route

- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [OWNER_MAP](OWNER_MAP.md)
- [PROVENANCE](PROVENANCE.md)
- [LANDING_LOG](LANDING_LOG.md)
- [ROADMAP](ROADMAP.md)
- [legacy index](legacy/INDEX.md)

## Functioning Parts

The active part map is [PARTS](PARTS.md). Source docs live in [docs](docs/).

## Historical Provenance

Use [PROVENANCE](PROVENANCE.md) first. Use [legacy](legacy/README.md) only when
auditing the old flat docs-root placement.

## Owner Boundary

Adoption remains a memo mechanic until a stronger owner accepts and validates
implementation, proof, role, runtime, or route behavior.

## Growth Posture

Future adoption work should add sharper evidence requirements and owner
handoff receipts before expanding the mechanic.
