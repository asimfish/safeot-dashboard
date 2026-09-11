# T-344 - 补齐七组输入消融结果与四段原始视频

Status: review
Owner: codex-astra-seven-panel
Agent: codex-astra-seven-panel
Created: 2026-09-11 23:40:29
Updated: 2026-09-11 23:40:29

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Complete seven seed9403 input conditions with four new original videos and per-episode accounting.
- Non-Goals: No new experiments or stable-rate/ranking claims; no SafeDuo results pooled into mainline gesture/long-horizon.
- Dependencies: Four terminal summaries, evaluations and independent sync receipts in remaining_stage.
- Expected Deliverables: Seven-row table, seven videos, source manifest, truthful mainline progress.
- Definition of Done: Source hashes and browser checks pass; parent review/gate and live hash-verified publish.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/, /home/liyufeng/ops/reports/astra_seven_panel_20260912/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Independently verify four terminal results and original sources.
- [x] Stage 2: Complete seven-condition table, media and boundaries.
- [x] Stage 3: Verify browser layout/playback and prepare publication.

## Stage Log

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- No updates yet.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Completed seven seed9403 input results with four new original videos and per-episode tokens/cost/wall/Hz, preserving one-valid-episode boundary and no new controlled mainline gesture/long-horizon claims.
- Tests: BROWSER_CHECK three widths and all seven videos PASS; SOURCE_CHECK original media/JSON hashes and independent sync PASS; 71calls/$7.33388 accounting PASS; git diff --check PASS
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-11 23:43:02
- Completed-at-ns: 1789141382641969890
