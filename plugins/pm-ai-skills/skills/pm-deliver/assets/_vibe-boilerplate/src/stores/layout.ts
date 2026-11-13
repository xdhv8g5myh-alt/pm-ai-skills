import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { getSavedCollapsed, setCollapsed, getSavedLayout, setLayout } from '@/theme/applyTheme'

export const useLayoutStore = defineStore('layout', () => {
  // 折叠状态
  const collapsed = ref(getSavedCollapsed())
  watch(collapsed, (v) => setCollapsed(v))

  // 布局模式：side（侧边栏通顶） / top（顶栏通栏）
  const layoutMode = ref<'top' | 'side'>(getSavedLayout())
  watch(layoutMode, (v) => setLayout(v))

  // 表格密度
  const tableDensity = ref<'medium' | 'small' | 'mini'>(
    (localStorage.getItem('arco-pro-table-density') as any) || 'medium'
  )
  watch(tableDensity, (v) => localStorage.setItem('arco-pro-table-density', v))

  function toggle() { collapsed.value = !collapsed.value }
  function setDensity(d: typeof tableDensity.value) { tableDensity.value = d }

  return { collapsed, layoutMode, tableDensity, toggle, setDensity }
})
