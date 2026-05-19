# Decisions

This directory holds durable decision records for `aoa-memo`.

Use it when a future contributor will need the rationale for a route,
topology, source-of-truth split, validator, public contract, or workflow
expectation.

## What Belongs Here

- structural placement decisions
- root or docs-root route-law decisions
- AGENTS mesh or agent-lane decisions
- validator-authority decisions
- public-contract and source-of-truth split decisions
- cross-repo boundary decisions that need local rationale

## What Stays Elsewhere

| Material | Home |
|---|---|
| active memory doctrine | current docs such as `MEMORY_MODEL`, `BOUNDARIES`, and `OPERATIONAL_BOUNDARY` |
| schemas and machine contracts | `schemas/` |
| public-safe examples | `examples/` |
| generated companions | `generated/` |
| release history | `CHANGELOG.md` |
| future work | `ROADMAP.md` or `QUESTBOOK.md` |
| raw evidence or private traces | not in this public repo unless sanitized and routed |

## Index

| Decision | Scope |
|---|---|
| [2026-05-18-memory-topology-spine](2026-05-18-memory-topology-spine.md) | add topology-spine surfaces before moving flat docs |
| [2026-05-18-spark-agent-lane-home](2026-05-18-spark-agent-lane-home.md) | move maintained Spark lane from root to `.agents/spark/` |
| [2026-05-18-agents-mesh-source-backed-route-cards](2026-05-18-agents-mesh-source-backed-route-cards.md) | add source-backed AGENTS mesh for current route cards |
| [2026-05-18-agon-docs-district](2026-05-18-agon-docs-district.md) | move flat Agon memo docs into `docs/agon/` |
| [2026-05-18-titan-docs-district](2026-05-18-titan-docs-district.md) | move flat Titan memo docs into `docs/titan/` |
| [2026-05-18-adoption-writeback-retention-mechanics](2026-05-18-adoption-writeback-retention-mechanics.md) | move adoption, writeback, and retention docs-root surfaces into memo mechanics |
| [2026-05-18-mechanics-subroutes-artifact-topology](2026-05-18-mechanics-subroutes-artifact-topology.md) | add docs/legacy mechanic subroutes and artifact placement law |
| [2026-05-18-agon-titan-memo-mechanics](2026-05-18-agon-titan-memo-mechanics.md) | supersede Agon/Titan docs districts with memo mechanic packages |
| [2026-05-18-antifragility-memo-mechanic](2026-05-18-antifragility-memo-mechanic.md) | move failure-lesson and recovery-pattern docs into an antifragility memo mechanic |
| [2026-05-18-governance-memo-mechanic](2026-05-18-governance-memo-mechanic.md) | move governance, federation, installation, certification, precedent, and stay-order docs into a governance authority-boundary memo mechanic |
| [2026-05-18-shape-guard-memo-mechanic](2026-05-18-shape-guard-memo-mechanic.md) | add shape-guard as the via-negativa operation-first memo mechanic |
| [2026-05-18-consumer-handoff-memo-mechanic](2026-05-18-consumer-handoff-memo-mechanic.md) | move agent, playbook, eval, KAG/ToS, KAG export, and orchestrator alignment docs into a consumer-handoff memo mechanic |
| [2026-05-18-operational-gate-memo-mechanic](2026-05-18-operational-gate-memo-mechanic.md) | move deployment, office/service, service revision, and post-release boundary docs into an operational-gate memo mechanic |
| [2026-05-18-recurrence-support-memo-mechanic](2026-05-18-recurrence-support-memo-mechanic.md) | move recurrence support, witness trace, and reviewed closeout landing docs into a recurrence-support memo mechanic |
| [2026-05-18-lineage-harvest-memo-mechanic](2026-05-18-lineage-harvest-memo-mechanic.md) | move pattern-lineage memory into a lineage-harvest memo mechanic |
| [2026-05-18-checkpoint-memo-mechanic](2026-05-18-checkpoint-memo-mechanic.md) | add checkpoint as the memo mechanic for checkpoint gates, carry, approval, health, improvement, and checkpoint-to-memory artifacts |
| [2026-05-18-readiness-boundary-memo-mechanic](2026-05-18-readiness-boundary-memo-mechanic.md) | move readiness boundary doctrine, schema, example, and regression test into a readiness-boundary memo mechanic |
| [2026-05-18-quest-generated-owner-routes](2026-05-18-quest-generated-owner-routes.md) | keep root quest generated companions builder-backed and mechanic-routed |
| [2026-05-18-questbook-lane-first-store](2026-05-18-questbook-lane-first-store.md) | add Questbook mechanic and move quest sources into lane-first root store |
| [2026-05-18-mechanic-artifact-topology-validator](2026-05-18-mechanic-artifact-topology-validator.md) | add a release-gate validator for mechanic-owned root artifact drift |
| [2026-05-18-root-technical-district-allowlist](2026-05-18-root-technical-district-allowlist.md) | make remaining root technical artifacts exact and machine-auditable |
| [2026-05-18-root-schema-family-contracts](2026-05-18-root-schema-family-contracts.md) | make root schemas family-owned and release-checkable |
| [2026-05-18-root-example-family-contracts](2026-05-18-root-example-family-contracts.md) | make root examples family-owned and release-checkable |
| [2026-05-18-root-config-manifest-control-plane](2026-05-18-root-config-manifest-control-plane.md) | make root config family-owned and root manifests policy-owned |
| [2026-05-18-root-generated-family-contracts](2026-05-18-root-generated-family-contracts.md) | make root generated outputs family-owned and release-checkable |
| [2026-05-18-root-script-family-contracts](2026-05-18-root-script-family-contracts.md) | make root scripts family-owned and release/test covered |
| [2026-05-18-root-test-family-contracts](2026-05-18-root-test-family-contracts.md) | make root tests and public fixtures family-owned and release-checkable |
| [2026-05-18-mechanic-artifact-inventory](2026-05-18-mechanic-artifact-inventory.md) | add a generated inventory for package-local mechanic artifacts |
| [2026-05-18-mechanic-parts-shape-validator](2026-05-18-mechanic-parts-shape-validator.md) | make functioning mechanic parts shape release-checkable |
| [2026-05-18-mechanic-physical-parts](2026-05-18-mechanic-physical-parts.md) | materialize each active mechanic part as a physical contract and validation node |
| [2026-05-19-agon-part-local-artifacts](2026-05-19-agon-part-local-artifacts.md) | move Agon runnable artifacts into the nearest functioning part-local homes |
| [2026-05-19-titan-part-local-artifacts](2026-05-19-titan-part-local-artifacts.md) | move Titan runnable artifacts into functioning part-local homes |
| [2026-05-19-adoption-retention-part-local-artifacts](2026-05-19-adoption-retention-part-local-artifacts.md) | move adoption and retention schemas, examples, and tests into functioning part-local homes |
| [2026-05-19-writeback-part-local-artifacts](2026-05-19-writeback-part-local-artifacts.md) | move writeback schemas, examples, generated companions, scripts, tests, and receipt fixtures into functioning part-local homes |
| [2026-05-19-checkpoint-part-local-artifacts](2026-05-19-checkpoint-part-local-artifacts.md) | move checkpoint schemas, examples, tests, and consumer refs into functioning part-local homes |
| [2026-05-19-consumer-handoff-part-local-artifacts](2026-05-19-consumer-handoff-part-local-artifacts.md) | move consumer-handoff schemas, examples, generated export, generator, and tests into functioning part-local homes |
| [2026-05-19-governance-part-local-artifacts](2026-05-19-governance-part-local-artifacts.md) | move governance schemas, examples, and regressions into functioning part-local homes |
| [2026-05-19-antifragility-part-local-artifacts](2026-05-19-antifragility-part-local-artifacts.md) | move antifragility schemas, examples, native pattern source, and regressions into functioning part-local homes |
| [2026-05-18-mechanic-readiness-matrix](2026-05-18-mechanic-readiness-matrix.md) | add a generated readiness matrix for all memo mechanic packages |
| [2026-05-18-mechanic-readiness-artifact-test-coverage](2026-05-18-mechanic-readiness-artifact-test-coverage.md) | require package-local tests for mechanics with package-local non-test artifacts |
| [2026-05-18-mechanic-readiness-local-test-routes](2026-05-18-mechanic-readiness-local-test-routes.md) | require route-card visibility for package-local mechanic test commands |
| [2026-05-18-mechanic-route-card-index](2026-05-18-mechanic-route-card-index.md) | add a generated route-card index for memo mechanic packages |
| [2026-05-18-mechanic-owner-route-matrix](2026-05-18-mechanic-owner-route-matrix.md) | add a generated owner-route matrix without claiming owner acceptance |
| [2026-05-18-mechanic-landing-log-index](2026-05-18-mechanic-landing-log-index.md) | add a generated landing receipt index for memo mechanic packages |
| [2026-05-18-writeback-curated-object-examples](2026-05-18-writeback-curated-object-examples.md) | move writeback-owned curated memory-object examples under the writeback mechanic |
| [2026-05-18-questbook-generated-views-part](2026-05-18-questbook-generated-views-part.md) | add a part-level contract for root-published Questbook generated read models |
| [2026-05-18-downstream-feed-test-localization](2026-05-18-downstream-feed-test-localization.md) | move consumer-handoff and writeback test artifacts out of root while keeping the cross-mechanic seed regression rooted |
| [2026-05-18-retention-local-regression-boundary](2026-05-18-retention-local-regression-boundary.md) | add a package-local regression boundary for retention docs, schemas, examples, and stop-lines |

## Review Rule

Before adding a decision, ask whether the note explains a real choice. If the
answer is only "this file changed", the changelog or PR summary is enough.
