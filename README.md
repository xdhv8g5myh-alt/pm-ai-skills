# pm-ai-skills

PM AI 协作平台的 Claude Code 插件市场 —— 覆盖需求分析 → 原型 → PRD → 前端交付的产品经理技能包，以及 功能详细设计 → 数据库 → 设计评审 → 后端 → 前端 → 单测 → 审查 的研发链技能包。

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
| `pm-annotate` | 原型标注 | 原型标注、生成标注、给原型加角标 |
| `pm-design-reverse` | 设计稿反推需求 | 设计稿反推、Figma转需求、逆向需求 |
| `pm-review` | PRD 评审自查 | PRD自查、评审自查、检查PRD |

研发链技能（功能详细设计 → 数据库 → 设计评审 → 后端 → 前端 → 单测 → 审查）：

| 技能 | 用途 | 触发词示例 |
|------|------|-----------|
| `pm-design-1-func` | 功能详细设计 | 详细设计、接口设计、技术设计 |
| `pm-design-2-db` | 数据库设计 | 数据库设计、建表、DDL |
| `pm-design-3-review` | 设计评审（五位一体） | 设计评审、评审设计、技术评审 |
| `pm-dev-1-backend` | Spring Boot 后端 TDD | 后端开发、写接口、Spring Boot |
| `pm-dev-2-frontend` | 独立前端工程（可选） | 前端工程、生成前端 |
| `pm-dev-3-test` | 单元测试 | 单元测试、写单测、测试覆盖率 |
| `pm-dev-4-codereview` | 代码审查 | 代码审查、code review、检查代码 |
| `pm-dev-autopilot` | 研发链自动编排 | 自动跑研发、一键开发、全自动设计开发 |

## 目录结构

- `.claude-plugin/marketplace.json` — 市场清单
- `plugins/pm-ai-skills/` — 插件本体
  - `.claude-plugin/plugin.json` — 插件 manifest
  - `skills/` — 技能（pm-analyze / pm-prototype / pm-prd / pm-deliver / pm-autopilot / pm-common / pm-annotate / pm-design-reverse / pm-review / pm-design-1-func / pm-design-2-db / pm-design-3-review / pm-dev-1-backend / pm-dev-2-frontend / pm-dev-3-test / pm-dev-4-codereview / pm-dev-autopilot）

## 关联仓库

- [pm-ai-platform](../pm-ai-platform) — 文档站点
- [pm-ai-projects](../pm-ai-projects) — 需求项目产物
