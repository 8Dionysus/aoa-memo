# Retention Mechanic

Retention is the memo-side mechanic for keeping retention evidence, watches,
markers, checks, outcomes, consolidation, and forgetting operations reviewable
without executing retention or claiming runtime authority.

## Mechanic card

- Status: `landed`

### Operation

preserve retention evidence, watches, markers, and outcomes as reviewable memory without executing retention

### Trigger

Use when cross-repo retention memory, office retention markers, governance
retention checks, consolidation or forgetting operations, or post-release
retention watch/outcome posture must become explicit and reviewable.

### Memo owns

Memo owns retention review posture, source refs, markers, lifecycle-changing
operation records, public-safe examples, and recall routes for retention
evidence.

### Stronger owner split

- `abyss-stack` owns runtime retention workers, storage, and schedules.
- `aoa-evals` owns proof that retention checks passed.
- `aoa-agents` owns actor rights and handoff authority.
- Governance or source repositories own stronger retention policy.
- Runtime owners own private data handling and live state.

### Inputs

Retention signals, public-safe markers, lifecycle triggers, post-release watch
notes, owner confirmations, and governance check candidates.

### Outputs

Bounded retention docs, reviewed consolidation/forgetting operations,
reviewable markers, source refs, and owner handoff notes.

### Must not claim

- retention execution ran
- hidden schedulers or workers exist
- private traces can be retained in this public repo
- `aoa-memo` owns live storage, runtime policy, proof, or role rights

### Validation

Use the validation lane in [AGENTS](AGENTS.md#validation).

### Next route

Route runtime retention to `abyss-stack`, proof to `aoa-evals`, role authority
to `aoa-agents`, and stronger policy to the owning repository.

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

Retention remains a memo review mechanic until runtime, proof, policy, or role
owners accept stronger behavior.

## Growth Posture

Future retention work should make receipts sharper before adding any stronger
claim.
