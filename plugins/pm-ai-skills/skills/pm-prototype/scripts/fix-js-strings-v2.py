#!/usr/bin/env python3
"""终极修复 v2：JS 数据字符串里的 FA HTML 标签 → emoji

简单可靠的逐行处理 + 上下文判断
"""
import os

# fa-xxx → emoji 映射（常用的）
FA_TO_EMOJI = {
    'fa-home': '🏠', 'fa-house': '🏠', 'fa-magnifying-glass': '🔍',
    'fa-user': '👤', 'fa-user-circle': '👤', 'fa-user-group': '👥', 'fa-users': '👥',
    'fa-cart-shopping': '🛒', 'fa-shopping-cart': '🛒',
    'fa-chart-column': '📊', 'fa-chart-bar': '📊', 'fa-chart-line': '📈',
    'fa-chart-area': '📉', 'fa-chart-pie': '🥧',
    'fa-clipboard-list': '📋', 'fa-clipboard': '📋',
    'fa-pen': '✏️', 'fa-pen-to-square': '✏️',
    'fa-check': '✅', 'fa-circle-check': '✅',
    'fa-plus': '➕', 'fa-circle-plus': '➕',
    'fa-lock': '🔒', 'fa-building': '🏢',
    'fa-gauge': '⚡', 'fa-bolt': '⚡', 'fa-wand-magic-sparkles': '✨',
    'fa-gear': '⚙️', 'fa-cog': '⚙️',
    'fa-bullseye': '🎯', 'fa-tag': '🏷️', 'fa-tags': '🏷️',
    'fa-credit-card': '💳', 'fa-mobile-screen': '📱', 'fa-globe': '🌐',
    'fa-box': '📦', 'fa-archive': '📦',
    'fa-star': '🌟', 'fa-lightbulb': '💡', 'fa-fire': '🔥',
    'fa-palette': '🎨', 'fa-paintbrush': '🎨',
    'fa-wrench': '🔧', 'fa-triangle-exclamation': '⚠️', 'fa-exclamation-triangle': '⚠️',
    'fa-arrow-rotate-right': '🔄', 'fa-sync': '🔄',
    'fa-arrow-up-right-from-square': '📤', 'fa-download': '📥',
    'fa-trash': '🗑️', 'fa-store': '🏪', 'fa-compass': '🧭', 'fa-trophy': '🏆',
    'fa-briefcase': '💼', 'fa-gift': '🎁',
    'fa-envelope': '📮', 'fa-signal': '📡',
    'fa-circle': '◉', 'fa-dot-circle': '◉', 'fa-bell': '🔔',
    'fa-comment': '💬', 'fa-comments': '💬', 'fa-comment-dots': '💬',
    'fa-moon': '🌙', 'fa-sun': '☀️',
    'fa-file': '📄', 'fa-file-lines': '📄',
    'fa-folder': '📁', 'fa-folder-open': '🗂️', 'fa-folder-plus': '📁',
    'fa-calendar-days': '📅', 'fa-calendar': '📅',
    'fa-rocket': '🚀', 'fa-robot': '🤖', 'fa-database': '🗄️',
    'fa-diagram-project': '🗺️', 'fa-shield-halved': '🛡️', 'fa-shield': '🛡️',
    'fa-xmark': '❌', 'fa-circle-info': 'ℹ️', 'fa-circle-question': '❓',
    'fa-cubes': '🧩', 'fa-filter': '🔽', 'fa-bars': '☰',
    'fa-chevron-left': '‹', 'fa-chevron-right': '›',
    'fa-angle-left': '‹', 'fa-angle-right': '›',
    'fa-code': '💻', 'fa-terminal': '⌨️', 'fa-keyboard': '⌨️',
    'fa-mug-hot': '☕', 'fa-coffee': '☕',
    'fa-handshake': '🤝', 'fa-money-bill-trend-up': '📈',
    'fa-user-group': '👥', 'fa-people-group': '👥',
    'fa-id-card': '🪪', 'fa-address-card': '🪪',
    'fa-folder-tree': '🗂️', 'fa-sitemap': '🗺️',
    'fa-table': '📊', 'fa-layer-group': '🗂️',
    'fa-circle-half-stroke': '🌗', 'fa-language': '🌐',
    'fa-flag': '🚩', 'fa-qrcode': '📱',
    'fa-check-double': '✅', 'fa-circle-dot': '◉',
    'fa-circle-exclamation': '❗', 'fa-circle-xmark': '❌',
    'fa-check-circle': '✅',
    'fa-bolt-lightning': '⚡', 'fa-lightning-bolt': '⚡',
    'fa-sparkles': '✨', 'fa-magic': '✨',
    'fa-sliders': '🎚️', 'fa-toolbox': '🧰',
    'fa-circle-plus': '➕', 'fa-square-plus': '➕',
    'fa-circle-trash': '🗑️', 'fa-square-xmark': '❌',
    'fa-circle-check': '✅', 'fa-square-check': '☑️',
    'fa-circle-info': 'ℹ️', 'fa-circle-question': '❓',
    'fa-plus-large': '➕', 'fa-minus': '➖', 'fa-minus-large': '➖',
    'fa-backward': '⏮️', 'fa-forward': '⏭️', 'fa-play': '▶️', 'fa-pause': '⏸️',
    'fa-stop': '⏹️', 'fa-record': '⏺️',
    'fa-skip-backward': '⏮️', 'fa-skip-forward': '⏭️',
}

