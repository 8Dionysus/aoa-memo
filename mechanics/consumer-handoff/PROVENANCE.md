# Consumer Handoff Provenance Bridge

Use active surfaces first:

- [README](README.md)
- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [OWNER_MAP](OWNER_MAP.md)
- [docs](docs/)
- [parts](parts/)

The active route is now `mechanics/consumer-handoff/docs/` because these
surfaces share one repeatable memory-layer operation: publish bounded
consumer-facing handoffs while stronger owners keep role policy, playbook
composition, proof, graph substrate, ToS source meaning, routing, and runtime.

Former flat docs-root surfaces were:

- `AGENT_MEMORY_POSTURE_SEAM.md`
- `PLAYBOOK_MEMORY_SCOPES.md`
- `MEMORY_EVAL_GUARDRAILS.md`
- `KAG_TOS_BRIDGE_CONTRACT.md`
- `KAG_SOURCE_EXPORT.md`
- `ORCHESTRATOR_MEMORY_ALIGNMENT.md`

The active technical artifacts now live under the nearest functioning part:

- KAG/ToS bridge faces: `parts/kag-tos-bridge-handoff/{schemas,examples}/`
- KAG source export donor, generator, and source contract:
  `parts/kag-source-export/{schemas,examples,generated,scripts}/`
- Eval guardrail pack: `parts/eval-guardrail-handoff/{schemas,examples}/`
- Playbook scope regression: `parts/playbook-scope-handoff/tests/`
- Consumer feed regression: `parts/downstream-feed-regression/tests/`

Former package-level `schemas/`, `examples/`, `generated/`, `scripts/`, and
`tests/` homes are placement history only after the 2026-05-19 part-local
artifact move.

Use [legacy/INDEX](legacy/INDEX.md) only to audit former placement. Legacy
paths are historical receipts, not active contracts.
