# PM Autopilot 执行步骤

> 本文件为编排执行步骤；概览与规则见同目录 `../SKILL.md`。被调用后按本文件流程严格执行。

## 前置约定

- 路径变量：`output/[项目名]/` 为项目根，所有产物按 `pm-common/project-management.md` 目录骨架存放
- **output 根**：以当前 cwd 为产物根；`output/` 目录不存在则自动创建；所有 `output/...` 路径拼成绝对路径后使用（`[cwd]/output/[项目名]/...`）
- run 文件：`output/[项目名]/.pm-run.md`（autopilot 运行态，不进产物索引）
- 被编排技能 prompt.md（subagent 必读）：
  - pm-analyze：`${CLAUDE_SKILL_DIR}/../pm-analyze/prompts/prompt.md`
  - pm-prototype：`${CLAUDE_SKILL_DIR}/../pm-prototype/prompts/prompt.md`
  - pm-prd：`${CLAUDE_SKILL_DIR}/../pm-prd/prompts/prompt.md`
  - pm-annotate：`${CLAUDE_SKILL_DIR}/../pm-annotate/prompts/prompt.md`
  - pm-deliver：`${CLAUDE_SKILL_DIR}/../pm-deliver/prompts/prompt.md`

---

## Step 0：状态探测与分流

> 主会话轻量执行，不 dispatch subagent。

### 0.1 确定项目名

- 用户传入 `--project [项目名]` → 直接使用
- 未传入 → 检查 `output/` 下有哪些项目目录
  - 只有 1 个 → 自动选择
  - 多个 → 列出让用户选择
  - 没有 → 询问项目名（将由 pm-analyze 创建骨架）

### 0.2 读取项目状态

1. 检查 `output/[项目名]/.pm-state.json` 是否存在
   - **不存在**（全新项目）：将从 Step 1（pm-analyze）开始，pm-analyze 会自动创建项目骨架
   - **已存在**：Read 获取 pipeline 各步状态

2. 检查 `output/[项目名]/.pm-run.md` 是否存在
   - **不存在** → 根据 `.pm-state.json` 的 pipeline 状态预标各步：
     - pm-analyze status=completed → 标 PASS
     - pm-prototype status=completed → 标 PASS
     - pm-prd status=completed → 标 PASS
     - pm-annotate status=completed → 标 PASS（`--skip-annotate` 时标跳过）
       - **兜底**：若 `pipeline` 中**无 pm-annotate 条目**，则以 `原型/[端]/*-标注版.html` 是否存在来判定 Step 4 的 PASS / 待执
     - pm-deliver status=completed → 标 PASS
   - **已存在** → 读取各步 STATUS

3. 如果用户传入 `--from pm-[技能名]`：将该步及其后重置为"待执"
4. 如果用户传入 `--skip-annotate`：Step 4 直接标"跳过"，不 dispatch

### 0.3 分流

- 定位第一个非 PASS（且非跳过）步作为起点
- 全部 PASS → 提示用户："所有步骤已完成。是否需要从某步重跑？"
- 有暂停标记（`PAUSE@*`）→ 检查暂停条件是否已解除：
  - `PAUSE@analyze-blocker`：re-check 需求分析报告.md 中 Blocker 遗留
    - 遗留 = 0 → 解除暂停，从下一步继续
    - 遗留 > 0 → 再次暂停，输出未解决 Blocker 清单

> **本编排器只处理 PM 链标记**（`PAUSE@analyze-blocker`）。`PAUSE@design-blocker` / `PAUSE@codereview`
> 属研发链，由 `pm-dev-autopilot` 写入 `.pm-dev-run.md` 并自行处理，**与本链互不干扰**
> （见 `pm-common/project-management.md` §十）。

### 0.4 创建/更新 run 文件

创建或更新 `output/[项目名]/.pm-run.md`，格式：

