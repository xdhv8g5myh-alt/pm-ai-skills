# HTML 到 Vue SFC 转换规则

## 结构转换

| HTML | Vue SFC |
|------|---------|
| `<div id="app" v-cloak>` | `<template>` 根元素 |
| `<style>` 内联样式 | `<style scoped>` |
| `<script>` setup() | `<script setup lang="ts">` |

## JS 转换

| HTML 原型 | Vue SFC |
|-----------|---------|
| `const { ref, reactive } = Vue` | `import { ref, reactive } from 'vue'` |
| `const { createApp } = Vue` | 删除（不需要） |
| `createApp({setup(){...}}).use(ArcoVue).mount('#app')` | 删除（由 main.ts 处理） |
| `window.location.href = 'xxx.html'` | `router.push('/xxx')` |
| `<a href="./xxx.html">` | `<router-link to="/xxx">` |
| `localStorage.getItem/setItem` | 封装到 `src/utils/storage.ts` |

## 组件库转换

| HTML 原型（CDN UMD） | Vue SFC（npm 包） |
|---------------------|-----------------|
| 全局注册，无需导入 | 按需导入或自动导入（unplugin-vue-components） |
| `<a-button>` 等组件名不变 | 组件名不变，但需要 import |
| `.use(ArcoVue)` in script | `app.use(ArcoVue)` in main.ts |

## Mock 数据提取

原型中的 `const MOCK_DATA = {...}` 提取为：

```typescript
// src/api/mock/[模块名].ts
export const MOCK_LIST: [InterfaceName][] = [
  { id: 1, title: '...', ... },
]

// src/api/[模块名].ts
import { MOCK_LIST } from './mock/[模块名]'

export async function getList() {
  if (import.meta.env.DEV) return MOCK_LIST
  // 生产环境：return await request('/api/list')
}
```

## 路由结构

从原型页面文件推断路由配置：

```typescript
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: () => import('@/views/DashboardView.vue') },
    { path: '/list', component: () => import('@/views/ListView.vue') },
    // ...
  ]
})
```

## 常见陷阱与修复

### 多根组件下的 transition / keep-alive

layout 布局组件中，`<transition>` 与 `<keep-alive>` **必须包裹在 `<router-view>` 内层**，禁止放在外层。多根组件（fragment root）配在外层会导致路由渲染异常：

| 症状 | 原因 |
|------|------|
| 菜单点击后页面空白 | 多根组件 + transition 无法确定过渡根节点 |
| 二次进入页面不刷新、读到旧缓存 | keep-alive 缓存键落在 layout 而非页面组件上 |

正确写法：

```vue
<!-- src/layouts/DefaultLayout.vue -->
<template>
  <a-layout>
    <a-layout-sider>...</a-layout-sider>
    <a-layout-content>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <keep-alive :include="cachedViews">
            <component :is="Component" />
          </keep-alive>
        </transition>
      </router-view>
    </a-layout-content>
  </a-layout>
</template>
```

> 若页面组件是**多根节点**（`<template>` 下多个并列元素），transition 会失效。此时给页面组件补一个单一根节点，或对该页面去掉 transition。

### 编译修复循环上限

`npm run build` 或 `vue-tsc` 报错时，自动修复循环**上限 5 轮**。5 轮后仍有错误 → 停止修复，输出完整错误清单交由人工处理，不得无限重试。

