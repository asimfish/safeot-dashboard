# T-RISK-001 - Mentor risk formulation audit and budget-consistent follow-up design

Status: review
Owner: mentor-risk-formulation
Agent: mentor-risk-formulation
Created: 2026-09-16 23:55:18
Updated: 2026-09-16 23:55:18

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Correct the risk formulation handoff using explicit statistics, deployment semantics, and reproducible analysis of existing T1593 trajectories.
- Non-Goals: No training, new environment interactions, changes to experiment-owned T1594 files, original theory/PDF edits, or claims of a performance repair.
- Dependencies: Read-only T1592/T1593 artifacts, DERIVATION_PACKAGE.md, existing first-hit theory; external T1594 worker currently receives model-capacity errors.
- Expected Deliverables: Chinese derivation/review note; reproducible zero-interaction signal and sample-complexity audit; verification and guidance handoff.
- Definition of Done: Every numerical assertion reproduced; exact/conditional/empirical statements separated; concrete protocol blockers and continuation recorded; task verification passes.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `mentor_reviews/risk_formulation_20260916`, `experiments/safeot_dual/progress_feed.json` (publication-stage additive entry only; preserve owner and all prior entries).
- Files likely to touch: DERIVATION_REVIEW.md, audit_existing.py, verify.py, generated CSV/JSON and HANDOFF.md in the isolated review directory.
- Files explicitly out of scope: diagnostic_runs/, doc/, experiments/ except the one additive feed entry, final_presetation/, DERIVATION_PACKAGE.md. Review files moved from doc/ because SAFEOT-104 owns that broad directory. The user-authorized dashboard source append requires a narrow scope exception to broad experiments/ claims; no producer code or existing entry is modified.

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Recover T1593 result and T1594 execution state; correct unsafe protocol assumptions via the authorized conversation API.
- [x] Stage 2: Write and verify a zero-interaction risk-signal audit and derivation note.
- [ ] Stage 3: Complete guidance handoff, task review, and persistent dashboard evidence publication with limitations and next steps.

## Stage Log
- 2026-09-17 00:04:35 Prepared additive persistent dashboard entry and isolated data worktree; preserved owner and every prior source/remote entry. Verification passed; task ready for review before publication.
- 2026-09-17 00:02:13 Mentor zero-interaction review: 53/1500 first-hit channel-batch advantages zero, 1447 nonzero; frozen 48-candidate union-risk-change MAE .040671 sample versus .379501 det. Corrected CP budget/selection semantics; no new training, no experiment-owned edits.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- 2026-09-16: T1594 guidance delivered as guidance-20260916-risk-audit-correction-1594-02; external platform twice reports selected model at capacity. No T1594 analysis process or training exists. Root writes separate mentor analysis only.

## Verification

- Commands to run:
  - `python3 mentor_reviews/risk_formulation_20260916/audit_existing.py`
  - `python3 mentor_reviews/risk_formulation_20260916/verify.py`
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Completed mentor risk formulation review and zero-interaction audit; 217 input hashes verified, deployment-kernel gap quantified; dashboard evidence prepared for post-review publication.
- Tests: audit_existing.py; verify.py PASS; agentctl check --mode manual OK
- Completed-at: 2026-09-17 00:04:35
