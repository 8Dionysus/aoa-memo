# Writeback Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Runtime and temperature | [RUNTIME_WRITEBACK_SEAM](./docs/RUNTIME_WRITEBACK_SEAM.md), [WRITEBACK_TEMPERATURE_POLICY](./docs/WRITEBACK_TEMPERATURE_POLICY.md) | keeps runtime writeback mapped without runtime ownership |
| Quest and chronicle | [QUEST_CHRONICLE_WRITEBACK](./docs/QUEST_CHRONICLE_WRITEBACK.md), [QUEST_EVIDENCE_WRITEBACK](./docs/QUEST_EVIDENCE_WRITEBACK.md), [QUESTBOOK_MANUAL_FIRST_WRITEBACK](./docs/QUESTBOOK_MANUAL_FIRST_WRITEBACK.md), [HARVEST_TO_MEMORY_WRITEBACK](./docs/HARVEST_TO_MEMORY_WRITEBACK.md) | keeps quest writeback source-linked and manual-first |
| Revision ledgers | [REVISION_LEDGER_WRITEBACK](./docs/REVISION_LEDGER_WRITEBACK.md), [RELEASE_REVISION_LEDGER_WRITEBACK](./docs/RELEASE_REVISION_LEDGER_WRITEBACK.md), [DECISION_HISTORY_WRITEBACK](./docs/DECISION_HISTORY_WRITEBACK.md), [REVOCATION_LEDGER_WRITEBACK](./docs/REVOCATION_LEDGER_WRITEBACK.md) | keeps revision and revocation writeback reviewable |
| Rollback and recovery | [ROLLBACK_MEMORY_WRITEBACK](./docs/ROLLBACK_MEMORY_WRITEBACK.md), [ROLLBACK_REVISION_LEDGER_WRITEBACK](./docs/ROLLBACK_REVISION_LEDGER_WRITEBACK.md), [TRAIN_ROLLBACK_MEMORY_WRITEBACK](./docs/TRAIN_ROLLBACK_MEMORY_WRITEBACK.md) | keeps rollback memory bounded |
| Growth and continuity | [GROWTH_REFINERY_WRITEBACK](./docs/GROWTH_REFINERY_WRITEBACK.md), [WORKSPACE_CHECKPOINT_GROWTH_WRITEBACK](./docs/WORKSPACE_CHECKPOINT_GROWTH_WRITEBACK.md), [SELF_AGENCY_CONTINUITY_WRITEBACK](./docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md), [A2A_CHILD_RETURN_WRITEBACK](./docs/A2A_CHILD_RETURN_WRITEBACK.md) | keeps growth and continuity writeback owner-routed |
| Receipt publication regression | `mechanics/writeback/parts/receipt-publication-regression/tests/fixtures/memo_writeback_receipts.example.jsonl`, `mechanics/writeback/parts/receipt-publication-regression/tests/test_publish_live_receipts.py`, `mechanics/writeback/parts/receipt-publication-regression/scripts/publish_live_receipts.py` | keeps tracked writeback receipts part-local and recall-surface backed |

## Interface

Inputs are reviewed source refs, target maps, and writeback candidates. Outputs
are bounded memo docs, generated companions, and owner handoff routes.
