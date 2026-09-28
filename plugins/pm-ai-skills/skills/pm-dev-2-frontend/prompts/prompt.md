# PM 独立前端工程 执行步骤

> 执行前必须 Read `${CLAUDE_SKILL_DIR}/../pm-common/project-management.md` 了解项目管理规范。

## 步骤 0：门禁检查（硬门禁，可强制跳过）

1. `backend/pom.xml` 存在 且 `.pm-state.json` 中 `pm-dev-1-backend` = `completed`
   - 不满足 → ❌ 停止：`请先执行 pm-dev-1-backend 完成后端`
2. 用户传 `--skip-frontend` → 本步标「跳过」：`.pm-state.json` 条目记 `"status":"skipped","skipped":true,"output":null`，直接结束
3. 用户强制跳过依赖 → 记 `"dependencySkipped": true`

## 步骤 1：读取上下文

1. 【主契约】`design/[项目名]-功能详细设计.md`（R 编号/method/URL/请求/响应，作为 `src/api/[模块].ts` 与 `types` 依据）
2. 【UIUE】`prototypes/[端]/*.html`（干净原型，**忽略 `.annotated.html`**；无则从设计推导页面结构）
3. 【脚手架】Read `${CLAUDE_SKILL_DIR}/../pm-deliver/prompts/vue3-scaffold-spec.md`
4. `output/[项目名]/project-spec.md`（baseURL、组件约定）
5. `.pm-state.json`（读 `devProjectType`）

## 步骤 2：判定性质

- `new` → 新建 `frontend/`
- `iteration` → 若已有 `frontend/` 就地增改；无则新建

## 步骤 3：工程骨架（复用脚手架，去 mock）

按 `vue3-scaffold-spec.md` 目录结构创建，差异点：
- **无 `src/api/mock/`**
- `src/api/request.ts`：`{code,message,data}` 解包 + `Authorization: Bearer` 头，无 mock 分支；`code !== 0` 抛业务错误
- `src/api/[模块].ts`：封装 R001-R010 真实调用
- `src/types/index.ts`：接口出参/入参类型，对齐功能详细设计响应 schema
- 路由/页面：从原型页面（或设计）映射 `src/views/[Page]View.vue`

## 步骤 4：构建验证

`cd frontend && npm install && npm run build` 必须通过（无 Node 环境则明确标注「环境性未验证」，但代码结构必须完整）。

## 步骤 5：落盘与更新

### 5.1 更新 .pm-state.json

- 正常完成：`{"step":"pm-dev-2-frontend","status":"completed","startedAt":null,"completedAt":"…Z","output":"frontend/","counters":{}}`
- 跳过：`{"step":"pm-dev-2-frontend","status":"skipped","startedAt":null,"completedAt":null,"output":null,"counters":{},"skipped":true}`
- 时间戳 UTC 带 `Z`

### 5.2 更新 README.md

`### 前端代码（pm-dev-2-frontend）` 章节追加一行（5 列：产物/路径/页面数/生成时间/批次），
追加在产物清单末尾（`### 变更记录` 之前）。跳过时写「已跳过」。**不要并入 `### 前端代码（pm-deliver）`**——按技能分节。

## 步骤 6：自检

1. 产物在 `frontend/`，未写 `vue/`
2. `src/api/` 无 mock 分支；request.ts 有 `{code,message,data}` 解包 + JWT 头
3. `src/api/[模块].ts` 覆盖设计里的 R 编号接口，走 `/api/v1`
4. types 对齐响应 schema 字段名
5. 跳过时 `.pm-state.json` 记 skipped=true
6. devPipeline 条目 6+ keys 齐全，时间戳 UTC 带 `Z`
7. README 表 5 列

## 步骤 7：会话内输出摘要

只回（不倒全文）：

```
✅ 前端工程：`output/[项目名]/frontend/`（或"已跳过"）

- 页面 [n] 个 · 封装接口 [m] 个
- 构建：通过 / 环境性未验证(注明原因)
```
