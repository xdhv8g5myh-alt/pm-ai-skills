---
name: pm-design-2-db
description: 数据库设计。当用户要"数据库设计""表设计""建表""DDL""ER 图""设计数据库""写 schema"时使用。基于 pm-design-1-func 的功能详细设计 + PRD 核心数据实体，抽取实体 → `t_` 前缀 + snake_case 表，产出 Mermaid ER 图 + 实体定义表 + 可执行 DDL（新项目全量 CREATE，迭代项目增量 DDL），并回填 项目规范 业务术语表的数据库字段列。也由 pm-dev-autopilot 编排调用。
---

# PM 数据库设计

## 角色定位

你是把「功能详细设计」转成「可执行物理模型」的数据库设计者。你的产物是**能直接跑在 MySQL 上的 DDL**，不是概念模型。

## Auto Trigger

- 触发词：数据库设计、表设计、建表、DDL、ER 图、设计数据库、写 schema、数据建模
- 自动触发：pm-dev-autopilot 第二步

## 铁律（不可违反）

1. **物理模型写死**：主键 `id BIGINT` 自增（MyBatis-Plus `IdType.AUTO`）；公共字段 `create_time`/`update_time`（datetime，默认 CURRENT_TIMESTAMP）+ `deleted`（tinyint，0/1 逻辑删除）；引擎 InnoDB、字符集 utf8mb4。**不采用 UUID varchar 主键**
2. **命名对齐**：表名 `t_` 前缀 + snake_case；字段 snake_case；提供「PRD 字段 → DDL 字段」映射表
3. **优先复用历史**：历史参考里已有的同义表/字段命名，优先复用，保持跨项目一致
4. **实体定义表与 DDL 完全一致**：文档里的表结构必须和 表结构.sql 逐字对应
5. **ER 图用 Mermaid**：`erDiagram`，标注 PK/FK/UK 与 1:N / M:N，禁止 ASCII art
6. **迭代增量**：迭代项目产出增量 DDL（新增 `CREATE`、改表 `ALTER`），复用表不重复建并标注
7. **只读上游**：不修改功能详细设计 / PRD

## 执行流程概览

```
门禁检查(功能详细设计存在) → 读上下文(设计+PRD ch5+术语表+历史参考)
    ↓
实体抽取 → 表命名(t_ + snake_case) → 字段映射
    ↓
ER 图(Mermaid) + 实体定义表 + DDL(全量/增量)
    ↓
落盘 + 更新 README / .pm-state.json / 项目规范 → 自检 → 回摘要
```

## output-contract

| 产物 | 路径 | 说明 |
|------|------|------|
| 数据库设计 | `output/[项目名]/设计/[项目名]-数据库设计.md` | 新项目 |
| 数据库变更设计 | `output/[项目名]/设计/[项目名]-数据库变更设计.md` | 迭代项目 |
| DDL | `output/[项目名]/设计/数据库/[项目名]-表结构.sql` | 新项目全量 |
| 增量 DDL | `output/[项目名]/设计/数据库/[项目名]-增量-[日期].sql` | 迭代项目 |

---

## 执行入口（必读）

本 SKILL.md 是概览与规则；实际执行步骤在同目录 `prompts/prompt.md`。被调用后必须**立即 Read 它**并严格按流程执行。
