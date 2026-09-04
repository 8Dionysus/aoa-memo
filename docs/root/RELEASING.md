# Releasing `aoa-memo`

`aoa-memo` is released as the provenance-aware memory and recall layer of AoA.

See also:

- [README](../README.md)
- [CHANGELOG](../CHANGELOG.md)

## Recommended release flow

1. Keep the release bounded to memory, recall, and writeback posture.
2. Update `CHANGELOG.md` in the `Summary / Validation / Notes` shape.
3. Start from a branch based on the current `origin/main`; inventory any
   pre-existing dirty worktree and carry only the intended diff.
4. Commit the bounded change with a surface-specific message.
5. Push the branch and open a pull request describing changed surfaces,
   validation, skipped checks, and remaining risk.
6. Wait for GitHub `Repo Validation` and required checks; repair and rerun on
   failure.
7. Merge through GitHub only after green checks and observed review authority;
   use the repository-required merge method and report what landed.
8. Return to `main`, fast-forward from `origin/main`, and confirm a clean
   worktree before closeout.
9. Run the repo-level verifier through the frozen `release_check` lane.
10. Run the workspace release-tool compatibility verifier through its named
    compatibility route.
11. Run federation preflight through the release tool and publish only through
    the release tool's publish route.

The repo-level verifier includes the OS Abyss ABI/provenance bundle and
consumer trust-gate check for `generated/memory-objects/`; keep
`abyss-machine` available when exercising the full release lane.

Workspace release tooling also probes `docs/RELEASING.md` and
`scripts/release_check.py`. Those files are compatibility entrypoints; this
file and `scripts/release/release_check.py` remain the active procedure and
gate.

If GitHub status, review, merge permissions, or post-merge state cannot be
observed, stop the landing route and report the exact blocker rather than
guessing. A local green lane proves only its declared contract; it does not
prove external CI, review, merge, runtime, memory acceptance, or Goal
completion.
