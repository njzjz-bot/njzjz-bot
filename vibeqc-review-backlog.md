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

Agent: ChatGPT
Model: GPT-5.6 Sol
