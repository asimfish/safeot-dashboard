# T-1590 - Joint local solver KL versus Gaussian W2 trust region

Status: review
Owner: joint-metric
Agent: joint-metric
Created: 2026-09-16 17:08:52
Updated: 2026-09-16 17:08:52

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Paired KL/W2 local joint trust-region solver in shared KL-Fisher basis under frozen deterministic excess screen.
- Non-Goals: No old result/default trainer/PDF/DERIVATION edits; no posthoc beta search or SafeOT novelty claim.
- Dependencies: Read-only T1589 snapshot/B_excess checkpoints and original Fisher solver.
- Expected Deliverables: Algebra and offline36-case gates, smoke12/development36, exact KL_s1 controls, paired curves, report, immutable evidence and visible feed commits.
- Definition of Done: Source/distance/transaction/step/eval replay audits pass; all36 bounded cells retained and prospective criterion judged; published report/feed HTTP validated.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/joint_metric_solver/v1`
- Files likely to touch: isolated joint_solver/worker/gates/controller/watcher, protocol/design, jobs/audits/curves/report and dashboard publish worktree.
- Files explicitly out of scope: T1588/T1589 source/result directories, global trainers, DERIVATION, paper/PDF and unrelated tasks.

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Freeze protocol; algebra, derivative and six old-batch offline gates.
- [x] Stage 2: 12 smoke and36 development with detached controller and final watcher.
- [x] Stage 3: Replay/audit/curves and prospective gate; additive evidence/feed publication.

- [ ] Stage 4: Publish immutable evidence then additive homepage feed, verify HTTP/cache/report SHA.

## Stage Log
- 2026-09-16 17:30:33 12smoke+36development verified exit0; six KL_s1 controls exactly reproduce T1589 through312eval;900cycles/1800distance audit PASS. No common safe-beneficial W2 scale; HOLD. Curves rendered and checked; preparing evidence/feed publication.
- 2026-09-16 17:18:29 12smoke passed including two-cycle KL_s1 exact replay and common6-arm firstbatch/PPO/anchor/D/calibration; 36 development running. Independent distance audit/curve watcher detached.
- 2026-09-16 17:14:32 Algebra gate passed including supplied anisotropic fixture; all36 offline metric-scale cases passed, six nondegenerate anchors and exact old KL_s1 actor/D. Detached smoke/controller launched.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- 2026-09-16: Narrow task session T1590, no active duplicate. Protocol frozen before numerical outcomes. Formula fixtures pass. Offline restore Tensor.copy and duplicate metadata key bugs retained as offline_failure_1/2 (zero environment steps); no objective/hyperparameter changes.

- 2026-09-16: Six anchors/36offline cases verified, KL_s1 old actor exact.12smoke exit0 with full two-cycle T1589 replay; 36development launched by controller3176819 with3single-thread CPU workers. Final watcher detached joint-metric-finalize; no GPU use or duplicate training.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: T1590 local joint metric experiment complete:36 development/432000 interactions, exact controls, full distance gates and curves; HOLD no expansion; publication prepared.
- Tests: math/offline/risk/transaction gates; verify smoke/development; distance1800; neural derivative6; constraints1800; source hashes; synthesis; agentctl manual PASS
- Completed-at: 2026-09-16 17:30:33
