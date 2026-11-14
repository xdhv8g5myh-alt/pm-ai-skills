#!/usr/bin/env python3
"""同步 admin 模板的导航菜单

权威源：list-calendar.html（最完整：list-group 10 项 + system 3 项 + dashboard + help）
修复：复刻 Vibe Design Pro 新增 8 模板后，旧模板导航没跟上

同步范围：
1. <a-menu> 块 — 整个侧边栏导航结构
2. NAV_MAP — 完整路由映射表
3. setup() 里的 openKeys 默认展开值（list-group 应默认展开）

保留：
- 每个文件的 selectedKeys 初始值（当前页自己的 key）
- 每个文件 setup return 里的特有 ref（如 calendarDays、cardData 等）
- selectedKeys.value 的赋值语句
"""
import os
import re

BASE = '/Users/zhangpanlang/Documents/pm-ai'
ADMIN_DIRS = [
    f'{BASE}/pm-ai-platform/docs/public/prototypes/admin',
    f'{BASE}/pm-ai-skills/plugins/pm-ai-skills/skills/pm-prototype/assets/admin',
]

# 提取权威源
SOURCE = f'{BASE}/pm-ai-platform/docs/public/prototypes/admin/list-calendar.html'

with open(SOURCE) as f:
    source = f.read()

# 提取 <a-menu> 块（简化版：每个模板只有一个）
def extract_menu(content):
    idx = content.find('<a-menu')
    if idx == -1:
        return None
    close = content.find('</a-menu>', idx)
    if close == -1:
        return None
    return content[idx:close + len('</a-menu>')]

# 提取 NAV_MAP 对象
def extract_nav_map(content):
    """提取 const NAV_MAP = { ... } 块"""
    idx = content.find('const NAV_MAP = {')
    if idx == -1:
        return None
    # 从 { 开始数括号
    brace_start = content.find('{', idx)
    depth = 0
    i = brace_start
    while i < len(content):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return content[idx:i+1]
        i += 1
    return None

# 提取 selectedKeys 初始值（每个文件自己的默认选中页）
def extract_selected_keys_val(content):
    """找到 const selectedKeys = ref([...])，提取里面的初始 key"""
    m = re.search(r"const selectedKeys\s*=\s*ref\(\[([^\]]*)\]\)", content)
    if m:
        return m.group(1).strip().strip("'").strip('"')
    return None

# 提取 openKeys 默认值
def extract_open_keys_val(content):
    m = re.search(r"const openKeys\s*=\s*ref\(\[([^\]]*)\]\)", content)
    if m:
        return m.group(1).strip()
    return "'list-group'"  # 默认展开 list-group

# 提取 setup return 块
def extract_setup_return(content):
    """提取 setup() return { ... } 块里的特有属性"""
    # 简单做法：找到 return { 到对应的 }
    idx = content.find('return {')
    if idx == -1:
        return None
    brace_start = content.find('{', idx)
    depth = 0
    i = brace_start
    while i < len(content):
        if content[i] == '{': depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return content[idx:i+1]
        i += 1
    return None

source_menu = extract_menu(source)
source_nav_map = extract_nav_map(source)

print(f'权威源：list-calendar.html')
print(f'  菜单块长度：{len(source_menu)} 字符')
print(f'  NAV_MAP 长度：{len(source_nav_map)} 字符')
print()

fixed = 0

for admin_dir in ADMIN_DIRS:
    print(f'\n📁 {admin_dir}')
    for fname in os.listdir(admin_dir):
        if not fname.endswith('.html'):
            continue
        
        fpath = os.path.join(admin_dir, fname)
        with open(fpath) as f:
            content = f.read()
        
        # 这个文件有没有 a-menu？
        if '<a-menu' not in content:
            continue  # exception/login 等简化页跳过
        
        original = content
        
        # 1. 替换 <a-menu> 块
        old_menu = extract_menu(content)
        if old_menu and old_menu != source_menu:
            content = content.replace(old_menu, source_menu)
        
        # 2. 替换 NAV_MAP
        old_map = extract_nav_map(content)
        if old_map and old_map != source_nav_map:
            content = content.replace(old_map, source_nav_map)
        
        if content != original:
            # 3. 替换后，修正 selectedKeys 初始值（保持每个文件自己的）
            # 比如 list-card.html 应该默认选中 list-card，不是 list-calendar
            sel_key = extract_selected_keys_val(original)
            if sel_key:
                content = re.sub(
                    r"const selectedKeys\s*=\s*ref\(\[([^\]]*)\]\)",
                    f"const selectedKeys = ref(['{sel_key}'])",
                    content
                )
            
            # 4. 修正 openKeys（权威源展开 list-group，所有文件都一样）
            content = re.sub(
                r"const openKeys\s*=\s*ref\(\[([^\]]*)\]\)",
                "const openKeys = ref(['list-group'])",
                content
            )
            
            with open(fpath, 'w') as f:
                f.write(content)
            
            rel = os.path.basename(fpath)
            print(f'  ✅ {rel}')
            fixed += 1

print(f'\n📊 共修复 {fixed} 个 HTML')
