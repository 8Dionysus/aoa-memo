# Role-first external actors preserve responsibility across pause and filtered return

## Memory

This is a bounded, reviewed claim about a reusable work contour—not a proof
verdict, production-readiness decision, or completion record for the parent
Goal.

The useful contour is:

`obligation -> role mandate -> model realization -> specialized external incarnation -> same-session pause/resume -> review-required return -> parent wake/reentry -> master filtering -> owner acceptance or rollback`

What is established by the reviewed material:

- The persistent Luna external Codex session stopped and resumed in the same
  thread/incarnation and produced a bounded workspace delta with terminal
  validation.
- The parent controller yielded and reentered with a distinct wake signal.
  Wake-helper delivery, Goal state, and master return filtering stayed separate
  rather than being treated as one acceptance event.
- `abyss-stack` PRs #379 and #386 and `aoa-agents` PRs #280 and #281 landed with
  the source and CI refs recorded below.
- The aoa-agents receipt producer and its post-merge repair validate typed
  responsibility receipt/source projections. They do not prove that a live
  canonical actor event was published to `aoa-stats`.

The rough edges are part of the memory, not incidental noise:

- `review_required` and wake delivery are not owner acceptance; the observed
  master return remained pending filtering.
- The fresh owner preparer failed closed when the writer plan did not bind an
  exact reviewer role.
- Helper success is transport evidence only. Timer drift/rearm, environment-
  limited checks, and a local stats-port validation block remain open.
- The actor shell required `GIT_OPTIONAL_LOCKS=0` to avoid private Git-lock
  drift. A non-empty workspace must be compared through baseline/final
  manifests, not source-manifest equality.

This central object is deliberately a `claim`, not a stronger recurring
`pattern`: the reviewed corpus does not yet contain two independent durable
episode objects for these task-local actor runs. Promotion is an explicit
future step, not an implication of this landing.

## Source Route

The owner source chain is the landed `aoa-agents` and `abyss-stack` material:

- `aoa-agents` PR #280: head `e12abe32fe894a8ea4af2a496408ce8847fa6c6b`,
  merge `17112d91693a9df6e225d61d8cd1e51e091c47bb`, CI run
  `31877734828` (`Repo Validation`).
- `aoa-agents` PR #281: head `b3a4e33e4e9b69c84bdd117bdd6e5de3556f3045`,
  merge `871ec883e9d685b19c57c7355a1c127d90a2a198`, CI run
  `31878584919` (`Repo Validation`).
- `aoa-agents` PR #282: head `96946530390abdb60fd6c917607166b070f719c9`,
  merge `eaecb25c43aadb4eb6f2d3be8c8e4f9334cc2b73`, CI run
  `31880217273` (`Repo Validation`); this is the landed origin-local memo
  candidate/export/receipt change.
- `aoa-agents` PR #283: head `287b5001745bb59417cea0fe39931bc3cdadc077`,
  merge `aa2670f06f439c9bce7715ee6e3988b1be951fb7`, CI run
  `31881265738` (`Repo Validation`); this is the origin-owner correction
  authorizing central materialization as a bounded claim while keeping the
  local candidate pattern-shaped.
- `abyss-stack` PR #379: head `86cb141fc1a20acae44fe29c545e1cbd5cc596b9`,
  merge `e61449fad7f93f2e68452709e4f100d8161db804`, CI run
  `31854045643` (`Repo Validation`, `validate-windows-host-bridge`).
- `abyss-stack` PR #386: head `b2264da25df57e7434fc176818cd851cfd3e1580`,
  merge `21652f9204af4db36b04604ae89fe4d97771eb41`, CI run
  `31876341382` (`Repo Validation`, `validate-windows-host-bridge`).

The exact local intake chain is preserved in the object provenance and in:

- `repo:aoa-agents/memo/candidates/20260815T102919Z.2f2fbde0.role-first-external-actor-work-is-reusable-only.candidate.json`
- `repo:aoa-agents/memo/exports/20260815T103403Z.role-first-external-actor-work-is-reusable-only.aoa-memo-intake.json`
- `repo:aoa-agents/memo/receipts/20260815T111200Z.role-first-external-actor-claim-correction.forwarding-receipt.json`
- `memo/intake/receipts/20260815T111816Z.aoa-agents.role-first-external-actor-responsibility-return.landing-receipt.json`

