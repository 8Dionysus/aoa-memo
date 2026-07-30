# Orchestrator recall alignment

This active part belongs to `mechanics/consumer-handoff/` and materializes the matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- [ORCHESTRATOR_MEMORY_ALIGNMENT](../../docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md)
- `schemas/codex_owner_orientation_profile_v0.schema.json`
- `schemas/codex_owner_orientation_sdk_compatibility_pin_v0.schema.json`
- `schemas/codex_owner_orientation_memo_bundle_v0.schema.json`
- `examples/codex_owner_orientation_v0.consumer-profile.json`
- `examples/codex_owner_orientation_v0.influence-policy.json`
- `examples/codex_owner_orientation_v0.sdk-compatibility-pin.json`
- `schemas/codex_owner_orientation_shadow_profile_v0.schema.json`
- `examples/codex_owner_orientation_shadow_v0.consumer-profile.json`
- `examples/codex_owner_orientation_shadow_v0.influence-policy.json`
- `schemas/codex_owner_orientation_shadow_sdk_compatibility_pin_v0.schema.json`
- `examples/codex_owner_orientation_shadow_v0.sdk-compatibility-pin.json`
- `schemas/codex_owner_orientation_shadow_bundle_v0.schema.json`
- `scripts/codex_owner_orientation_shadow.py`
- `schemas/codex_owner_orientation_canary_profile_v0.schema.json`
- `schemas/codex_owner_orientation_canary_sdk_compatibility_pin_v0.schema.json`
- `schemas/codex_owner_orientation_canary_bundle_v0.schema.json`
- `examples/codex_owner_orientation_canary_v0.consumer-profile.json`
- `examples/codex_owner_orientation_canary_v0.influence-policy.json`
- `examples/codex_owner_orientation_canary_v0.sdk-compatibility-pin.json`
- `scripts/codex_owner_orientation_canary.py`
- `schemas/outcome_qualified_episodic_utility_policy_proposal_v0.schema.json`
- `scripts/episodic_utility.py`
- `schemas/agent_local_shared_promotion_candidate_v0.schema.json`
- `schemas/agent_local_promotion_admission_receipt_v0.schema.json`
- `examples/agent_local_shared_promotion_candidate_v0.example.json`
- `examples/agent_local_promotion_admission_receipt_v0.example.json`
- `scripts/agent_local_promotion.py`
- `config/codex-hooks.aoa-memo-participation-shadow.fragment.json`
- `schemas/aoa_memo_participation_hook_fragment_v0.schema.json`
- `schemas/aoa_memo_participation_receipt_v0.schema.json`
- `schemas/aoa_memo_participation_retention_report_v0.schema.json`
- `scripts/aoa_memo_participation_hook.py`
- `scripts/codex_owner_orientation_packet.py`
- `tests/test_codex_owner_orientation_profile.py`
- `tests/test_episodic_utility_policy_proposal.py`
- `tests/test_agent_local_promotion.py`
- `tests/test_aoa_memo_participation_hook.py`
- `tests/test_aoa_memo_participation_retention.py`

## Function

Aligns router, review, and bounded-execution quest families to memo recall
posture. The `codex_owner_orientation_v0` pack additionally turns one exact
SDK selection plan into memo-owned C08/C09 without granting runtime,
writeback, policy, role, or effect authority.

The separate `codex_owner_orientation_shadow_v0` profile admits D0/R4
consumer-invisible packet construction for selective and always-shadow labs.
It accepts pressure and quarantine semantics, currentness and outcome inputs,
and may emit retention or policy proposals, but it cannot persist a candidate,
perform a semantic transition, deliver content, or promote a policy.

`codex_owner_orientation_canary_v0` is a third consumer with its own
operator-approved D0/R2 profile and C11 policy. It may turn exactly one frozen
selective-shadow item into a source/currentness-visible observation under an
eval-owned randomized assignment, stats-owned outcome refs, current host
admission, one-reminder window, cooldown, and kill switch. It cannot issue a
directive, persist content, write or transition memory, approve policy,
change roles or permissions, supply tool parameters, or authorize effects.

The Phase 9 episodic utility surface consumes an exact descriptive
`aoa-stats` aggregate and an `aoa-evals` verdict. It may produce only a
bounded ranking, cooldown, projection, abstraction, cadence, or budget
proposal with an exact rollback target. It cannot apply policy, use access
count as utility, mutate semantic memory, or change owner, tenant,
permissions, promotion, deletion, or retraction.

The Phase 12 agent-local federation surface accepts a content-minimized
promotion nomination from one exact `aoa-agents` namespace and tenant. It
records operator review, duplicate and conflict handling, and promotion burden
but can yield only a memo candidate or an explicit no-write result. The shared
ledger and semantic lifecycle remain unchanged.

The participation-shadow fragment is an independent H0 Codex hook source for
ordinary persistent sessions. It classifies only coarse opportunity and
lifecycle stages, hashes session/turn/tool refs, and observes completed
`aoa_memo` tool calls without retaining prompt, transcript, tool input, tool
response, memory payload, or assistant output. It emits no stdout, injects no
context, blocks nothing, continues nothing, and writes no memory. A neutral
`abyss-stack` compositor must bind and merge the fragment; neither
`aoa-session-memory` nor its hook renderer is a dependency.

H0 receipt retention is likewise independent and operator-driven. The
`retention` command plans by default and can erase only whole, valid chains
whose final event is `SessionEnd` and whose final observation is outside a
minimum 30-day window (45 days by default). Execution requires both
`--execute` and `--acknowledge-whole-session-erasure`; it never runs from a
Codex hook, never changes semantic memory, and emits only aggregate,
content-free counts.

## Next Route

Use `../../OWNER_MAP.md` for stronger owner routing and `../../PROVENANCE.md` for placement history.
