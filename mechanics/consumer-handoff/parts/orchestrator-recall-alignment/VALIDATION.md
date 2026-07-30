# Orchestrator recall alignment Validation

Executable validation for this part is routed through the package validation lane.

Run from the repository root:

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
```

Then run the package-specific commands named in `../../AGENTS.md#validation` for any changed source docs, schemas, examples, generated companions, scripts, tests, manifests, or owner routes.

Focused validation:

```bash
python -m pytest -q mechanics/consumer-handoff/parts/orchestrator-recall-alignment/tests
ruff check mechanics/consumer-handoff/parts/orchestrator-recall-alignment
```

The source-local integration lane additionally supplies an exact SDK plan
schema to `scripts/codex_owner_orientation_packet.py`; there is no implicit
checkout lookup or compatibility fallback.

The canary integration lane must additionally supply the exact SDK canary
release schema and memo-owned compatibility pin to
`scripts/codex_owner_orientation_canary.py`. The builder fails closed on any
profile, policy, release-schema, shadow-source, or self-digest drift.

The Phase 9 utility tests validate the strict proposal schema, bounded weight
delta, delayed-outcome freeze, reward-hacking and accidental-success freeze,
access-count invariance, rare-critical preservation, semantic immutability,
and exact rollback target.

The Phase 12 promotion tests validate exact namespace/tenant binding,
outcome-qualified nomination, duplicate/no-write, conflict quarantine,
operator approve/reject/defer/narrow decisions, and the invariant that
admission leaves the shared ledger and semantic lifecycle unchanged:

```bash
python mechanics/consumer-handoff/parts/orchestrator-recall-alignment/scripts/agent_local_promotion.py
python -m pytest -q mechanics/consumer-handoff/parts/orchestrator-recall-alignment/tests/test_agent_local_promotion.py
```

The participation-shadow lane validates exact trigger classes, sibling
handoffs, correct silence, synthetic-goal exclusion, receipt schema and hash
chain, concurrent appends, fail-open behavior, content minimization, zero hook
output, false authority, and refusal to claim use or benefit:

```bash
python -m pytest -q \
  mechanics/consumer-handoff/parts/orchestrator-recall-alignment/tests/test_aoa_memo_participation_hook.py \
  mechanics/consumer-handoff/parts/orchestrator-recall-alignment/tests/test_aoa_memo_participation_contract.py \
  mechanics/consumer-handoff/parts/orchestrator-recall-alignment/tests/test_aoa_memo_participation_retention.py
```

The retention lane additionally proves plan-only default behavior, a minimum
30-day window, explicit execution acknowledgement, whole-session erasure,
closed-session eligibility, invalid-chain preservation, content-free reports,
and coordination with the append path.

The source fragment must then be bound and merged by the independent
`abyss-stack` Codex-hook compositor. Passing this part-local lane does not prove
Codex trust, live execution, prompt-visible skill selection, use, action
change, outcome, or benefit.
