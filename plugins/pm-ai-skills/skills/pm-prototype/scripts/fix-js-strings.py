#!/usr/bin/env python3
"""终极修复：JS 数据字符串里的所有 FA HTML 标签 → emoji

根因：sync-icons.mjs 批量替换硬编码 emoji 时，也把 JS 数据 ref 里的值
如 icon: '🏠' → icon: '<span class="fas fa-home"></span>'，
但模板用 {{ }} 文本插值渲染时，Vue 把 HTML 标签当纯文本显示。

本脚本遍历所有模板，定位 JS 字符串值（单引号/双引号）里的 FA HTML 标签，
替换为对应 emoji。模板 HTML 结构里的硬编码 FA 保持不动。
"""
import os
import re

# fa-xxx → emoji 完整映射
FA_TO_EMOJI = {
    'fa-home': '🏠', 'fa-house': '🏠', 'fa-magnifying-glass': '🔍',
    'fa-user': '👤', 'fa-user-circle': '👤', 'fa-user-group': '👥', 'fa-users': '👥',
    'fa-cart-shopping': '🛒', 'fa-shopping-cart': '🛒', 'fa-cart-plus': '🛒',
    'fa-chart-column': '📊', 'fa-chart-bar': '📊', 'fa-chart-line': '📈',
    'fa-chart-area': '📉', 'fa-chart-pie': '🥧',
    'fa-clipboard-list': '📋', 'fa-clipboard': '📋', 'fa-clipboard-check': '✅',
    'fa-pen': '✏️', 'fa-pen-to-square': '✏️', 'fa-pen-fancy': '✏️',
    'fa-check': '✅', 'fa-circle-check': '✅', 'fa-square-check': '☑️',
    'fa-plus': '➕', 'fa-circle-plus': '➕', 'fa-square-plus': '➕',
    'fa-lock': '🔒', 'fa-lock-open': '🔓',
    'fa-building': '🏢', 'fa-city': '🏙️',
    'fa-gauge': '⚡', 'fa-gauge-high': '⚡', 'fa-bolt': '⚡', 'fa-zap': '⚡',
    'fa-wand-magic-sparkles': '✨', 'fa-sparkles': '✨',
    'fa-gear': '⚙️', 'fa-cog': '⚙️', 'fa-sliders': '🎚️',
    'fa-bullseye': '🎯', 'fa-crosshairs': '🎯',
    'fa-tag': '🏷️', 'fa-tags': '🏷️',
    'fa-credit-card': '💳', 'fa-wallet': '💳', 'fa-money-bill': '💰',
    'fa-mobile-screen': '📱', 'fa-mobile': '📱', 'fa-mobile-alt': '📱',
    'fa-globe': '🌐', 'fa-earth-asia': '🌏', 'fa-earth-americas': '🌎',
    'fa-box': '📦', 'fa-archive': '📦',
    'fa-star': '🌟', 'fa-star-half': '⭐', 'fa-star-of-life': '⭐',
    'fa-lightbulb': '💡', 'fa-idea': '💡',
    'fa-fire': '🔥',
    'fa-palette': '🎨', 'fa-paintbrush': '🎨', 'fa-paint-roller': '🎨',
    'fa-wrench': '🔧', 'fa-screwdriver': '🪛', 'fa-hammer': '🔨',
    'fa-eye': '👀', 'fa-eye-slash': '🙈',
    'fa-triangle-exclamation': '⚠️', 'fa-exclamation-triangle': '⚠️', 'fa-circle-exclamation': '❗',
    'fa-arrow-rotate-right': '🔄', 'fa-sync': '🔄', 'fa-rotate': '🔄',
    'fa-arrow-up-right-from-square': '📤', 'fa-external-link': '📤',
    'fa-download': '📥', 'fa-cloud-download': '📥',
    'fa-trash': '🗑️', 'fa-trash-can': '🗑️',
    'fa-store': '🏪', 'fa-storefront': '🏪',
    'fa-compass': '🧭', 'fa-map': '🗺️', 'fa-map-signs': '🗺️',
    'fa-trophy': '🏆', 'fa-award': '🏆', 'fa-medal': '🏅',
    'fa-briefcase': '💼', 'fa-suitcase': '🧳',
    'fa-gift': '🎁', 'fa-gift-wrap': '🎁',
    'fa-envelope': '📮', 'fa-envelope-open': '📬', 'fa-envelope-open-text': '📨',
    'fa-signal': '📡', 'fa-satellite': '📡',
    'fa-circle': '◉', 'fa-circle-dot': '◉', 'fa-dot-circle': '◉',
    'fa-bell': '🔔', 'fa-bell-slash': '🔕', 'fa-envelope-bulk': '📬',
    'fa-comment': '💬', 'fa-comments': '💬', 'fa-comment-dots': '💬',
    'fa-moon': '🌙', 'fa-sun': '☀️',
    'fa-file': '📄', 'fa-file-lines': '📄', 'fa-file-alt': '📄',
    'fa-file-circle': '📄',
    'fa-folder': '📁', 'fa-folder-open': '🗂️', 'fa-folder-plus': '📁',
    'fa-calendar-days': '📅', 'fa-calendar': '📅', 'fa-calendar-alt': '📅',
    'fa-rocket': '🚀', 'fa-rocket-launch': '🚀',
    'fa-robot': '🤖', 'fa-robot-arm': '🦾',
    'fa-database': '🗄️', 'fa-database': '🗄️',
    'fa-diagram-project': '🗺️', 'fa-diagram-venn': '📊',
    'fa-shield-halved': '🛡️', 'fa-shield': '🛡️',
    'fa-check-double': '✅', 'fa-circle-dot': '◉',
    'fa-xmark': '❌', 'fa-circle-xmark': '❌',
    'fa-circle-info': 'ℹ️', 'fa-info': 'ℹ️',
    'fa-circle-question': '❓', 'fa-question': '❓',
    'fa-cubes': '🧩', 'fa-puzzle-piece': '🧩',
    'fa-filter': '🔽', 'fa-filter-circle-dollar': '💲',
    'fa-bars': '☰', 'fa-bars-staggered': '☰',
    'fa-chevron-left': '‹', 'fa-chevron-right': '›',
    'fa-angle-left': '‹', 'fa-angle-right': '›',
    'fa-menu-fold': '☰', 'fa-menu-unfold': '☰',
    'fa-mug-hot': '☕', 'fa-coffee': '☕', 'fa-beer-mug-empty': '🍺',
    'fa-code': '💻', 'fa-terminal': '⌨️', 'fa-keyboard': '⌨️',
    'fa-plug': '🔌', 'fa-usb': '🔌',
    'fa-server': '🖥️', 'fa-desktop': '🖥️', 'fa-laptop': '💻',
    'fa-table': '📊', 'fa-table-cells': '📊',
    'fa-layer-group': '🗂️', 'fa-object-group': '🗂️',
    'fa-eye-dropper': '🎨', 'fa-pipette': '🎨',
    'fa-house-chimney': '🏠', 'fa-office-building': '🏢',
    'fa-industry': '🏭', 'fa-factory': '🏭',
    'fa-handshake': '🤝', 'fa-users-gear': '👥',
    'fa-money-bill-trend-up': '📈', 'fa-arrow-trend-up': '📈',
    'fa-receipt': '🧾', 'fa-file-invoice': '📄',
    'fa-people-group': '👥', 'fa-user-group': '👥',
    'fa-meteor': '🌠', 'fa-comments': '💬',
    'fa-arrow-down-long': '⬇️', 'fa-arrow-up-long': '⬆️',
    'fa-ellipsis': '⋯', 'fa-ellipsis-h': '⋯', 'fa-ellipsis-v': '⋮',
    'fa-paper-plane': '📨', 'fa-send': '📨', 'fa-share': '📤',
    'fa-hand': '✋', 'fa-hand-pointer': '👆', 'fa-thumbs-up': '👍',
    'fa-heart': '❤️', 'fa-heart-crack': '💔',
    'fa-smile': '😊', 'fa-face-smile': '😊', 'fa-face-grin': '😁',
    'fa-circle-half-stroke': '🌗',
    'fa-language': '🌐', 'fa-globe-americas': '🌎',
    'fa-flag': '🚩', 'fa-flag-checkered': '🏁',
    'fa-qrcode': '📱', 'fa-barcode': '📊',
    'fa-id-card': '🪪', 'fa-address-card': '🪪', 'fa-credit-card': '💳',
    'fa-folder-tree': '🗂️', 'fa-sitemap': '🗺️',
}

