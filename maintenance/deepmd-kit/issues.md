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

### #5983 — pair_style deepmd/kk does not populate global virial / thermo pressure for a DPA4 pt_expt model

- URL: https://github.com/deepmodeling/deepmd-kit/issues/5983
- Status: **RETRY_REPLY**
- Last checked: 2026-09-25
- Evidence:
  - The reporter tested changing the Kokkos guard from `if (vflag_global)` to `if (vflag_either)`.
  - The reporter confirmed that the same reproduction then reports nonzero global thermo stress and that summed per-atom centroid virial remains consistent with the non-Kokkos path.
  - The issue is still open.
- Suggested maintainer reply:

> Thanks for testing and confirming the guard change. That is strong evidence that the Kokkos path should use `vflag_either` here rather than `vflag_global`.
>
> We should carry this as a code fix in `source/lmp/pair_deepmd_kokkos.cpp` and add a regression test that covers global thermo pressure together with per-atom/centroid virial requests, so the Kokkos and non-Kokkos paths cannot diverge again.
>
> Agent: ChatGPT  
> Model: GPT-5.6 Sol

## Check log

### 2026-09-25

- Initialized this persistent maintainer inbox.
- Seeded #5983 because a maintainer follow-up is still warranted and a previous direct-comment attempt failed.

---
Maintained by ChatGPT. Model: GPT-5.6 Sol.
