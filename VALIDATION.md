# VALIDATION.md

On-demand human procedure for the repository root.

## On-demand procedure

Run the repository-wide CI modes from the repository root when the change crosses their corresponding surface:

```bash
python scripts/ci_gate.py --mode source-fast
python scripts/ci_gate.py --mode generated
python scripts/ci_gate.py --mode memory
python scripts/ci_gate.py --mode tests
```

### Local changed-path feedback (advisory)

For an ordinary edit, pass the complete changed-path set to the existing
entrypoint to run the mapped owner tests without running release preparation:

```bash
python scripts/ci_gate.py --feedback --changed-path mechanics/adoption/parts/adoption-boundary/schemas/adoption_memory_writeback_v1.json
```

Repeat `--changed-path` for each edited file. The selector reads the existing
root topology and test inventory, unions matching script/test families, and
discovers registered `mechanics/<package>/parts/<part>/tests` files. Duplicate
tests are removed. Runner, mapping, pytest fixture, environment, unknown, or
uncovered paths expand to the existing `release` lane. This is local edit
feedback only: it is not transitive cross-owner coverage, CI, release
admission, or owner acceptance. `--lf`/`--last-failed` is available only for a
bounded selection and delegates retry to ordinary pytest. It may deselect other
affected tests, so run feedback again without it for the complete affected set;
it is ignored when the selector has to use the full fallback. The bounded
pytest subprocess disables ambient third-party plugin autoloading while using
the repository's own `pytest.ini`; named validation modes keep their existing
environment and plugin behavior.

### Frozen release gate

```bash
python scripts/release/release_check.py
```
