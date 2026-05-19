# Spark Scenario: memory-audit

Use `memory-audit` for read-only checks of one bounded memory surface.

## Scope

Read one memory doctrine file, object profile, schema family, example family,
mechanic-local docs lane, generated reader seam, or small file family. Editing
is out of scope unless the user explicitly asks for audit plus fix.

## Done Signal

Findings are scoped, evidenced, and routed to the memory source, mechanic,
validator, generated builder, or sibling owner that can act on them.

## Stop-line

Do not rewrite the audited surface during audit-only work.

## Handoff Route

Write a handoff when findings require architecture, owner-local decisions,
large rewrites, public status promotion, or cross-repo synthesis.

## Validation

Use the smallest validator tied to the audited surface. If no validator exists,
report a manual source-owner consistency pass.
