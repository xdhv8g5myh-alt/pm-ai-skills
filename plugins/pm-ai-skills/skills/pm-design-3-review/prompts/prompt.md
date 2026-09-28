# PM 设计评审（五位一体） 执行步骤

> 执行前必须 Read `${CLAUDE_SKILL_DIR}/../pm-common/project-management.md` 了解项目管理规范。
> 检查项库在同目录 `checklist.md`，步骤 3 开始前必须 Read 它。

## 步骤 0：产物依赖门禁（硬门禁，可强制跳过）

1. 检查 `design/[项目名]-功能详细设计.md` **和** `design/db/[项目名]-schema.sql`（或 delta SQL）都存在
   - 缺任一 → ❌ 停止：`请先完成功能详细设计与数据库设计`
2. 检查 `.pm-state.json` 中 `pm-design-1-func`、`pm-design-2-db` 均 `completed`
3. 用户强制跳过 → 记 `"dependencySkipped": true`

## 步骤 1：读取上下文

按顺序读取：

1. 【主对象】`design/[项目名]-功能详细设计.md`（接口设计块 + 字段溯源表）
2. 【主对象】`design/[项目名]-数据库设计.md`（或 数据库变更设计.md）+ `design/db/*-schema.sql`（或 delta SQL）
3. 佐证：`prd/*-PRD-*.md`（需求依据）、`prototypes/[端]/*.html`（UIUE 依据，存在则读）
4. `output/[项目名]/project-spec.md`（约定基准）
5. `.pm-state.json`（读 `devProjectType`，判断是否迭代项目）

## 步骤 2：判定迭代维度

- `devProjectType == "iteration"` → 额外核对 checklist.md「迭代项目额外核对」E-1/E-2/E-3
- `new` → 只过五个维度

## 步骤 3：过五位一体 checklist

对 checklist.md 的 D1~D5（+ 迭代时 E1~E3）逐项判定，每项给：

| 字段 | 要求 |
|------|------|
| 结论 | ✅ / ❌ / N/A |
| 证据 | 引用功能详细设计 / DDL 的具体位置 + 原文 |
| 级别 | 仅 ❌ 项：Blocker / Major / Minor / Question |
| 建议改法 | 仅 ❌ 项：可直接落进设计/DDL 的成稿文字 |

判定规则：找不到 = ❌（缺失），不假设"应该写了"；N/A 必须写原因。

## 步骤 4：生成报告

写入 `output/[项目名]/design/review/[项目名]-设计评审-[日期].md`（日期 `YYYY-MM-DD`，重跑生成新日期文件）。

```markdown
# 设计评审报告（五位一体）

> 批次：[B] | 评审对象：`design/[项目名]-功能详细设计.md` + `design/db/*-schema.sql` | 生成时间：[时间] | 技能：pm-design-3-review v1.4.0
> 项目性质：新项目 / 迭代

## 一、结论

五维：字段溯源 / 连通性 / 状态并发 / 性能 / 合规（+ 迭代兼容性）

**Blocker [a] 项**（须评审前解决）· Major [b] 项 · Minor [c] 项 · Question [d] 项

## 二、Blocker（须开发前解决）

| 编号 | 维度 | 现状（位置 + 原文） | 建议改法（可粘贴） |
|------|------|--------------------|--------------------|

## 三、Major / 四、Minor / 五、Question

（格式同上）

## 六、逐项结论

| 编号 | 维度 | 结论 | 证据 / 级别 |
|------|------|------|------------|
```

三条硬要求：每条 ❌ 有证据；每条 ❌ 有可粘贴改法；结论行数字准确。

## 步骤 5：落盘与更新

### 5.1 更新 .pm-state.json

`devPipeline` 插入/更新 `pm-design-3-review` 条目（splice，重跑先摘旧条目）：
`{"step":"pm-design-3-review","status":"completed","startedAt":null,"completedAt":"…Z","output":"design/review/[项目名]-设计评审-[日期].md","counters":{},"blockerCount":N}`。时间戳 UTC 带 `Z`。

### 5.2 更新 README.md

`### 设计评审（pm-design-3-review）` 章节追加一行（5 列：产物/路径/Blocker 数/生成时间/批次），
追加在产物清单末尾（`### 变更记录` 之前）。

### 5.3 project-spec.md

不写（本技能不产生技术决策）。

## 步骤 6：自检

1. 五个维度都过了，未漏维度
2. 每条 ❌ 有证据 + 可粘贴改法
3. Blocker ≤ 5，每条满足「开发会做错/上线必然整改」门槛
4. 迭代项目 E-1/E-2/E-3 已核对
5. 报告落在 `design/review/`（绝对路径核对过）
6. devPipeline 条目 6+ keys 齐全，时间戳 UTC 带 `Z`；`blockerCount` 数字与报告一致
7. README 表 5 列
8. 未修改功能详细设计 / DDL / PRD

## 步骤 7：会话内输出摘要

只回（不倒全文）：

```
✅ 设计评审报告：`output/[项目名]/design/review/[项目名]-设计评审-[日期].md`

🔴 Blocker [a] 项（须开发前解决）
  - [维度] — [一句话说清缺什么]

🟡 Major [b] · 🔵 Minor [c] · ❓ Question [d]（详见报告）
```
