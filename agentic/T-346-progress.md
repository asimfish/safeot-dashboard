# T-346 - 重整机器人面板信息架构与中文输入解释

Status: review
Owner: codex-astra-panel-ia
Agent: codex-astra-panel-ia
Created: 2026-09-12 14:47:37
Updated: 2026-09-12 14:47:37

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Platform-first four-part navigation, Chinese information descriptions, illustrative example and one selectable original-video player.
- Non-Goals: No experiment reruns or pooled platform scores; preserve original history.
- Dependencies: TWO_SEED_RESULTS and PsiBot identity audit, original media.
- Expected Deliverables: Three platform cards, five Chinese descriptions, example, seven-row table with one player, collapsed archives.
- Definition of Done: Layout/14 player selections/source hashes pass; independent review and publication.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/, /home/liyufeng/ops/reports/astra_panel_ia_20260912/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: Audit platform attribution and two-seed outcomes.
- [x] Stage 2: Rebuild main information architecture.
- [x] Stage 3: Verify layout, keyboard, 14 selections and source preservation.

## Stage Log

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- No updates yet.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Readable three-platform dashboard and Chinese input explanations, two-seed seven-condition table, one video selector, PsiBot historical success link, collapsed archives. Fixed old/new result ID collision.
- Tests: BROWSER_CHECK three widths/all14 playback/archive keyboard PASS; FINAL_STRUCTURE_CHECK unique IDs/all links/preserved media PASS; NEW_SOURCE_CHECK original hashes PASS; git diff --check PASS
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-12 14:55:27
- Completed-at-ns: 1789196127718169260
