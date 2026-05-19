# Spark Scenario: release-prep

Use `release-prep` for a fast release-readiness pass before publication,
support hardening, or GitHub landing.

## Scope

Inspect changed surfaces, public claims, generated parity, validation routes,
and owner boundaries for one branch or release slice.

## Done Signal

Changed surfaces, checks, public-claim risks, generated parity, and owner
routes are named.

## Stop-line

Do not publish, tag, push, or merge without an explicit user command.

## Handoff Route

Write a handoff when release readiness needs broad repair, CI debugging,
cross-repo owner action, or human release approval.

## Validation

Run `python scripts/release/release_check.py` when release-prep is intended to be
gating; otherwise report why it was skipped.
