# PM Dev Autopilot 执行步骤

> 本文件为编排执行步骤；概览与规则见同目录 `../SKILL.md`。被调用后按本文件流程严格执行。

## 前置约定

- 路径变量：`output/[项目名]/` 为项目根，产物按 `pm-common/project-management.md` 目录骨架存放
- run 文件：`output/[项目名]/.pm-dev-run.md`（运行态，不进产物索引）
- 被编排技能 prompt.md（subagent 必读）：
  - pm-design-1-func：`${CLAUDE_SKILL_DIR}/../pm-design-1-func/prompts/prompt.md`
  - pm-design-2-db：`${CLAUDE_SKILL_DIR}/../pm-design-2-db/prompts/prompt.md`
  - pm-design-3-review：`${CLAUDE_SKILL_DIR}/../pm-design-3-review/prompts/prompt.md`
  - pm-dev-1-backend：`${CLAUDE_SKILL_DIR}/../pm-dev-1-backend/prompts/prompt.md`
  - pm-dev-2-frontend：`${CLAUDE_SKILL_DIR}/../pm-dev-2-frontend/prompts/prompt.md`
  - pm-dev-3-test：`${CLAUDE_SKILL_DIR}/../pm-dev-3-test/prompts/prompt.md`
  - pm-dev-4-codereview：`${CLAUDE_SKILL_DIR}/../pm-dev-4-codereview/prompts/prompt.md`

---

## Step 0：状态探测与分流

> 主会话轻量执行，不 dispatch subagent。

### 0.1 确定项目名

- 用户传入 `--project [项目名]` → 直接使用
- 未传入 → 检查 `output/` 下有哪些项目目录：只有 1 个自动选；多个列出让用户选；没有则询问项目名

### 0.2 判定项目性质 + 输入来源 + 参考目录 + 配置文档

- **配置文档**：`--config <路径>` 或 `output/[项目名]/project-config.md`（可选，见 pm-common §十三）；存在则读，其「1 项目信息 / 2 输入来源」覆盖下述判定；工程拉取/DB 基线/CLAUDE.md 由 Step 1 的 pm-design-1-func 消费
- **项目性质**：`--iterate` 或目标目录已有 `backend/`/`schema.sql`/devPipeline 历史 → 迭代；否则新项目
- **输入来源**：`--prd <路径>` → 模式 A；`--requirement <文本/文件>` → 模式 B；都未传 → 探测 `output/[项目名]/prd/*-PRD-*.md` 是否存在，存在即模式 A，否则询问
- **参考目录**：`--ref <路径>`，缺省 `D:/pm-ai/pm-ai-projects/output/`（配置「7. 参考模块」并入）
- 把判定结果写进 run 文件头部

### 0.3 读取项目状态

1. 检查 `output/[项目名]/.pm-state.json`
   - **不存在**：全新项目，从 Step 1（pm-design-1-func）开始，由该技能建骨架
   - **存在**：Read 获取 `devPipeline` 各步状态 + `devProjectType`
2. 检查 `output/[项目名]/.pm-dev-run.md`
   - **不存在** → 按 `devPipeline` 状态预标各步 PASS/待执
   - **存在** → 读取各步 STATUS
3. 用户传 `--from pm-X` → 该步及其后重置为待执
4. 用户传 `--skip-frontend` → Step 5 直接标「跳过」

### 0.4 分流

- 定位第一个非 PASS（且非跳过）步作为起点
- 全部 PASS → 提示「研发链所有步骤已完成。是否从某步重跑？」
- 有 `PAUSE@*` 标记 → 检查暂停条件是否解除：
  - `PAUSE@design-blocker`：re-check 最新 `design/review/*.md` 的 Blocker
    - 遗留 = 0 → 解除，从下一步继续
    - 遗留 > 0 → 再次暂停，输出未解决 Blocker 清单
  - `PAUSE@codereview`：re-check 最新 `review/*.md` 严重问题是否已修复应答
    - 已全部应答 → 解除；否则再次暂停

