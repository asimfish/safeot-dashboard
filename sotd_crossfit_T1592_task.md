# T-1592 - Cross-fitted episodic reward baseline controlled development

Status: review
Owner: crossfit-reward
Agent: crossfit-reward
Created: 2026-09-16 18:43:04
Updated: 2026-09-16 18:43:04

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Isolate reward-advantage baseline intervention in frozen joint solver, with exact timeLOO controls and independent mechanism bank.
- Non-Goals: No radius/ridge/features search, no changes to budgets/shaping/cost baseline/PPO/critics/excess screen/det; no old results or global trainers/DERIVATION/PDF edits.
- Dependencies: Read-only T1590 solver/worker/snapshot and T1591 fixed-bank index. CPU only, three single-thread workers.
- Expected Deliverables: Frozen protocol/math gates; 8smoke,24development,12independent mechanism anchors; per-episode data/baseline folds/checkpoint receipts; seed-level report/CSV/plots and durable dashboard feed.
- Definition of Done: Full24development and12mechanism jobs verified or concrete failures retained; exact timeLOO replay; exploratory recipe decision separate from OT value; task review and verified publication.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/crossfit_reward_baseline/v1`, `experiments/safeot_dual/progress_feed.json` (authorized additive publication source entry only; preserve owner/all previous entries).
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Freeze recipe and implement leakage/algebra/gradient and replay gates.
- [x] Stage 2: Detached8smoke →24development; independent12anchor mechanism with new seeds.
- [x] Stage 3: Audit complete budgets, synthesis, decision, persistent feed publication.

## Stage Log
- 2026-09-16 21:05:30 T1592 all44jobs verified,12 exact controls,478848 total environment steps. HOLD_THIS_RECIPE: all CF configurations retain observed violations; no matching-safe OT advantage. Mechanism optimism reduction6/12 seed-metric summaries only; K2s187 worsens. No extension.
- 2026-09-16 20:58:01 T1592 fixed recipe gates and8smoke PASS; controller3983672 now full24development followed by12mechanism. Detached final watcher installed. No recipe tuning; original time controls exact verification required.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: T1592 completed8smoke/24development/12mechanism with12 exact controls; HOLD_THIS_RECIPE; persistent feed prepared for post-review publication
- Tests: gate.py; verify.py smoke/development; verify_final.py PASS; source/hash/CRN/OOF/optimizer and312episode exact replay; agentctl check manual
- Completed-at: 2026-09-16 21:07:16
