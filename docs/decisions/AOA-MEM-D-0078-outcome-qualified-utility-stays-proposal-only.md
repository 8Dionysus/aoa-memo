# Decision: Keep outcome-qualified episodic utility proposal-only

- Decision ID: AOA-MEM-D-0078

## Status

Accepted on 2026-07-29 for source-local Phase 9 implementation and evaluation.
Policy application, runtime deployment, and landing remain deferred.

## Index Metadata

- Original date: 2026-07-29
- Surface classes: consumer handoff, boundary/runtime/sibling
- Mechanic parents: consumer-handoff
- Guard families: memory surface, sibling and boundary
- Memory object classes: decision, episode
- Posture: active proposal-only utility rationale

## Context

Phase 6 produced strict C10 outcome receipts with action-before/action-after,
terminal and delayed outcome, holdout or paired counterfactual, accidental
success, harm, evaluator, and reward-hacking evidence posture. Phase 8 then
passed a source-local selective canary mechanism. Neither result authorizes
access count, terminal success, retrieval frequency, or a learned score to
change reviewed meaning or lifecycle.

The active-organ goal permits Phase 9 to test bounded utility-informed ranking,
cooldown, projection, abstraction, cadence, and budget proposals. It forbids
semantic promotion, deletion, retraction, owner or tenant expansion,
permission expansion, and automatic policy self-approval.

## Decision

Admit a distinct outcome-qualified episodic utility contour with four owners:

- `aoa-stats` validates C10 and produces descriptive compatible aggregates;
- `aoa-evals` decides whether the evidence supports a bounded proposal and
  owns reward-hacking, accidental-success, holdout, and adversarial verdicts;
- `aoa-memo` owns the meaning and strict shape of an episodic utility policy
  proposal, including its authority ceiling and rollback target;
- `aoa-kag` may materialize only a disposable, lab-only ranking projection
  from an exact proposal and decision pin.

`aoa-sdk` remains the future control-plane admission owner. No proposal or
projection becomes a consumer policy without a separate operator-approved
version and SDK admission. `abyss-stack` receives no Phase 9 runtime mutation.

Utility qualification requires:

- memory use and a material action change;
- terminal task-owner outcome evidence;
- holdout, paired, or always-shadow counterfactual evidence;
- delayed outcome posture and confounder accounting;
- independent eval posture, including reward-hacking evidence;
- explicit accidental-success and harm posture.

Pending or overdue delayed effects freeze positive adjustment. Terminal
success without action change carries no qualified positive utility.
Access count is absent from the measurement and proposal ABIs.

Rare critical or constitutional memory cannot disappear because its observed
frequency or signed utility is low. Phase 9 may propose source-first projection
or a bounded cooldown, but it cannot demote, archive, delete, retract, or
rewrite that memory.

Every proposal pins the previous and candidate policy versions and an exact
rollback target. Phase 9 may prove application and exact rollback only in a
disposable lab projection with no runtime consumer and no recall eligibility.

This decision authorizes source-local contracts, deterministic validators,
adversarial evaluation, and lab artifacts. It does not authorize policy
approval, live ranking change, semantic transition, deployment, or landing.

## Alternatives

- Add utility fields directly to reviewed episode objects. Rejected because
  outcome-derived ranking evidence is volatile and must not rewrite semantic
  memory.
- Let `aoa-stats` issue the adjustment verdict. Rejected because statistics
  owns compatible aggregation, not proof or policy.
- Let `aoa-evals` write ranking weights. Rejected because eval owns the verdict,
  not memory meaning or consumer policy.
- Apply a score directly inside `abyss-stack`. Rejected because runtime cannot
  manufacture semantic, proof, or control-plane authority.
- Use access or retrieval count as a reinforcement signal. Rejected because it
  creates popularity lock-in and poisoning amplification without task benefit.

## Consequences

- Outcome evidence can influence a bounded proposal without modifying reviewed
  memory or broadening authority.
- Positive adjustment freezes while delayed outcomes remain unresolved.
- Accidental success and reward-hacking failures cannot increase utility.
- Rare critical evidence keeps an explicit preservation floor.
- Rollback can be tested against an exact prior policy and projection digest.
- A positive Phase 9 lab remains weaker than deployed multi-tenant,
  natural-traffic, and long-horizon evidence.

## Affected Surfaces

- `mechanics/consumer-handoff/parts/orchestrator-recall-alignment/`
- `docs/memory/MEMORY_MODEL.md`
- `aoa-stats` measurement-packet crossing
- `aoa-evals` active-organ offline replay bundle
- `aoa-kag` projection-health part
- `aoa-sdk` C24 rollback envelope as a future composition boundary

## Verification

Phase 9 must prove:

- positive evidence requires outcome, action change, counterfactual, and eval;
- delayed pending evidence freezes positive change;
- reward hacking and accidental success do not earn weight;
- access-count perturbation does not change the proposal;
- rare critical evidence survives low frequency and adverse score;
- semantic state, owner, tenant, permissions, promotion, deletion, and
  retraction remain unchanged;
- a lab-applied weight version rolls back exactly to its pinned predecessor.
