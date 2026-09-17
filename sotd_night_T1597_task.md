# T-1597 - Publish verified night campaign evidence and persistent feed

Status: review
Owner: campaign-publish
Agent: campaign-publish
Created: 2026-09-17 09:01:35
Updated: 2026-09-17 09:01:35

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Publish verified A/C, T1595, T1596 results and honest receipt-time ledger on the actual homepage feed.
- Non-Goals: No training, no changes to old results, PDF, DERIVATION, status or gap_plan.
- Dependencies: completed experiment receipts, dashboard data branch, persistent feed producer.
- Expected Deliverables: immutable report/CSV evidence commit, source-backed feed commit and HTTP receipt.
- Definition of Done: task review before push; new entry in remote first14; report hash match; old owner/entries preserved.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `diagnostic_runs/eight_hour_20260917/publication` and `experiments/safeot_dual/progress_feed.json` (incremental, preserve prior entries/owner)
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Snapshot latest feed and prepare evidence.
- [x] Stage 2: Validate report/feed and finish review before pushing.
- [ ] Stage 3: Push and HTTP verify immutable report and homepage feed.

## Stage Log
- 2026-09-17 09:03:35 T1597 publication prepared from latest data1751f38: evidence report/CSVs and persistent source feed entry, all prior source/remote entries and owner preserved. Corrected report distinguishes 42 development vs54 receipt-covered jobs and .8713h union vs2.8550 worker-hours; no training.

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Night campaign evidence and source-backed feed prepared and locally verified; prior owner and all entries preserved, no new training. Ready for scoped publication; HTTP receipt to follow normal push.
- Tests: python3 diagnostic_runs/eight_hour_20260917/publication/prepare.py; python3 tools/agentctl.py check --mode manual
- Completed-at: 2026-09-17 09:03:58
