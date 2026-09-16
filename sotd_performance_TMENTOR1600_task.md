# T-MENTOR-1600 - Diagnose remaining performance gap after candidate span and sampling allocation

Status: review
Owner: performance-mentor
Agent: performance-mentor
Created: 2026-09-17 02:19:20
Updated: 2026-09-17 02:19:20

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Independently audit the completed A/C pilots, identify concrete installation/objective gaps, and dispatch a preregistered fix without interrupting the active eight-hour supervisor.
- Non-Goals: No edits to producer experiment code, no new performance claims, no change to fixed rewards/budgets or the independent checker.
- Dependencies: T1593 frozen controls, T1595 closed-loop adapter, T-NIGHT-002 supervision.
- Expected Deliverables: Reproducible zero-environment-step audit, source hashes, bounded follow-up protocol and delivery receipt.
- Definition of Done: Audit reproduces from original artifacts, concrete guidance is delivered or safely integrated into the running queue, and evidence is handed to the eight-hour loop.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `mentor_reviews/performance_gap_20260917`, plus additive-only `experiments/safeot_dual/progress_feed.json` for the user-authorized dashboard update. Preserve the feed owner and every prior entry; do not edit producer experiment code or data. This is the same narrow publication exception used by T-NIGHT-002.
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Restore executor progress and independently recompute completed pilots.
- [x] Stage 2: Quantify actual accepted updates, deployment risks, and matching/control issues.
- [x] Stage 3: Freeze and deliver bounded improvement protocol and record verification.

## Stage Log
- 2026-09-17 02:25:11 Independent audit: 420 surrogate-feasible candidates, 320 deterministic screen mean failures; 56/61 installed PPO updates bypass .01 KL radius; 14 unsafe final actors exactly match four-episode zero-event acceptance. Frozen common-eligibility test prepared.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 mentor_reviews/performance_gap_20260917/audit.py`
  - `python3 -m py_compile mentor_reviews/performance_gap_20260917/audit.py`
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Audited 18 completed pilots and 420 cycles, isolated deployment-surrogate and unrestricted-PPO update gaps, froze bounded integration and common-KL ablation, delivered acknowledged guidance, prepared additive dashboard evidence
- Tests: Read-only audit: 120 stable input hashes; 18 exact actor checks; six allocation ledgers; py_compile; agentctl check manual OK; external acknowledgement14088207
- Completed-at: 2026-09-17 02:30:29
