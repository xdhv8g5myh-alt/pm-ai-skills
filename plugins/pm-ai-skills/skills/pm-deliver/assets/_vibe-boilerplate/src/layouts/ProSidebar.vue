<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLayoutStore } from '@/stores/layout'
import router from '@/router'

const layout = useLayoutStore()
const route = useRoute()
const vueRouter = useRouter()

// 从路由 children 自动生成菜单（跳过 login / 404）
interface MenuItem { key: string; title: string; icon?: string }
const menuItems = computed<MenuItem[]>(() => {
  const root = router.options.routes.find(r => r.path === '/')
  if (!root?.children) return []
  return root.children
    .filter(c => c.name && c.meta?.title)
    .map(c => ({
      key: '/' + c.path,
      title: c.meta!.title as string,
      icon: c.meta!.icon as string | undefined,
    }))
})

function onMenuClick(key: string) {
  vueRouter.push(key)
}
</script>

<template>
  <aside class="pro-sider">
    <!-- Logo 区 -->
    <div class="pro-brand">
      <div class="pro-brand-icon">V</div>
      <span class="pro-brand-name" v-show="!layout.collapsed">Vibe Admin</span>
    </div>

    <!-- 菜单区 -->
    <a-menu
      mode="vertical"
      :collapsed="layout.collapsed"
      :selected-keys="[route.path]"
      style="border-right: 0; padding-top: 4px"
      @menu-item-click="onMenuClick"
    >
      <a-menu-item v-for="item in menuItems" :key="item.key">
        <span v-if="item.icon" :class="['fas', item.icon]" />
        {{ item.title }}
      </a-menu-item>
    </a-menu>
  </aside>
</template>
