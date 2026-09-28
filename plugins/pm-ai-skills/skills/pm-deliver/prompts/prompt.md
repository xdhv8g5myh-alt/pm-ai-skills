> 执行前必须 Read `${CLAUDE_SKILL_DIR}/../pm-common/project-management.md` 了解项目管理规范。

# PM 前端交付执行步骤

## 步骤 -1：产物依赖门禁检查（硬门禁，不可跳过）

1. 检查 `output/[项目名]/prototypes/` 下是否有至少 1 个端类型子目录，且子目录中有至少 1 个 HTML 文件
   - **不满足** → ❌ 停止执行，输出：
     ```
     ❌ 前置依赖不满足：未找到原型文件。
     请先执行 pm-prototype 生成原型，再执行 pm-deliver。
     ```
   - **满足** → 继续
2. 检查 `.pm-state.json` 中 `pipeline` 的 pm-prototype status：
   - **不是 `completed`** → ❌ 停止执行，提示"pm-prototype 尚未完成"
3. **用户强制跳过**：仅当用户明确说"跳过依赖检查"时可跳过，记录 `"dependencySkipped": true`

## 步骤 0：读取项目上下文（规范引用铁律）

按顺序检查（**未读取 project-spec.md 不得进入步骤 1**）：
1. **【强制】** `output/[项目名]/project-spec.md`：获取接口规范（baseURL、鉴权方式、响应格式）、组件使用约定
2. 检查是否存在 `CLAUDE.md`，提取：
   - 项目目录结构约定
   - 已有组件封装（避免重复封装）
   - 接口 baseURL 和鉴权方式
   - 命名规范（文件名、组件名、变量名）
3. 如果是增量模式，Read 已有工程的 `src/router/index.ts` 和 `src/types/index.ts`，了解现有结构
4. `output/[项目名]/.pm-state.json`：获取当前批次和编号计数器

## 步骤 1：判断交付模式

- 用户提供的是一个完整原型目录且没有已有工程 → **全量转换模式**
- 用户提供的是已有工程路径 + 新增页面的原型 → **增量模式**
- 不确定时询问："是要生成全新的 Vue 项目，还是将新页面添加到已有工程？"

## 步骤 2：分析原型文件

逐一 Read 所有 HTML 原型文件，提取：
- 页面名称和对应路由
- `const MOCK_DATA = {}` 的数据结构（→ TypeScript interface）
- 使用到的 Arco 组件名（→ 确认导入方式）
- 页面间跳转关系（→ 路由配置）

（此处继续读取并使用 `${CLAUDE_SKILL_DIR}/prompts/html-to-vue-rules.md` 和 `${CLAUDE_SKILL_DIR}/prompts/vue3-scaffold-spec.md` 中的转换规则和脚手架模板）

请在执行步骤 3 前分别 Read：
- `${CLAUDE_SKILL_DIR}/prompts/html-to-vue-rules.md`
- `${CLAUDE_SKILL_DIR}/prompts/vue3-scaffold-spec.md`

## 步骤 3：更新项目管理文件

### 3.1 更新 README.md
在 `output/[项目名]/README.md` 的"前端代码（pm-deliver）"表格中追加产物行。

### 3.2 更新 .pm-state.json
- `pipeline` 中 pm-deliver 的 `status` → `completed`
- 如果 pipeline 中所有 4 个步骤都是 `completed`，自动将 `batchStatus` 设为 `completed`

### 3.3 追加 project-spec.md
将转换过程中发现的新组件使用约定追加到"组件使用约定"表格。

### 3.4 批次完成提示
如果本步骤是 pipeline 中最后一个完成的步骤，输出：
```
✅ 项目"[项目名]"批次 B[N] 全部步骤已完成！

产物索引：output/[项目名]/README.md
共享规范：output/[项目名]/project-spec.md

如需冻结此批次（禁止修改），输入"冻结批次"
如需开始新的迭代，输入"新批次"
```

### 3.5 产物头部标注
在生成的 Vue 项目 README.md 头部追加：
```
> 批次：B[N] | 来源原型：output/[项目名]/prototypes/[端]/ | pm-deliver v2.0.0
```