def fix_line_fa_in_quotes(line):
    """如果一行里有引号包裹的 <span class="fas fa-xxx"></span>，替换为 emoji"""
    original = line
    changed = False
    
    # 逐个处理 FA 类名
    for fa_class, emoji in FA_TO_EMOJI.items():
        # 模式1: '<span class="fas fa-xxx"></span>'  （单引号包裹）
        pat1 = f"'<span class=\"fas {fa_class}\"></span>'"
        if pat1 in line:
            line = line.replace(pat1, f"'{emoji}'")
            changed = True
        # 模式2: "<span class=\"fas fa-xxx\"></span>" （双引号包裹）
        pat2 = f'"<span class=\"fas {fa_class}\"></span>"'
        if pat2 in line:
            line = line.replace(pat2, f'"{emoji}"')
            changed = True
        # 模式3: '<i class="fas fa-xxx"></i>'
        pat3 = f"'<i class=\"fas {fa_class}\"></i>'"
        if pat3 in line:
            line = line.replace(pat3, f"'{emoji}'")
            changed = True
        # 模式4: 带其他 fas 类的（如 fas fa-xxx text-red）
        import re2_missing
        # 直接用简单字符串查找：只要引号里有 <span class="fas fa-xxx 或 <span class="fas fa-xxx">
        for prefix in ["'<span class=\"fas ", "'<i class=\"fas ", '"<span class=\"fas ', '"<i class=\"fas ']:
            for suffix in ['"></span>', '"></i>']:
                # 检查引号位置
                token = prefix + fa_class + suffix
                if token in line:
                    # 确认它在引号里（前后应该有引号）
                    idx = line.find(token)
                    if idx >= 0:
                        # 向前找最近的引号
                        before = line[:idx]
                        last_quote = -1
                        for q in ['"', "'"]:
                            p = before.rfind(q)
                            if p > last_quote:
                                last_quote = p
                        # 向后找最近的引号
                        after = line[idx + len(token):]
                        next_quote = len(line)
                        for q in ['"', "'"]:
                            p = after.find(q)
                            if p >= 0 and p < next_quote:
                                next_quote = p
                        # 如果前后都有引号，说明这是个 JS 字符串
                        if last_quote >= 0 and next_quote < len(after):
                            line = line.replace(token, emoji)
                            changed = True
    
    return line, changed

