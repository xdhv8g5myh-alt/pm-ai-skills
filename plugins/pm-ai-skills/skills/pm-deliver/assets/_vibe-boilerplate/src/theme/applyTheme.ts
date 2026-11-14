/**
 * 主题切换核心逻辑（复刻 arco-theme.js applyTheme / toggleTheme）
 * - 改 :root CSS 变量（primary-5/6/7）
 * - 切换 body[arco-theme] 属性（Arco 暗色模式）
 * - localStorage 持久化
 */
import { PRESETS, DEFAULT_THEME_KEY, STORAGE } from './presets'

export function applyTheme(key: string) {
  const preset = PRESETS.find(p => p.key === key) ?? PRESETS[0]
  const root = document.documentElement
  const body = document.body

  // :root 层（自定义组件 + 原型 Shell）
  root.style.setProperty('--primary-5', preset.p5)
  root.style.setProperty('--primary-6', preset.p6)
  root.style.setProperty('--primary-7', preset.p7)
  root.style.setProperty('--brand-color', preset.color)

  // body 层（Arco Design 组件必须覆盖 body {} 下的变量）
  body.style.setProperty('--primary-5', preset.p5)
  body.style.setProperty('--primary-6', preset.p6)
  body.style.setProperty('--primary-7', preset.p7)
  body.style.setProperty('--arcoblue-5', preset.p5)
  body.style.setProperty('--arcoblue-6', preset.p6)
  body.style.setProperty('--arcoblue-7', preset.p7)

  localStorage.setItem(STORAGE.themeColor, key)
}

export function toggleDark(isDark: boolean) {
  if (isDark) {
    document.body.setAttribute('arco-theme', 'dark')
    localStorage.setItem(STORAGE.themeMode, 'dark')
  } else {
    document.body.removeAttribute('arco-theme')
    localStorage.setItem(STORAGE.themeMode, 'light')
  }
}

/** 启动时调用：恢复主题 */
export function initTheme() {
  const saved = localStorage.getItem(STORAGE.themeColor) || DEFAULT_THEME_KEY
  applyTheme(saved)

  if (localStorage.getItem(STORAGE.themeMode) === 'dark') {
    document.body.setAttribute('arco-theme', 'dark')
  }
}

export function getSavedTheme(): string {
  return localStorage.getItem(STORAGE.themeColor) || DEFAULT_THEME_KEY
}

export function getSavedDark(): boolean {
  return localStorage.getItem(STORAGE.themeMode) === 'dark'
}

export function getSavedCollapsed(): boolean {
  return localStorage.getItem(STORAGE.menuCollapsed) === 'true'
}

export function setCollapsed(v: boolean) {
  localStorage.setItem(STORAGE.menuCollapsed, String(v))
}

export function getSavedLayout(): 'top' | 'side' {
  return (localStorage.getItem(STORAGE.layoutMode) as 'top' | 'side') || 'side'
}

export function setLayout(mode: 'top' | 'side') {
  localStorage.setItem(STORAGE.layoutMode, mode)
}
