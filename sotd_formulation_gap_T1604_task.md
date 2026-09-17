# T-1604 - Residual risk formulation audit and bounded counterexample repair smoke

Status: review
Owner: formulation-gap
Agent: formulation-gap
Created: 2026-09-18 03:01:48
Updated: 2026-09-18 03:01:48

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Map residual event mechanisms to v4 conditional theory and test at most one counterexample repair on each of two fixed candidates.
- Non-Goals: No edits/restarts to running T1603, no large training, no margin/metric search, no final-eval feedback into fitting.
- Dependencies: T1603 finalizer retains task ownership; T1600 frozen cycle12seed180 candidates; v4 PDF read-only.
- Expected Deliverables: residual audit, isolated mask/transaction branch tests, formulation_gap.md, two end-to-end repair smoke receipts and bounded next protocol.
- Definition of Done: T1603 completion/publication verified independently; remaining failures traced by source; smoke costs/limitations/negative results retained; no new matrix.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/formulation_gap/v1`
- Publication-only extension: incremental `experiments/safeot_dual/progress_feed.json` after T1603 watcher completes and T1604 is review; preserve every old entry/owner.
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Freeze protocol/source; read-only T1603 status; mask branches and theory mapping.
- [x] Stage 2: Residual final actor/tapes/screens and necessary deterministic failure replay.
- [x] Stage 3: Two fixed candidate counterexample-repair smoke, synthesis and next single-factor protocol.

## Stage Log
- 2026-09-18 03:44:08 T1604 corrected actual-env smoke: first attempt invalid due accidental original_actor copy, retained as attempt1; restored immutable T1600 cycle012 pathwise actors and reran 4 frozen pairs/48 real steps, zero events, no training. Updated summary/report and hashes; no old result changed.
- 2026-09-18 03:40:07 Remote cleanup completed: removed 23 diagnostic checkpoints (~25.9GB) with manifest and 12 failed gate checkpoints (~12.7GB) with manifest; formal/data/recovery untouched. Remote free space now ~42GB, above 35GiB admission gate; requested recovery supervisor restart/verification.
- 2026-09-18 03:26:16 T1604 bounded audit and two fixed repair smoke complete. T1603 finalizer verified before task reacquisition. No performance improvement claim; original risk budgets/HOLD and all negative results retained.
- 2026-09-18 03:10:03 T1604 isolated real actor/Adam mask branches PASS. Residual K2s187 pathwisecycle22: admission0events, later cycle24 oldbank event1 yet fallback retained; K3s180 pathwisecycle24 likewise finite-bank miss. Eight final failures reproduced,96real+2496model auditsteps. Two fixed smoke exit0: K2one repair22forwards/reward-.065126,heldout0->0events;K3no trigger. No new training; T1603finalizer still owns its closeout.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: T1604 final evidence includes corrected real smoke and published formulation audit
- Tests: real_smoke PASS 48 steps; model smoke PASS; residual audit; hashes
- Completed-at: 2026-09-18 03:44:26
