# T-1588 - Full actor transactional candidate joint selection

Status: review
Owner: fulljoint
Agent: fulljoint
Created: 2026-09-16 14:05:59
Updated: 2026-09-16 14:05:59

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Test full-network finite-candidate deployment-aligned selection with matched none/KL/W2 arms and resource-matched PPOLag/Fisher.
- Non-Goals: No global trainer, prior result, DERIVATION or PDF edits; no SOTA claim or automatic failed-arm expansion.
- Dependencies: Read-only T1587 snapshot/checkpoints and original PPOLag/Fisher implementations.
- Expected Deliverables: Frozen protocol/snapshot, algebra/transaction gate, bounded 36-case prior-grid audit, 10 smoke and 30 development receipts, audited results and additive dashboard export.
- Definition of Done: Verify actual full-network updates, step accounting, optimizer transactions and raw eval; apply prospective promotion criteria and preserve negative results.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/full_actor_joint/v1`
- Files likely to touch: independent v1 scripts, protocol, checkpoints, reports and publish export.
- Files explicitly out of scope: old diagnostic directories, global trainers, DERIVATION_PACKAGE.md, paper/PDF.

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Freeze full-actor protocol; pass parameter/optimizer/regularizer gates.
- [x] Stage 2: Complete 36 offline cases/396 eval episodes, 10 smoke and 30 development jobs.
- [x] Stage 3: Audit 450 transactions, synthesize seed-level results and stop expansion under failed prospective criteria.
- [ ] Stage 4: Publish additive dashboard evidence.

## Stage Log
- 2026-09-16 14:21:50 30 development and 10 smoke verified; 450 full actor/Adam transactions passed; all promotion gates fail, HOLD. Offline 36 paired cases complete. Preparing additive dashboard export.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- 2026-09-16: Original smoke new arms failed JSON numpy scalar serialization; preserved. Attempt2 changes only float serialization and reuses 4 verified baseline smoke jobs. Controller PID 2533567 finished exit0; 40 receipts verified.
- 2026-09-16: 450 full actor transactions and Gaussian regularizer recomputations passed. 30 development jobs/360000 training interactions/9360 final eval episodes. HOLD_NO_EXPANSION: no stable OT increment and none of new arms meets Fisher joint/risk gate.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Full-network prototype completed: 10 smoke, 30 development, 450 transaction audits and 36 bounded old-grid cases; prospective criteria fail, no expansion. Additive dashboard export prepared.
- Tests: gate.py PASS; analyze.py PASS; supplement.py PASS; agentctl check --mode manual PASS
- Completed-at: 2026-09-16 14:22:45
