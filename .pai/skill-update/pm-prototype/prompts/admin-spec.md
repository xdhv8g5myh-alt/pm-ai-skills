# 管理后台原型规格（Admin）

## 布局结构
```
左侧边栏（220px 展开 / 48px 折叠）
├── Logo 区
└── a-menu（多级菜单）

顶部导航栏（64px，fixed，left 随边栏宽度变化）
├── 左：折叠按钮 + 面包屑
└── 右：搜索 + 通知 + 主题切换 + 头像下拉

主内容区（margin-left 随边栏宽度变化）
└── 面包屑下方的内容卡片
```

## 常用页面类型

### 仪表盘（dashboard）
- 顶部 KPI 卡片（4列）：总数/增长/完成/待处理
- 图表区（a-grid，echarts 占位 div）
- 近期动态列表

### 列表页（list）
- 搜索筛选区（a-form inline）
- 操作按钮区（新增/导出/批量删除）
- a-table（含分页）
- 多状态：loading/empty/error

### 详情页（detail）
- 顶部操作栏（编辑/删除/返回）
- a-descriptions 基本信息
- 下方扩展卡片（日志/关联数据等）

### 新增/编辑表单（form-add）
- a-form（label-col 4列）
- 底部：取消 + 保存草稿 + 提交

### 步骤表单（form-step）
- a-steps（当前步骤）
- 分步内容区
- 上一步/下一步按钮

## 内容区 JS 模式
```js
// 列表页示例
const tableData = ref(MOCK_DATA.list)
const columns = [
  { title: 'ID', dataIndex: 'id', width: 80 },
  { title: '名称', dataIndex: 'title' },
  { title: '状态', dataIndex: 'status' },
  { title: '操作', slotName: 'action', width: 120 }
]
const pagination = reactive({ total: 100, current: 1, pageSize: 10 })
```
