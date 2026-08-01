# MCP owner evidence review

This active part belongs to `mechanics/consumer-handoff/` and materializes the
matching row in `../../PARTS.md`.

## Start Here

- [CONTRACT](CONTRACT.md)
- [VALIDATION](VALIDATION.md)

## Source Surfaces

- `config/review_trust.json`
- `schemas/aoa-memo-brief-review.schema.json`
- `scripts/review_memo_mcp_result.py`
- `tests/test_review_memo_mcp_result.py`
- `aoa-sdk:schemas/organ-access/organ-owner-result-review.schema.json`

## Function

Authenticate one private stack-issued `aoa_memo_brief` capture, bind every
returned reviewed-memory row and central contract to the exact current
`aoa-memo` source revision and generated catalog, and emit a bounded SDK-shaped
owner review.

## Next Route

Send a grounded, exact, unexpired review to `aoa-evals` for central proof.
Owner acceptance remains a later independent `aoa-memo` decision. Use
`../../OWNER_MAP.md` for stronger owner routing.
