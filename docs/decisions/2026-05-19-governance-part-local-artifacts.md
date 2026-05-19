# Governance Part-Local Artifacts

## Context

Governance already had functioning parts for governance boundaries,
federation boundaries, install/certification boundaries, and
precedent/stay-order memory.

Its active schemas, examples, and local regressions still lived at the package
level. That made governance `parts/` descriptive while the actual authority
contracts sat one layer above the operation that owned them.

## Decision

Move governance technical artifacts to the nearest functioning part:

- governance decision and writeback contracts plus local regressions under
  `parts/governance-boundary/`
- federation gate and forgetting contracts under `parts/federation-boundary/`
- installation and certification contracts under
  `parts/install-and-certification-boundary/`
- policy precedent contracts under `parts/precedent-and-stay-order/`

Keep governance docs as the authored authority-boundary doctrine and keep
cross-mechanic seed regressions in their existing owner lanes while pointing
them at the new part-local contracts.

## Alternatives

Leaving artifacts under package-level `schemas/`, `examples/`, and `tests/`
would preserve shorter paths but leave the functional parts without their own
contracts.

Moving all artifacts into one generic governance artifact directory would
reduce package sprawl but would blur the difference between council/governance
memory, federation memory gates, install/certification facts, and policy
precedent recall.

## Consequences

Governance parts are now executable owner nodes for their authority-boundary
contracts. Cross-mechanic tests still validate Wave 2, Wave 3, Wave 4, and Wave
5 seed surfaces, but those tests no longer require governance package-level
artifact homes.

The move keeps `aoa-memo` below stronger owners. It does not grant council
authority, release approval, proof verdicts, Tree-of-Sophia writes, route
dispatch, role authority, source-owner consent, or runtime governance.

## Affected Surfaces

- `mechanics/governance/PARTS.md`
- `mechanics/governance/PROVENANCE.md`
- `mechanics/governance/parts/*`
- `mechanics/governance/AGENTS.md`
- `config/root_technical_districts.json`
- `mechanics/lineage-harvest/PARTS.md`
- `tests/test_experience_wave3_seed_contracts.py`
- `mechanics/operational-gate/tests/test_experience_wave5_seed_contracts.py`
- `generated/mechanic_artifacts.min.json`
- `generated/memo_mechanic_readiness.min.json`

## Verification Route

Expected verification:

- `python -m pytest -q mechanics/governance/parts/governance-boundary/tests tests/test_experience_wave2_seed_contracts.py tests/test_experience_wave3_seed_contracts.py mechanics/operational-gate/tests/test_experience_wave5_seed_contracts.py mechanics/lineage-harvest/tests/test_lineage_harvest_mechanic.py`
- `python scripts/build_mechanic_artifact_inventory.py --check`
- `python scripts/validate_mechanic_artifact_inventory.py`
- `python scripts/build_memo_mechanic_readiness.py --check`
- `python scripts/validate_memo_mechanic_readiness.py`
- `python scripts/release_check.py`
