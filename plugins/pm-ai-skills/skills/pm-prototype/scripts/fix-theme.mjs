/**
 * 批量修复：主题色切换 + 明暗按钮 v-html
 * 用法：node ./scripts/fix-theme.mjs <目录1> <目录2> ...
 * 同时修复 pm-prototype 资产 + VitePress 公共目录
 */
import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs'
import { join } from 'path'

function collectHtmlFiles(dir, files = []) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) collectHtmlFiles(full, files)
    else if (entry.endsWith('.html')) files.push(full)
  }
  return files
}

function fixToggleBtn(content) {
  // Bug：{{ isDark ? '<span class="fas fa-sun"></span>' : '<span class="fas fa-moon"></span>' }}
  // 用 {{ }} 会被 Vue 当作文本转义
  // 改为 v-html: <span v-html="isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>'"></span>
  // 注意：FA 用 <i> 更标准，class 从 fas 改为 fa（FA6 默认）
  return content.replace(
    /\{\{\s*isDark\s*\?\s*'<span class="fas fa-sun"><\/span>'\s*:\s*'<span class="fas fa-moon"><\/span>'\s*\}\}/g,
    '☼☾_REPLACED_vhtml_☼☾'
  ).replace(
    /\{\{\s*isDark\s*\?\s*"sun"\s*:\s*"moon"\s*\}\}/g,
    '☼☾_REPLACED_icon_☼☾'
  )
}

function fixApplyTheme(content) {
  // Bug：applyTheme 只改了 --primary-*，没改 Arco 的 --arcoblue-*
  // 在 applyTheme 函数里加入 arcoblue 覆盖
  if (!content.includes('function applyTheme')) return content
  if (content.includes('--arcoblue-6')) return content // 已修过

  // 找到 setProperty('--primary-7', t.p7) 那一行，在后面插入 arcoblue 覆盖
  const marker = "r.style.setProperty('--primary-7', t.p7)"
  if (!content.includes(marker)) return content

  const injection = `
      /* 同步覆盖 Arco Design --arcoblue-* 变量（按钮/标签/链接等组件跟随主题色变）*/
      r.style.setProperty('--arcoblue-1', t.p1)
      r.style.setProperty('--arcoblue-2', t.p1)
      r.style.setProperty('--arcoblue-3', t.p5)
      r.style.setProperty('--arcoblue-4', t.p5)
      r.style.setProperty('--arcoblue-5', t.p5)
      r.style.setProperty('--arcoblue-6', t.p6)
      r.style.setProperty('--arcoblue-7', t.p7)
      r.style.setProperty('--arcoblue-8', t.p7)
      /* 同步覆盖 color-primary（自定义通用组件引用）*/
      r.style.setProperty('--color-primary', 'rgb(' + t.p6 + ')')`

  return content.replace(marker, marker + injection)
}

// 修复 theme.css：加 arcoblue 覆盖
function fixThemeCss(content) {
  if (content.includes('--arcoblue-1')) return content // 已修过
  // 在 :root 里加 arcoblue 变量别名
  const marker = '--color-primary:     rgb(var(--primary-6, 108 92 231));'
  if (!content.includes(marker)) return content
  const injection = `
  /* 覆盖 Arco Design CSS 变量 — 让 a-button/a-tag/a-link 跟随主题 */
  --arcoblue-1: 242 240 255;
  --arcoblue-2: 230 226 252;
  --arcoblue-3: 175 164 243;
  --arcoblue-4: 140 125 237;
  --arcoblue-5: 140 125 237;
  --arcoblue-6: 108 92 231;
  --arcoblue-7: 90 75 209;
  --arcoblue-8: 83 53 165;`
  return content.replace(marker, injection + '\n  ' + marker)
}

// 主流程
const dirs = process.argv.slice(2)
if (dirs.length === 0) {
  console.log('用法：node fix-theme.mjs <dir1> <dir2> ...')
  process.exit(1)
}

let htmlFixed = 0, cssFixed = 0

for (const dir of dirs) {
  console.log(`\n📁 处理目录：${dir}`)

  // 1. 修 theme.css
  const cssPath = join(dir, '_shared', 'theme.css')
  try {
    let content = readFileSync(cssPath, 'utf-8')
    const fixed = fixThemeCss(content)
    if (fixed !== content) {
      writeFileSync(cssPath, fixed, 'utf-8')
      console.log('  ✅ theme.css 加 arcoblue 覆盖')
      cssFixed++
    }
  } catch { /* 可能是 _公共资源 */ }

  const cssPath2 = join(dir, '_公共资源', 'theme.css')
  try {
    let content = readFileSync(cssPath2, 'utf-8')
    const fixed = fixThemeCss(content)
    if (fixed !== content) {
      writeFileSync(cssPath2, fixed, 'utf-8')
      console.log('  ✅ _公共资源/theme.css 加 arcoblue 覆盖')
      cssFixed++
    }
  } catch {}

  // 2. 修 HTML
  const htmlFiles = collectHtmlFiles(dir)
  for (const file of htmlFiles) {
    let content = readFileSync(file, 'utf-8')
    let changed = false

    // Bug 1: applyTheme 缺 arcoblue
    let c1 = fixApplyTheme(content)
    if (c1 !== content) { changed = true; content = c1 }

    // Bug 2: 明暗按钮 v-html
    let c2 = fixToggleBtn(content)
    if (c2 !== content) { changed = true; content = c2 }

    if (changed) {
      writeFileSync(file, content, 'utf-8')
      const rel = file.slice(dir.length + 1)
      console.log(`  ✅ ${rel} 已修复`)
      htmlFixed++
    }
  }
}

console.log(`\n📊 共修复 ${htmlFixed} 个 HTML + ${cssFixed} 个 CSS`)