```markdown
# PM Autopilot 运行状态

> 项目：[项目名] | 批次：[批次号] | 启动时间：[时间]

## 运行状态：进行中

## 各步进度

| 步骤 | 技能 | STATUS | 开始时间 | 完成时间 | 产物路径 | 备注 |
|------|------|--------|---------|---------|---------|------|
| Step 1 | pm-analyze | 待执/进行中/PASS/FAIL | — | — | — | — |
| Step 2 | pm-prototype | 待执 | — | — | — | — |
| Step 3 | pm-prd | 待执 | — | — | — | — |
| Step 4 | pm-annotate | 待执 | — | — | — | — |
| Step 5 | pm-deliver | 待执 | — | — | — | — |

## 暂停记录

（无）
```

---

## Step 1：dispatch pm-analyze 需求分析

### 1.1 更新 run 文件

Step 1 STATUS = 进行中，写启动时间。

### 1.2 dispatch subagent

使用 `Agent` 工具，`subagent_type: "general-purpose"`，prompt 如下：

```
你是 pm-analyze 技能执行者（需求分析）。项目名：[项目名]，工作空间根：[workspace_root]。

**立即 Read** `[pm-analyze prompt.md 的绝对路径]` 并严格按其流程执行（步骤 0 → 步骤 1 → ... → 步骤 7），不得跳步。

执行前先 Read `[pm-common/project-management.md 的绝对路径]` 了解项目管理规范。

用户的原始需求描述：
[插入用户提供的需求描述或文件路径]

完成后只回报（不回传产物全文）：
STATUS(PASS|FAIL)
OUTPUT(关键产物路径列表)
SUMMARY(一句话)
BLOCKER_COUNT(待确认 Blocker 数)
```

### 1.3 subagent 返回后验证

只检查关键产物存在性（不读全量）：
- `output/[项目名]/需求分析/需求分析报告.md` **或** `output/[项目名]/需求分析/轻量分析-*.md` 存在？（**二者有其一即 PASS**；轻量模式产出后者）
- `output/[项目名]/.pm-state.json` 已更新？
- `output/[项目名]/README.md` 已更新？

### 1.4 更新 run 文件

- 产物存在 → STATUS = PASS + 产物路径 + SUMMARY
- 产物缺失 → STATUS = FAIL + 原因

### 1.5 门禁检查（Blocker）

Read `output/[项目名]/需求分析/需求分析报告.md` 第 7 章，统计风险等级=高且状态="待确认"的问题数：

> **轻量模式补充**：若本次为轻量模式（报告无第 7 章，产物为 `需求分析/轻量分析-*.md`），
> Blocker 数取轻量报告中 **风险等级=高 且 状态="待确认"** 的条数；
> 若轻量报告无「状态」列，则按 **风险等级=高** 的条数计。

- **Blocker > 0**：
  - run 文件：Step 1 STATUS = PASS（产物完成），**同时**记 `PAUSE@analyze-blocker`
  - 向用户输出 Blocker 清单：
    ```
    ⚠️ 需求分析已完成，但存在 [N] 个 Blocker 级问题未解决：
    1. [问题描述] — 风险：[影响]
    2. ...

    请解决以上问题后，重新执行 /pm-autopilot 续做。
    如确认可带问题推进，请回复"继续"。
    ```
  - 用户回复"继续" → 解除暂停，进入 Step 2；同时在 run 文件**该步备注**写
    `analyze-blocker 已确认放行（用户 [时间]）`（步骤 0.3 与 Step 2.0 见到该备注则不再重复暂停）
  - 否则 → 暂停 autopilot，**退出**
- **Blocker = 0** → 进入 Step 2

---

## Step 2：dispatch pm-prototype 原型生成

### 2.0 Blocker re-check（仅 PAUSE@analyze-blocker 续做时）

如果本批次曾因 `PAUSE@analyze-blocker` 暂停，dispatch 前再次检查：
- Read 需求分析报告.md 第 7 章，确认"待确认" Blocker = 0
- 仍 > 0 → 再次暂停，不 dispatch pm-prototype

### 2.1 更新 run 文件