The earlier `20260815T104000Z` receipt is retained as a machine-readable
`result: rejected` pre-authorization attempt, linked to the current landing
receipt through `receipt_refs`; it is not an active successful landing. The
corpus audit event
`memo.audit.2026-08-15.role-first-external-actor-pre-correction-landing-receipt`
records this provenance/lifecycle correction. The current `20260815T111816Z`
receipt is the only successful landing authority.

The task-local evidence refs are intentionally retained as refs-only
provenance, including the exact sections for runtime proof, parent
pause/resume, master wake separation, responsibility return, receipt repair,
clock-agent filtering, and wake proof:

- `operator:evidence:aoa-external-actors-goal-20260808/live-proof-20260814/runtime-update-luna-handoff.json#/external_actor_proof`
- `operator:evidence:aoa-external-actors-goal-20260808/live-proof-20260814/runtime-update-luna-handoff.json#/parent_pause_resume`
- `operator:evidence:aoa-external-actors-goal-20260808/live-proof-20260814/runtime-update-luna-handoff.json#/master_wake_state_separation`
- `operator:evidence:aoa-external-actors-goal-20260808/live-proof-20260814/runtime-update-luna-handoff.json#/responsibility_return`
- `operator:evidence:aoa-external-actors-goal-20260808/live-proof-20260814/actor-receipt-landing-repair-luna-handoff.json#/final_owner_source`
- `operator:evidence:aoa-external-actors-goal-20260808/live-proof-20260814/clock-agent-003-handoff.json#/return_filter`
- `operator:evidence:aoa-external-actors-goal-20260808/live-proof-20260814/wake-steward-luna-handoff.json#/wake_proof`
- `operator:aoa:sessions/2026-08-15__019__you-are-one-external-codex-process-carrying-a/session.manifest.json#review_status`
- `operator:aoa:sessions/2026-08-15__019__you-are-one-external-codex-process-carrying-a/segments/001__compaction-to-latest.md#event-000040`

`.aoa` raw/session material remains provisional supporting evidence. It is
not silently upgraded to reviewed truth by this memo. The copied reviewed
intake packet retains the exact machine-resolved operator refs; this public
object uses owner-relative aliases so generated readmodels do not expose
machine-local roots.

## Review Posture

Identity: `memo.claim.2026-08-15.role-first-external-actor-responsibility-return`.

Lifecycle/currentness: `confirmed` and `promoted` in the reviewed corpus,
`current_recall.status=allowed`, temperature `cool`, confidence `0.86`, valid
from the corrected landing at `2026-08-15T11:18:16Z`. Recheck the active runtime release, rollback
admission, wake/timer state, workspace manifests, and live-feed status before
using this memory to orchestrate a new actor.

The origin port was reviewed for `reviewed_write` after its pattern-shaped
candidate, correction forwarding receipt, source refs, evidence refs, and
guardrails resolved. The correction explicitly authorizes `aoa-memo` to
materialize a bounded `claim`; it does not authorize recurring-pattern
admission. The forwarding receipt is only a route check. The central landing
receipt records the separate `aoa-memo` source landing and its
schema/guardrail checks.

The accepted boundary is typed responsibility surviving a pause, wake, and
return when each transition is evidenced and filtering remains explicit. This
memo does not claim full parent-Goal completion, autonomous agency, model fit,
recurring production readiness, benefit, live aoa-stats admission, host/service
lifecycle change, or owner acceptance inferred from transport.

## Next Routes

- For role meaning and receipt contracts, continue in `aoa-agents` at
  `skills/aoa-summon/` and decision `AOA-AG-D-0066`.
- For runtime activation, rollback, workspace delta, and external-process
  mechanics, recheck the `abyss-stack` PR #386 landing and its runtime handoff.
- For canonical actor-event publication and live statistics, route separately
  to `aoa-stats`; do not infer it from PR #280/#281 or a green source check.
- For evaluator/model-fit and role-scoped MCP admission, route to the owning
  proof/eval surfaces when fresh evidence exists.
- After two independent reviewed episode objects exist, review whether this
  bounded claim should be superseded or promoted to a recurring pattern.
