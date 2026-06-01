# Test Topology

This map keeps the `aoa-memo` test surface readable as a memory-layer contract
harness. Tests should answer: what surface is protected, which source owns the
truth, which validation lane runs the check, whether the result blocks ordinary
work, and where a failure routes next.

The machine inventory is [test_inventory.json](test_inventory.json). Update it
when adding, deleting, renaming, splitting, folding, or changing the lane of a
test file.

## Baseline

The pre-refactor green baseline was captured on 2026-05-31 from a clean
`main...origin/main` worktree:

- `python -m pytest -q tests`: `184 passed`, `196 subtests passed` in `11.06s`.
- `python scripts/release_check.py`: release-gate final pytest reported
  `367 passed`, `815 subtests passed` in `19.89s`.

The refactor preserves the broad release gate by moving command authority into
`config/validation_lanes.json`; Python entrypoints now load and execute that
manifest instead of keeping separate command lists. Validator meaning lives in
`docs/validation/VALIDATOR_TOPOLOGY.md`.

## Operating Shape

Use the compact route shape: family -> protects -> owner source -> lane ->
focused target -> failure route.

Test files are not command authority. Blocking lane sequences live in
[`../../config/validation_lanes.json`](../../config/validation_lanes.json).
Validator layer meaning lives in
[`../validation/VALIDATOR_TOPOLOGY.md`](../validation/VALIDATOR_TOPOLOGY.md).
`scripts/validation_lanes.py` is only the loader/API. `scripts/ci_gate.py` and
`scripts/release/release_check.py` are orchestrators.
`scripts/memory/validate_memo.py` is likewise only a compatibility CLI; tests
must keep the implementation in `scripts/memory/validators/` layer modules.

## Families

| Family | Protects | Owner Source | Lane | Failure Route |
|---|---|---|---|---|
| `memory/*` | memory object contracts, reviewed corpus, local memo ports, operation modes, provenance, and generated memory parity | `docs/memory/`, `docs/posture/`, `memo/`, schemas, examples, generated companions | `memory` | Fix authored memory source, schema/example, builder, or corpus before changing generated output. |
| `mechanics/*` | mechanic package contracts, part-local artifacts, owner maps, readiness, landing logs, and cross-mechanic boundaries | nearest `mechanics/<slug>/` source surface | `mechanics` | Fix the mechanic-local owner surface before widening repo-wide tests. |
| `agents/*` | AGENTS mesh, semantic route cards, and agent companion skill scripts | `DESIGN.AGENTS.md`, `.agents/`, `config/agents/agents_mesh.json` | `topology` / `agents` | Fix route-card source or mesh config before changing generated readouts. |
| `root/*` | root placement law, docs districts, roadmap parity, root technical atlas, and topology spine | `docs/root/ROOT_SURFACE_LAW.md`, `config/root-topology/root_technical_districts.json`, `ROADMAP.md` | `topology` | Fix root topology source, builder, or generated atlas before widening release validation. |
| `validation/test-topology` | validator topology, validation lane manifest, release gate composition, CI lane selection, and test inventory coverage | `docs/validation/VALIDATOR_TOPOLOGY.md`, `docs/testing/TEST_TOPOLOGY.md`, `config/validation_lanes.json` | `topology` | Fix validator topology, lane manifest, loader, or inventory before changing workflow YAML. |
| `agent-lane/spark` | Spark lane registry, scenarios, templates, stop-lines, and lane validator | `.agents/spark/AGENTS.md` | `agents` | Fix the Spark lane source, registry, scenario files, or validator before release. |

## Lane Rules

- `source-fast`, `generated`, `memory`, `handoff`, `eval`, `audit`, `runtime`,
  `export/runtime`, `security`, and compatibility lanes must stay deterministic
  and repo-local.
- `release` is the full local gate and may compose narrower lanes, but it must
  not become a second source of command truth.
- Tests may assert that lane composition is correct, but broad validators
  should live in `config/validation_lanes.json` with layer meaning in
  `docs/validation/VALIDATOR_TOPOLOGY.md`.
- Mechanic-local tests belong under `mechanics/<slug>/parts/<part>/tests/`
  when they protect one repeatable operation.
- Advisory or live checks must be visibly named before they can enter a
  default lane. Memory remains weaker than proof, routing, runtime state, role
  authority, KAG truth, playbook choreography, and source-authored knowledge.
