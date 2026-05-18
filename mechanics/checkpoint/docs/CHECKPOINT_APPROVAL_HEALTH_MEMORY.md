# Checkpoint Approval And Health Memory

Checkpoint approval and health records are memory objects only when they remain
source-linked and weaker than the stronger owner decision.

## Approval Records

Approval records map to `decision` objects. They may preserve that a reviewed
gate outcome existed, who or what the source route names, and which future
recall status applies.

They must not grant future approval by themselves.

## Health Records

Health records map to `episode` or `audit_event` objects depending on whether
the surface records observed execution or review posture.

They must not become current health truth.

## Improvement Threads

Checkpoint improvement threads use `provenance_thread` to connect approval,
rollback, health, and improvement-log evidence.

They keep walk-back possible without turning a past checkpoint into proof of
present readiness.