def fix_js_string_fa(content):
    """把 JS 字符串值里的 <span class="fas fa-xxx"></span> 替换为 emoji"""
    original = content
    
    # 匹配引号 + 可选前缀 + <span class="xxx fa-xxx"></span> + 可选后缀 + 引号
    # 只匹配 JS 字符串里的（引号包裹的）
    pattern = re.compile(
        r"(['\"])((?:[^'\"]*?)<span class=\"(?:fas|far|fal|fab)\s+([^\s\"]+)(?:\s+[^\"]+)?\"></span>([^'\"]*?)(['\"])"
    )
    
    def replacer(m):
        opening = m.group(1)   # ' 或 "
        fa_class = m.group(2)  # fa-home
        suffix = m.group(3)    # 可选后缀（应该为空）
        closing = m.group(4)   # ' 或 "
        
        emoji = FA_TO_EMOJI.get(fa_class, fa_class)
        return f"{opening}{emoji}{suffix}{closing}"
    
    fixed = pattern.sub(replacer, content)
    
    # 同样处理 <i class="fas fa-xxx"></i>
    pattern2 = re.compile(
        r"(['\"])((?:[^'\"]*?)<i class=\"(?:fas|far|fal|fab)\s+([^\s\"]+)(?:\s+[^\"]+)?\"></i>([^'\"]*?)(['\"])"
    )
    
    def replacer2(m):
        opening = m.group(1)
        fa_class = m.group(2)
        suffix = m.group(3)
        closing = m.group(4)
        emoji = FA_TO_EMOJI.get(fa_class, fa_class)
        return f"{opening}{emoji}{suffix}{closing}"
    
    fixed = pattern2.sub(replacer2, fixed)
    
    return fixed, fixed != original

