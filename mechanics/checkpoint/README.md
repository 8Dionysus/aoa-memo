# Checkpoint Memo Mechanic

Checkpoint is the memo-side mechanic for preserving checkpoint gates, carry
packets, approval and health records, and checkpoint-to-memory mappings so OS
Abyss can resume work from reviewable memory without making `aoa-memo` the
checkpoint executor.

## Mechanic card

- Status: `landed`

### Operation

preserve checkpoint gates, carry packets, approval and health records, and checkpoint-to-memory mappings as reviewable memory without becoming checkpoint executor, runtime store, role authority, proof layer, or route ledger

### Trigger

Use when a checkpoint artifact, checkpoint approval, health check, improvement
thread, checkpoint carry packet, or checkpoint-to-memory mapping must become
reviewable memory-layer posture.

### Memo owns

Memo owns checkpoint memory posture, checkpoint artifact schemas and examples,
approval and health record examples, improvement-thread provenance, source
refs, carry boundaries, mapping into existing memory objects, and stop-lines
that keep checkpoint recall bounded.

### Stronger owner split

- `Agents-of-Abyss` owns checkpoint doctrine, program law, and center meaning.
- `aoa-agents` owns actor rights, checkpoint authority, and handoff policy.
- `aoa-playbooks` owns scenario choreography and checkpoint play.
- `aoa-routing` owns dispatch, route compression, and return navigation.
- `abyss-stack` owns live checkpoint workers, runtime stores, retry loops, and
  checkpoint logs.
- `aoa-evals` owns proof, score, and quality verdicts.
- Source owner repositories own acceptance of a checkpoint consequence.

### Inputs

Checkpoint refs, checkpoint carry packets, inquiry checkpoint exports,
approval records, health records, improvement-thread traces, runtime
checkpoint refs, reviewed closeout refs, return pack refs, and stronger owner
feedback that a checkpoint surface is overclaiming.

### Outputs

Checkpoint memory docs, checkpoint schemas and examples, checkpoint-to-memory
mapping contracts, bounded carry guidance, provenance threads, owner-routed
next claims, and validator requirements.

### Must not claim

- checkpoint execution or retry authority
- live runtime storage, checkpoint workers, or hidden scratchpad persistence
- actor rights, role permission, or identity continuity
- route dispatch, route ledger authority, or scenario acceptance
- eval proof, adoption verdict, or quality score
- a new checkpoint-only memory-object family
- owner acceptance, source truth, or current truth by implication

### Validation

Use the validation lane in [AGENTS](AGENTS.md#validation).

### Next route

Route checkpoint doctrine to `Agents-of-Abyss`, actor rights to `aoa-agents`,
checkpoint play to `aoa-playbooks`, route behavior to `aoa-routing`, runtime
checkpoint work to `abyss-stack`, proof to `aoa-evals`, and source acceptance
to the owning repository.

## Active Route

- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [OWNER_MAP](OWNER_MAP.md)
- [PROVENANCE](PROVENANCE.md)
- [LANDING_LOG](LANDING_LOG.md)
- [ROADMAP](ROADMAP.md)
- [docs](docs/)
- [legacy index](legacy/INDEX.md)

## Functioning Parts

The active part map is [PARTS](PARTS.md). Source docs live in [docs](docs/).

## Historical Provenance

Use [PROVENANCE](PROVENANCE.md) first. Use [legacy](legacy/README.md) only when
auditing old root technical placement.

## Owner Boundary

Checkpoint remains a memo mechanic until stronger owners accept execution,
role rights, route consequence, proof, scenario meaning, or runtime state.
Memo can preserve why a checkpoint matters; it cannot decide what the
checkpoint authorizes.

## Growth Posture

Future work should add stricter checkpoint examples or validators only when
repeated checkpoint-carry evidence proves a stable contract. Do not widen this
package into runtime state, route dispatch, or identity-continuity doctrine.
