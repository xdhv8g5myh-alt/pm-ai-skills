<script setup lang="ts">
import { computed } from 'vue'
import ProSidebar from './ProSidebar.vue'
import ProNavbar from './ProNavbar.vue'
import { useLayoutStore } from '@/stores/layout'

const layout = useLayoutStore()

const layoutClass = computed(() => [
  layout.layoutMode,              // 'top' or 'side'
  layout.collapsed ? 'collapsed' : '',
])
</script>

<template>
  <div class="pro-layout">
    <ProSidebar v-if="layout.layoutMode === 'side'" :class="layoutClass" />
    <ProNavbar  :class="layoutClass" />
    <main class="pro-main" :class="[layout.layoutMode, layout.collapsed ? 'collapsed' : '']">
      <div class="pro-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>