def fix_empty_string_span(content):
    """还有一种情况：引号里只剩 <span ...></span> 没其他内容"""
    pattern = re.compile(
        r"(['\"])<span class=\"(?:fas|far|fal|fab)\s+([^\s\"]+)(?:\s+[^\"]+)?\"></span>(['\"])"
    )
    def replacer(m):
        emoji = FA_TO_EMOJI.get(m.group(2), m.group(2))
        return f"'{emoji}'"
    
    return pattern.sub(replacer, content)

def process_dir(dir_path):
    print(f'\n📁 {dir_path}')
    count = 0
    details = []
    
    for root, dirs, files in os.walk(dir_path):
        # 跳过 _shared / _公共资源 / vendor / _shells
        skip_dirs = {'_shared', '_公共资源', 'vendor', '_shells', '_vibe-boilerplate', 'node_modules'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r') as f:
                content = f.read()
            
            fixed, changed = fix_js_string_fa(content)
            if changed:
                rel = os.path.relpath(fpath, dir_path)
                with open(fpath, 'w') as f:
                    f.write(fixed)
                count += 1
                details.append(f'  ✅ {rel}')
    
    if details:
        for d in details[:15]:
            print(d)
        if len(details) > 15:
            print(f'  ... 还有 {len(details)-15} 个')
    
    return count

if __name__ == '__main__':
    dirs = [
        '/Users/zhangpanlang/Documents/pm-ai/pm-ai-platform/docs/public/prototypes',
        '/Users/zhangpanlang/Documents/pm-ai/pm-ai-skills/plugins/pm-ai-skills/skills/pm-prototype/assets',
    ]
    
    total = 0
    for d in dirs:
        total += process_dir(d)
    
    print(f'\n📊 共修复 {total} 个 HTML 文件')
