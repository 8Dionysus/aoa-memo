# Antifragility Memo Mechanic Docs

This directory contains source docs for the antifragility memo mechanic.

The files here preserve failure lesson memory, recovery pattern memory, recall
posture, drift-review lesson posture, and rollback-followthrough pattern
posture. They do not prove failures or recoveries, authorize rollback, own
route behavior, or repair runtime state.

## Source Families

| Family | Surfaces |
|---|---|
| Failure lesson memory | [FAILURE_LESSON_MEMORY](FAILURE_LESSON_MEMORY.md), [FAILURE_LESSON_RECALL](FAILURE_LESSON_RECALL.md), [DRIFT_REVIEW_LESSON_MEMORY](DRIFT_REVIEW_LESSON_MEMORY.md) |
| Recovery pattern memory | [RECOVERY_PATTERN_MEMORY](RECOVERY_PATTERN_MEMORY.md), [RECOVERY_PATTERN_RECALL](RECOVERY_PATTERN_RECALL.md), [ROLLBACK_FOLLOWTHROUGH_PATTERN](ROLLBACK_FOLLOWTHROUGH_PATTERN.md) |

## Companion Surfaces

Antifragility docs currently pair with:

- `mechanics/antifragility/parts/failure-lesson-memory/schemas/failure_lesson_memory_v1.json`
- `mechanics/antifragility/parts/failure-lesson-memory/schemas/shared_lesson_memory_v1.json`
- `mechanics/antifragility/parts/recovery-pattern-memory/schemas/recovery_pattern_memory_v1.json`
- `mechanics/antifragility/parts/failure-lesson-memory/examples/failure_lesson_memory*.json`
- `mechanics/antifragility/parts/failure-lesson-memory/examples/shared_lesson_memory.example.json`
- `mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory*.json`
- `mechanics/antifragility/parts/recovery-pattern-memory/examples/pattern.antifragility-stress-recovery-window.example.json`
- `generated/memory_object_*.json`
- `mechanics/antifragility/parts/failure-lesson-memory/tests/test_antifragility_failure_lessons.py`
- `mechanics/antifragility/parts/recovery-pattern-memory/tests/test_antifragility_recovery_patterns.py`

## Stop-Lines

Antifragility memo surfaces may say:

- what repeated stress or recovery context should be preserved
- which source refs, eval refs, stats refs, route hints, or lineage refs matter
- when recall should be suppressed, cooled, or treated as provisional

They may not say:

- that current health is proven
- that a rollback or repair is authorized
- that route behavior has landed
- that stats are source truth
- that runtime work happened

## Validation

The mechanic-doc route is pinned by:

```bash
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```
