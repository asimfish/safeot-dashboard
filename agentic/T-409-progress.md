# T-409 - 更新PsiBot相对接口采集启动状态

Status: done
Owner: codex-psibot-relative-status
Agent: codex-psibot-relative-status
Created: 2026-09-13 17:03:57
Updated: 2026-09-13 17:03:57

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: 最小更新相对接口执行检查通过和三组启动中状态。
- Non-Goals: 不改已完成结果、分数、费用和视频；不提前声称实际模型请求。
- Dependencies: root独立T405执行检查确认，等待实际请求回执。
- Expected Deliverables: HTML两处运行状态替换。
- Definition of Done: root审核实际状态后发布，旧结果不变。

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/, /home/liyufeng/ops/reports/astra_relative_status_20260913/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: root核执行检查通过，实际准入等待4090，未调用模型。
- [x] Stage 2: 四处文案精确diff检查，无数字媒体改动。
- [ ] Stage 3: root gate发布。

## Stage Log

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- No updates yet.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: 准确标记执行检查通过/等待4090未调用模型，修正两条过时路线图摘要
- Tests: COPY_CHECK仅四处精确替换，数字媒体不变
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-13 17:06:39
- Completed-at-ns: 1789290399721871447
