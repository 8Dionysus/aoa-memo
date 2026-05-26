# Adoption And Retention Part-Local Artifacts

- Decision ID: AOA-MEM-D-0043

## Status

Accepted on 2026-05-19.

## Index Metadata

- Original date: 2026-05-19
- Surface classes: lifecycle/retention, mechanic package, mechanic part
- Mechanic parents: adoption, retention
- Guard families: mechanic topology, part and payload, lifecycle/retention
- Memory object classes: none
- Posture: active rationale

## Context

Adoption and retention already had functioning `parts/` nodes, but their
schemas, examples, and local tests still lived at the package level. That made
the parts visually present but weaker than the mechanic contract they were
supposed to own.

The previous readiness checks could prove that the package had at least one
local test, but they did not make it obvious which part owned each contract.
Retention also still named a governance test in its package validation route,
mixing neighboring mechanic coverage into the local retention route.

## Decision

Move adoption and retention technical artifacts to the nearest functioning
part:

- adoption boundary artifacts under `mechanics/adoption/parts/adoption-boundary/`
- adoption revision/retention artifacts under
  `mechanics/adoption/parts/revision-and-retention-pressure/`
- adoption scar/routing artifacts under
  `mechanics/adoption/parts/scar-and-routing-adoption/`
- retention cross-repo/governance artifacts under
  `mechanics/retention/parts/cross-repo-and-governance-retention/`
- retention office marker artifacts under
  `mechanics/retention/parts/office-markers/`
- retention post-release artifacts under
  `mechanics/retention/parts/post-release-retention/`

Keep cross-mechanic candidate-contract regression coverage at root, but point it at the new
part-local homes. Keep governance tests in governance; retention names only its
own part-local test route.

## Consequences

- Adoption and retention parts now carry the schemas, examples, and tests that
  make their contracts executable.
- Generated mechanic artifact inventory and readiness surfaces can show these
  contracts as part-owned instead of package-owned.
- Root technical district config still protects cross-mechanic contract refs,
  but the protected refs now route through part-local homes.
- `aoa-memo` still does not claim adoption proof, retention execution,
  runtime storage, route dispatch, role authority, KAG truth, source-owner
  acceptance, or stronger policy authority.

## Verification

Expected verification:

- `python -m pytest -q mechanics/adoption/parts/adoption-boundary/tests mechanics/adoption/parts/revision-and-retention-pressure/tests mechanics/adoption/parts/scar-and-routing-adoption/tests`
- `python -m pytest -q mechanics/retention/parts/cross-repo-and-governance-retention/tests mechanics/retention/parts/office-markers/tests mechanics/retention/parts/post-release-retention/tests`
- `python -m pytest -q tests/test_cross_mechanic_candidate_contracts.py`
- `python scripts/validate_mechanic_artifact_topology.py`
- `python scripts/build_mechanic_artifact_inventory.py --check`
- `python scripts/validate_mechanic_artifact_inventory.py`
- `python scripts/build_memo_mechanic_readiness.py --check`
- `python scripts/validate_memo_mechanic_readiness.py`
- `python scripts/release_check.py`
