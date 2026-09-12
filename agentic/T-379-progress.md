# T-379 - 补充输入定义与逐条失败判据注解

Status: done
Owner: codex-astra-failure-notes
Agent: codex-astra-failure-notes
Created: 2026-09-13 01:51:38
Updated: 2026-09-13 01:51:38

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: 展开说明解释末端/基座、相机内外参及跟踪误差；播放器呈现逐条失败判据。
- Non-Goals: 不修改影片、分数或实验运行态，不推断真实损坏或未证实因果。
- Dependencies: 原evaluation/evaluator_trace/synchronized_samples与实际candidate。
- Expected Deliverables: 白名单失败注解JSON、播放器联动、现有输入详情解释。
- Definition of Done: 五条终止证据逐源核验、文字无因果越界、选择切换正确、root审核发布。

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/, /home/liyufeng/ops/reports/astra_failure_notes_20260913/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: 原评估/120Hz trace/15fps时间逐源读取。
- [x] Stage 2: 五条注解与中文定义、390浏览器联动验收。
- [ ] Stage 3: root gate与发布。

## Stage Log

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.

- No updates yet.

## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: 补末端/基座、内外参、跟踪误差中文解释及五条停止判据/录像时差注解
- Tests: SOURCE_CHECK原eval/trace/sync；BROWSER_CHECK五条切换/成功隐藏/390无溢出/零视频自动加载；node --check
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-13 01:54:45
- Completed-at-ns: 1789235685871759613
