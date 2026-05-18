# Memo Mechanic Artifact Topology

## Purpose

Memo mechanics are not documentation archives only.

This surface explains where mechanic-adjacent schemas, examples, config,
generated companions, scripts, tests, manifests, and questbook surfaces should
live as the mechanics tree matures.

It owns placement law only. It does not replace package cards, source docs,
schema contracts, generated indexes, or release validation.

## Root Technical Districts

Root technical districts remain valid when an artifact is repo-wide, public
contract-shaped, or shared across multiple memory families:

| District | Root-owned when |
|---|---|
| `schemas/` | the contract is part of the public memory-object or support-object canon |
| `examples/` | the example teaches public-safe object shape across more than one mechanic |
| `config/` | the input config drives repo-wide builders or validators |
| `generated/` | the output is a compact public companion consumed outside one package |
| `scripts/` | the builder or validator is part of the release gate or shared contract lane |
| `tests/` | the regression protects repo-wide behavior or cross-district references |
| `manifests/` | the recurrence manifest is shared across mechanics rather than package-local |
| `quests/` | the obligation belongs in the public Questbook item store and should survive the current diff |

Root technical districts must not keep convenience aliases for mechanic-owned
source docs. Route to `mechanics/<slug>/docs/` directly.

Root `schemas/` files have a positive ownership rule through
`schema_families`. Each allowed root schema must belong to exactly one family
that names its role, owner surface, source refs, and validators. Root schemas
remain only when they define public memory-object canon, recall/posture
contracts, shared support-object contracts, or generated-surface contracts;
single-mechanic schemas belong under the owning mechanic.

Root `examples/` files use the same positive ownership rule through
`example_families`. Each allowed root example must belong to exactly one family
that names its role, owner surface, source refs, and validators. Root examples
remain only when they teach shared public memory-object shape, lifecycle/audit
posture, recall contracts, support contracts, generated-surface manifests, or
cross-family continuity examples; single-mechanic examples belong under the
owning mechanic.

## Mechanic Artifact Lane

Use a mechanic-local artifact home when the artifact only makes sense inside
one mechanic's owner boundary:

```text
mechanics/<slug>/
  config/
  generated/
  manifests/
  schemas/
  examples/
  scripts/
  tests/
```

If a mechanic later grows functioning parts, use the nearest part-local home
instead:

```text
mechanics/<slug>/parts/<part>/
  config/
  generated/
  manifests/
  schemas/
  examples/
  scripts/
  tests/
```

Package-local artifact homes must still follow the same stop-lines as the
mechanic card. A package-local artifact does not become proof, routing logic,
runtime storage, role authority, KAG substrate truth, or owner acceptance.

## Current Placement Rule

Root technical districts now keep only shared, repo-wide, or cross-mechanic
surfaces.

`config/root_technical_districts.json` is the exact current allowlist for root
technical artifacts. If a file is not a route card and is not listed there, it
must either be added with a repo-wide/shared reason or moved under its owning
mechanic.

Root `schemas/` entries in that config must also be grouped by
`schema_families`. This keeps the public schema canon distinct from package-local
mechanic contracts while preserving the root home for shared memory-object,
recall/posture, support-object, and generated-surface contracts.

Root `examples/` entries must be grouped by `example_families` as well. This
keeps public shared examples distinct from mechanic-local examples and makes
their validator coverage explicit.

Root `generated/` has an additional family contract in that same config. Each
allowed root generated output must belong to exactly one `generated_families`
entry that names its owner surface, source refs, validators, and builders when
the output is generator-backed or a projection. This keeps root generated files
from becoming an unowned parking lot while preserving public compact companions
that are intentionally consumed outside one mechanic package.

Root `scripts/` has the same positive ownership rule through `script_families`.
Each allowed root script must belong to exactly one family that names its role,
owner surface, and coverage refs. Package-local mechanic scripts still belong
under the owning mechanic; root scripts remain only when they operate as shared
release gates, repo-wide validators, builders, or imported helpers.

Root `tests/` has a parallel positive ownership rule through `test_families`.
Each allowed root test file or public fixture must belong to exactly one family
that names its role, owner surface, and protected refs. Root tests remain only
when they protect repo-wide behavior, cross-district references, shared memory
contracts, route-card surfaces, or cross-mechanic regressions; package-local
mechanic tests belong under the owning mechanic.

Single-mechanic artifacts live in the owning package with their local docs and
route card. This includes mechanic-local schemas, examples, config seeds,
generated companions, scripts, tests, manifests, and hook manifests.

Examples:

- Agon config, schemas, examples, generated registries, manifests, hooks,
  validators, builders, and tests live under `mechanics/agon/`.
- Titan schemas, examples, and tests live under `mechanics/titan/`.
- adoption, governance, retention, operational-gate, antifragility,
  checkpoint, readiness-boundary, recurrence-support, lineage-harvest,
  shape-guard, consumer-handoff, and writeback schemas/examples/tests live
  under their package lanes when they serve that one mechanic.
- writeback generated companions such as `runtime_writeback_targets`,
  `runtime_writeback_intake`, `runtime_writeback_governance`,
  `growth_refinery_writeback_lanes`, and `phase_alpha_writeback_map` live under
  `mechanics/writeback/generated/`.
- the KAG source export lives under `mechanics/consumer-handoff/generated/`.
- root quest generated companions live under `generated/` only because they
  project the public Questbook store for outside consumers. Their
  `owner_surface` and `anchor_ref` values must still route into real memo docs
  or mechanic docs.

Root `schemas/`, `examples/`, `generated/`, `scripts/`, `tests/`, and `config/`
remain valid for shared memory-object canon, shared recall contracts,
repo-wide validators, release gates, and cross-mechanic regression tests.
Root `manifests/` is reserved for future shared recurrence manifests; the
current active manifests are package-local.

`generated/mechanic_artifacts.min.json` is the compact generated inventory of
package-local mechanic artifacts. It is not source truth. It lets agents and
validators inspect which mechanic currently owns each local schema, example,
config seed, generated companion, script, test, or manifest without forcing
`PARTS.md` files to become raw file inventories.

Questbook is the intentional root-store exception: `mechanics/questbook/` owns
quest lifecycle, source contracts, validation, and generated projections, while
root `QUESTBOOK.md` stays the compact index and root `quests/` stays the public
lane-first item store.

Do not leave active root aliases for moved mechanic artifacts.

## Move Rule

Before moving a root technical artifact into a mechanic:

1. identify the mechanic and stronger owner split
2. confirm the artifact is not a repo-wide public contract
3. add or update the nearest package or part `AGENTS.md`
4. update callers, docs, tests, builders, and generated companions
5. remove root aliases rather than preserving duplicate active paths
6. update `config/memo_mechanics.json` or another source map only when it owns
   the changed index
7. run the narrow mechanic validators before the broad release gate

## Legacy Rule

Legacy preserves placement history and provenance. It is not an artifact
parking lot.

Do not put active schemas, examples, generated outputs, scripts, or tests under
`legacy/` unless they are intentionally preserved as old evidence and are
indexed as legacy.

## Validation

Executable validation commands live in [mechanics/AGENTS](AGENTS.md#validation).

For release-bound artifact placement changes, run:

```bash
python scripts/validate_mechanic_artifact_topology.py
python scripts/build_mechanic_artifact_inventory.py --check
python scripts/validate_mechanic_artifact_inventory.py
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```
