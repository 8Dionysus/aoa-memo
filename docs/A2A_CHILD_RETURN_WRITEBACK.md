# A2A Child Return Writeback

## Purpose

This note defines the memo-side writeback posture for reviewed A2A child
returns.

It does not create a new memory object family.
It does not make `aoa-memo` a child-task runtime store.
It does not turn child traces, SDK plans, eval packets, or runtime dry-run
receipts into memo truth.

The owning route remains in `aoa-playbooks`.
The summon contract remains in `aoa-skills`.
The A2A helper payload remains in `aoa-sdk`.
The proof bundle remains in `aoa-evals`.
The dry-run adapter remains in `abyss-stack`.

## Core Rule

A reviewed A2A child return may write only bounded memo candidates through the
existing runtime writeback seam.

The memo layer may preserve replay aids, decisions, and audit witnesses.
It may not promote a child result, checkpoint bridge, or runtime receipt into
canonical route truth.

## Mapping

Reuse `examples/checkpoint_to_memory_contract.example.json`.

Recommended mapping:

- `return_plan` and `summon_decision` may become a `decision` candidate through
  the existing `transition_record` mapping when they shaped re-entry.
- `checkpoint_bridge_plan` may become a `decision` candidate when it records a
  reviewed closeout decision rather than a provisional checkpoint hint.
- reviewed child verification may become an `audit_event` candidate through
  the existing `review_trace` mapping.
- the bounded checkpoint state carried for parent re-entry may become a
  `state_capsule` candidate through the existing `checkpoint_export` mapping.
- a replay chain across summon request, SDK decision, child result, checkpoint
  bridge, eval packet, memo writeback ref, and dry-run receipt may use
  `examples/provenance_thread.example.json` as a provenance-thread precedent
  when a human needs route replay.
- the current full-chain replay candidate is
  `examples/provenance_thread.a2a-summon-return-checkpoint.example.json`,
  anchored to
  `repo:aoa-sdk/examples/a2a/summon_return_checkpoint_e2e.fixture.json`.

`provenance_thread` remains a bounded replay aid. It is not a runtime target
inside `generated/runtime_writeback_targets.min.json`.

## Review Gates

Before any durable memo candidate is accepted:

- the parent anchor must be named
- the child result must be reviewed
- the checkpoint bridge plan must be lower-authority than reviewed closeout
- the eval packet must remain a proof candidate
- the runtime receipt must remain dry-run only
- source refs must point back to owning repositories rather than copying their
  meaning into `aoa-memo`

## What To Refuse

Refuse writeback when:

- the child result is unreviewed
- the route needs split or human gate but proceeds anyway
- the memo candidate is being used as proof
- the runtime dry-run receipt is described as live execution
- a checkpoint note is treated as final harvest, progression, or quest truth
- SDK payloads are treated as runtime authority

## Reference Surfaces

- `docs/RUNTIME_WRITEBACK_SEAM.md`
- `examples/checkpoint_to_memory_contract.example.json`
- `examples/provenance_thread.example.json`
- `docs/PROVENANCE_THREADS.md`
- `docs/AUDIT_EVENTS.md`