### 0.5 创建/更新 run 文件

```markdown
# PM Dev Autopilot 运行状态

> 项目：[项目名] | 项目性质：新项目/迭代 | 输入来源：PRD/需求 | 参考目录：[路径] | 配置文档：[路径/无] | 启动时间：[时间]

## 运行状态：进行中

## 各步进度

| 步骤 | 技能 | STATUS | 开始时间 | 完成时间 | 产物路径 | 备注 |
|------|------|--------|---------|---------|---------|------|
| Step 1 | pm-design-1-func | 待执/进行中/PASS/FAIL | — | — | — | — |
| Step 2 | pm-design-2-db | 待执 | — | — | — | — |
| Step 3 | pm-design-3-review | 待执 | — | — | — | — |
| Step 4 | pm-dev-1-backend | 待执 | — | — | — | — |
| Step 5 | pm-dev-2-frontend | 待执/跳过 | — | — | — | — |
| Step 6 | pm-dev-3-test | 待执 | — | — | — | — |
| Step 7 | pm-dev-4-codereview | 待执 | — | — | — | — |

## 暂停记录

（无）
```

---

## Step 1：dispatch pm-design-1-func 功能详细设计

### 1.1 更新 run 文件 → 1.2 dispatch subagent

```
你是 pm-design-1-func 技能执行者（功能详细设计）。项目名：[项目名]，工作空间根：[workspace_root]。

**立即 Read** `[pm-design-1-func prompt.md 绝对路径]` 并严格按其流程执行，不得跳步。

执行前先 Read `[pm-common/project-management.md 绝对路径]` 了解项目管理规范。

项目性质：[新项目/迭代] | 输入来源：[PRD 路径 / 需求文本] | 参考目录：[路径]

（有配置文档时附上）项目初始化配置：[--config 路径 / project-config.md 路径]

（模式 B 时附上）用户需求内容：[需求文本或文件路径]

完成后只回报：
STATUS(PASS|FAIL)
OUTPUT(关键产物路径列表)
SUMMARY(一句话)
```

### 1.3 返回后验证

- `output/[项目名]/design/[项目名]-功能详细设计.md` 存在？
- `.pm-state.json` 出现 `devPipeline` 且 `pm-design-1-func` completed？

### 1.4 更新 run 文件 → 1.5 门禁（无）→ Step 2

---

## Step 2：dispatch pm-design-2-db 数据库设计

dispatch prompt（同上模板，role 改为「数据库设计」），上游产物路径：功能详细设计、project-spec、PRD ch5。

验证：
- 新项目：`design/db/[项目名]-schema.sql` 存在？
- 迭代项目：`design/db/[项目名]-delta-*.sql` 存在？

---

## Step 3：dispatch pm-design-3-review 设计评审

dispatch prompt（role「设计评审」），回报多一行 `BLOCKER_COUNT(Blocker 数)`。

验证：`design/review/[项目名]-设计评审-[日期].md` 存在？

### 3.x 门禁检查（设计 Blocker）

- 读 `.pm-state.json` `pm-design-3-review` 条目的 `blockerCount`（或报告 Blocker 数）
- **Blocker > 0**：
  - run 文件：Step 3 STATUS = PASS（报告完成），**同时**记 `PAUSE@design-blocker`
  - 向用户输出 Blocker 清单，提示「解决后重新执行 /pm-dev-autopilot 续做；确认带问题推进请回复"继续"」
  - 用户回复"继续" → 解除暂停，进入 Step 4；否则暂停退出
- **Blocker = 0** → 进入 Step 4

---

## Step 4：dispatch pm-dev-1-backend 后端 TDD

dispatch prompt（role「后端开发」），上游产物：功能详细设计、schema/delta SQL、project-spec。

验证：
- `backend/pom.xml` 存在？
- `backend/src/main/java` 存在？

门禁：pom.xml 缺失或 subagent 回报编译失败 → FAIL，暂停。

---

