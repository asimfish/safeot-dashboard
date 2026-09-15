# T-DO-001 - Dual-only actor transfer and selection bias gates

Status: review
Owner: dualonly
Agent: dualonly
Created: 2026-09-15 16:46:11
Updated: 2026-09-15 16:46:11

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Complete dual-only gradient gate, bias diagnostic and gated development pilot.
- Non-Goals:
- Dependencies:
- Expected Deliverables:
- Definition of Done:

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/dual_only`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Audit closed finite results and selection bias.
- [x] Stage 2: Pass actual PPO gradient gates and complete6 development jobs.
- [x] Stage 3: Promotion gate failed; retain all negative results, no confirm expansion.

## Stage Log
- 2026-09-15 16:50:10 Completed gradient gate and six dual-only/PPOLag/finite pilot jobs, exit0/exact2400steps/checkpoint pass. Dual-only joint1 in both environments, no strict reward+joint gain over PPOLag; promotion gate fails, seeds170-174 not launched. Fixed-action paired-noise diagnostic demonstrates selection optimism. report diagnostic_runs/dual_only/v1/report.md.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Completed dual-only gradient gate and6 pilots; strict promotion criterion fails
- Tests: gradient_gate.py; bias.py; acceptance.json; agentctl check --mode manual
- Completed-at: 2026-09-15 16:50:27
