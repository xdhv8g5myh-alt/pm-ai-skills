<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLayoutStore } from '@/stores/layout'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import { Modal } from '@arco-design/web-vue'

const layout = useLayoutStore()
const theme  = useThemeStore()
const auth   = useAuthStore()
const route  = useRoute()
const router = useRouter()

// 面包屑
const breadcrumbs = computed(() =>
  route.matched.filter(r => r.meta?.title).map(r => r.meta!.title as string)
)

function onLogout() {
  Modal.confirm({
    title: '确认登出？',
    content: '登出后需要重新登录',
    onOk: () => {
      auth.logout()
      router.push('/login')
    },
  })
}

function onGoProfile() {
  // pm-deliver 后续可扩展
}
</script>

<template>
  <header class="pro-navbar">
    <!-- 左侧：折叠 + 面包屑 -->
    <div style="display:flex;align-items:center;gap:12px">
      <a-button type="text" @click="layout.toggle">
        <span :class="['fas', layout.collapsed ? 'fa-bars' : 'fa-bars']" />
      </a-button>
      <a-breadcrumb>
        <a-breadcrumb-item v-for="(b, i) in breadcrumbs" :key="i">{{ b }}</a-breadcrumb-item>
      </a-breadcrumb>
    </div>

    <!-- 右侧：主题色 + 明暗 + 密度 + 用户 -->
    <div style="display:flex;align-items:center;gap:8px">
      <!-- 主题色选择（5 色） -->
      <div class="theme-color-picker" title="主题色">
        <button
          v-for="p in theme.presets" :key="p.key"
          :style="{ background: p.color }"
          :class="{ active: theme.themeKey === p.key }"
          :title="p.name"
          @click="theme.setTheme(p.key)"
        />
      </div>

      <!-- 明暗切换 -->
      <a-tooltip :content="theme.isDark ? '切换到亮色' : '切换到暗色'">
        <a-button type="text" @click="theme.toggleDarkMode">
          <span :class="['fas', theme.isDark ? 'fa-sun' : 'fa-moon']" />
        </a-button>
      </a-tooltip>

      <!-- 表格密度 -->
      <a-dropdown trigger="click">
        <a-button type="text">
          <span class="fas fa-table" />
          <span style="margin-left:4px">密度</span>
        </a-button>
        <template #content>
          <a-doption value="mini"  @select="layout.setDensity('mini')">紧凑</a-doption>
          <a-doption value="small" @select="layout.setDensity('small')">舒适</a-doption>
          <a-doption value="medium" @select="layout.setDensity('medium')">宽松</a-doption>
        </template>
      </a-dropdown>

      <!-- 用户 -->
      <a-dropdown trigger="click">
        <div style="display:flex;align-items:center;gap:8px;cursor:pointer;padding:4px 8px;border-radius:4px">
          <div style="width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,rgb(var(--primary-6)),rgb(var(--primary-5));display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px">
            {{ auth.user?.name?.charAt(0) || 'A' }}
          </div>
          <span style="font-size:13px">{{ auth.user?.name || '未登录' }}</span>
        </div>
        <template #content>
          <a-doption @select="onGoProfile"><span class="fas fa-user" style="margin-right:8px"/>个人中心</a-doption>
          <a-doption @select="onLogout"><span class="fas fa-right-from-bracket" style="margin-right:8px"/>退出登录</a-doption>
        </template>
      </a-dropdown>
    </div>
  </header>
</template>
