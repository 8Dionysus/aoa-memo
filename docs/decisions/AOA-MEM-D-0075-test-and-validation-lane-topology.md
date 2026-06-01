# Test And Validation Lane Topology

- Decision ID: AOA-MEM-D-0075

## Status

Accepted on 2026-06-01.

## Index Metadata

- Original date: 2026-06-01
- Surface classes: root/topology, validation guard, agents/mesh, release/tooling
- Mechanic parents: none
- Guard families: root technical district, docs route, generated/read-model, AGENTS/mesh, release/tooling
- Memory object classes: decision
- Posture: accepted validation topology

## Context

The release gate in `aoa-memo` had a long command list embedded directly in
`scripts/release/release_check.py`. Tests were already split across `tests/`,
mechanic-local part tests, and the Spark lane, but there was no single map that
named what each test family protected or which validation lane owned the
command sequence.

That made the validator surface harder to evolve: release orchestration,
focused CI commands, docs, and tests could drift independently even when they
were describing the same gate.

The deeper pressure is that agentic OS validators should protect boundaries,
not become historical script sediment. `aoa-memo` must distinguish source
topology, generated projection parity, capability/export boundaries, runtime
policy declarations, trace/eval routing, memory context authority, inter-agent
handoffs, auditability, adversarial memory posture, and release/nightly
composition.

## Decision

Make `docs/validation/VALIDATOR_TOPOLOGY.md` the source-authored validator
topology owner and `config/validation_lanes.json` the source-authored command
authority for validation lanes.

Follow-up hardening adds `docs/validation/COMMAND_AUTHORITY.md` and
`docs/validation/validator_inventory.json`, matching the sibling `aoa-skills`
lesson that command storage, human topology, validator inventory, and test
inventory are separate surfaces. The lane manifest owns executable sequences;
the validator inventory owns validation-like entrypoint coverage and prevents
manual or compatibility validators from becoming unlabeled historical gates.

Each command step now carries effective metadata:

- validator layer
- mode (`blocking`, `blocking-in-release`, `boundary-only`, or `advisory`)
- owner surface
- failure route

The required validator layers are:

- Source/Topology Validators
- Projection/Generated Validators
- Capability/Permission Validators
- Runtime Policy Validators
- Trace/Eval Validators
- Memory/RAG/Context Validators
- Inter-Agent/Handoff Validators
- Observability/Audit Validators
- Security/Adversarial Validators
- Release/Nightly/Post-Merge Validators

Keep Python entrypoints as orchestration only:

- `scripts/validation_lanes.py` loads and validates the lane manifest.
- `scripts/ci_gate.py` runs named focused lanes from the manifest.
- `scripts/release/release_check.py` preserves the broad release gate by
  executing the manifest-composed `release_check` sequence.
- `scripts/root-topology/validate_validator_topology.py` validates that the
  topology, lane manifest, source-fast boundary, generated lane, audit
  promotion, and release/nightly split stay aligned.
- `scripts/memory/validate_memo.py` remains a compatibility entrypoint, but
  release lanes call focused profiles instead of the unprofiled broad gate:
  `schema`, `memory-context`, `runtime-boundary`, `handoff-boundary`, and
  `eval-boundary`.
- The focused profile implementations live under `scripts/memory/validators/`.
  `scripts/memory/validate_memo.py` must stay a thin CLI/facade and must not
  regain schema, runtime, handoff, eval, or memory-context implementation
  ownership.

Add `docs/validation/` as the current docs district for validator topology:

- `docs/validation/VALIDATOR_TOPOLOGY.md`
- `docs/validation/COMMAND_AUTHORITY.md`
- `docs/validation/validator_inventory.json`
- `docs/validation/AGENTS.md`

Keep `docs/testing/` as the current docs district for human test topology and
machine inventory:

- `docs/testing/TEST_TOPOLOGY.md`
- `docs/testing/test_inventory.json`
- `docs/testing/AGENTS.md`

The testing topology also names the agentic test layers that `aoa-memo` can
legitimately own: contract core, tool boundary, deterministic scenario replay,
state/memory/session checks, fault/safety fixtures, and generated-surface
parity. Full multi-turn trace grading, online canaries, and cost/token/latency
telemetry stay routed to stronger eval/runtime owners.

## Alternatives

Keeping the command list only in `release_check.py` would preserve the old
entrypoint, but focused lanes and test topology would still need to duplicate
or infer release behavior.

Moving command authority into GitHub workflow YAML would make CI explicit, but
it would turn platform automation into source doctrine and hide local
validation composition from agents.

Using only `AGENTS.md` prose for validation lanes would be readable, but not
machine-checkable enough for release-gate regressions.

