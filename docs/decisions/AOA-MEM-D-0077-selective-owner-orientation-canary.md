# Decision: Admit a separate selective owner-orientation canary contour

- Decision ID: AOA-MEM-D-0077

## Status

Accepted on 2026-07-29 for source-local Phase 8 implementation and evaluation.
Runtime deployment and landing remain deferred to the final consolidated gate.

## Index Metadata

- Original date: 2026-07-29
- Surface classes: consumer handoff, boundary/runtime/sibling
- Mechanic parents: consumer-handoff
- Guard families: memory surface, sibling and boundary
- Memory object classes: decision
- Posture: active bounded-canary rationale

## Context

The Phase 1 owner decision intentionally admitted
`codex_owner_orientation_v0` only as an explicit-pull, D0/R1, read-only
consumer. Phase 7 has now composed the SDK, memo, host, runtime, stats, and
eval owners in a consumer-invisible shadow and passed its preregistered
mechanism and safety gate.

The active owner goal separately authorizes Phase 8 selective low-risk canary
work. Hiding that authority change inside the existing pull-only profile would
erase the distinction between operator pull and proactive observation, weaken
rollback, and make later consumer-zero proof ambiguous.

## Decision

Keep `codex_owner_orientation_v0` unchanged as the architecture-A pull-only
rollback target. Add a distinct
`codex_owner_orientation_canary_v0` contour for source-local Phase 8
implementation and evaluation.

The canary contour is limited to:

- one `owner-local` allowlisted consumer and tenant;
- D0 public reviewed memory only;
- R2 bounded proactive observation;
- at most one non-directive reminder per policy window;
- exact source route and currentness shown in the reminder;
- randomized holdout and always-shadow counterfactual;
- no secrets, permissions, role changes, exact tool parameters, external
  effects, irreversible or high-risk actions;
- an operator-versioned C11 policy, explicit kill switch, cooldown, and
  immediate rollback to the unchanged pull-only consumer;
- fresh C18/C19 host admission and a refs-only C20 receipt;
- zero semantic write, candidate persistence, policy self-approval, training,
  tenant expansion, or authority transfer.

SDK may reuse a frozen shadow selection as evidence, but canary delivery
requires a separate typed release plan. The shadow plan is not mutated and
does not retroactively authorize delivery. `aoa-memo` authors the canary
semantics, `abyss-stack` enforces the runtime window and returns only the exact
authorized observation, and `aoa-evals` owns the holdout and benefit verdict.

This decision authorizes source-local implementation and laboratory canary
execution under the active goal. It does not authorize live deployment,
landing, policy promotion beyond this version, or a second consumer.

## Alternatives

- Widen `codex_owner_orientation_shadow_v0` to become visible. Rejected because
  it would invalidate the Phase 7 no-delivery contract and its receipts.
- Widen `codex_owner_orientation_v0` with a proactive mode. Rejected because
  explicit pull is the stable rollback authority and must remain easy to
  reason about and remove.
- Deliver directly from the shadow bundle in `abyss-stack`. Rejected because
  runtime transport cannot manufacture semantic or policy authority.
- Wait for landing before testing Phase 8. Rejected because the active goal
  requires implementation and evidence before the single final landing.

## Consequences

- Phase 8 has a visible and independently removable authority boundary.
- Source-local canary work requires additional profile, policy, SDK release,
  runtime receipt, host-admission, C10, and eval surfaces.
- The canary can fail closed to A without changing the pull-only profile.
- A positive source-local result remains weaker than natural traffic,
  7/30-day soak, or production evidence.
- Every later consumer or policy widening requires a new decision and cannot
  inherit this approval.

## Affected Surfaces

- `mechanics/consumer-handoff/parts/orchestrator-recall-alignment/`
- `docs/memory/MEMORY_MODEL.md`
- `aoa-sdk` consumed-surface posture gate
- `abyss-stack` memo runtime seam
- `abyss-machine` active-organ host admission
- `aoa-stats` C10 outcome receipts
- `aoa-evals` active-organ offline replay bundle

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
Phase 8 additionally requires randomized holdout, always-shadow, instant
disable, rollback-to-A, one-reminder-per-window, boundary tamper, and
counterfactual-versus-actual outcome checks before this contour can advance.
