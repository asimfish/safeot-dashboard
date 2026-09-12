# T-356 - 增加逐决策四视图与模型可见状态查看器

Status: done
Owner: codex-astra-step-viewer
Agent: codex-astra-step-viewer
Created: 2026-09-12 17:40:08
Updated: 2026-09-12 17:40:08

## Format Rules

- Keep this task doc factual and current; do not paste long reasoning transcripts.
- Preserve all top-level headings. Add subsections only under the existing headings.
- Update `Status:` through the workflow commands when possible.
- Use stable paths relative to the repo root.
- If a human edits this file, agents must re-read it and run `python3 tools/agentctl.py refresh` before continuing.

## Task Contract

- Goal: 展示逐轮实际四图、模型可见状态、动作及独立执行反馈。
- Non-Goals: 不重跑实验、不改变结果、不用视频帧冒充模型输入。
- Dependencies: T357 public 证据包。
- Expected Deliverables: 通用逐轮查看器、26 集选择联动、验证回执。
- Definition of Done: 中文状态边界准确，选择切换无陈旧数据，移动端四图可读，首载零视频请求，root 审核后发布。

## Context To Read Before Starting

- `AGENTS.md`
- `.agent/PROJECT_PLAN.md`
- `.agent/TASKS.md`
- `.agent/rules/agent-operating-rules.md`
- `.agent/rules/github-standards.md`

## Work Scope

- Allowed write scope: `/home/liyufeng/ops/reports/astra_panel_readability_20260910/repo/, /home/liyufeng/ops/reports/astra_step_viewer_20260912/, github:asimfish/safeot-dashboard/agentic_robotics.html, github:asimfish/safeot-dashboard/agentic/`
- Files likely to touch:
- Files explicitly out of scope:

## Stage Plan

Use one checkbox per stage. Do not delete completed stages; append changed or new stages with a short reason.

- [x] Stage 1: 集成证据与查看器。
- [x] Stage 2: 语义与浏览器验收。
- [ ] Stage 3: 审核发布。

## Stage Log
- 2026-09-12 18:00:26 按独立审阅修正 FR3 近景/全景/俯视/腕部命名；mask metadata 优先且仅无对应metadata的FR3兼容推断；未知费用明确显示未知与已知部分。

Format: `- YYYY-MM-DD HH:MM:SS <short factual update>`.


## Verification

- Commands to run:
  - `python3 tools/agentctl.py check --mode manual`
- Expected result:
  - Workflow checks pass and task-specific acceptance criteria are met.

## Completion Record
- Summary: 独立审阅修正已落：FR3四机位、完整metadata优先、费用未知明确标识
- Tests: 既有 BROWSER_CHECK/SOURCE_CHECK；最终 node --check 通过
- Worker-runtimes: host-runtime:a9eb20a03fb8e0048371e6124cab34a1
- Completed-at: 2026-09-12 18:00:45
- Completed-at-ns: 1789207245233869649
