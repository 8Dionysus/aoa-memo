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

For quick inspection, `generated/root-topology/root_technical_districts.min.json` is the
compact atlas of district roles, route cards, family ids, and local routing.
The exact file allowlist stays in `config/root-topology/root_technical_districts.json`.

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

Root `config/` files use `config_families` for the same reason. Each allowed
root config file must belong to exactly one source-map family that names its
role, owner surface, source refs, and validators. Root config stays limited to
repo-wide source maps and technical control-plane contracts.

Root `manifests/` is reserved by `manifest_policy` until a shared recurrence
manifest exists. The policy must match the current root `manifests.allowed_files`
list, which is empty now. Mechanic-local manifests belong under the owning
mechanic.

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
  README.md
  CONTRACT.md
  VALIDATION.md
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
Every active row in `mechanics/<slug>/PARTS.md` must now have a physical
`parts/<part>/` node with a contract and validation surface before deeper
part-local artifacts are added.

## Current Placement Rule

Root technical districts now keep only shared, repo-wide, or cross-mechanic
surfaces.

`config/root-topology/root_technical_districts.json` is the exact current allowlist for root
technical artifacts. If a file is not a route card and is not listed there, it
must either be added with a repo-wide/shared reason or moved under its owning
mechanic.

`generated/root-topology/root_technical_districts.min.json` is rebuilt from that config so
agents can inspect the root district topology before opening the full contract.

Root `schemas/` entries in that config must also be grouped by
`schema_families`. This keeps the public schema canon distinct from package-local
mechanic contracts while preserving the root home for shared memory-object,
recall/posture, support-object, and generated-surface contracts.

Root `examples/` entries must be grouped by `example_families` as well. This
keeps public shared examples distinct from mechanic-local examples and makes
their validator coverage explicit.

Root `config/` entries must be grouped by `config_families`; root `manifests/`
must match `manifest_policy`. This closes the root technical control plane
without promoting config or manifests into memory truth.

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
route card. When a functioning part exists, use the nearest part-local home.
This includes mechanic-local schemas, examples, config inputs, generated
companions, scripts, tests, manifests, and hook manifests.

Examples:

- Agon prebinding, bridge/evidence, and stage recurrence config, schemas,
  examples, generated registries, manifests, hooks, validators, builders, and
  tests live under the nearest `mechanics/agon/parts/<part>/` home.
- Titan recall/remembrance, closeout/digest, and audit-personality-and-swarm-policy schemas,
  examples, and tests live under the nearest `mechanics/titan/parts/<part>/`
  home.
- adoption boundary, adoption revision/retention, adoption scar/routing,
  retention cross-repo/governance, retention office-marker, and retention
  post-release schemas, examples, and tests live under their nearest
  `mechanics/<slug>/parts/<part>/` homes.
- governance authority-boundary, federation, installation/certification, and
  precedent/stay-order schemas/examples/tests live under their nearest
  `mechanics/governance/parts/<part>/` homes.
- antifragility failure-lesson and recovery-pattern schemas/examples/tests
  live under their nearest `mechanics/antifragility/parts/<part>/` homes.
- operational-gate deployment, office incident, service revision, and
  post-release schemas/examples/tests live under their nearest
  `mechanics/operational-gate/parts/<part>/` homes.
- readiness-boundary contract schemas/examples/tests live under
  `mechanics/readiness-boundary/parts/memory-readiness-boundary/`.
- recurrence-support witness trace schemas/examples/tests live under
  `mechanics/recurrence-support/parts/witness-trace-contract/`.
- lineage-harvest pattern-lineage schemas/examples/tests live under
  `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/`.
- shape-guard via negativa tests live under
  `mechanics/shape-guard/parts/via-negativa-checklist/`.
- Questbook source validation lives under
  `mechanics/questbook/parts/source-contract/`, while the read-model projection
  builder lives under `mechanics/questbook/parts/quest-read-model-projections/`.
