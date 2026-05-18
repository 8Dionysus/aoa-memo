# Checkpoint Roadmap

## Next

- Keep checkpoint schemas, examples, writeback consumers, recurrence consumers,
  generated surfaces, and validators aligned.
- Add stricter machine checks for checkpoint carry packets only when repeated
  OS Abyss checkpoint work proves a stable contract.
- Keep checkpoint mapping tied to existing object kinds:
  `state_capsule`, `decision`, `episode`, `audit_event`, `claim`, `pattern`,
  `bridge`, and `provenance_thread`.

## Not Yet

- Do not create a `checkpoint_memory` object kind.
- Do not absorb route dispatch, runtime retry policy, actor rights, proof, or
  playbook choreography into this package.
- Do not move shared recall contracts or reviewed closeout quest artifacts into
  this package unless they stop serving cross-mechanic recall and quest
  surfaces.
