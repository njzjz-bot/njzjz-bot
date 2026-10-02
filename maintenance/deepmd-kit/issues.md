# DeepMD-kit maintainer inbox

This branch is a persistent queue for DeepMD-kit issue triage and maintainer replies when direct GitHub commenting is unavailable or unreliable.

## Workflow

- Check new and recently active issues in `deepmodeling/deepmd-kit`.
- Reply directly when a maintainer response is clearly useful and the GitHub write succeeds.
- If a reply cannot be posted, record it here instead of dropping it.
- Keep enough evidence to retry later without re-investigating the whole issue.
- Do not reply to resolved, duplicate, adequately answered, or purely tracking issues.
- Every GitHub-facing reply should end with:
  - `Agent: ChatGPT`
  - `Model: GPT-5.6 Sol`

## Status values

- **PENDING_REPLY** — maintainer reply is warranted but has not been posted.
- **RETRY_REPLY** — a direct reply was attempted but the write failed.
- **REPLIED** — reply was posted successfully.
- **SKIPPED** — reviewed; no maintainer reply is needed.
- **RESOLVED** — issue no longer needs action.

## Queue

### #6039 — conda install cannot freeze fine-tuned checkpoint because cuda.h is missing

- URL: https://github.com/deepmodeling/deepmd-kit/issues/6039
- Status: **REPLIED**
- Last checked: 2026-09-30
- Reply: https://github.com/deepmodeling/deepmd-kit/issues/6039#issuecomment-5894316148
- Evidence:
  - The traceback fails in Triton/AOTInductor while compiling a CUDA helper that includes `cuda.h`.
  - The current conda-forge feedstock has `cuda-driver-dev` in host/test requirements but not in the Python runtime output requirements.
- Posted maintainer reply: identified the packaging/runtime dependency gap, suggested `cuda-driver-dev` as the immediate workaround, and recommended a runtime dependency plus freeze/AOTI smoke-test fix in the feedstock.

### #5995 — DeepMD LAMMPS pair styles misinterpret comm_style tiled as CommBrick

- URL: https://github.com/deepmodeling/deepmd-kit/issues/5995
- Status: **REPLIED**
- Last checked: 2026-09-30
- Reply: https://github.com/deepmodeling/deepmd-kit/issues/5995#issuecomment-5894316798
- Evidence:
  - Current `master` still lacks a `Comm::BRICK` guard in the common base path and in `PairDPA4Spin`.
  - The contributor reproduced a real two-rank message-passing DPA4 failure with huge invalid allocations under `comm_style tiled`.
- Posted maintainer reply: asked the contributor to proceed now with the focused fail-fast guard and regressions, without waiting for #6012.

### #5993 — dpa4spin accepts non-metal units but uses metal-unit hbar

- URL: https://github.com/deepmodeling/deepmd-kit/issues/5993
- Status: **REPLIED**
- Last checked: 2026-09-30
- Reply: https://github.com/deepmodeling/deepmd-kit/issues/5993#issuecomment-5894317449
- Evidence:
  - Current `master` still rejects only `lj` while using the hard-coded metal-unit reduced Planck constant `6.5821191e-04 eV.ps`.
  - #6012 remains a separate draft runtime-plugin registration PR.
- Posted maintainer reply: requested an independent metal-only guard PR with focused tests and explicitly said not to wait for #6012.

### #5954 — Record exact label availability when building LMDB datasets

- URL: https://github.com/deepmodeling/deepmd-kit/issues/5954
- Status: **REPLIED**
- Last checked: 2026-09-30
- Reply: https://github.com/deepmodeling/deepmd-kit/issues/5954#issuecomment-5894318089
- Evidence:
  - The contributor reproduced the rare-signature case through the real dpdata writer and DeePMD LMDB reader.
  - #5962 is merged and intentionally retains a legacy bounded-probe fallback; it explicitly tracks exact generation-time metadata in #5954.
- Posted maintainer reply: accepted the coordinated producer/consumer direction and recommended small versioned metadata, strict validation, transactional publication, legacy fallback, and explicit merge/filter behavior.

### #6000 — Support decoupled observer-model inference for model deviation in deepmd/kk

- URL: https://github.com/deepmodeling/deepmd-kit/issues/6000
- Status: **REPLIED**
- Last checked: 2026-09-27
- Reply: https://github.com/deepmodeling/deepmd-kit/issues/6000#issuecomment-5857368210
- Evidence:
  - Current `master` still rejects `numb_models != 1` in `PairDeepMDKokkos::init_style()`.
  - The regular `pair_style deepmd` path initializes the multi-model model-deviation backend and already separates the model-0 dynamics output from committee deviation evaluation.
  - The issue therefore describes a real `deepmd/kk` feature gap rather than a usage problem.
- Posted maintainer reply: confirmed the gap, endorsed the driver/observer split as the implementation direction, and suggested a narrow first milestone around compatible `.pt2` committee models, model-0 dynamics, `out_freq` observer evaluation, device-graph reuse, and deterministic agreement with regular `deepmd`.

### #5983 — pair_style deepmd/kk does not populate global virial / thermo pressure for a DPA4 pt_expt model

- URL: https://github.com/deepmodeling/deepmd-kit/issues/5983
- Status: **REPLIED**
- Last checked: 2026-09-26
- Reply: https://github.com/deepmodeling/deepmd-kit/issues/5983#issuecomment-5843298527
- Evidence:
  - The reporter tested changing the Kokkos guard from `if (vflag_global)` to `if (vflag_either)`.
  - The reporter confirmed that the same reproduction then reports nonzero global thermo stress and that summed per-atom centroid virial remains consistent with the non-Kokkos path.
  - The issue remains open; the maintainer follow-up has now been posted.

## Check log

### 2026-10-03

- No new DeepMD-kit issues required a maintainer reply in this review.
- Rechecked recent open issues and found no new reporter follow-up needing action.
- No new PENDING_REPLY or RETRY_REPLY entries were added.

### 2026-09-30

- Cleared all four previously unfinished maintainer replies: #6039, #5995, #5993, and #5954.
- All four direct GitHub comments succeeded.
- Recorded each item as **REPLIED** with the comment URL; no pending/retry drafts remain from this batch.

### 2026-09-27

- Manually retried the maintainer reply for #6000.
- Direct GitHub comment succeeded; recorded the item as **REPLIED** with the comment URL.

### 2026-09-26

- Retried the pending maintainer reply for #5983.
- Direct GitHub comment succeeded; marked the item **REPLIED** and recorded the comment URL.

### 2026-09-25

- Initialized this persistent maintainer inbox.
- Seeded #5983 because a maintainer follow-up is still warranted and a previous direct-comment attempt failed.

---
Maintained by ChatGPT. Model: GPT-5.6 Sol.
