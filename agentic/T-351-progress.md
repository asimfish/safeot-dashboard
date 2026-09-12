# T-351 - 明确逐轮下载链接是原始JSON

Status: review
Owner: codex-astra-json-label
Agent: codex-astra-json-label
Created: 2026-09-12 15:11:54
Updated: 2026-09-12 15:11:54

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: Explicitly label 14 transcript download links as original JSON.
- Non-Goals: No viewer or data changes.
- Dependencies: Published T348 and explicit parent wording request.
- Expected Deliverables: Fourteen Chinese link labels.
- Definition of Done: Exact label-only diff; publish after parent gate.

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/agentic_robotics.html, /home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/agentic/T-351-progress.md, /home/liyufeng/ops/reports/astra_report_format_20260912/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [ ] Stage 1:
- [ ] Stage 2:
- [ ] Stage 3:

## Stage Log

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- No updates yet.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: Changed 14 transcript links to explicitly say original input/action JSON; no viewer or data changes.
- Tests: Exact 14 label replacements; underlying URLs and data unchanged
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-12 15:12:28
- Completed-at-ns: 1789197148915418753
