#!/usr/bin/env python3
"""批量修复原型模板：主题色切换 + 明暗按钮

修复内容：
1. theme.css 加 --arcoblue-* 变量覆盖（Arco Design 组件跟随主题色变）
2. 所有 HTML 的 applyTheme() 函数加 --arcoblue-* setProperty
3. 明暗切换按钮：{{ isDark ? '<span ...>' : '<span ...>' }} → v-if/v-else
"""
import os
import re

ARCoblue_INJECTION = """
      /* 同步覆盖 Arco Design --arcoblue-* 变量（按钮/标签/链接等组件跟随主题色变）*/
      r.style.setProperty('--arcoblue-1', t.p1)
      r.style.setProperty('--arcoblue-2', t.p1)
      r.style.setProperty('--arcoblue-3', t.p5)
      r.style.setProperty('--arcoblue-4', t.p5)
      r.style.setProperty('--arcoblue-5', t.p5)
      r.style.setProperty('--arcoblue-6', t.p6)
      r.style.setProperty('--arcoblue-7', t.p7)
      r.style.setProperty('--arcoblue-8', t.p7)
      r.style.setProperty('--color-primary', 'rgb(' + t.p6 + ')')"""

ARCoblue_CSS = """
  /* 覆盖 Arco Design CSS 变量 — 让 a-button/a-tag/a-link 跟随主题 */
  --arcoblue-1: 242 240 255;
  --arcoblue-2: 230 226 252;
  --arcoblue-3: 175 164 243;
  --arcoblue-4: 140 125 237;
  --arcoblue-5: 140 125 237;
  --arcoblue-6: 108 92 231;
  --arcoblue-7: 90 75 209;
  --arcoblue-8: 83 53 165;"""

# 明暗按钮：{{ }} 里的 fas sun/moon 替换为 v-if/v-else 直接渲染
# 匹配各种变体
DARK_BTN_PATTERNS = [
    # 带 tooltip content 在内联的情况
    (r'\{\{\s*isDark\s*\?\s*[\'"]([^"]*fa-sun[^"]*)[\'"]\s*:\s*[\'"]([^"]*fa-moon[^"]*)[\'"]\s*\}\}',
     '<i v-if="isDark" class="fas fa-sun"></i><i v-else class="fas fa-moon"></i>'),
]

def fix_theme_css(content):
    """给 theme.css 加 arcoblue 覆盖"""
    if '--arcoblue-1' in content:
        return content
    marker = '--color-primary:     rgb(var(--primary-6, 108 92 231));'
    if marker not in content:
        return content
    return content.replace(marker, ARCoblue_CSS + '\n  ' + marker)

def fix_apply_theme(content):
    """给 applyTheme 函数加 arcoblue setProperty"""
    if '--arcoblue-6' in content:
        return content
    marker = "r.style.setProperty('--primary-7', t.p7)"
    if marker not in content:
        return content
    return content.replace(marker, marker + ARCoblue_INJECTION)

def fix_toggle_btn(content):
    """修复明暗按钮：{{ }} 替换为 v-if/v-else"""
    original = content
    
    # 模式1：{{ isDark ? '<span class="fas fa-sun"></span>' : '<span class="fas fa-moon"></span>' }}
    content = re.sub(
        r'\{\{\s*isDark\s*\?\s*[\'<]([^<>]*fa-sun[^<>]*)[\'>]\s*:\s*[\'<]([^<>]*fa-moon[^<>]*)[\'>]\s*\}\}',
        '<i v-if="isDark" class="fas fa-sun"></i><i v-else class="fas fa-moon"></i>',
        content
    )
    
    # 模式2：{{ isDark ? 'fa-sun' : 'fa-moon' }} 等更短的
    content = re.sub(
        r'\{\{\s*isDark\s*\?\s*[\'"]fa-sun[\'"]\s*:\s*[\'"]fa-moon[\'"]\s*\}\}',
        '<i v-if="isDark" class="fas fa-sun"></i><i v-else class="fas fa-moon"></i>',
        content
    )
    
    return content

def process_dir(dir_path):
    """处理一个目录"""
    print(f'\n📁 {dir_path}')
    html_count = 0
    css_count = 0
    
    # theme.css
    for css_name in ['theme.css']:
        for root, dirs, files in os.walk(dir_path):
            if css_name in files:
                css_path = os.path.join(root, css_name)
                rel = os.path.relpath(css_path, dir_path)
                with open(css_path, 'r') as f:
                    content = f.read()
                fixed = fix_theme_css(content)
                if fixed != content:
                    with open(css_path, 'w') as f:
                        f.write(fixed)
                    print(f'  ✅ {rel} 加 arcoblue 覆盖')
                    css_count += 1
                break
    
    # HTML 文件
    for root, dirs, files in os.walk(dir_path):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r') as f:
                content = f.read()
            
            changed = False
            
            # 修 applyTheme
            c1 = fix_apply_theme(content)
            if c1 != content:
                content = c1
                changed = True
            
            # 修 toggle btn
            c2 = fix_toggle_btn(content)
            if c2 != content:
                content = c2
                changed = True
            
            if changed:
                with open(fpath, 'w') as f:
                    f.write(content)
                rel = os.path.relpath(fpath, dir_path)
                print(f'  ✅ {rel}')
                html_count += 1
    
    return html_count, css_count

if __name__ == '__main__':
    dirs = [
        '/Users/zhangpanlang/Documents/pm-ai/pm-ai-platform/docs/public/prototypes',
        '/Users/zhangpanlang/Documents/pm-ai/pm-ai-skills/plugins/pm-ai-skills/skills/pm-prototype/assets',
    ]
    
    total_html = 0
    total_css = 0
    
    for d in dirs:
        h, c = process_dir(d)
        total_html += h
        total_css += c
    
    print(f'\n📊 共修复 {total_html} 个 HTML + {total_css} 个 CSS')
