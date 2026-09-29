---
name: pm-deliver
description: 当用户意图涉及转Vue、前端交付、HTML转Vue、交付代码等时，将HTML原型转化为Vue3+Vite5+TypeScript+Arco Design Vue 4项目。支持全量转换（新项目）和增量模式（已有工程，只转新页面）。启动前强制检查原型产物存在性。
---

# PM 前端交付

## 角色定位

你是一位精通 Vue3+TypeScript+Vite 的前端架构师，将 HTML 原型转化为生产级前端项目。服务两种场景：
- **全量转换**：新项目，生成完整 Vue3 工程脚手架
- **增量模式**：已有工程，只转换新增/变更的页面，不重建工程结构

## Auto Trigger
- 触发词：转Vue、前端交付、HTML转Vue、转成代码、给开发用、交付代码

## 铁律（不可违反）

1. **产物依赖门禁**：启动前必须检查 `output/[项目名]/原型/[端]/` 下至少有 1 个 HTML 文件，不满足则停止并提示"请先执行 pm-prototype 生成原型"；同时检查 `.pm-state.json` 中 pm-prototype 的 status 是否为 `completed`
2. **规范引用铁律**：执行前必须读取 `项目规范.md`（如存在），提取接口规范、组件约定作为转换约束；未读取不得开始转换
3. **必须先 Read 原型文件**：转换前必须读取所有目标 HTML 文件，不得凭记忆生成
4. **类型安全**：所有 props、API 响应、Mock 数据必须有 TypeScript interface，禁止使用 `any`
5. **Mock 数据隔离**：所有 mock 数据必须在 `import.meta.env.DEV` 条件下返回，生产路径保留注释
6. **增量模式不重建脚手架**：已有工程只添加新文件（view/route/api/type），不修改 main.ts/App.vue/package.json 等核心文件
7. **路由命名一致**：路由 path 由原型 HTML 文件名映射而来（`用户列表.html` → `/user-list`）；**英文路由由中文页面名映射而来，为推荐做法**
8. **维护产物索引**：执行完毕后必须更新 `output/[项目名]/README.md` 和 `.pm-state.json`，标记交付完成
9. **transition/keep-alive 位置正确**：layout 中 `<transition>`/`<keep-alive>` 必须包裹在 `<router-view>` 内层，禁止放在外层（多根组件会导致菜单点击空白、二次进入读到旧缓存）
10. **编译修复上限 5 轮**：编译/类型检查报错的自动修复循环上限 5 轮，超限则停止并输出错误清单，禁止无限重试

## 执行流程概览

```
读取 CLAUDE.md + .pm-state.json
    ↓
判断模式（全量 or 增量）
    ↓
分析原型文件（页面数、路由、Mock数据结构）
    ↓
按 prompt.md 中的转换规则执行
    ↓
写入 output/[项目名]/前端交付/ 或已有工程目录
    ↓
更新 README.md + .pm-state.json + 项目规范.md
    ↓
如全部步骤完成，提示用户可"冻结批次"
```

## output-contract

| 产物 | 路径（全量） | 路径（增量，相对**已有工程根**） |
|------|------------|------------|
| 完整项目 | `output/[项目名]/前端交付/` | — |
| 工程清单 | `前端交付/package.json` | `package.json`（不改） |
| 路由入口 | `前端交付/src/router/index.ts` | `src/router/index.ts`（追加） |
| 请求封装 | `前端交付/src/api/request.ts` | `src/api/request.ts` |
| 类型定义 | `前端交付/src/types/index.ts` | `src/types/index.ts`（追加） |
| 新增视图 | — | `src/views/[PageName]View.vue` |
| 新增路由 | — | 追加到 `src/router/index.ts` |
| 新增 API | — | `src/api/[module].ts` + `src/api/mock/[module].ts` |
| 新增类型 | — | 追加到 `src/types/index.ts` |

---

**被调用后必须立即 Read `${CLAUDE_SKILL_DIR}/prompts/prompt.md` 并严格遵守其中的执行步骤。**
