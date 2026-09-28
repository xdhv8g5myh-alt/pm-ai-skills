# 移动端 H5 原型规格

## 布局结构
```
.h5-body（灰色背景）
└── .h5-phone（375px 居中，手机框）
    ├── .h5-status（状态栏，显示时间+电池）
    ├── .h5-navbar（44px，顶部导航）
    ├── .h5-content（主内容区，overflow-y auto）
    └── .h5-tabbar（56px，底部Tab，部分页面无）
```

## theme.css 已定义的 H5 类（直接使用，不要重复定义）
`.h5-body` `.h5-phone` `.h5-status` `.h5-navbar` `.h5-navbar-back` `.h5-navbar-title`
`.h5-navbar-action` `.h5-content` `.h5-tabbar` `.h5-tab` `.h5-tab.active`
`.h5-section` `.h5-section-title` `.h5-cell` `.h5-cell-icon` `.h5-cell-body`
`.h5-cell-title` `.h5-cell-desc` `.h5-cell-right` `.h5-banner` `.h5-grid`
`.h5-grid-item` `.h5-grid-icon` `.h5-grid-label` `.h5-tag-*` `.h5-form-field`

## TabBar 页（有底部Tab）
首页、列表/发现页

## 无 TabBar 页
详情页、表单页、成功页、搜索页

## 常用页面类型

### 首页（home）
- 顶部 Banner（渐变背景）
- 快捷入口 Grid（4列，8格）
- 内容列表（.h5-cell）

### 列表页（list）
- 搜索框
- 筛选 Tab（a-tabs）
- .h5-cell 列表（带状态 tag）

### 详情页（detail）
- 顶部信息卡（带状态）
- .h5-section 内容段落
- .h5-cell 字段列表
- 底部固定操作按钮（2个）

### 表单页（form）
- .h5-form-field 布局
- a-input/a-select/a-textarea
- 底部固定：取消 + 提交

### 成功页（success）
- 大 ✅ 图标（80px）
- 标题+副标题
- 操作按钮
