# Owner source return

Resolve the canonical `aoa-memo` owner before any owner-relative read. This
route establishes package provenance and owner navigation only; it does not
prove current memory meaning, installed parity, or a disposition.

## Gate

1. Use the `<bundle_dir>` recorded from the loaded `SKILL.md`. Initialize one
   unresolved `<source_route>` and `<owner_root>`.
2. In one tool turn, use one file-read operation against exactly:

   ```text
   <bundle_dir>/.aoa-skill-source.json
   ```

   Await the result. Do not precede the read with `test`, `stat`, `ls`, or
   another existence probe, and do not append `&&`, `||`, a fallback, or a
   second command. A not-found result permits the Git branch below; any other
   read error is terminal.
3. If that path is a regular file:

   - set `<source_route>` to `source-handle`
   - require schema `aoa_skill_source_receipt_v1` or
     `aoa_skill_source_receipt_v2`
   - require bundle `aoa-memo` and owner `aoa-memo`
   - require version `0.1.21`
   - require an existing absolute `owner_root`
   - require a safe relative `source_path`
   - require `<owner_root>/<source_path>/SKILL.md`
   - for v2, require non-empty `digest`, `source_fingerprint`,
     `source_fingerprint_scope`, and `prompt_description_sha256`; when
     `capability_graph_hash` is present, require it to be a non-empty string
     and preserve it

   If the path exists but is invalid, mismatched, or not a regular file, return
   `blocked_missing_owner_source`. Do not try another route.
4. Only when the exact same-bundle handle path does not exist, set
   `<source_route>` to `git` and run exactly once:

   ```text
   git -C <bundle_dir> rev-parse --show-toplevel
   ```

   Require the returned root to contain `skills/port.manifest.json`.
5. In the next tool turn, read only:

   ```text
   <owner_root>/skills/port.manifest.json
   ```

   Await the result. Do not batch an owner document, candidate, object,
   evidence read, or unrelated command with the manifest.
6. Require owner `aoa-memo`, bundle `aoa-memo`, and the actual bundle path. In
   the source-handle branch, also require the same owner, name, and path as the
   handle. A mismatch returns `blocked_missing_owner_source`.
7. Only after manifest success may a later tool turn read owner surfaces
   required by the selected mode.

If the manifest shared a tool batch with an owner document, return
`blocked_owner_source_gate_not_observed` and do not use either result.

## Prohibited fallback

Never use `find`, `rg --files`, parent traversal, sibling scans, workspace
conventions, temporary fixtures, `.system`, or another skill directory to
discover a substitute owner. Do not retry the unused branch after a later
owner read fails.

Resolve every owner-relative path beneath the returned root. Treat handle
schema, owner ref, dirty posture, digest, source fingerprint, capability graph
hash, and prompt-description hash as install provenance rather than authority
or current-parity proof.

## Receipt

Report:

- `<source_route>`
- `<owner_root>`
- handle schema and identity dimensions, or git action ref
- manifest action ref
- first later owner-read path and action ref

A failed or non-serial resolution is terminal for the invocation. Do not
produce an owner-dependent memory disposition from the installed package alone.
