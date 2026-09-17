# T-1600 - Fixed 2 percent intermediate pathwise margin on N100

Status: review
Owner: scenario-margin
Agent: scenario-margin
Created: 2026-09-17 23:06:34
Updated: 2026-09-17 23:06:34

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Test fixed2% intermediate model budget margin vs N100 DT; conditional smoke/replay then six development.
- Non-Goals: Do not change task budgets, observations, PPO, screens, eval, seeds, margin grid, or old files.
- Dependencies: Verified T1598 N100 controls and model tapes.
- Expected Deliverables: Frozen protocol/source, margin0 replay, margin.02 smoke, six receipts, report.
- Definition of Done: All bounded jobs accounted, original-task safety/reward gate evaluated, model cost and final source attribution reported.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/scenario_margin/v1`
- Additional carry-over publication scope: `diagnostic_runs/scenario_generalization/v1/publish`, `publication_followup.py`, `publication_receipt.json`, `publication.log`, and `experiments/safeot_dual/progress_feed.json` for completing T1598/T1600 review-approved evidence and persistent feed publication. Publication API script/receipts/export remain inside scenario_margin/v1; no changes to other owners or status/gap_plan.
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Frozen protocol, exact margin0 replay and full smoke.
- [x] Stage 2: Six bounded development jobs completed, HOLD.
- [x] Stage 3: Final actor/raw trace audit and deterministic scenario replay.
- [ ] Stage 4: Publish T1598/T1600 evidence and persistent feed; HTTP verification.

## Stage Log
- 2026-09-18 01:21:24 T1600 audit PASS: six final actors exact; 1872 eval episode costs/events re-summed float32; three K2s180 failures reproduced in real env and model. Original100 max5.879999 withinBopt5.88. Audit36real+1236model steps, zero training; stale handoff corrected. Prior publisher462814 exited before publication; API path available.
- 2026-09-17 23:09:50 First T1600 margin.02 K2 smoke exit0:480real steps,200scenario constraint rows,3basis directions,taskB[6,6],optB[5.88,5.88],18queries/21600modelsteps; fullPPO accepted (margin only affects middle). Controller454319 live; two margin0 exact replays andK3 smoke now running. Six development remain gated. T1598 publish watcher462814 waits original fetch (bounded15min), no false HTTP success.
- 2026-09-17 23:08:06 T1600 frozen2% middle-model margin only: task budgets/observations/PPO/screens/evaluator unchanged. All150 N100 tapes exact, shared adapter/risk/solver/eval byte identical. tmux t1600-margin starts single480step smoke, then margin0 exact replay/two smoke gates before six development. T1598 evidence export prepared; remote publication network fetch pending, no success claim.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: T1600六项完成HOLD；冻结actor、原始1872回合及三失败轨迹/100优化场景审计PASS；准备发布已验证证据
- Tests: training_gate PASS; audit_final.py exit0,36 real+1236 model replay steps; source_freeze exact; controller exit0
- Completed-at: 2026-09-18 01:21:30