Step 2 STATUS = 进行中。

### 2.2 dispatch subagent

```
你是 pm-prototype 技能执行者（原型生成）。项目名：[项目名]，工作空间根：[workspace_root]。

**立即 Read** `[pm-prototype prompt.md 的绝对路径]` 并严格按其流程执行，不得跳步。

执行前先 Read `[pm-common/project-management.md 的绝对路径]` 了解项目管理规范。

上游产物路径：
- 分析报告：output/[项目名]/需求分析/需求分析报告.md
- 项目规范：output/[项目名]/项目规范.md

完成后只回报：
STATUS(PASS|FAIL)
OUTPUT(关键产物路径列表)
SUMMARY(一句话)
```

### 2.3 返回后验证

- `output/[项目名]/原型/[端]/` 下**有 ≥1 个 `.html` 文件即 PASS**
- `index.html` 导航页**不再是硬性通过条件**：缺 `index.html`（单页模式）**只记提示，不阻断**

### 2.4 更新 run 文件 + 门禁检查

- 该端目录下 `.html` 文件数 ≥1 → PASS，进入 Step 3
- 无 `.html` 文件 → FAIL，暂停

---

## Step 3：dispatch pm-prd 文档生成

### 3.1 更新 run 文件

Step 3 STATUS = 进行中。

### 3.2 dispatch subagent

```
你是 pm-prd 技能执行者（PRD 文档生成）。项目名：[项目名]，工作空间根：[workspace_root]。

**立即 Read** `[pm-prd prompt.md 的绝对路径]` 并严格按其流程执行，不得跳步。

执行前先 Read `[pm-common/project-management.md 的绝对路径]` 了解项目管理规范。

上游产物路径：
- 分析报告：output/[项目名]/需求分析/需求分析报告.md
- 原型目录：output/[项目名]/原型/
- 项目规范：output/[项目名]/项目规范.md

完成后只回报：
STATUS(PASS|FAIL)
OUTPUT(关键产物路径列表)
SUMMARY(一句话)
```

### 3.3 返回后验证

- `output/[项目名]/需求文档/[项目名]-PRD-*.md` 存在？
- `output/[项目名]/需求文档/[项目名]-测试用例.md` 存在？
- `output/[项目名]/需求文档/[项目名]-工时估算.md` 存在？

### 3.4 更新 run 文件 + 门禁检查

- 三个文件均存在 → PASS，进入 Step 4
- 缺失 → FAIL，暂停

---

## Step 4：dispatch pm-annotate 原型标注

> 可选步骤。用户传 `--skip-annotate` → 本步标"跳过"，直接进入 Step 5。

### 4.0 更新 run 文件

Step 4 STATUS = 进行中。

### 4.1 dispatch subagent

```
你是 pm-annotate 技能执行者（原型标注）。项目名：[项目名]，工作空间根：[workspace_root]。

**立即 Read** `[pm-annotate prompt.md 的绝对路径]` 并严格按其流程执行，走 Workflow A（初始化标注），不得跳步。

执行前先 Read `[pm-common/project-management.md 的绝对路径]` 了解项目管理规范。

上游产物路径：
- PRD：output/[项目名]/需求文档/
- 原型目录：output/[项目名]/原型/
- 项目规范：output/[项目名]/项目规范.md

**编排层约定（必须遵守）**：
- 标注结果输出为 `output/[项目名]/原型/[端]/[页面名]-标注版.html` **副本**，
  **禁止覆盖原原型 HTML**——pm-deliver 仍需读取干净原型。
- 编号需回写到 PRD 对应需求描述开头。

完成后只回报：
STATUS(PASS|FAIL)
OUTPUT(关键产物路径列表)
SUMMARY(一句话)
```

### 4.2 返回后验证

- `output/[项目名]/原型/[端]/` 下存在 `*-标注版.html`？
- 原原型 HTML 文件未被覆盖（文件列表与 Step 2 一致）？

### 4.3 更新 run 文件 + 门禁检查

