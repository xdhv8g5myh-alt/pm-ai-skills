> 执行前必须 Read `${CLAUDE_SKILL_DIR}/../pm-common/project-management.md` 了解项目管理规范。

# PM 前端交付执行步骤

## 步骤 -1：产物依赖门禁检查（硬门禁，不可跳过）

1. 检查 `output/[项目名]/原型/` 下是否有至少 1 个端类型子目录，且子目录中有至少 1 个 HTML 文件
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

按顺序检查（**未读取 项目规范.md 不得进入步骤 1**）：
1. **【强制】** `output/[项目名]/项目规范.md`：获取接口规范（baseURL、鉴权方式、响应格式）、组件使用约定
2. 检查 `output/[项目名]/CLAUDE.md` 是否存在（其次当前目录；**项目内优先，只读不回写**），提取：
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

逐一 Read 所有 HTML 原型文件（**跳过 `*-标注版.html`** —— 标注版是 pm-annotate 的评审产物，不是交付输入），提取：
- 页面名称和对应路由
- `const MOCK_DATA = {}` 的数据结构（→ TypeScript interface）
- 使用到的 Arco 组件名（→ 确认导入方式）
- 页面间跳转关系（→ 路由配置）

（此处继续读取并使用 `${CLAUDE_SKILL_DIR}/prompts/html-to-vue-rules.md` 和 `${CLAUDE_SKILL_DIR}/prompts/vue3-scaffold-spec.md` 中的转换规则和脚手架模板）

请在执行步骤 2.5 前分别 Read：
- `${CLAUDE_SKILL_DIR}/prompts/html-to-vue-rules.md`
- `${CLAUDE_SKILL_DIR}/prompts/vue3-scaffold-spec.md`

## 步骤 2.5：生成/更新 Vue 工程（核心落盘步骤）

> **本步骤是交付的实际产物生成步骤。产物落盘根目录 = `output/[项目名]/前端交付/`。**
> 此前各步只做门禁、读上下文、判模式、分析原型；**不落盘工程就不算交付**。

### 2.5.1 依据

执行前必须已 Read（见步骤 2）：
- `${CLAUDE_SKILL_DIR}/prompts/html-to-vue-rules.md` —— HTML → Vue SFC 转换规则（结构 / JS / 组件库 / Mock 数据 / 路由，含常见陷阱）
- `${CLAUDE_SKILL_DIR}/prompts/vue3-scaffold-spec.md` —— Vue3 工程脚手架规格（目录结构 + `package.json` / `vite.config.ts` / `main.ts` / `tsconfig.json` 模板）

### 2.5.2 全量转换模式 —— 写出完整工程

在 `output/[项目名]/前端交付/` 下落盘**完整可构建**的工程，产物清单（缺一不可）：

| 类别 | 产物 |
|------|------|
| 脚手架 | `package.json`、`vite.config.ts`、`tsconfig.json`、`index.html` |
| 入口 | `src/main.ts`、`src/App.vue` |
| 路由 | `src/router/index.ts` |
| 页面 | `src/views/[PageName]View.vue`（每个（非标注版）原型页面一个，页面名由中文原型名映射） |
| 复用逻辑 | `src/composables/use[功能名].ts` |
| 接口 | `src/api/[module].ts` + `src/api/mock/[module].ts` |
| 类型 | `src/types/index.ts` |

### 2.5.3 增量模式 —— 只写新增文件

只写**已有工程**对应的新文件，**不重建脚手架**：

- 新增页面：`src/views/[PageName]View.vue`
- 追加路由：`src/router/index.ts`
- 新增接口：`src/api/[module].ts` + `src/api/mock/[module].ts`
- 追加类型：`src/types/index.ts`

**不得修改**已有工程的 `main.ts`、`App.vue`、`package.json` 等核心文件（见铁律 6）。

### 2.5.4 编译验证（强制）

生成/写入完毕后**必须**验证工程可构建：

```bash
# 仅类型检查（更快、推荐先跑）
npx vue-tsc --noEmit
# 全量模式完整构建（首次需先安装依赖）
cd output/[项目名]/前端交付 && npm install && npm run build
```

- 报错则自动修复，**编译修复上限 5 轮**（见铁律 10）；超限则停止并输出完整错误清单，禁止无限重试
- 验证通过后方可进入步骤 3

## 步骤 3：更新项目管理文件

### 3.1 更新 README.md
在 `output/[项目名]/README.md` 的"前端代码（pm-deliver）"表格中追加产物行。

### 3.2 更新 .pm-state.json
- `pipeline` 中 pm-deliver 的 `status` → `completed`
- 如果 PM 链 `pipeline` 中所有**非跳过**步都是 `completed`，自动将 `batchStatus` 设为 `completed`

### 3.3 追加 项目规范.md
将转换过程中发现的新组件使用约定追加到"组件使用约定"表格。

### 3.4 批次完成提示
如果本步骤是 pipeline 中最后一个完成的步骤，输出：
```
✅ 项目"[项目名]"批次 B[N] 全部步骤已完成！

产物索引：output/[项目名]/README.md
共享规范：output/[项目名]/项目规范.md

如需冻结此批次（禁止修改），输入"冻结批次"
如需开始新的迭代，输入"新批次"
```

### 3.5 产物头部标注
在生成的 Vue 项目 README.md 头部追加：
```
> 批次：B[N] | 来源原型：output/[项目名]/原型/[端]/ | pm-deliver v1.5.0
```
