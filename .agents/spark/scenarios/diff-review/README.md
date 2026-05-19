# Spark Scenario: diff-review

Use `diff-review` to review a concrete diff or pull request for memory-layer
risks and missed checks.

## Scope

Review one diff, branch, or PR. Do not rewrite it while acting as reviewer.

## Done Signal

Findings are ordered by severity and tied to exact paths, validators, and owner
routes.

## Stop-line

Do not rewrite the diff while acting as reviewer.

## Handoff Route

Write a handoff when the diff requires deeper architecture, cross-repo owner
judgment, or broad validation that should run outside Spark.

## Validation

Use `git diff --check` plus any narrow validator clearly tied to the diff if
the user asked for validation.
