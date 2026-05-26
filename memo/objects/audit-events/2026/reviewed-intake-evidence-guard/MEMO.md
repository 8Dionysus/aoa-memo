# Reviewed intake landing now rejects missing source and evidence refs

## Memory
Reviewed intake landing must reject packets that lose candidate, receipt, source, or evidence refs before durable corpus landing.

## Source Route
- `docs/decisions/AOA-MEM-D-0064-reviewed-intake-landing.md`
- `scripts/memory/land_reviewed_memo_intake.py`
- `tests/memory/test_reviewed_intake_landing.py`
- `commit:aoa-memo:4844182a46f37aeccb752d10cdf61b5322439792`

## Review Posture
This is a confirmed audit memory for the write path. It can guide future poisoning, over-promotion, and missing-evidence checks, but the script and tests remain the executable truth.

## Next Routes
- Use `scripts/memory/land_reviewed_memo_intake.py` for dry-run and write landing.
- Use `tests/memory/test_reviewed_intake_landing.py` when the landing contract changes.
- Route eval-facing guardrail cases through `mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md`.