def process_file(fpath):
    """逐行处理文件"""
    with open(fpath) as f:
        lines = f.readlines()
    
    new_lines = []
    changed = False
    
    for line in lines:
        # 跳过纯 HTML 模板行（不含引号赋值的）
        # 这些行只包含 <div class="fas ..."></div> 这种硬编码
        if '<span class="fas ' in line or '<i class="fas ' in line:
            # 检查是不是 JS 数据定义行（有 = ref([ 或 icon: 或 status: 等字段）
            if re.search(r"(:\s*)?", line):  # 简单启发式
                new_line, l_changed = fix_line_fa_in_quotes(line)
                if l_changed:
                    changed = True
                new_lines.append(new_line)
                continue
        new_lines.append(line)
    
    return changed, ''.join(new_lines)

def process_dir(dir_path):
    print(f'\n📁 {dir_path}')
    count = 0
    
    for root, dirs, files in os.walk(dir_path):
        skip = {'_shared', '_公共资源', 'vendor', '_shells', 'node_modules'}
        dirs[:] = [d for d in dirs if d not in skip]
        
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            
            # 简单粗暴：直接全局替换引号里的 FA HTML
            with open(fpath) as f:
                content = f.read()
            
            new_content = content
            file_changed = False
            
            for fa_class, emoji in FA_TO_EMOJI.items():
                # 各种可能的引号包裹形式
                patterns = [
                    # '<span class="fas fa-xxx"></span>'
                    f"'<span class=\"fas {fa_class}\"></span>'",
                    # "<span class=\"fas fa-xxx\"></span>"
                    f'"<span class=\"fas {fa_class}\"></span>"',
                    # '<i class="fas fa-xxx"></i>'
                    f"'<i class=\"fas {fa_class}\"></i>'",
                    # "<i class=\"fas fa-xxx\"></i>"
                    f'"<i class=\"fas {fa_class}\"></i>"',
                ]
                for pat in patterns:
                    if pat in new_content:
                        new_content = new_content.replace(pat, f"'{emoji}'" if pat.startswith("'") else f'"{emoji}"')
                        file_changed = True
                
                # 扩展形式：有额外 fas 类的，如 fa-xxx text-red
                import re as _re
                regexes = [
                    (_re.compile(rf"'<span class=\"(?:fas|far|fal|fab)\s+{_re.escape(fa_class)}(?:\s+[^\"]*)?\"></span>'"), f"'{emoji}'"),
                    (_re.compile(rf'"<span class=\"(?:fas|far|fal|fab)\s+{_re.escape(fa_class)}(?:\s+[^\"]*)?\"></span>"'), f'"{emoji}"'),
                    (_re.compile(rf"'<i class=\"(?:fas|far|fal|fab)\s+{_re.escape(fa_class)}(?:\s+[^\"]*)?\"></i>'"), f"'{emoji}'"),
                    (_re.compile(rf'"<i class=\"(?:fas|far|fal|fab)\s+{_re.escape(fa_class)}(?:\s+[^\"]*)?\"></i>"'), f'"{emoji}"'),
                ]
                for rx, repl in regexes:
                    new_content = rx.sub(repl, new_content)
            
            if new_content != content:
                rel = os.path.relpath(fpath, dir_path)
                with open(fpath, 'w') as f:
                    f.write(new_content)
                print(f'  ✅ {rel}')
                count += 1
    
    return count

if __name__ == '__main__':
    import re
    dirs = [
        '/Users/zhangpanlang/Documents/pm-ai/pm-ai-platform/docs/public/prototypes',
        '/Users/zhangpanlang/Documents/pm-ai/pm-ai-skills/plugins/pm-ai-skills/skills/pm-prototype/assets',
    ]
    
    total = 0
    for d in dirs:
        total += process_dir(d)
    
    print(f'\n📊 共修复 {total} 个 HTML 文件')
