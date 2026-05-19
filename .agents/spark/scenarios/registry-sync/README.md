# Spark Scenario: registry-sync

Use `registry-sync` when Spark lane source, registry, validator, tests, release
gate, and generated companions need alignment.

## Scope

Change only Spark lane contract surfaces or generated AGENTS mesh surfaces
that reflect those contracts.

## Done Signal

Spark source, registry, docs, validator, release gate, and generated mesh
agree.

## Stop-line

Do not create a new source of truth while syncing derived routes.

## Handoff Route

Write a handoff when the sync reveals a broader agent-surface design question,
root route-law change, or model-agnostic lane rename.

## Validation

Run Spark lane validation and the AGENTS mesh generated companion checks.