- 存在标注版副本且原原型未被覆盖 → PASS，进入 Step 5
- 不满足 → FAIL，暂停

---

## Step 5：dispatch pm-deliver 前端交付

### 5.1 更新 run 文件

Step 5 STATUS = 进行中。

### 5.2 dispatch subagent

```
你是 pm-deliver 技能执行者（前端交付）。项目名：[项目名]，工作空间根：[workspace_root]。

**立即 Read** `[pm-deliver prompt.md 的绝对路径]` 并严格按其流程执行，不得跳步。

执行前先 Read `[pm-common/project-management.md 的绝对路径]` 了解项目管理规范。

上游产物路径：
- 原型目录：output/[项目名]/原型/（读取原原型，**忽略 -标注版.html 副本**）
- PRD：output/[项目名]/需求文档/
- 项目规范：output/[项目名]/项目规范.md

完成后只回报：
STATUS(PASS|FAIL)
OUTPUT(关键产物路径列表)
SUMMARY(一句话)
```

### 5.3 返回后验证

- `output/[项目名]/前端交付/package.json` 存在？
- `output/[项目名]/前端交付/src/` 目录存在？

### 5.4 更新 run 文件

- 验证通过 → PASS
- 不通过 → FAIL，暂停

---

## Step 6：完成与提示

当 Step 1-5 全部 PASS（Step 4 跳过视为通过）：

1. 更新 run 文件：运行状态 = 已完成
2. 更新 `.pm-state.json`：`batchStatus` = `completed`
3. 向用户输出完成报告：

```
✅ 项目"[项目名]"批次 B[N] 全流程已完成！

📊 执行摘要：
- pm-analyze：[SUMMARY]
- pm-prototype：[SUMMARY]
- pm-prd：[SUMMARY]
- pm-annotate：[SUMMARY]（或"已跳过"）
- pm-deliver：[SUMMARY]

📁 产物索引：output/[项目名]/README.md
📌 规格版原型（带需求编号标注）：output/[项目名]/原型/[端]/*-标注版.html

🔒 如需冻结此批次（禁止修改），输入"冻结批次"
🆕 如需开始新的迭代，输入"新批次"
```

---

## 重跑续做逻辑

- autopilot 被调用 → Step 0 读 `.pm-state.json` + `.pm-run.md` → 定位第一个非 PASS 步 → 从该步 dispatch 续做
- run 文件各步 STATUS 是续做的唯一依据
- subagent 间状态靠产物文件 + `.pm-state.json` 传递，subagent 不读主会话历史
- 用户可传 `--from pm-[技能名]`（技能名 ∈ pm-analyze / pm-prototype / pm-prd / pm-annotate / pm-deliver）强制从某步重跑
- 用户可传 `--skip-annotate` 跳过 Step 4 原型标注（该步记"跳过"，不影响后续步骤与完成判定）
- **换会话可恢复**：状态全落盘，新会话执行 `/pm-autopilot` 即自动接续

## subagent dispatch 通用模板

```
你是 [技能名] 技能执行者（[中文名]）。项目名：{项目名}，工作空间根：{workspace_root}。

**立即 Read** `{被执行技能 prompt.md 绝对路径}` 并严格按其流程执行（从步骤 0 开始到最后一步），不得跳步。

执行前先 Read `{pm-common/project-management.md 绝对路径}` 了解项目管理规范。

上游产物路径：
{上游产物列表}

执行要点：
- 产物一律落 `output/{项目名}/` 下各阶段子目录
- 遵循规范引用铁律（先读 项目规范.md 再产出）
- 产物依赖门禁检查可跳过（autopilot 已在编排层保证依赖顺序）

完成后只回报（不回传产物全文）：
STATUS(PASS|FAIL)
OUTPUT(关键产物路径列表)
SUMMARY(一句话)
```

> 注：subagent dispatch 时追加 `产物依赖门禁检查可跳过`，因为 autopilot 已在编排层保证了拓扑顺序依赖，subagent 无需重复检查。