## Step 5：dispatch pm-dev-2-frontend 前端工程（可选）

> 用户传 `--skip-frontend` → 本步标「跳过」，直接进入 Step 6。

dispatch prompt（role「前端工程」），上游产物：功能详细设计、原型（干净 HTML）、后端。

验证：`frontend/package.json` 存在？

门禁：未 `--skip-frontend` 但 package.json 缺失 → FAIL，暂停。

---

## Step 6：dispatch pm-dev-3-test 单元测试

dispatch prompt（role「单元测试」），上游产物：功能详细设计、backend/、frontend/（可选）。

验证：`test/[项目名]-单元测试报告-[日期].md` 存在？

门禁：报告标注覆盖率未达标或单测未通过 → FAIL，暂停。

---

## Step 7：dispatch pm-dev-4-codereview 代码审查

dispatch prompt（role「代码审查」），回报多一行 `BLOCKER_COUNT(严重问题数)`。

验证：`review/[项目名]-代码审查报告-[日期].md` 存在？

### 7.x 门禁检查（审查严重问题）

- 读 `.pm-state.json` `pm-dev-4-codereview` 条目的 `reviewBlockerCount`
- **严重问题 > 0**：run 文件 Step 7 STATUS = PASS，同时记 `PAUSE@codereview`；输出严重问题清单，提示修复后回来填「修复应答」
- **= 0** → 进入 Step 8

---

## Step 8：完成与提示

当 Step 1-7 全部 PASS（Step 5 跳过视为通过）：

1. 更新 run 文件：运行状态 = 已完成
2. **不碰 `.pm-state.json` 的 `batchStatus`**（那是 PM 链的事）
3. 向用户输出完成报告：

```
✅ 项目"[项目名]"研发链已完成！（项目性质：新项目/迭代）

📊 执行摘要：
- pm-design-1-func：[SUMMARY]
- pm-design-2-db：[SUMMARY]
- pm-design-3-review：[SUMMARY]（Blocker [n]）
- pm-dev-1-backend：[SUMMARY]
- pm-dev-2-frontend：[SUMMARY]（或"已跳过"）
- pm-dev-3-test：[SUMMARY]
- pm-dev-4-codereview：[SUMMARY]（严重 [n]）

📁 产物索引：output/[项目名]/README.md
```

---

## 重跑续做逻辑

- 被调用 → Step 0 读 `.pm-state.json`（devPipeline）+ `.pm-dev-run.md` → 定位第一个非 PASS 步 → 续做
- run 文件各步 STATUS 是续做唯一依据
- 用户可传 `--from pm-X` 强制重跑某步
- `--skip-frontend` 跳过 Step 5
- **换会话可恢复**：状态全落盘，新会话执行 `/pm-dev-autopilot` 即自动接续

## subagent dispatch 通用模板

```
你是 [技能名] 技能执行者（[中文名]）。项目名：{项目名}，工作空间根：{workspace_root}。

**立即 Read** `{被执行技能 prompt.md 绝对路径}` 并严格按其流程执行（从步骤 0 到最后一步），不得跳步。

执行前先 Read `{pm-common/project-management.md 绝对路径}` 了解项目管理规范。

项目性质：{new/iteration} | 参考目录：{路径} | 配置文档：{路径/无}

上游产物路径：
{上游产物列表}

执行要点：
- 产物一律落 `output/{项目名}/` 下各阶段子目录
- 遵循规范引用铁律（先读 project-spec.md 再产出）
- 产物依赖门禁检查可跳过（autopilot 已在编排层保证依赖顺序）

完成后只回报（不回传产物全文）：
STATUS(PASS|FAIL)
OUTPUT(关键产物路径列表)
SUMMARY(一句话)
{仅 pm-design-3-review 与 pm-dev-4-codereview 追加}BLOCKER_COUNT(数字)
```

> 注：subagent dispatch 时追加「产物依赖门禁检查可跳过」，因为 autopilot 已在编排层保证拓扑顺序依赖。
