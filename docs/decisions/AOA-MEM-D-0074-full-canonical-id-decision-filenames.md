# Full Canonical ID Decision Filenames

- Decision ID: AOA-MEM-D-0074

## Status

Accepted on 2026-05-26.

## Index Metadata

- Original date: 2026-05-26
- Surface classes: root/topology, generated/readout, validation guard, agents/mesh
- Mechanic parents: none
- Guard families: decision index/read-model, docs route, generated/read-model, AGENTS/mesh, release/tooling
- Memory object classes: decision
- Posture: accepted canonical cleanup

## Context

AOA-MEM-D-0071 introduced stable decision IDs. AOA-MEM-D-0072 moved decision
source files from date-prefixed names to numbered names. AOA-MEM-D-0073 removed
the compatibility layer so the decision lane would not keep a second lookup
route.

That left one remaining local/agent mismatch: the stable handle was
`AOA-MEM-D-####`, while the filename only carried `####`. Inside
`docs/decisions/` that is readable, but outside the lane a short numbered path
does not carry owner, organ, or decision-class identity.

For OS Abyss, filenames are part of the operational map. A distant agent should
be able to inspect a path or search result and see the owner organ and object
class immediately, without reconstructing it from directory context.

## Decision

Use the full canonical decision ID as the decision filename prefix:

- `docs/decisions/AOA-MEM-D-0001-*.md`
- `docs/decisions/AOA-MEM-D-0002-*.md`
- `docs/decisions/AOA-MEM-D-####-*.md`

The `Decision ID` inside the file remains the stable handle. The filename
prefix must match that handle exactly. Short numbered filenames are no longer an
active source route and do not get compatibility maps or stub files.

## Alternatives

Keeping `####-slug.md` would be shorter and still sortable, but it depends on
directory context to recover the full identity.

Adding a second generated map from short paths to full paths would preserve
lookup convenience, but it would recreate the compatibility-layer problem that
AOA-MEM-D-0073 closed.

Duplicating the full ID only in generated indexes would help search, but not
manual file inspection, grep output, or cross-repo source refs.

## Consequences

Decision paths are longer, but the active file path now carries the complete
canonical handle.

Agents can route from path alone: `AOA-MEM-D` names the memo decision lane,
the number gives stable order, and the slug keeps human readability.

The decision-index builder, index contract, generated indexes, route card,
README, AGENTS mesh readout, and topology tests now enforce
`AOA-MEM-D-####-*.md` as the active source filename format.

## Affected Surfaces

- `docs/decisions/AOA-MEM-D-*.md`
- `docs/decisions/AGENTS.md`
- `docs/decisions/README.md`
- `docs/decisions/indexes/*`
- `docs/decisions/indexes/index_contract.yaml`
- `scripts/root-topology/decision_index_common.py`
- `generated/agents/agents_mesh.min.json`
- `tests/root-topology/test_topology_spine.py`

## Verification

Current executable checks are owned by `config/validation_lanes.json`;
focused owner routes live in the nearest `AGENTS.md` or `VALIDATION.md`.
