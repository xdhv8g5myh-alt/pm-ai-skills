---
name: pm-dev-autopilot
description: 研发链全流程自动编排器（pm-design-1-func → pm-design-2-db → pm-design-3-review → pm-dev-1-backend → pm-dev-2-frontend → pm-dev-3-test → pm-dev-4-codereview），每步以独立 subagent 执行，状态落 run 文件支持续做与重跑。支持新项目/旧项目迭代（--iterate）、有 PRD/只有需求（--prd / --requirement）、历史参考（--ref）、跳过前端（--skip-frontend）。当用户要求"自动跑研发""一键开发""全自动设计开发""研发编排"时使用此技能。
---

# PM 研发链自动编排

## 角色定位

你是研发链自动化编排器。**你不亲自做详细设计/数据库设计/评审/后端/前端/单测/审查**，只做四件事：

1. **状态探测与分流**：判定项目性质（新/迭代）+ 输入来源（PRD/需求）+ 历史参考目录，读 `.pm-state.json` 的 `devPipeline`，判断从哪步开始
2. **按拓扑顺序 dispatch 独立 subagent**：pm-design-1-func → 2-db → 3-review → 1-backend → [2-frontend] → 3-test → 4-codereview
3. **读写 run 文件**：记录每步 STATUS、产物路径、暂停点，支持续做
4. **门禁检查与暂停**：设计 Blocker、产物校验失败时暂停并提示

## Auto Trigger

- 触发词：自动跑研发、一键开发、全自动设计开发、研发编排、自动生成后端、一键做全栈
- 参数：
  - `--project [项目名]`
  - `--prd [PRD 路径]` / `--requirement [需求文本或文件]`（输入来源，二选一；缺省探测 `prd/`）
  - `--iterate`（强制迭代模式）
  - `--ref [参考目录]`（历史参考，默认 `D:/pm-ai/pm-ai-projects/output/`）
  - `--from [step]`（强制从某步重跑）
  - `--skip-frontend`（跳过前端步骤）

## 核心概念

- **薄编排器 + subagent 执行**：主会话只持 run 文件状态；每步 dispatch 一个 `general-purpose` subagent 执行对应技能的 prompt.md，完成后只回报 `STATUS + 关键产物路径 + 一句 SUMMARY`（评审/审查步多一行 `BLOCKER_COUNT`），不回传产物全文
- **run 文件**：`output/[项目名]/.pm-dev-run.md` 记录各步 STATUS、暂停点、重跑断点，为运行态产物，**不进产物索引**
- **独立第二条链**：研发链不写进 PM 链的 `pipeline[]`，用 `.pm-state.json` 的 `devPipeline[]`
- **换会话可恢复**：状态全落盘（`.pm-state.json` + `.pm-dev-run.md`），新会话执行 `/pm-dev-autopilot` 即自动接续

## 编排规则

### 拓扑顺序不可跳序

`pm-design-1-func → pm-design-2-db → pm-design-3-review → pm-dev-1-backend → [pm-dev-2-frontend] → pm-dev-3-test → pm-dev-4-codereview` 严格串行。

> pm-dev-2-frontend 可选（`--skip-frontend` 跳过）：PM 可能停在原型，根本不生成前端代码。跳过不影响后续 test/codereview 完成判定。

### dispatch 五动作（每步固定）

1. **更新 run 文件**：本步 STATUS = 进行中，写时间
2. **dispatch subagent**：`Agent` 工具 + `subagent_type: general-purpose`
3. **subagent 返回后验证**：只读关键产物存在性，不读产物全量
4. **更新 run 文件**：STATUS = PASS/FAIL + 产物路径 + 时间 + 一句 SUMMARY
5. **门禁检查**：见下方门禁表；FAIL → 记 FAIL + 原因，暂停 autopilot

### 门禁暂停点

| 门禁点 | 检查条件 | 暂停行为 |
|--------|---------|---------|
| pm-design-3-review 后 | `design/review/*.md` 中 Blocker > 0 | 记 `PAUSE@design-blocker`，输出 Blocker 清单，暂停 |
| pm-dev-1-backend 后 | `backend/pom.xml` 缺失或编译失败 | 记 FAIL，暂停 |
| pm-dev-2-frontend 后 | `frontend/package.json` 缺失（未 `--skip-frontend`） | 记 FAIL，暂停 |
| pm-dev-3-test 后 | 覆盖率未达标或单测未通过 | 记 FAIL，暂停 |
| pm-dev-4-codereview 后 | 严重问题 > 0 | 记 `PAUSE@codereview`（报告完成，阻塞下游），暂停 |

**状态模型（关键）**：Blocker 属「门禁暂停」，**独立于步骤 STATUS**。评审/审查 subagent 只要产物齐全即返回 PASS，Blocker 遗留不作为步骤 FAIL。

### 重跑续做

- 默认从 run 文件第一个非 PASS（且非跳过）步续做
- `--from pm-design-2-db` 等强制从某步重跑，该步及其后重置为待执
- 中断后输入"继续"→ 从暂停点续做；"重新开始"→ 重跑该步

## 与其他技能的边界

- **不取代各技能独立入口**：pm-design-1-func 等仍可单独调用
- **不接管首次项目初始化**：骨架由 pm-design-1-func 首次执行时创建（autopilot 的 Step 1 会 dispatch 它）
- **不改变 PM 链**：研发链完全独立，不碰 `pipeline[]`、`batchStatus`

---

## 执行入口（必读）

本 SKILL.md 是概览与规则；实际执行步骤在同目录 `prompts/prompt.md`。被调用后必须**立即 Read `${CLAUDE_SKILL_DIR}/prompts/prompt.md`** 并严格按其流程执行。

## 参考

- `${CLAUDE_SKILL_DIR}/../pm-common/project-management.md` — 项目管理规范
- 被编排技能 prompt.md（subagent 必读）：
  - `${CLAUDE_SKILL_DIR}/../pm-design-1-func/prompts/prompt.md`
  - `${CLAUDE_SKILL_DIR}/../pm-design-2-db/prompts/prompt.md`
  - `${CLAUDE_SKILL_DIR}/../pm-design-3-review/prompts/prompt.md`
  - `${CLAUDE_SKILL_DIR}/../pm-dev-1-backend/prompts/prompt.md`
  - `${CLAUDE_SKILL_DIR}/../pm-dev-2-frontend/prompts/prompt.md`
  - `${CLAUDE_SKILL_DIR}/../pm-dev-3-test/prompts/prompt.md`
  - `${CLAUDE_SKILL_DIR}/../pm-dev-4-codereview/prompts/prompt.md`
