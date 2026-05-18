# Checkpoint Memory Boundary

Checkpoint memory preserves evidence that a route paused, reviewed, carried,
or resumed through a checkpoint-shaped artifact.

Memo owns the memory posture around that artifact. It does not own the
checkpoint's authority.

## Memo May Preserve

- checkpoint artifact refs
- approval and health record examples
- checkpoint carry packets and return packs
- improvement-thread provenance
- mapping into existing memory object kinds
- source refs and owner handoff refs
- review state, temperature, current recall, and retention posture

## Memo Must Not Preserve As Authority

- that a checkpoint executed successfully
- that a route is authorized to continue
- that a runtime store contains current checkpoint state
- that an actor has rights to resume
- that an eval verdict passed
- that a playbook accepted the checkpoint consequence
- that a source owner accepted the memory candidate

## Object Shape

Checkpoint artifacts map into existing object kinds:

- `state_capsule` for bounded checkpoint exports
- `decision` for approval or transition records
- `episode` for execution traces
- `audit_event` for review traces
- `claim`, `pattern`, or `bridge` only as reviewed candidates
- `provenance_thread` for walk-back and improvement chains

Do not create `checkpoint_memory`.
