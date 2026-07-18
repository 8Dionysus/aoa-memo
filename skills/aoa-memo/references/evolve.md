# Evolve

Use this mode when the request asks to create, land, change, consolidate,
supersede, retract, withdraw, quarantine, or rebuild an owner corpus,
lifecycle, contract, object source, or read-model source. Select this mode from
the requested operation even when the entry gates below will block execution.

## Owner entry

After source return:

1. The next tool turn must read only
   `<owner_root>/memo/AGENTS.md`. Await its result before reading the target,
   origin port, origin evidence, or another owner document.
2. For reviewed intake, durable corpus landing, object creation, or a
   source-backed read-model rebuild, the following tool turn must read only
   `<owner_root>/docs/decisions/AOA-MEM-D-0064-reviewed-intake-landing.md`.
   Await its result before reading the target.

If either required serial read is skipped, reordered, or batched with another
read, return `blocked_owner_entry_not_observed`. Later reads cannot repair the
gate.

## Entry gates

Require all of:

- resolved origin and durable owner
- accepted review or explicit source-owned review
- one bounded target and acceptance criteria
- explicit effect authority
- any human confirmation required by the owner route

If any gate is missing, return `blocked` or `needs_owner_review` before
planning writes, comparing unrelated objects, running landing commands, or
creating artifacts.

When the request names one exact candidate or export, read that target once
immediately after the serial owner entry when its state is needed to evaluate
the entry gates. This must be the first task-workspace read. Use a
line-number-preserving read on that first pass when citations may be needed;
never reread the target only to add citations.

If that target itself says review is required, direct durable write is false,
or reviewed intake is required without an accepted reviewed-write export, the
durable-review gate is missing. Return `needs_owner_review` immediately. Do not
read its origin refs, origin port, neighboring packet, receipt, corpus object,
generated companion, or another task-workspace source. An origin source may
support the local candidate, but it cannot turn that candidate into accepted
durable intake. Do not load the `review` procedure merely because review is a
missing gate.

For this terminal pre-review result, `missing_inputs` may contain only:

- a reviewed export with `allowed_result: reviewed_write`
- explicit origin-owner acceptance for durable reviewed intake
- explicit `aoa-memo` review accepting the exact material
- explicit effect authority
- required human confirmation after an accepted dry-run plan exists

A dry-run landing plan, corpus object, copied intake, receipt, or generated
companion is a future output, not a missing entry input.

## Procedure

1. Choose the owner surface before the file shape:
   - raw session evidence stays in `.aoa`
   - pre-review project memory stays in the origin `memo/` port
   - accepted durable memory lands in `aoa-memo/memo/objects/`
   - material lifecycle changes also produce an `audit_event`
   - generated catalogs and access planes remain derived
   - proof, role, route, workflow, graph, and runtime changes hand off
2. Compare reuse, correction, consolidation, supersession, retraction,
   withdrawal, archive, quarantine, new object, and `no_change`. Prefer the
   smallest existing owner surface that satisfies the accepted review.
3. For an incoming reviewed export, run the source-owned landing command
   without write first. Inspect the exact export, candidates, receipts, object
   ID, kind, slug, title, summary, provenance, lifecycle, recall posture,
   copied intake, and landing receipt.
4. Add write only after review and owner confirmation accept that exact plan.
   Capture the owner-required checkpoint or rollback posture before mutation.
5. Change authored source before generated companions. Rebuild only declared
   read models, inspect the actual object and projections, and keep source refs
   walkable backward.
6. Exercise the motivating case, stale or contradictory case, strongest
   negative case, and one intended consumer handoff manually. Add permanent
   automation only for a stable long-lived invariant exposed by those trials.
7. Return the common output ABI with actual effects, artifacts, verification,
   skipped checks, remaining uncertainty, authority ceiling, and stop line.

## Verification

- inspect the source object and every generated companion actually changed
- prove generated outputs remain weaker than their source
- verify the exact reviewed target rather than a neighboring candidate
- report skipped live, cross-owner, model, host, security, and consumer checks

## Stop

Stop before mutation when review, owner, target, authority, confirmation,
checkpoint, rollback, or exact landing inputs are missing. A successful write
without verified source and consumer posture is not `verified_bounded`.
