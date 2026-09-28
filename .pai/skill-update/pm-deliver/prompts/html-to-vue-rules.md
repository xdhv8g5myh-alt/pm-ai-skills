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
