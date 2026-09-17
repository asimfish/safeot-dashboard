# T-1603 - Independent deployment admission paired diagnostic

Status: review
Owner: independent-admission
Agent: independent-admission
Created: 2026-09-18 02:11:58
Updated: 2026-09-18 02:11:58

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Isolate independent det model admission mask vs equal-compute monitor; frozen12-policy fresh generalization audit.
- Non-Goals: No changes to old results, margin/solver/reward/budget/real screens; no new eight-hour campaign, no parameter search.
- Dependencies: T1598 N100 and T1600 margin.02 frozen actors and exact replay.
- Expected Deliverables: Protocol/hash/seed manifests, replay and smoke gates,12 frozen evaluations,12 matched jobs+fresh eval, paired reports/cost ledger/persistent dashboard.
- Definition of Done: Account all failures; per-seed safety/reward decision; auto collector; review then evidence/feed HTTP verified.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/independent_admission/v1`
- Additional publication-only scope: `experiments/safeot_dual/progress_feed.json` incremental T1603 entry after review, preserving all owners/prior entries. Publication script/receipts remain inside this task directory.
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Freeze protocol/data/source; import/microcases; two monitor exact replays and two gate smoke.
- [x] Stage 2: Frozen A12 evaluation;12 development and fresh finalE evaluation; maximum4CPU,2h/job,6h batch.
- [ ] Stage 3: Full paired audit/decision/costs, review and persistent publication.

## Stage Log
- 2026-09-18 03:25:42 T1603 bounded evaluation/training complete, six monitor controls exact. Summary/report/costs and failures collected; scientific decision per frozen gate. Preparing source-backed publication.
- 2026-09-18 02:21:22 T1603 single K2 gate smoke exit0:480real steps,9216 independent admission model steps; all3candidates logged, PPO accepted with original Adam moments; disk reload verified. K3smoke and K2monitor replay exit0, K3monitor replay ongoing. Controller1817758; detached finalizer active for collection/review/publication, no auto repeat.
- 2026-09-18 02:18:44 T1603 protocol and55,296 unique reserved uint64 scene IDs frozen; old ID intersection0; snapshot/solver/risk exact. Preflight PASS mask/fallback microcases and48 model-step old-trace mirror,0 real steps. Starting single gate smoke before exact monitor replay; no development yet.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Independent admission bounded diagnostic complete; frozen gate decision and full accounting retained
- Tests: preflight; training_gate; six25cycle monitor replays; raw episode transaction/source audit
- Completed-at: 2026-09-18 03:25:42
