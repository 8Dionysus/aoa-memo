# Contributing to aoa-memo

Thank you for helping shape the AoA memory layer.

This repository is the memory and recall layer of AoA.
Contributions here should improve the clarity, coherence, and usefulness of memory-layer surfaces rather than turning this repository into a generic dump of context.

## What belongs here

Good contributions include:
- memory layer definitions
- memory object shapes
- provenance and recall guidance
- temporal and salience-oriented memory surfaces
- memory registries, schemas, and validation
- clearer boundaries between memory, proof, execution, and routing

## What usually does not belong here

Do not use this repository as the default home for:
- new technique bundles
- new skill bundles
- new eval bundles
- cross-repo routing surfaces as such
- infrastructure implementation details
- untyped notes with no memory-layer contract

If a change mainly defines reusable practice, bounded execution, or bounded proof, prefer the specialized neighboring repository first.

## Source-of-truth discipline

When contributing, preserve this rule:
- `aoa-memo` owns memory and recall meaning
- neighboring AoA repositories still own their own meaning

Examples:
- `aoa-techniques` owns practice meaning
- `aoa-skills` owns execution meaning
- `aoa-evals` owns proof meaning
- `aoa-routing` owns navigation surfaces
- `aoa-agents` should own role and persona meaning

## How to decide where a change belongs

Ask these questions in order:

1. Is this change mainly about memory, recall, provenance, salience, or temporal relevance?
   - If yes, it may belong here.
2. Is this change mainly about reusable practice?
   - If yes, it probably belongs in `aoa-techniques`.
3. Is this change mainly about bounded execution?
   - If yes, it probably belongs in `aoa-skills`.
4. Is this change mainly about bounded proof?
   - If yes, it probably belongs in `aoa-evals`.
5. Is this change mainly about dispatch across repos?
   - If yes, it probably belongs in `aoa-routing`.

## Pull request shape

A strong pull request in this repository should explain:
- what memory-layer surface changed
- why the change belongs in `aoa-memo`
- what neighboring AoA layers are affected
- what was intentionally not absorbed into this repository

## Style guidance

Prefer:
- compactness over memory sprawl
- explicit provenance over vague recall
- reviewable memory objects over magical context
- bounded memory contracts over overloaded metaphors