## Consequences

The broad release gate remains available through the compatibility entrypoints,
but command composition is now inspectable and testable as data.

Future test additions must update the testing inventory and root technical
district contracts. Future validation-lane changes must update validator
topology, command authority, validator inventory, the lane manifest, and focused
regression tests instead of editing hidden command lists.

`docs/validation/` becomes an allowed docs district because validator meaning
needs an explicit source owner. `docs/testing/` remains allowed because it owns
test-family topology, not memory doctrine or a mechanic-owned doc package.

`source-fast` is now constrained to Source/Topology Validators. Generated
parity checks move to the `generated` lane. Runtime, capability, security, and
full trace/eval checks are explicitly boundary-only or routed to stronger
owners unless a local owner surface promotes a command into release.

The old memory-validator monolith is no longer a release command. Its checks
are still available through the compatibility `all` profile, but release uses
profiled commands so each lane fails against the owner layer it is actually
testing.

The memory-validator implementation is now physically split by boundary layer:
shared schema/ref helpers, schema checks, memory-context checks, Questbook
projection checks, runtime writeback checks, live receipt checks, handoff
checks, and eval guardrail checks. Validator topology tests enforce the thin
entrypoint and per-module size budget so future growth lands in the owner
module rather than recreating a monolith.

The memory-validator regression tests are likewise split by boundary:
`test_memo_schema_contracts.py`, `test_memo_memory_context_boundaries.py`,
`test_memo_runtime_writeback_boundaries.py`,
`test_memo_live_receipt_boundaries.py`, `test_memo_questbook_boundaries.py`,
`test_memo_handoff_boundaries.py`, `test_memo_eval_guardrails.py`, and
`test_memo_generated_surface_contracts.py`. `docs/testing/test_inventory.json`
and `tests/root-topology/test_test_topology.py` keep that split explicit so
tests do not become a second hidden architecture.

Historical test files preserved under `mechanics/*/legacy/raw/tests/` are
provenance snapshots, not current hard gates. The test inventory must keep them
separate from active `parts/*/tests/` replacements and mark them advisory so a
raw snapshot cannot silently re-enter release as a blocking test. Active test
files also carry a 300-line compactness guard to prevent the split suites from
regrowing into bulky hidden architecture.

The mechanic artifact topology validator is also split after follow-up review:
`validate_mechanic_artifact_topology.py` remains the CLI and district
allowlist orchestrator, `mechanic_artifact_topology_common.py` owns shared root
topology constants/helpers, and `mechanic_artifact_family_contracts.py` owns
the repeated generated/script/test/schema/example/config family-contract
checks. `tests/root-topology/test_mechanic_artifact_topology.py` keeps the
entrypoint thin so future family additions do not recreate another bulky
validator.

The validator-topology gate follows the same rule: `validate_validator_topology.py`
keeps the checks and CLI, while `validator_topology_common.py` owns shared
constants, path refs, inventory discovery, and helper routines.

Active route cards no longer carry broad repeated validation command blocks as
their default proof. They name lane ids and focused owner checks; the full
sequences remain in `config/validation_lanes.json`.

## Affected Surfaces

- `docs/validation/`
- `docs/testing/`
- `config/validation_lanes.json`
- `scripts/validation_lanes.py`
- `scripts/ci_gate.py`
- `scripts/release/release_check.py`
- `scripts/root-topology/validate_validator_topology.py`
- `scripts/root-topology/validator_topology_common.py`
- `scripts/root-topology/validate_docs_districts.py`
- `scripts/mechanics/mechanic_artifact_family_contracts.py`
- `scripts/mechanics/mechanic_artifact_topology_common.py`
- `scripts/mechanics/validate_mechanic_artifact_topology.py`
- `config/root-topology/root_technical_districts.json`
- `config/agents/agents_mesh.json`
- `scripts/memory/validators/`
- `tests/root-topology/test_validation_lanes.py`
- `tests/root-topology/test_ci_gate.py`
- `tests/root-topology/test_release_check.py`
- `tests/root-topology/test_test_topology.py`
- `tests/root-topology/test_validator_topology.py`

## Verification

Use:

```bash
python scripts/root-topology/validate_validator_topology.py
python -m pytest -q tests/root-topology/test_validation_lanes.py tests/root-topology/test_validator_topology.py tests/root-topology/test_ci_gate.py tests/root-topology/test_release_check.py tests/root-topology/test_test_topology.py
python scripts/root-topology/build_decision_indexes.py --check
python scripts/agents/build_agents_mesh_index.py --check
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/release/release_check.py
```
