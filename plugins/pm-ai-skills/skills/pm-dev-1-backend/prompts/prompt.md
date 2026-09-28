# PM 后端 TDD 开发 执行步骤

> 执行前必须 Read `${CLAUDE_SKILL_DIR}/../pm-common/project-management.md` 了解项目管理规范。

## 步骤 0：门禁检查

### 0.1 硬门禁（可强制跳过）

1. `design/[项目名]-功能详细设计.md` 存在 且 `design/db/[项目名]-schema.sql`（或 delta SQL）存在
   - 缺任一 → ❌ 停止：`请先完成功能详细设计与数据库设计`
2. 用户强制跳过 → 记 `"dependencySkipped": true`

### 0.2 软门禁（评审 Blocker）

- 读 `.pm-state.json` 中 `pm-design-3-review` 条目的 `blockerCount`
- 或读最新 `design/review/*-设计评审-*.md` 的「二、Blocker」，看是否仍有「搁置待定」Blocker
- **有搁置 Blocker → 停止**：输出 Blocker 清单，提示「请先解决设计评审 Blocker 或确认带问题推进」
- 用户明确「继续/带问题推进」→ 继续，但在 SUMMARY 里标注

## 步骤 1：读取上下文

1. 【主输入】`design/[项目名]-功能详细设计.md`（接口设计块：R 编号/method/URL/请求/响应/错误码/业务规则）
2. `design/db/[项目名]-schema.sql`（或 delta SQL）：表结构与 DDL
3. `output/[项目名]/project-spec.md`（响应格式 pre-seed：`{code:0,message:"ok",data:{}}`、baseURL、技术决策）
4. `.pm-state.json`：读 `devProjectType`（new/iteration）

## 步骤 2：判定性质 + 工程骨架

### 2.1 新项目（devProjectType == "new"）

创建 `backend/` Maven 工程：

```
backend/
├── pom.xml                       # Spring Boot 3.x + MyBatis-Plus + MySQL + JUnit 5 + Mockito
├── src/main/java/com/[项目包名]/
│   ├── [AppName]Application.java
│   ├── common/
│   │   ├── Result.java           # Result<T>{code,message,data}
│   │   ├── ErrorCode.java        # 错误码枚举，对齐功能详细设计
│   │   └── BusinessException.java
│   ├── controller/[模块]Controller.java
│   ├── service/[模块]Service.java  + impl/
│   ├── mapper/[模块]Mapper.java
│   ├── entity/[实体].java         # @TableName("t_xxx")、@TableId(type=AUTO)
│   ├── po/[入参].java
│   └── vo/[出参].java
└── src/test/java/com/[项目包名]/
    └── [模块]ControllerTest.java  # @SpringBootTest 基线测试
```

- `Result<T>`：`{ code:int, message:String, data:T }`，`code==0` 成功
- 错误码：非零整数，per-module 分段，与功能详细设计错误码清单一致
- entity 与 DDL 逐字对应：主键 `id`（`@TableId(type = IdType.AUTO)`）、逻辑删除 `deleted`（`@TableLogic`）

### 2.2 迭代项目（devProjectType == "iteration"）

**就地增改**现有 `backend/`：
- 盘点现有包结构、`Result`、鉴权、分页约定，沿用不另起
- 新增：新 controller/service/mapper/entity/po/vo（对应「新增」接口/表）
- 修改：只改「修改」接口对应的类
- 不重建工程、不覆盖现有代码

## 步骤 3：TDD 按 R 编号（红-绿-重构）

对每个 R 编号：

1. **红**：先写测试——`@SpringBootTest` 基线（正常路径 + 关键异常）；核心逻辑单测用 Mockito（`@Mock/@InjectMocks`）
2. **绿**：实现 `IService → ServiceImpl → Mapper → Controller`，直到测试通过
3. **重构**：清理重复、抽公共，保持测试绿

测试要点：正常路径、参数校验失败、业务错误码、状态流转非法、幂等（如设计有要求）。

## 步骤 4：编译 + 基线测试（交付门槛）

1. `cd backend && mvn -q compile` 必须通过
2. `mvn -q test` 跑基线测试
3. **环境性失败**（如无 MySQL 实例导致 `@SpringBootTest` 起不来）：明确标注「环境性失败 + 原因」，
   不冒充通过；Mockito 纯单测应能通过

## 步骤 5：落盘与更新

### 5.1 更新 .pm-state.json

`devPipeline` 插入/更新 `pm-dev-1-backend` 条目：
`{"step":"pm-dev-1-backend","status":"completed","startedAt":null,"completedAt":"…Z","output":"backend/","counters":{}}`。时间戳 UTC 带 `Z`。

### 5.2 更新 README.md

`### 后端代码（pm-dev-1-backend）` 章节追加一行（5 列：产物/路径/接口数/生成时间/批次），
追加在产物清单末尾（`### 变更记录` 之前）。

## 步骤 6：自检

1. controller 路径对功能详细设计接口清单，动词正确
2. 所有接口返回 `Result<T>`，错误码与设计一致
3. entity 与 DDL 逐字对应（主键 id 自增、deleted 逻辑删除）
4. TDD 先测后实现；`mvn -q compile` 通过
5. 迭代项目就地增改，未重建/未覆盖既有代码
6. devPipeline 条目 6 keys 齐全，时间戳 UTC 带 `Z`
7. README 表 5 列

## 步骤 7：会话内输出摘要

只回（不倒全文）：

```
✅ 后端工程：`output/[项目名]/backend/`

- 项目性质：新项目（新建）/ 迭代（就地增改）
- 实现接口 R [n] 个 · 新增/修改类 [m] 个
- 编译：通过 / 环境性失败(注明原因)
- 基线测试：通过 [x] / 失败 [y]
```
