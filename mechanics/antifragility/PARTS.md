# Antifragility Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Failure lesson memory | [FAILURE_LESSON_MEMORY](./docs/FAILURE_LESSON_MEMORY.md), [FAILURE_LESSON_RECALL](./docs/FAILURE_LESSON_RECALL.md), [DRIFT_REVIEW_LESSON_MEMORY](./docs/DRIFT_REVIEW_LESSON_MEMORY.md) | keeps repeated failure lessons recallable without becoming proof |
| Recovery pattern memory | [RECOVERY_PATTERN_MEMORY](./docs/RECOVERY_PATTERN_MEMORY.md), [RECOVERY_PATTERN_RECALL](./docs/RECOVERY_PATTERN_RECALL.md), [ROLLBACK_FOLLOWTHROUGH_PATTERN](./docs/ROLLBACK_FOLLOWTHROUGH_PATTERN.md) | keeps reviewed recovery windows recallable without authorizing rollback or route behavior |

## Part-Local Artifacts

| Part | Artifact Homes |
|---|---|
| Failure lesson memory | `parts/failure-lesson-memory/schemas/`, `parts/failure-lesson-memory/examples/`, `parts/failure-lesson-memory/tests/` |
| Recovery pattern memory | `parts/recovery-pattern-memory/schemas/`, `parts/recovery-pattern-memory/examples/`, `parts/recovery-pattern-memory/tests/` |

## Interface

Inputs are reviewed receipts, drift windows, rollback-followthrough windows,
eval reports, stats summaries, route hints, and lineage refs. Outputs are
bounded memo docs, schema/example refs, generated object inputs, and
stronger-owner routes.
