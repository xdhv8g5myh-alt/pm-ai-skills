---
name: pm-common
description: PM 技能包共享的项目管理规范（目录骨架、编号体系、产物依赖门禁、Blocker 门禁、批次管理）。被 pm-analyze / pm-prototype / pm-prd / pm-deliver / pm-autopilot 在运行时引用，一般无需单独调用。
---

# PM 共享规范

本目录是 pm-* 系列技能包共享的规范引用，实际内容在同目录的 `project-management.md`，由其它技能通过 `${CLAUDE_SKILL_DIR}/../pm-common/project-management.md` 读取。

## 覆盖内容

- 项目目录骨架（`output/[项目名]/` 结构）
- 编号体系（F 功能 / T 测试 / R 接口 / P 页面 / C 变更）
- 产物依赖门禁
- Blocker 门禁
- 批次管理（新建 → 进行中 → 已完成 → 已冻结 → 已归档）

## 使用

单独需要时，直接 Read `${CLAUDE_SKILL_DIR}/project-management.md` 获取完整规范。
