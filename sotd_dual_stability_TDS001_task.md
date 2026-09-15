# T-DS-001 - Independent dual-only stability protocol and matched ablation

Status: review
Owner: dualstability
Agent: dualstability
Created: 2026-09-15 20:07:50
Updated: 2026-09-15 20:07:50

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Independently assess dual-only stability and mechanism contribution without changing the historical FAIL.
- Non-Goals: Formal superiority, power certification, further parameter search, PDF changes.
- Dependencies: Verified dual_only/v1 snapshots and user-authorized independent protocol.
- Expected Deliverables: 20 stability runs, 3 matched ablations, noise-price and epoch audits, final receipts and dashboard export.
- Definition of Done: Exact training steps, checkpoint reload, source hashes and exit codes verified; exploratory synthesis preserves negative findings.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/dual_stability`
- Files likely to touch: v1 scripts, protocol, immutable snapshots, job outputs, dashboard export.
- Files explicitly out of scope: Shared algorithm defaults, old protocols/results, papers/PDF.

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Historical audit and independently frozen protocol.
- [x] Stage 2: 20 stability jobs and 3 separate ablations, all verified exit0.
- [x] Stage 3: Noise-price diagnostic and synthesis with prior FAIL retained.

## Stage Log
- 2026-09-15 20:14:11 23 jobs verified exit0 and checkpoint reload; final K2/K3 synthesis and noise-price audit complete; old superiority FAIL retained.
- 2026-09-15 20:10:49 New independent protocol frozen; old FAIL preserved. 20 stability jobs +3 separate ablations running with4 one-thread CPUs. Old dual active2/10 K2 and4/10 K3; ablation all joint1 but dynamic reward8.4838 vs zero8.8071. Noise-only critical action cohorts raw y-price0..1.2608 and1/20 infeasible. No causal or formal superiority claim.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Independent stability and mechanism study complete:23 verified jobs, negative/mixed findings preserved
- Tests: final_audit.py;23 exit0 and checkpoint reload/source/step checks;agentctl check --mode manual
- Completed-at: 2026-09-15 20:14:12
