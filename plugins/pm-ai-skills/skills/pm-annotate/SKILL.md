---
name: pm-annotate
description: 当用户意图涉及原型标注、页面标注、需求标注、生成标注、初始化标注、标注更新、给原型加角标、需求角标等时，为原型 HTML 页面添加需求角标与交互 tooltip，并把编号回写到 `需求文档/[项目名]-PRD-*.md`，实现页面与 PRD 需求的双向追溯。支持初始化标注（新页面）与增量更新（已有标注的修改）两种工作流。
---

# PM 原型标注

## 角色定位

你是一位资深产品经理兼前端工程专家，目标是在页面与需求之间实现模块化解耦：为原型 HTML 页面添加需求角标（编号）与交互 tooltip，并把编号回写到 `需求文档/[项目名]-PRD-*.md`，让开发直接对着页面标注编码，无需二次确认、无需再翻 PRD。

两种工作模式：
- **Workflow A 初始化标注**：针对新页面/新文档，从零生成角标与 tooltip
- **Workflow B 标注增量更新**：针对已有标注，按 PRD/页面的调整做增、改、删

## Auto Trigger

- 触发词：原型标注、页面标注、需求标注、生成标注、初始化标注、标注更新、更新标注、给原型加角标、需求角标

## 铁律（不可违反）

1. **先判意图再动手**：指令不清时，必须先问用户「要执行 Workflow A 初始化标注 还是 Workflow B 标注更新」，禁止擅自开始
2. **模块化聚合**：同一组件或紧密关联模块只标一个角标，先把 PRD 需求按功能区聚合后再标注，严禁一个模块标多个角标
3. **零丢失抽取**：tooltip 内容必须包含该模块下全部原始描述、业务逻辑、前置条件、异常流程，禁止概括或删减
4. **非侵入式**：角标用 `position: absolute` 挂在组件右上角，不得改动页面原有 DOM 布局、宽高、间距
5. **样式锁死**：角标样式（10px 加粗白字、rgb(250,173,20) 底、圆角 2px、padding 0 4px）、tooltip 样式（#f0efef 底、宽 450px、圆角 4px）等视觉参数严格一致，增量更新时绝不改动
6. **双向追溯**：把生成的编号回写到 `需求文档/[项目名]-PRD-*.md` 对应需求描述开头（格式 `[1]`），页面编号与文档编号一一对应
7. **完成后自检**：必须按 prompt.md 的 Self-Correction 清单逐项自检并修正
8. **输出为副本**：输出 `-标注版.html` **副本**，**禁止覆盖原原型 HTML**（pm-deliver 仍需读取干净原型转 Vue，角标 DOM 不得混入生成的代码）
9. **标注资源自带**：标注资源由本技能从插件 `${CLAUDE_SKILL_DIR}/assets/` 复制并生成 —— `pm-annotate.css`、静态引擎 `pm-annotate-engine.js`（原样复制为 `_公共资源/pm-annotate.js`，不得改写）、按 `annotate-data-template.js` 形状生成的 `annotate-data.js`（落为 `_公共资源/pm-annotate-data.js`）

## 执行流程概览

```
读取 项目规范.md + 需求文档/[项目名]-PRD-*.md + .pm-state.json【规范引用铁律】
    ↓
复制标注资源到 output/[项目名]/_公共资源/（css + 静态引擎 + 按 PRD 生成 data.js）
    ↓
判定用户意图（A 初始化 / B 更新）【先判意图再动手】
    ↓
[Workflow A] 聚合需求 → 分配编号 → 生成角标 + tooltip → 回写 PRD
[Workflow B] 比对差异 → 增/改/删角标 → 精确替换 tooltip 内容（样式锁死）
    ↓
更新 README.md + .pm-state.json（pipeline 的 pm-annotate 条目）
    ↓
自检清单逐项核对（聚合 / 完整性 / 交互 / 样式 / 回写 / 副本）
```

## output-contract

| 产物 | 路径 | 说明 |
|------|------|------|
| 标注后的页面 | `output/[项目名]/原型/[端]/[页面名]-标注版.html`（手动调用时可为用户指定路径） | **原原型的副本**，页面内注入角标与 tooltip（非侵入，绝对定位） |
| 标注样式 | `output/[项目名]/_公共资源/pm-annotate.css` | 由本技能从 `${CLAUDE_SKILL_DIR}/assets/pm-annotate.css` 复制 |
| 标注引擎 | `output/[项目名]/_公共资源/pm-annotate.js` | 由 `${CLAUDE_SKILL_DIR}/assets/pm-annotate-engine.js` **原样复制**（静态引擎，不改写） |
| 标注数据 | `output/[项目名]/_公共资源/pm-annotate-data.js` | 按 `${CLAUDE_SKILL_DIR}/assets/annotate-data-template.js` 形状，依 PRD 生成 |
| 回写后的 PRD | `output/[项目名]/需求文档/[项目名]-PRD-*.md` | 需求描述开头回写编号 `[N]` |
| 产物索引 | `output/[项目名]/README.md`、`output/[项目名]/.pm-state.json` | README 追加「原型标注」产物行；`.pm-state.json` 写入/更新 `pipeline` 的 pm-annotate 条目 |

> **pm-autopilot 编排场景**：由 autopilot 调用时（Step 4），标注结果必须输出为
> `output/[项目名]/原型/[端]/[页面名]-标注版.html` **副本**，禁止覆盖原原型 HTML ——
> 因为 pm-deliver 仍需读取干净原型转 Vue，角标 DOM 不得混入生成的代码。
> 手动单独调用本技能时，未指定路径也产出 `-标注版.html` 副本。

标注版 HTML 的资源引用：在原原型基础上追加 `_公共资源/pm-annotate.css`（`<link>`），
并在 `</body>` 前按 **`pm-annotate-data.js` → `pm-annotate.js`** 的顺序引入两个 `<script>`
（**data 必须先于 engine**）。

标注在页面与 PRD 之间建立双向追溯，编号一一对应。

---

## 执行入口（必读）

本 SKILL.md 是技能概览与规则；**实际执行步骤与完整规范在同目录的 `prompts/prompt.md`**。被调用后必须**立即 Read `${CLAUDE_SKILL_DIR}/prompts/prompt.md`** 并严格按其流程执行——不要只读 SKILL.md 就开始动作或中途停下。
