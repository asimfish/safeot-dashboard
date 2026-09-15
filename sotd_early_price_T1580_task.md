# T-1580 - Early LP price causal intervention

Status: review
Owner: earlyprice
Agent: earlyprice
Created: 2026-09-15 21:20:30
Updated: 2026-09-15 21:20:30

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Isolate first-update path-LP price effect with matched-state interventions.
- Non-Goals: New safety theorem, radius/epoch search, PDF edits, historical gate changes.
- Dependencies: Frozen residual_feedback/v1 snapshot and LP reference logs.
- Expected Deliverables:3-arm development,conditional2seed paired check,preupdate states/batches,receipts,theory design and synthesis.
- Definition of Done: Reproduction and same-batch checks; exactstep/checkpoint/hash/exit verified; conditional route completed.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/early_price`
- Files likely to touch: Independent v1 failed infrastructure receipt;v2 snapshots,driver,controller,protocol,checkpoints,analysis and additive dashboard export.
- Files explicitly out of scope: Original results,global trainers,papers/PDF.

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Frozen protocol;v1 failed serialization retained;v2 baseline reproduced within1e-6.
- [x] Stage 2:3 development arms plus4 conditional newseed runs verified exit0;common preupdate loaded.
- [x] Stage 3: Local seed180 support;seed186 remains poor and187 no-op;theory-only neighborhood design and final synthesis.

## Stage Log
- 2026-09-15 21:25:51 7verified jobs:seed180 first y removal reward+.5631 joint1;conditional186 joint0→.03,187 no-op. Same-batch state/RNG checks and archived reproduction pass. Local mechanism only;no stablefix.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Early-price causal intervention completed with conditional seed186/187;local support but unstable learning;theory design retained
- Tests: analyze.py;baseline10epoch/final reproduction1e-6;7exit0 checkpoint/source/batch checks;manual workflow check
- Completed-at: 2026-09-15 21:25:51
