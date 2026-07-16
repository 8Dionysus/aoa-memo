# aoa-memo Owner Skill Bundle

- Decision ID: AOA-MEM-D-0076

## Status

Accepted on 2026-07-16.

## Index Metadata

- Original date: 2026-07-16
- Surface classes: skills/home, agents/mesh, root/topology, boundary/runtime/sibling
- Mechanic parents: none
- Guard families: skill admission, source/projection parity, memory surface, AGENTS/mesh
- Memory object classes: none
- Posture: accepted owner skill

## Context

The repository exposed 25 copied shared bundles under `.agents/skills` but had
no canonical home for its own callable procedure. Those copies competed with
the shared user profile, included obsolete aliases, and made a generated
foreign catalog look like an `aoa-memo` source surface. A root regression test
also imported a helper from one of those copied projections, turning that
accident into a release dependency.

Manual work exercised route-only candidate review, a lifecycle withdrawal
case, generic JSON analytics, coexistence with decision lookup, raw session
evidence retrieval, and an authorized source-first evolution in a disposable
worktree. It compared the existing copied catalog, no owner skill, and the
candidate; used held-out positive and strongest negative requests; and checked
that generated read models changed only after their authored source. The work
also exposed and corrected an over-broad verification step before admission.

The trials established useful owner-specific routing, a stable result ABI,
negative applicability, coexistence, and bounded mutation posture. They did not
establish a general token, latency, cross-model, or cross-host improvement.

## Decision

Admit one repository-owned `aoa-memo` bundle with internal `recall`, `review`,
and `evolve` modes. Its canonical source lives at
`skills/aoa-memo/SKILL.md`; `skills/port.manifest.json` declares version and
admission. The exact repo-scoped Codex copy is generated at
`.agents/skills/aoa-memo` through the common `aoa-skills` home-port contract.

Remove the 25 undeclared shared copies from the repository projection. Do not
split the three modes into separate prompt-visible bundles unless later
held-out trials establish independent triggers, ABIs, composition value, and
outcome benefit.

Remove the root test that imported a helper from the copied
`aoa-safe-infra-change` projection. Infrastructure change behavior belongs to
its stronger owner and shared workflow family, not to `aoa-memo`; retaining the
test would make a generated foreign projection a hidden source.

## Alternatives

Keeping the copied shared catalog would avoid a projection migration, but
would preserve routing interference, obsolete names, and false local
ownership.

Advertising separate recall, review, and evolve skills would make the modes
more visible, but would multiply semantically adjacent candidates before any
independent benefit has been demonstrated.

Keeping no owner skill would avoid prompt cost, but manual comparisons showed
repeated value from the memory-specific authority ceiling, disposition ABI,
source-first DAG, negative applicability, and explicit stop lines.

## Consequences

- Codex sees one memo-specific repository skill instead of 25 copied shared
  names.
- Recall and review remain read-only; source mutation requires explicit
  `evolve` authority and owner-first verification.
- Raw `.aoa` retrieval, generic analytics, proof verdicts, routing, role
  rights, workflow execution, KAG substrate, runtime storage, and already-named
  validator execution remain negative cases.
- Structural validation can prove owner and byte parity but cannot prove
  routing quality, cross-model transfer, safety, or outcome improvement.
- A material model, workflow, or bundle change requires new isolated,
  negative, held-out, coexistence, and bounded-write work before lifecycle
  expansion.
- Raw trials and task-local DAGs remain session evidence rather than durable
  repository truth.

## Affected Surfaces

- `AGENTS.md`
- `DESIGN.md`
- `DESIGN.AGENTS.md`
- `docs/root/ROOT_SURFACE_LAW.md`
- `skills/AGENTS.md`
- `skills/README.md`
- `skills/aoa-memo/SKILL.md`
- `skills/port.manifest.json`
- `.agents/AGENTS.md`
- `.agents/skills/aoa-memo/SKILL.md`
- `config/agents/agents_mesh.json`
- `config/root-topology/root_technical_districts.json`
- `aoa-skills:docs/decisions/AOA-SK-D-0040-owner-skill-homes-and-projection-boundaries.md`
- `aoa-skills:docs/decisions/AOA-SK-D-0041-minimal-owner-home-port-contract.md`

## Verification

Decision and topology indexes, portable skill validation, the pinned common
home-port action, prompt-visible fresh-session inspection, repo-local KAG
parity, and the root release gate protect the durable shape. Manual trials
remain the semantic admission evidence; green checks do not replace them.
