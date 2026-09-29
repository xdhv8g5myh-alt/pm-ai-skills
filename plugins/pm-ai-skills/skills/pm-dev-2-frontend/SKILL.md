---
name: pm-dev-2-frontend
description: 独立前端工程（Vue3，真实后端对接，可选）。当用户要"前端工程""前端代码""生成前端""写前端页面"、或要把功能详细设计转成对接真实后端的 Vue3 工程时使用。对齐 pm-deliver 脚手架（Vue 3.4 + Vite 5 + TS + Arco + Pinia + vue-router），但 API 层是真实后端对接（无 mock 分支、无 isDev 开关）。产物落 独立前端工程/（独立新工程，与 pm-deliver 的前端交付/ 区分）。可 `--skip-frontend` 跳过（用户已用 pm-deliver 交付过 mock 前端，或本轮不需要独立前端工程）。也由 pm-dev-autopilot 编排调用。
---

# PM 独立前端工程

## 角色定位

你是把「功能详细设计 + 后端」转成**对接真实后端**的 Vue3 前端工程的资深前端工程师。产物是可 `npm run build` 通过的独立新工程，API 层直接调 `/api/v1`，不掺 mock。

## 技术栈（单源权威）

- Vue 3.4 + Vite 5 + TypeScript + Arco Design Vue 2.55.3 + Pinia + vue-router
- 复用 `pm-deliver/prompts/vue3-scaffold-spec.md` 脚手架约定
- **差异点**：API 层真实后端对接，**无 `src/api/mock/`**、无 `isDev` mock 分支

## Auto Trigger

- 触发词：前端工程、前端代码、生成前端、写前端页面、前端开发、对接后端
- 自动触发：pm-dev-autopilot 第五步（可 `--skip-frontend` 跳过）

## 铁律（不可违反）

1. **绝不写 `前端交付/`**：产物落 `独立前端工程/`，与 pm-deliver 的 `前端交付/`（mock 前端）严格区分
2. **无 mock**：API 层真实调后端，`src/api/[模块].ts` 封装 R 编号接口，走 `/api/v1`
3. **响应解包**：复用 pm-deliver `request.ts` 的 `{code,message,data}` 解包 + JWT `Authorization: Bearer`
4. **UIUE 来源**：原型 `原型/[端]/*.html`（首选，忽略 `-标注版.html` 副本）；无原型时从功能详细设计推导页面
5. **可选不阻塞**：本步可跳过（`--skip-frontend`；用户已用 pm-deliver 交付过 mock 前端，或本轮不需要独立前端工程），不影响后续 测试/代码审查 判定
6. **只读上游**：不修改功能详细设计 / 后端 / 原型

## 执行流程概览

```
门禁检查(后端工程 存在) → 读上下文(设计契约+原型+脚手架)
    ↓
判定(是否跳过 / new/iteration) → 工程骨架(复用脚手架,去 mock)
    ↓
API 层(request 解包 + src/api/[模块].ts) → 页面 → npm run build
    ↓
落盘 + 更新 README / .pm-state.json(skipped 或 completed) → 自检 → 回摘要
```

## output-contract

| 产物 | 路径 | 说明 |
|------|------|------|
| 前端工程 | `output/[项目名]/独立前端工程/` | 独立新工程；迭代项目若已有则就地增改 |
| 工程清单 | `output/[项目名]/独立前端工程/package.json` | 脚手架依赖与脚本（`npm run build`） |
| API 入口 | `output/[项目名]/独立前端工程/src/api/request.ts` | `{code,message,data}` 解包 + `Authorization: Bearer` 头，无 mock 分支 |

---

## 执行入口（必读）

本 SKILL.md 是概览与规则；实际执行步骤在同目录 `prompts/prompt.md`。被调用后必须**立即 Read 它**并严格按流程执行。
