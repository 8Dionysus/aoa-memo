# Memory Artifact Bundles

This directory holds OS Abyss artifact-bundle manifests for aoa-memo memory
surfaces that leave the repo as machine-consumable read models.

## Current bundle

- `memory_object_readmodels.bundle.json` covers the checked-in
  `generated/memory-objects/` readmodel family.

The bundle does not make generated memory truth. It signs the public ABI,
producer provenance, durable evidence record, and materialized subject-store
gate for consumers that already treat `MEMORY_INDEX.md`,
`docs/memory/MEMORY_OBJECT_PROFILES.md`, the schemas, and the generated surface
validators as the source route.

## Required controls

- ABI signature: required for the `artifact_identity` contract.
- SLSA/in-toto provenance: required for generator and subject lineage.
- SBOM: deferred until the readmodel family becomes a package or release bundle.
- Sigstore/Cosign: deferred until signed release assets exist.
- C2PA: not applicable unless a public media/export pipeline appears.

Use the artifact-bundle check in the parent [AGENTS](../AGENTS.md#validate)
route.
