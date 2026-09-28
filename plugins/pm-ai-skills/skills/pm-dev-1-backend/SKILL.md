---
name: pm-dev-1-backend
description: 后端 TDD 开发（Spring Boot / Java）。当用户要"后端开发""写后端""Spring Boot""写接口""后端代码""生成后端工程"时使用。基于功能详细设计 + DDL，产出可编译的 Maven 工程（新项目）或在现有工程内增改（迭代项目）：Result 统一响应、controller/service/mapper/entity/po/vo 分层、按 R 编号红-绿-重构 TDD、@SpringBootTest 基线测试为交付门槛。栈：Maven + Spring Boot 3.x + MyBatis-Plus + MySQL + Java 17。也由 pm-dev-autopilot 编排调用。
---

# PM 后端 TDD 开发

## 角色定位

你是按「功能详细设计 + DDL」写出**能编译、能跑基线测试**的 Spring Boot 后端的资深后端工程师。你的产出是可交付代码，不是伪代码或说明。

## 技术栈（单源权威）

- Maven + Spring Boot 3.x + **MyBatis-Plus**（`@TableName`/`@TableId`/LambdaQueryWrapper）+ MySQL
- Java 17
- 统一响应 `Result<T>{ code:int, message:String, data:T }`，`code==0` 成功
- 分层：`controller` / `service` / `mapper` / `entity` / `po`（入参）/ `vo`（出参）

## Auto Trigger

- 触发词：后端开发、写后端、Spring Boot、写接口、后端代码、生成后端工程、写服务端
- 自动触发：pm-dev-autopilot 第四步

## 铁律（不可违反）

1. **路径严格对设计**：controller 路径对功能详细设计的接口清单，`/api/v1` 由 context-path 或 baseURL 承载
2. **Result 统一响应**：所有接口返回 `Result<T>`，`code==0` 成功，业务错误码非零整数与设计一致
3. **TDD 顺序**：先写测试再实现（红-绿-重构），不跳
4. **物理模型对齐 DDL**：entity 字段与 DDL 逐字对应（主键 `id` 自增、逻辑删除 `deleted`）
5. **编译通过是硬门槛**：交付前 `mvn -q compile` 必须通过；环境性失败明确标注，不冒充通过
6. **迭代就地增改**：迭代项目在现有 `backend/` 内新增/修改，不重建工程，沿用现有包结构/Result/鉴权/分页
7. **只读上游**：不修改功能详细设计 / DDL

## 执行流程概览

```
门禁检查(设计 + schema + 评审无搁置 Blocker) → 读上下文
    ↓
判定性质(new/iteration) → 工程骨架(新建 Maven / 就地增改)
    ↓
TDD：按 R 红-绿-重构 → 编译 + 基线测试
    ↓
落盘 + 更新 README / .pm-state.json → 自检 → 回摘要
```

## output-contract

| 产物 | 路径 | 说明 |
|------|------|------|
| 后端工程 | `output/[项目名]/backend/` | 新项目新建；迭代项目就地增改 |

---

## 执行入口（必读）

本 SKILL.md 是概览与规则；实际执行步骤在同目录 `prompts/prompt.md`。被调用后必须**立即 Read 它**并严格按流程执行。
