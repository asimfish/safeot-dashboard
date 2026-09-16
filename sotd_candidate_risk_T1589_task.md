# T-1589 - Candidate support and episode excess factorial

Status: review
Owner: candidate-risk
Agent: candidate-risk
Created: 2026-09-16 16:35:45
Updated: 2026-09-16 16:35:45

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Finite 2x2 support-set versus episode-excess risk intervention, with exact A_mean replication.
- Non-Goals: No beta sweep, no global trainer/old evidence/PDF/DERIVATION edits, no Fisher-as-OT attribution.
- Dependencies: Read-only T1588 attempt2 snapshot, full_none trajectories and contextual baseline receipts.
- Expected Deliverables: Frozen protocol, stall_audit, risk and transaction gates, 8 smoke/24 development receipts, paired contrasts and additive dashboard publication.
- Definition of Done: Independent replay/episode audits, complete bounded matrix, prospective gate classification, synthesis and published receipt.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/candidate_risk_factorial/v1`
- Files likely to touch: candidate_risk_factorial/v1 independent scripts, snapshot, jobs, protocol, findings, report and publication worktree.
- Files explicitly out of scope: source T1588, global trainer, PDF, DERIVATION and other agent records.

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Reproduce all supplied stall counts, freeze protocol and pass mathematical/transaction gates.
- [x] Stage 2: 8 two-cycle smoke and exact original first-cycle/paired-shadow verification.
- [x] Stage 3: Complete 24 development and full original A_mean replay; summarize paired factorial effects.
- [ ] Stage 4: Workflow verification and additive dashboard publication.

## Stage Log
- 2026-09-16 16:46:34 All24 development verified with exact six A_mean replays; 600 transaction/RNG/episode audits passed. B_excess joint1 both environments but lower reward vs A_mean; frozen gate fails, no expansion.
- 2026-09-16 16:42:26 Exact stall audit and 8 smoke gates passed; bounded 24 development running with paired PPO/Fisher shadows, detached synthesis watcher, no baseline reruns.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- 2026-09-16: Independent T-1589 claimed, prior T-1551 broad lock overridden only for narrow new scope. Controller PID3027027, tmux candidate-risk-t1589; detached synthesis watcher candidate-risk-finalize.
- 2026-09-16: All source stall counts reproduced; smoke8 exit0, paired first shadows and A_mean old firstcycle exact. 24 development launched after gate.

- 2026-09-16: Controller3027027 exit0; synthesis watcher exit0. All24 development completed; source hashes match; 600 optimizer/RNG/risk audits PASS. B_excess K2 reward9.215463/joint1, K3 reward9.485178/joint1. Mean reward differences versus A_mean −.095883/−.051711: HOLD.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Completed 2x2 candidate/risk factorial, 8 smoke+24 development, exact controls and 600-cycle audits; retained failed reward gate and prepared additive dashboard.
- Tests: audit.py; gate.py; risk_gate.py; verify.py smoke/development; extra_audit.py; synthesize.py; py_compile; agentctl check manual: all PASS
- Completed-at: 2026-09-16 16:46:34
