/**
 * 原型模板 emoji → FontAwesome 图标批量替换脚本
 * 同时注入 FA CSS <link> 到每个 HTML
 *
 * 用法：node ./scripts/sync-icons.js
 * 工作目录：pm-prototype/assets/（脚本放在 skills/pm-prototype/scripts/）
 */
import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs'
import { resolve, join } from 'path'

const ASSETS_ROOT = resolve(import.meta.dirname, '../assets')

// emoji → FA class 映射（保守映射，确保都有 solid 图标）
const EMOJI_TO_FA = {
  '◉': 'fa-circle',
  '⚡': 'fa-bolt',
  '☀️': 'fa-sun',
  '🌙': 'fa-moon',
  '📊': 'fa-chart-column',
  '📈': 'fa-chart-line',
  '📉': 'fa-chart-area',
  '🗂️': 'fa-folder-open',
  '📁': 'fa-folder',
  '📅': 'fa-calendar-days',
  '✨': 'fa-wand-magic-sparkles',
  '⚙️': 'fa-gear',
  '🎯': 'fa-bullseye',
  '🔍': 'fa-magnifying-glass',
  '👤': 'fa-user',
  '🔔': 'fa-bell',
  '✅': 'fa-check',
  '❌': 'fa-xmark',
  '🚀': 'fa-rocket',
  '💬': 'fa-comments',
  '📝': 'fa-pen',
  '📣': 'fa-bullhorn',
  '🏷️': 'fa-tag',
  '💳': 'fa-credit-card',
  '📱': 'fa-mobile-screen',
  '🌐': 'fa-globe',
  '🔒': 'fa-lock',
  '📦': 'fa-box',
  '📋': 'fa-clipboard-list',
  '🌟': 'fa-star',
  '💡': 'fa-lightbulb',
  '🔥': 'fa-fire',
  '🎨': 'fa-palette',
  '🔧': 'fa-wrench',
  '👀': 'fa-eye',
  '⚠️': 'fa-triangle-exclamation',
  '🔄': 'fa-arrow-rotate-right',
  '➕': 'fa-plus',
  '➖': 'fa-minus',
  '📤': 'fa-arrow-up-right-from-square',
  '📥': 'fa-download',
  '✏️': 'fa-pen',
  '🗑️': 'fa-trash',
  '👥': 'fa-users',
  '🛒': 'fa-cart-shopping',
  '🏢': 'fa-building',
  '🥧': 'fa-chart-pie',
  '🍕': 'fa-chart-pie',
  '🎁': 'fa-gift',
  '🏪': 'fa-store',
  '🧭': 'fa-compass',
  '🔗': 'fa-link',
  '🧧': 'fa-gift',
  '🏆': 'fa-trophy',
  '💼': 'fa-briefcase',
  '🪪': 'fa-id-card',
  '📠': 'fa-print',
  '📮': 'fa-envelope',
  '📱': 'fa-mobile-screen',
  '📡': 'fa-signal',
  '🎪': 'fa-tent',
}

// 收集所有 HTML 文件
function collectHtmlFiles(dir, files = []) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) {
      collectHtmlFiles(full, files)
    } else if (entry.endsWith('.html')) {
      files.push(full)
    }
  }
  return files
}

// 替换策略：emoji 作为纯文本内容 → <span class="fas fa-xxx"></span>
// emoji 后面还有文字（如 "⚠️ 出错"）→ 替换 emoji 为 <span class="fas fa-xxx" style="margin-right:4px"></span>
function replaceEmojis(content) {
  let result = content
  let changed = false

  for (const [emoji, faClass] of Object.entries(EMOJI_TO_FA)) {
    const regex = new RegExp(emoji, 'g')
    if (regex.test(result)) {
      result = result.replace(regex, `<span class="fas ${faClass}"></span>`)
      changed = true
    }
  }
  return { content: result, changed }
}

// 注入 FA CSS link（放在 arco.css 之后）
function injectFaLink(content) {
  if (content.includes('fontawesome.min.css')) return { content, changed: false }

  // 原型模板 link 格式两种：
  //   <link ... href="../_公共资源/vendor/arco.css"/>
  //   <link ... href="../_公共资源/vendor/arco.css" />
  const regex = /href="\.\.\/_公共资源\/vendor\/arco\.css"\s*\/>/
  const match = content.match(regex)
  if (!match) return { content, changed: false }

  const endIdx = match.index + match[0].length
  const afterLine = content.indexOf('\n', endIdx) + 1

  const faLink = '  <link rel="stylesheet" href="../_公共资源/vendor/fontawesome/css/fontawesome.min.css"/>\n'
  const newContent = content.slice(0, afterLine) + faLink + content.slice(afterLine)
  return { content: newContent, changed: true }
}

// 主流程
const htmlFiles = collectHtmlFiles(ASSETS_ROOT)
let emojiChanged = 0, linkChanged = 0

for (const file of htmlFiles) {
  const content = readFileSync(file, 'utf-8')
  const relToAssets = file.slice(ASSETS_ROOT.length + 1)
  const subDir = relToAssets.split('/')[0] // admin / h5 / user-pc / miniapp / _shells

  let { content: c1, changed: ec } = replaceEmojis(content)
  let { content: c2, changed: lc } = injectFaLink(c1)

  if (ec) emojiChanged++
  if (lc) linkChanged++

  if (ec || lc) {
    writeFileSync(file, c2, 'utf-8')
    console.log(`✅ ${relToAssets} ${ec ? '(emoji)' : ''} ${lc ? '(link)' : ''}`)
  }
}

console.log(`\n📊 共处理 ${htmlFiles.length} 个文件`)
console.log(`   emoji 替换：${emojiChanged} 个文件`)
console.log(`   FA link 注入：${linkChanged} 个文件`)
