# 微信小程序模拟原型规格

## 布局结构
```
.mp-shell（375px，手机外框，圆角，阴影）
├── .mp-statusbar（44px，黑色状态栏）
├── .mp-navbar（44px，白色导航）
├── .mp-content（主内容，background: #f7f8fa）
└── .mp-tabbar（56px，底部Tab）
```

## theme.css / 内联 CSS 已定义的类
`.mp-shell` `.mp-statusbar` `.mp-navbar` `.mp-navbar-back` `.mp-navbar-title`
`.mp-content` `.mp-tabbar` `.mp-tab` `.mp-tab.active`
`.mp-section` `.mp-section-title` `.mp-cell` `.mp-cell-icon` `.mp-cell-body`
`.mp-banner` `.mp-grid` `.mp-grid-item` `.mp-tag-*` `.mp-form-item`

注意：miniapp 样式通常内联在各页面 `<style>` 中，不依赖 theme.css 的 h5 类。

## TabBar 颜色
激活色使用微信绿：`#07c160`

## 常用页面类型

### 首页（home）
- Banner（绿色渐变）
- 8格快捷入口
- 内容列表

### 列表页（list）
- 搜索框（圆角白色）
- 横向分类 Tab
- .mp-cell 列表

### 详情页（detail）
- 顶部信息卡
- 内容区 + 字段列表
- 底部固定双按钮

### 表单页（form）
- .mp-form-item 布局
- 底部提交 + 成功态切换
