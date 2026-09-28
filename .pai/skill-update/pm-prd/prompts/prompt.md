> 执行前必须 Read `{{SKILL_DIR}}/../pm-common/project-management.md` 了解项目管理规范。

# PM PRD 文档生成执行步骤

## 步骤 -1：产物依赖门禁检查（硬门禁，不可跳过）

1. 检查 `output/[项目名]/analysis/analysis-report.md` 是否存在
   - **不存在** → ❌ 停止执行，输出：
     ```
     ❌ 前置依赖不满足：未找到需求分析报告。
     请先执行 pm-analyze 完成需求分析，再执行 pm-prd。
     ```
   - **存在** → 继续
2. 检查 `.pm-state.json` 中 `pipeline` 的 pm-analyze status：
   - **不是 `completed`** → ❌ 停止执行，提示"pm-analyze 尚未完成"
3. **用户强制跳过**：仅当用户明确说"跳过依赖检查"或"我有自己的分析文档"时可跳过，但必须记录 `"dependencySkipped": true`

## 步骤 0：读取上下文（规范引用铁律）

按顺序检查（**未读取 project-spec.md 不得进入步骤 1**）：
1. **【强制】** `output/[项目名]/project-spec.md`：获取已有技术决策、接口清单，确保 PRD 中的接口命名和数据格式与已有规范一致
2. 当前目录 `CLAUDE.md`：提取技术栈、接口规范格式、组件库约定
3. `output/[项目名]/analysis/analysis-report.md`：如存在，直接基于此报告生成，不重新分析用户已分析过的需求
4. `output/[项目名]/analysis/quick-analysis-[日期].md`：轻量分析报告，用于变更单场景
5. `output/[项目名]/.pm-state.json`：获取当前批次、F/T/R 计数器，检查是否断点续做

## 步骤 1：判断文档模式

- 需求来自"新项目"、"完整功能模块" → **完整 PRD 模式**（七章节）
- 需求包含"迭代"、"小功能"、"改了X"、"增加一个" → **变更单模式**（1-2页）
- 不确定时询问

## 变更单模板（轻量模式）

```markdown
# 变更单 C[编号]：[功能名]
> 批次：B[N] | 变更自：B[M]:F[XXX] | 生成时间：[日期时间] | pm-prd v2.0.0

**变更日期**：[日期] | **影响版本**：vX.X | **变更类型**：新增/修改/删除

## 变更描述
[1段话说明变更内容和原因]

## 影响范围
- 涉及页面：[页面名]
- 涉及接口：[接口名]（新增/修改/不变）
- 涉及数据库：[表名]（如有）

## 功能说明
[具体的交互逻辑，字段说明]
使用组件：`AForm` `AInput` ...

## 测试要点
| 场景 | 操作 | 预期结果 |
|------|------|---------|
| 正常流程 | ... | ... |
| 边界值 | ... | ... |
| 异常处理 | ... | ... |

## 工时估算
前端：X-X天 | 后端：X-X天 | 测试：X-X天
```

## 步骤 2：生成完整 PRD（完整模式）

（此处读取并使用 `{{SKILL_DIR}}/prompts/prd-template.md` 和 `test-case-template.md` 的模板内容）

请在执行时 Read 这两个文件：
- `{{SKILL_DIR}}/prompts/prd-template.md`
- `{{SKILL_DIR}}/prompts/test-case-template.md`

按照其中的模板逐章节输出，然后写入 output-contract 定义的路径。

## 步骤 3：更新项目管理文件

### 3.1 更新 README.md
在 `output/[项目名]/README.md` 的"PRD 文档（pm-prd）"表格中追加产物行，标注 F 编号范围。

### 3.2 更新 .pm-state.json
- `pipeline` 中 pm-prd 的 `status` → `completed`
- `counters.T` 和 `counters.R` 更新为最后分配的编号数字

### 3.3 追加 project-spec.md
将 PRD 中新增的接口追加到 project-spec.md 的"接口清单"表格。

### 3.4 产物头部标注
在 PRD 文件头部追加：
```
> 批次：B[N] | 功能编号：F001-F012 | 生成时间：[日期时间] | pm-prd v2.0.0
```

### 3.5 编号使用规则
- F 编号：引用 pm-analyze 已分配的编号，如需新增功能则从 counters.F+1 续编
- T 编号：每个测试用例独立编号（T001, T002...），每条标注关联的 F 编号
- R 编号：每个接口独立编号（R001, R002...），标注关联的 F 编号
