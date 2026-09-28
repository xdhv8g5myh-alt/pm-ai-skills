# pm-ai-skills

PM AI 协作平台的 Claude Code 插件市场 —— 覆盖需求分析 → 原型 → PRD → 前端交付全流程的产品经理技能包。

## 安装

在 Claude Code 中执行：

```
/plugin marketplace add xdhv8g5myh-alt/pm-ai-skills
/plugin install pm-ai-skills@pm-ai-marketplace
```

安装后即可用触发词或技能名调用：

| 技能 | 用途 | 触发词示例 |
|------|------|-----------|
| `pm-analyze` | 需求分析 | 分析需求、需求拆解、功能梳理 |
| `pm-prototype` | 原型生成 | 生成原型、做原型、H5原型 |
| `pm-prd` | PRD 文档 | 写PRD、生成PRD、需求文档 |
| `pm-deliver` | 前端交付 | 转Vue、前端交付、交付代码 |
| `pm-autopilot` | 全流程自动编排 | 全自动跑需求、一键跑完、autopilot |

## 目录结构

- `.claude-plugin/marketplace.json` — 市场清单
- `plugins/pm-ai-skills/` — 插件本体
  - `.claude-plugin/plugin.json` — 插件 manifest
  - `skills/` — 技能（pm-analyze / pm-prototype / pm-prd / pm-deliver / pm-autopilot / pm-common / pm-annotate / generate-mini-app）

## 关联仓库

- [pm-ai-platform](../pm-ai-platform) — 文档站点
- [pm-ai-projects](../pm-ai-projects) — 需求项目产物
