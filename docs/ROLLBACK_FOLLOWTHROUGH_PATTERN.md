# ROLLBACK FOLLOWTHROUGH PATTERN

Use this note when one source-owned `rollback_followthrough_window` preserves a
bounded recovery route that should remain recallable across shared-root rollout
maintenance.

Keep the writeback inside `recovery_pattern_memory_v1`.
Do not mint a cadence-only memo kind.

## Recommended shape

- ordered window scope points to one campaign window plus one rollback-followthrough window
- source refs point back to `8Dionysus` campaign and rollback-followthrough windows
- stats refs stay descriptive and subordinate
- trust posture stays provisional until a reviewed real cadence run exists

## Boundary

This note preserves bounded recall only.
It does not authorize rollback or replace source-owned cadence windows.
