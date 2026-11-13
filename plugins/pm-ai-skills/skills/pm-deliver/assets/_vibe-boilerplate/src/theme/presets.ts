/**
 * Vibe Design Pro · 主题预设（复刻 arco-theme.js PRESETS）
 * 5 种色 + 明暗模式，localStorage 持久化
 * RGB 三值格式，CSS 变量层用 rgb(var(--primary-6)) 引用
 */

export interface ThemePreset {
  key: string
  name: string
  /** 品牌展示色（纯 Hex） */
  color: string
  /** primary-6（RGB 三值，Arco token: --primary-6） */
  p6: string
  p5: string
  p7: string
}

/** Vibe Design Pro 官方 5 预设 + 新增紫色（原型默认） */
export const PRESETS: ThemePreset[] = [
  { key: 'vibe',   name: 'Vibe 紫',    color: '#6C5CE7', p5: '140 125 237', p6: '108 92 231',  p7: '90 75 209'  },
  { key: 'indigo', name: '靛蓝（Vibe默认）', color: '#5B5BD6', p5: '118 118 224', p6: '91 91 214',   p7: '74 74 191'  },
  { key: 'blue',   name: '品牌蓝',    color: '#165DFF', p5: '61 126 255',  p6: '22 93 255',   p7: '18 72 199'  },
  { key: 'green',  name: '生机绿',    color: '#00B42A', p5: '0 210 50',    p6: '0 180 42',    p7: '0 140 33'   },
  { key: 'orange', name: '活力橙',    color: '#FF7D00', p5: '255 158 0',   p6: '255 125 0',   p7: '200 95 0'   },
]

export const DEFAULT_THEME_KEY = 'vibe'

/** 存储键（复刻 arco-theme.js 里的 localStorage key） */
export const STORAGE = {
  themeColor: 'arco-pro-theme-color',
  themeMode:  'arco-pro-theme-mode',
  menuCollapsed: 'arco-pro-menu-collapsed',
  layoutMode: 'arco-pro-layout-mode',
  tableDensity: 'arco-pro-table-density',
}

/** 默认设置（复刻 settings.js ArcoProSettings） */
export const DEFAULT_SETTINGS = {
  menuWidth: 220,
  menuCollapsedWidth: 48,
  navbarHeight: 56,
  layoutMode: 'side' as 'top' | 'side',
  tableDensity: 'medium' as 'medium' | 'small' | 'mini',
  themePersist: true,
}
