# Validation Companions Are Route Metadata

- Decision ID: AOA-MEM-D-0089

## Status

Accepted on 2026-09-04.

## Index Metadata

- Original date: 2026-09-04
- Surface classes: validation guard, agents/mesh, root/topology, mechanic package
- Mechanic parents: none
- Guard families: AGENTS/mesh, docs route, mechanic topology, root technical district, release/tooling
- Memory object classes: none
- Posture: accepted route-companion classification; no source, proof, runtime, or release claim

## Context

`AOA-MEM-D-0087` requires one same-directory `VALIDATION.md` companion for
every tracked `AGENTS.md`. The first complete materialization exposed a second
set of classifiers that still treated every new Markdown file as ordinary
payload. A docs companion appeared to be unregistered doctrine, the Questbook
companion appeared to be a quest source, and companions under root technical
districts appeared to be uncatalogued artifacts.

Adding every companion to each payload allowlist would make route metadata
look authoritative for the adjacent domain and would duplicate the AGENTS mesh
inventory across several topology sources.

## Decision

A same-directory `VALIDATION.md` is route metadata when, and only when, its
sibling `AGENTS.md` is tracked. Root technical artifact classification derives
that bounded companion set from tracked cards and keeps it outside payload
allowlists, just as route cards themselves stay outside those allowlists.

Domain validators recognize the companion without counting it as doctrine,
quest content, manifest content, generated output, or mechanic source docs.
Mechanic package, docs, and parts companions remain required structural
surfaces; individual part validation continues to link its package validation
owner rather than copying the shared mechanic-topology command.

The AGENTS mesh remains the authority for companion presence, one-document
shape, explicit route targets, and duplicate executable ownership. A loose
untracked pair does not acquire a topology exemption merely by using these
filenames.

## Alternatives

- Add every companion to every technical and domain payload allowlist.
- Exclude every file named `VALIDATION.md` without checking its sibling card.
- Remove local companions and fall through to ancestor procedure.

## Consequences

- Route metadata no longer contaminates domain payload inventories.
- The exception stays bounded by Git-tracked owner cards rather than filename
  convention alone.
- Package readiness can require active package, docs, and parts companions
  without treating legacy validation as active payload.
- Green topology establishes placement and routing shape only; it does not
  establish command success, proof, CI, review, merge, runtime, or acceptance.

## Affected Surfaces

- tracked `AGENTS.md` and same-directory `VALIDATION.md` pairs
- `config/root-topology/root_technical_districts.json`
- `scripts/mechanics/mechanic_artifact_topology_common.py`
- `scripts/mechanics/validate_mechanic_artifact_topology.py`
- `scripts/mechanics/memo_mechanics_common.py`
- `scripts/mechanics/validate_memo_mechanics.py`
- `scripts/mechanics/validate_memo_mechanic_parts.py`
- `scripts/root-topology/validate_docs_districts.py`
- Questbook source validation
- root-topology and mechanic regression tests

## Verification

Use the nearest validation companions for decision indexes, AGENTS mesh,
mechanic topology, root technical districts, docs placement, Questbook source
shape, generated companions, and the full owner-local release lane. These
checks remain bounded to their declared contracts.
