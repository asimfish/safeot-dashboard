# T-1591 - Frozen candidate surrogate gap and variance decomposition

Status: review
Owner: surrogate-gap
Agent: surrogate-gap
Created: 2026-09-16 18:11:35
Updated: 2026-09-16 18:11:35

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Frozen-bank decomposition of train/holdout LR, stochastic rollout and official deterministic gains; variance intervention.
- Non-Goals: No training, optimization, radius changes, or edits to old results/trainers/DERIVATION/PDF.
- Dependencies:
- Expected Deliverables: Protocol, source manifest, 2 smoke and 30 formal evaluation receipts, paired episode traces, decomposition CSV/plots/report and publication receipt.
- Definition of Done: Verified 38400 formal episodes, seed-level analysis, conditional bootstrap uncertainty, single evidence-based next modification and published evidence/feed.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/surrogate_gap_decomposition/v1`, `experiments/safeot_dual/progress_feed.json` (authorized additive persistent T1591 entry; preserve owner and other entries).
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Freeze bank/protocol; audit existing observations.
- [x] Stage 2: Two smoke anchors then 30 formal anchors in detached three-worker controller.
- [x] Stage 3: Synthesis, persistent feed producer audit and publication.

## Stage Log
- 2026-09-16 18:31:12 T1591 all30 formal anchors +2smoke verified. 38400 formal episodes/460800 steps, no training. Largest gap T;42/60 sample-positive det-nonpositive; variance-only operational explanation2/42. Preserve two failed48-step replay receipts; exact original accumulator fixes gate. Persistent feed source append preserves owner/all35 prior entries.
- 2026-09-16 18:24:53 T1591 29 formal anchors verified; anchor21 replay reduction mismatch isolated before fresh sampling. Original float32 mean restored, tolerance unchanged; retry only21 with original failure preserved. No training.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: T1591 fixed-bank evaluation and decomposition verified; producer-source feed entry prepared, evidence publication follows review
- Tests: verify_final.py PASS; agentctl check --mode manual PASS; prediction/selection replay; paired CRN/LOO identities; immutable checkpoint hashes; reward precision audit
- Completed-at: 2026-09-16 18:32:16

- Publication update: immutable evidence commit 20d0413aa419cdbd54a8334256b4c903b89253ed pushed after task review. Persistent source entry preserves T1484 owner/all35 entries; homepage feed publication/HTTP check follows.

- Final publication verified: evidence 20d0413aa419cdbd54a8334256b4c903b89253ed; feed c0011caa8f517589480b61f591c06e76e32c4db0. HTTP200 cache-busted feed first14 includesT1591, all35 prior entries preserved, report hash equals local. Receipt: diagnostic_runs/surrogate_gap_decomposition/v1/publication_receipt.json. No new training pending; next estimator experiment awaits separately frozen instruction.
