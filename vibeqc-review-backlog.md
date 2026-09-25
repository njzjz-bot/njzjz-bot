# VibeQC review backlog

Temporary fallback log for VibeQC PR review findings when direct GitHub review/comment writes to `jinzhezenggroup/vibeqc` are blocked.

Rules:
- Record the VibeQC PR number, full reviewed head SHA, intended review disposition, concrete findings, and tests/evidence.
- Keep entries in English.
- Do not treat an entry here as a submitted GitHub review.
- Publish the review to the original PR when write access becomes available, then mark the backlog entry as published.
- Do not use this branch to bypass branch protection, approvals, or merge requirements.

Initialized by:
- PR #1289, head c549d7e644f876a1e8ea8906def08f5c13f60090, intended COMMENT: repaired an escaped-newline source corruption in `project_occupied_density` that commented out the norm-loss calculation and left an unconditional throw. Repair commit c549d7e644f876a1e8ea8906def08f5c13f60090 restores the intended residual guard. Previous exact-head evidence: gcc/clang `vibeqc_initial_density_tests` and the xTB orbital validation both failed with `occupied projection loses too much source occupied norm`; after the repair, exact-head clang CI passed while gcc/validation and other lanes were still pending at review time. Keep Draft until the PR's stated GFN2 source-basis translation and endpoint qualification gates are complete. Direct review/inline-comment publication was blocked.

Agent: ChatGPT
Model: GPT-5.6 Sol


## 2026-09-25 pending publications

- PR #1278, head 8caa88ecf8c031b8db6e0e6e492cd6fdc0779310, intended COMMENT: current source and exact-head checks reviewed; keep Draft because real NVIDIA SR/LR K execution/qualification is still required. Direct review publication was unavailable.
- PR #1274, head 7a09854e315d56fbe2c52d80c2081e1c89106e8e, intended repair note: restored the ten exact profiler blobs declared by migration.json as retained_exports (42,679 bytes total); fresh exact-head CI required. Direct comment publication was unavailable.
- PR #1282, head 23b5fbce94b992618ebbe9962cbc5c180678eccc, intended repair note: validation/timeout/local-probe fixes are present; repaired two PLW1510 negative-path subprocess calls with explicit check=False; fresh exact-head CI required. Direct review publication was unavailable.
- PR #1294, head c07b1ef8b43d079c2ec1dbe018fc2686a202028a, intended repair note: repaired the PLW1510 seed-probe negative-path subprocess call with explicit check=False; fresh exact-head CI required. Direct review publication was unavailable.

- PR #1288, head 87571f60631219f3fbc66762614c54453f26aad5, intended COMMENT/changes needed: the compact D3 product integrity repair is present, but the current exact-head python(core) and python(compiler-heavy) jobs still fail the PR's offline ordinary-test contract. `tools/vibeqc_d3/reference.py` reads the now-remote-only xTBloom source registry during normal D3 qualification, and an ordinary GFN1 geometry test still runs the remote-backed generator `--check`. With the vendored snapshot deleted and no explicit maintainer sync, both routes raise `FileNotFoundError` from `.cache/vibeqc-sources`. Ordinary reference/validation consumers should use the checked-in authenticated compact/generated products; remote source-registry access should remain limited to explicit regeneration/source-integrity paths. Do not mask this by adding an implicit network sync to normal CI. Direct review/inline-comment publication was blocked. Evidence: exact-head workflow run 36102371270, python(core) job 107967929141 and python(compiler-heavy) job 107967929137; no local test execution claimed.
- PR #1274, head 7a09854e315d56fbe2c52d80c2081e1c89106e8e, updated intended repair note: exact-head python(core) now fails because `test_trimmed_members_remain_recoverable_offline` requires every bulk-snapshot member to be absent, while this PR intentionally restored profiler CSV exports. The retention owner explicitly defines same-stem CSVs as `retained_exports` for archived .sqlite/.nsys-rep/.ncu-rep artifacts. The test should keep strict absence for every other archived member but require each allowed retained export to be a regular non-symlink file whose bytes exactly match its baseline Git object. A prepared narrow test repair could not be written because the GitHub mutation was blocked. Evidence: exact-head workflow run 36106351128, python(core) job 107979645592; 9538 tests passed and this single retention assertion failed.

Agent: ChatGPT
Model: GPT-5.6 Sol