- writeback generated companions such as `runtime_writeback_targets`,
  `runtime_writeback_intake`, `runtime_writeback_governance`,
  `growth_refinery_writeback_lanes`, and `phase_alpha_writeback_map` live under
  their nearest `mechanics/writeback/parts/<part>/generated/` home, with
  runtime targets/intake/governance under `runtime-and-temperature` and growth
  or Phase Alpha surfaces under `growth-and-continuity`.
- the KAG source export lives under
  `mechanics/consumer-handoff/parts/kag-source-export/generated/`.
- root quest generated companions live under `generated/` only because they
  project the public Questbook store for outside consumers. Their
  `owner_surface` and `anchor_ref` values must still route into real memo docs
  or mechanic docs, and their placement contract lives under
  `mechanics/questbook/parts/quest-read-model-projections/`.

Root `schemas/`, `examples/`, `generated/`, `scripts/`, `tests/`, and `config/`
remain valid for shared memory-object canon, shared recall contracts,
repo-wide validators, release gates, and cross-mechanic regression tests.
Root `manifests/` is reserved for future shared recurrence manifests; the
current active manifests are package-local.

`generated/mechanics/mechanic_artifacts.min.json` is the compact generated inventory of
package-local and part-local mechanic artifacts. It is not source truth. It lets
agents and validators inspect which mechanic or functioning part currently owns
each local schema, example, config input, generated companion, script, test, or
manifest without forcing `PARTS.md` files to become raw file inventories.

`generated/mechanics/memo_mechanic_readiness.min.json` is the compact generated readiness
matrix for current mechanic packages. It joins package cards, source maps,
owner maps, validation routes, stop-lines, and the artifact inventory so agents
can detect when a mechanic is structurally present but not ready for OS Abyss
use.
Readiness also checks local artifact test coverage: a mechanic with local
config, examples, generated companions, manifests, schemas, or scripts must
have at least one package-local or part-local test before it can be considered
ready.
Test-only mechanics remain valid when their operation is a validator or
shape-guard surface.
When package-local or part-local tests exist, the mechanic's validation route
must name the local pytest command or test directory so a future agent can run
the package check without reverse-engineering the inventory.

`generated/mechanics/memo_mechanic_owner_routes.min.json` is the compact generated
matrix of package-local owner maps and route cards. It exists because
stronger-owner routing is cross-mechanic and OS Abyss needs one inspection
surface. It is not an owner request queue, owner acceptance, proof, runtime
authority, route dispatch, role authority, KAG truth, playbook choreography,
stats truth, or source doctrine.

`generated/mechanics/memo_mechanic_landing_logs.min.json` is the compact generated
landing receipt index for package-local `LANDING_LOG.md` files. It exists
because OS Abyss needs one inspection surface for what was landed, where
executable validation is owned, and which stop-lines were preserved. It is not
proof, owner acceptance, runtime authority, release authority, route dispatch,
role authority, KAG truth, playbook choreography, stats truth, or source
doctrine.

Questbook is the intentional root-store exception: `mechanics/questbook/` owns
quest lifecycle, source contracts, validation, and generated projections, while
root `QUESTBOOK.md` stays the compact index and root `quests/` stays the public
lane-first item store. The quest-read-model-projections part explains why Questbook read
models stay root-published instead of moving into package-local `generated/`.

Do not leave active root aliases for moved mechanic artifacts.

## Move Rule

Before moving a root technical artifact into a mechanic:

1. identify the mechanic and stronger owner split
2. confirm the artifact is not a repo-wide public contract
3. add or update the nearest package or part `AGENTS.md`
4. update callers, docs, tests, builders, and generated companions
5. remove root aliases rather than preserving duplicate active paths
6. update `config/mechanics/memo_mechanics.json` or another source map only when it owns
   the changed index
7. run the narrow mechanic validators before the broad release gate

## Legacy Rule

Legacy preserves placement history and provenance. It is not an artifact
parking lot.

Do not put active schemas, examples, generated outputs, scripts, or tests under
`legacy/` unless they are intentionally preserved as old evidence and are
indexed as legacy.

## Validation

Executable validation commands for artifact placement changes live in
[mechanics/AGENTS](AGENTS.md#validation).
