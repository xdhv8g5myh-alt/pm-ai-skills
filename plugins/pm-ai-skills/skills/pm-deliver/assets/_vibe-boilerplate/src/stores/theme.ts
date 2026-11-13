import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { applyTheme, toggleDark, getSavedTheme, getSavedDark } from '@/theme/applyTheme'
import { PRESETS } from '@/theme/presets'

export const useThemeStore = defineStore('theme', () => {
  const themeKey = ref(getSavedTheme())
  const isDark   = ref(getSavedDark())
  const presets  = PRESETS

  function setTheme(key: string) {
    themeKey.value = key
    applyTheme(key)
  }

  function toggleDarkMode() {
    isDark.value = !isDark.value
    toggleDark(isDark.value)
  }

  return { themeKey, isDark, presets, setTheme, toggleDarkMode }
})
