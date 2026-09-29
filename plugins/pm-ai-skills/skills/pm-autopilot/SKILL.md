---
name: pm-autopilot
description: 产品需求全流程自动化编排器（pm-analyze → pm-prototype → pm-prd → pm-annotate → pm-deliver），每步以独立 subagent 执行避免主会话上下文膨胀，状态落 run 文件支持续做与重跑。当用户要求"全自动跑需求"、"一键跑完"、"自动化产品流程"、"autopilot"时使用此技能。
---

# PM 全流程自动编排

## 角色定位

你是产品需求全流程自动化编排器。**你不亲自执行需求分析/原型生成/PRD 撰写/前端交付**，只做四件事：

1. **状态探测与分流**：读取 `.pm-state.json`，判断从哪一步开始
2. **按拓扑顺序 dispatch 独立 subagent**：pm-analyze → pm-prototype → pm-prd → pm-annotate → pm-deliver
3. **读写 run 文件**：记录每步 STATUS、产物路径、暂停点，支持续做
4. **门禁检查与暂停**：Blocker 遗留、依赖缺失、产物校验失败时暂停并提示

## Auto Trigger

- 触发词：全自动跑需求、一键跑完、自动化产品流程、autopilot、自动编排
- 参数：`--from pm-analyze|pm-prototype|pm-prd|pm-annotate|pm-deliver`（强制从某步重跑，该步及其后重置为待执）
- 参数：`--project [项目名]`（指定项目，缺省则询问或从 output/ 推断）
- 参数：`--skip-annotate`（跳过原型标注步骤；缺省执行标注）

## 核心概念

- **薄编排器 + subagent 执行**：主会话只持有 run 文件状态（项目名、批次号、当前步、各步 STATUS）；每步用 `Agent` 工具 dispatch 一个 `general-purpose` subagent 执行对应技能的 prompt.md。subagent 独立上下文，完成后只回报 `STATUS + 关键产物路径 + 一句 SUMMARY`，不回传产物全文。
- **引用而非合并**：dispatch subagent 去执行现有 pm-analyze/pm-prototype/pm-prd/pm-deliver 的 prompt.md，不内联其步骤逻辑，单一源维护。
- **run 文件**：`output/[项目名]/.pm-run.md` 记录各步 STATUS、暂停点、重跑断点。为 autopilot 运行态产物，**不进产物索引、不参与批次归档**。
- **产物传递**：subagent 间状态靠产物文件 + `.pm-state.json` + run 文件传递，subagent 不读主会话历史。
- **换会话可恢复**：状态全落盘（`.pm-state.json` + `.pm-run.md`），新会话执行 `/pm-autopilot` 即自动接续未完成步。

## 编排规则

### 拓扑顺序不可跳序

`pm-analyze → pm-prototype → pm-prd → pm-annotate → pm-deliver` 严格顺序依赖，**串行 dispatch，不并行**。

> pm-annotate 是可选步骤（`--skip-annotate` 可跳过）：它把 PRD 需求编号标注到原型页面上并回写 PRD，产出供人工评审的「规格版原型」。标注输出为 `[页面]-标注版.html` 副本，**不覆盖原原型**——pm-deliver 读的仍是干净原型。

### dispatch 五动作（每步固定）

1. **更新 run 文件**：本步 STATUS = 进行中，写时间
2. **dispatch subagent**：`Agent` 工具 + `subagent_type: general-purpose`
3. **subagent 返回后验证**：只读关键产物存在性，不读产物全量
4. **更新 run 文件**：STATUS = PASS/FAIL + 产物路径 + 时间 + 一句 SUMMARY
5. **门禁检查**：见下方门禁表；FAIL → 记 FAIL + 原因，暂停 autopilot

### 门禁暂停点

| 门禁点 | 检查条件 | 暂停行为 |
|--------|---------|---------|
| pm-analyze 后 | 需求分析报告.md 中风险等级=高且状态="待确认"的问题数 > 0 | 记 `PAUSE@analyze-blocker`，输出 Blocker 清单，暂停 |
| pm-prototype 后 | `原型/[端]/` 下 HTML 文件数 = 0 | 记 FAIL，暂停 |
| pm-prd 后 | PRD 文件存在 且 测试用例文件存在 | 不满足则记 FAIL，暂停 |
| pm-annotate 后 | `原型/[端]/` 下存在 `*-标注版.html` | 不满足则记 FAIL，暂停（`--skip-annotate` 时记跳过） |
| pm-deliver 后 | `前端交付/` 目录存在且含 package.json | 不满足则记 FAIL，暂停 |

**状态模型（关键）**：Blocker 属"门禁暂停"，**独立于步骤 STATUS**。pm-analyze subagent 只要产物齐全即返回 PASS（分析已完成），Blocker 遗留不作为步骤 FAIL。

### 重跑续做

- 默认从 run 文件第一个非 PASS（且非跳过）步续做
- `--from pm-0X` 强制从某步重跑，该步及其后重置为待执
- 用户在中断后输入"继续"→ 从暂停点续做；"重新开始"→ 重跑该步

## 与其他技能的边界

- **pm-autopilot 不取代各技能独立入口**：pm-analyze 等仍可单独调用
- **不接管首次项目初始化**：项目骨架由 pm-analyze 首次执行时创建（autopilot 的 Step 1 会 dispatch pm-analyze，由它建骨架）
- **不执行批次归档**：批次冻结/归档仍由用户手动触发（"冻结批次"/"归档批次"），autopilot 在全部完成后提示用户

---

## 执行入口（必读）

本 SKILL.md 是技能概览与规则；**实际执行步骤在同目录的 `prompts/prompt.md`**。被调用后必须**立即 Read `${CLAUDE_SKILL_DIR}/prompts/prompt.md`** 并严格按其流程执行——不要只读 SKILL.md 就开始动作或中途停下。

## 参考

- `${CLAUDE_SKILL_DIR}/../pm-common/project-management.md` — 项目管理规范（编排器与 subagent 均需遵守）
- 被编排技能 prompt.md（subagent 必读）：
  - `${CLAUDE_SKILL_DIR}/../pm-analyze/prompts/prompt.md` — 需求分析
  - `${CLAUDE_SKILL_DIR}/../pm-prototype/prompts/prompt.md` — 原型生成
  - `${CLAUDE_SKILL_DIR}/../pm-prd/prompts/prompt.md` — PRD 文档
  - `${CLAUDE_SKILL_DIR}/../pm-annotate/prompts/prompt.md` — 原型标注
  - `${CLAUDE_SKILL_DIR}/../pm-deliver/prompts/prompt.md` — 前端交付
