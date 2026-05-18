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
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```
