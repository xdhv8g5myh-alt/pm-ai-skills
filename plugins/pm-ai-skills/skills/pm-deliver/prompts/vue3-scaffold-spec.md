# Vue3 项目脚手架规格

## 目录结构

```
[项目名]/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tsconfig.node.json
├── index.html
├── README.md
├── public/
│   └── favicon.ico
└── src/
    ├── main.ts
    ├── App.vue
    ├── router/
    │   └── index.ts
    ├── api/
    │   ├── request.ts         # axios 实例：baseURL / 拦截器 / 统一错误提示
    │   ├── [模块名].ts        # 接口函数（内部 import request）
    │   └── mock/
    │       └── [模块名].ts    # Mock 数据
    ├── types/
    │   └── index.ts           # TypeScript 接口定义
    ├── composables/
    │   └── use[功能名].ts     # 可复用逻辑
    ├── utils/
    │   ├── index.ts
    │   └── storage.ts         # localStorage 读写封装
    └── views/
        ├── [PageName]View.vue
        └── ...
```

## package.json 模板

```json
{
  "name": "[项目名]",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.3.0",
    "@arco-design/web-vue": "^2.55.3"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.3.0",
    "vite": "^5.2.0",
    "vue-tsc": "^2.0.0"
  }
}
```

## vite.config.ts 模板

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': resolve(__dirname, 'src') }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:3000', changeOrigin: true }
    }
  }
})
```

## main.ts 模板

```typescript
import { createApp } from 'vue'
import ArcoVue from '@arco-design/web-vue'
import '@arco-design/web-vue/dist/arco.css'
import router from './router'
import App from './App.vue'

createApp(App).use(ArcoVue).use(router).mount('#app')
```

## tsconfig.json 模板

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```
