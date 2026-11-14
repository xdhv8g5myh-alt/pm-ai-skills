#!/usr/bin/env python3
"""终极修复：主题色切换无效

根因：
- Arco CSS 变量定义在 body {} 下
- theme.css 变量定义在 :root {} 下
- CSS 变量继承链：html(root) → body，body 上的值覆盖 html 上同名变量
- applyTheme() 只改了 document.documentElement(:root)，没改 body

修复：
1. theme.css 加 body {} 块，覆盖 Arco 的 body 层
2. applyTheme() 同时改 document.body.style
"""
import os
import re

def fix_theme_css(content):
    """给 theme.css 加 body {} 块（覆盖 Arco 的 body 层）"""
    # 如果已经有 body { --primary-1 就跳过
    if 'body { --primary-1' in content or 'body{' in content and '--primary-6' in content:
        return content
    
    # 在文件末尾加 body 覆盖块
    body_block = """
/* 覆盖 Arco CSS body {} 层的变量（Arco 变量在 body 下定义，:root 覆盖不了）*/
body {
  --primary-1: 242 240 255;
  --primary-2: 230 226 252;
  --primary-3: 205 198 248;
  --primary-4: 175 164 243;
  --primary-5: 140 125 237;
  --primary-6: 108 92 231;
  --primary-7: 90 75 209;
  --primary-8: 83 53 165;
  --primary-9: 68 35 140;
  --primary-10: 42 16 110;

  --arcoblue-1: 242 240 255;
  --arcoblue-2: 230 226 252;
  --arcoblue-3: 205 198 248;
  --arcoblue-4: 175 164 243;
  --arcoblue-5: 140 125 237;
  --arcoblue-6: 108 92 231;
  --arcoblue-7: 90 75 209;
  --arcoblue-8: 83 53 165;

  --link-1: var(--primary-1);
  --link-2: var(--primary-2);
  --link-3: var(--primary-3);
  --link-4: var(--primary-4);
  --link-5: var(--primary-5);
  --link-6: var(--primary-6);
  --link-7: var(--primary-7);
  --link-8: var(--primary-8);
}
"""
    return content.rstrip() + '\n' + body_block + '\n'

def fix_apply_theme(content):
    """applyTheme 同时改 body.style"""
    # 已经有 body.style 就跳过
    if 'document.body.style.setProperty' in content or 'body.style.setProperty' in content:
        return content
    
    # 找到 applyTheme 函数里 setProperty('--primary-7', t.p7) 那一行
    marker = "r.style.setProperty('--primary-7', t.p7)"
    if marker not in content:
        return content
    
    body_code = """
      /* 同时改 body.style — Arco CSS 变量定义在 body {} 下，必须覆盖 */
      var b = document.body;
      b.style.setProperty('--primary-1', t.p1);
      b.style.setProperty('--primary-5', t.p5);
      b.style.setProperty('--primary-6', t.p6);
      b.style.setProperty('--primary-7', t.p7);
      b.style.setProperty('--arcoblue-1', t.p1);
      b.style.setProperty('--arcoblue-5', t.p5);
      b.style.setProperty('--arcoblue-6', t.p6);
      b.style.setProperty('--arcoblue-7', t.p7);
      b.style.setProperty('--color-primary', 'rgb(' + t.p6 + ')')"""
    
    return content.replace(marker, marker + body_code)

def process_dir(dir_path):
    print(f'\n📁 {dir_path}')
    html_count = 0
    css_count = 0
    
    # theme.css
    for root, dirs, files in os.walk(dir_path):
        if 'theme.css' in files:
            css_path = os.path.join(root, 'theme.css')
            rel = os.path.relpath(css_path, dir_path)
            with open(css_path, 'r') as f:
                content = f.read()
            fixed = fix_theme_css(content)
            if fixed != content:
                with open(css_path, 'w') as f:
                    f.write(fixed)
                print(f'  ✅ {rel} 加 body {{}} 覆盖块')
                css_count += 1
    
    # HTML
    for root, dirs, files in os.walk(dir_path):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r') as f:
                content = f.read()
            
            fixed = fix_apply_theme(content)
            if fixed != content:
                with open(fpath, 'w') as f:
                    f.write(fixed)
                rel = os.path.relpath(fpath, dir_path)
                print(f'  ✅ {rel} applyTheme 加 body.style')
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
