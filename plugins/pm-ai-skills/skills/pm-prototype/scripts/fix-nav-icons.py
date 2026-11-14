#!/usr/bin/env python3
"""修复导航页 JS 数据里的 icon 值（FA HTML → emoji）

根因：之前 sync-icons.mjs 批量替换 emoji 时，也把 index.html 导航页
JS 数据里的 icon: '🔍' 替换成了 icon: '<span class="fas fa-magnifying-glass"></span>'，
但模板用 {{ page.icon }} 文本插值，Vue 把 HTML 当纯文本渲染了。

修复：index.html 导航页 JS 数据里的 icon 值改回 emoji
"""
import os
import re

# FA HTML → emoji 反向映射
FA_TO_EMOJI = {
    'fa-home': '🏠',
    'fa-magnifying-glass': '🔍',
    'fa-user': '👤',
    'fa-users': '👥',
    'fa-user-circle': '👤',
    'fa-cart-shopping': '🛒',
    'fa-chart-column': '📊',
    'fa-chart-line': '📈',
    'fa-chart-area': '📉',
    'fa-clipboard-list': '📋',
    'fa-clipboard': '📋',
    'fa-pen': '✏️',
    'fa-check': '✅',
    'fa-plus': '➕',
    'fa-lock': '🔒',
    'fa-building': '🏢',
    'fa-gauge': '⚡',
    'fa-table': '📊',
    'fa-cubes': '🧩',
    'fa-bullseye': '🎯',
    'fa-wand-magic-sparkles': '✨',
    'fa-bolt': '⚡',
    'fa-circle': '◉',
    'fa-folder': '📁',
    'fa-folder-open': '🗂️',
    'fa-calendar-days': '📅',
    'fa-gear': '⚙️',
    'fa-tag': '🏷️',
    'fa-credit-card': '💳',
    'fa-mobile-screen': '📱',
    'fa-globe': '🌐',
    'fa-box': '📦',
    'fa-star': '🌟',
    'fa-lightbulb': '💡',
    'fa-fire': '🔥',
    'fa-palette': '🎨',
    'fa-wrench': '🔧',
    'fa-eye': '👀',
    'fa-triangle-exclamation': '⚠️',
    'fa-arrow-rotate-right': '🔄',
    'fa-arrow-up-right-from-square': '📤',
    'fa-download': '📥',
    'fa-trash': '🗑️',
    'fa-store': '🏪',
    'fa-compass': '🧭',
    'fa-trophy': '🏆',
    'fa-briefcase': '💼',
    'fa-chart-pie': '🥧',
    'fa-gift': '🎁',
    'fa-envelope': '📮',
    'fa-signal': '📡',
    'fa-database': '🗄️',
    'fa-robot': '🤖',
    'fa-cog': '⚙️',
    'fa-diagram-project': '🗺️',
    'fa-shield-halved': '🛡️',
    'fa-rocket': '🚀',
    'fa-comment-dots': '💬',
    'fa-bell': '🔔',
    'fa-moon': '🌙',
    'fa-sun': '☀️',
    'fa-file': '📄',
    'fa-file-lines': '📄',
    'fa-folder-plus': '📁',
    'fa-plus': '➕',
    'fa-filter': '🔽',
    'fa-bars': '☰',
    'fa-xmark': '❌',
    'fa-chevron-left': '‹',
    'fa-chevron-right': '›',
    'fa-angle-left': '‹',
    'fa-angle-right': '›',
    'fa-menu-fold': '☰',
    'fa-menu-unfold': '☰',
}

def fix_icon_values(content):
    """把 icon: '<span class="fas fa-xxx"></span>' 改回 icon: 'emoji'"""
    original = content
    
    # 匹配 icon: '<span class="fas fa-xxx"></span>' 模式
    # 处理几种变体
    patterns = [
        # icon: '<span class="fas fa-xxx"></span>'
        r'(icon:\s*[\'"<])<span class="fas ([^"]+)"></span>([\'">])',
        # icon: '<i class="fas fa-xxx"></i>'
        r'(icon:\s*[\'"<])<i class="fas ([^"]+)"></i>([\'">])',
        # icon: '<span class="far fa-xxx"></span>'
        r'(icon:\s*[\'"<])<span class="far ([^"]+)"></span>([\'">])',
    ]
    
    changed = False
    for pattern in patterns:
        def replace_match(m):
            prefix = m.group(1)
            fa_class = m.group(2)  # e.g. 'fa-chart-column'
            suffix = m.group(3)
            
            # 提取 fa-xxx 部分
            class_name = fa_class  # 已经是完整 fa-xxx
            
            # 查映射表
            emoji = FA_TO_EMOJI.get(class_name)
            if emoji:
                return f"icon: '{emoji}'"
            else:
                # 没找到映射，保持原样但去掉 span 标签
                return f"icon: '{class_name}'"
        
        content = re.sub(pattern, replace_match, content)
    
    if content != original:
        changed = True
    
    return content, changed

def process_dir(dir_path):
    print(f'\n📁 {dir_path}')
    count = 0
    
    for root, dirs, files in os.walk(dir_path):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r') as f:
                content = f.read()
            
            fixed, changed = fix_icon_values(content)
            if changed:
                with open(fpath, 'w') as f:
                    f.write(fixed)
                rel = os.path.relpath(fpath, dir_path)
                print(f'  ✅ {rel}')
                count += 1
    
    return count

if __name__ == '__main__':
    dirs = [
        '/Users/zhangpanlang/Documents/pm-ai/pm-ai-platform/docs/public/prototypes',
        '/Users/zhangpanlang/Documents/pm-ai/pm-ai-skills/plugins/pm-ai-skills/skills/pm-prototype/assets',
    ]
    
    total = 0
    for d in dirs:
        total += process_dir(d)
    
    print(f'\n📊 共修复 {total} 个 HTML')
