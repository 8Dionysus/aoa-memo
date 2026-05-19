# Consumer Handoff Parts Index

Functioning Consumer Handoff memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Agent posture handoff](agent-posture-handoff/README.md) - names memo-side fields that agent rights may apply to without becoming role policy
- [Playbook scope handoff](playbook-scope-handoff/README.md) - tells playbooks how to request bounded recall modes and scopes
- [Eval guardrail handoff](eval-guardrail-handoff/README.md) - names memory quality risk cases for downstream proof owners
- [KAG/ToS bridge handoff](kag-tos-bridge-handoff/README.md) - defines chunk-face, graph-face, and ToS bridge posture without graph ownership
- [KAG source export](kag-source-export/README.md) - describes the source-owned tiny donor export for KAG readiness
- [Orchestrator recall alignment](orchestrator-recall-alignment/README.md) - aligns router, review, and bounded-execution quest families to memo recall posture
- [Downstream feed regression](downstream-feed-regression/README.md) - keeps consumer-facing recall, KAG export, checkpoint, and writeback read surfaces aligned without becoming runtime authority

## Validation

Use the package validation lane in [AGENTS](../AGENTS.md#validation).

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```
