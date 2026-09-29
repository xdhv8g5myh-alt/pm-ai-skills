/**
 * pm-annotate · 标注数据模板
 *
 * 本文件由 pm-annotate 按项目生成，落盘为 `output/[项目名]/_公共资源/pm-annotate-data.js`。
 * 静态引擎 `pm-annotate.js` 在运行时读取 `window.PM_ANNOTATE_TOOLTIPS`，因此本文件
 * **必须先于 `pm-annotate.js` 加载**。
 *
 * 数据来源：`需求文档/[项目名]-PRD-*.md` 的功能点与接口清单。
 * 键 = 标注编号（与页面内 `<i class="pm-anno-anchor" data-n="N">` 的 N 一一对应，1-999）。
 * 每个条目的 title 固定为「需求描述：[功能名]」，html 由以下片段按需拼装。
 */
window.PM_ANNOTATE_TOOLTIPS = {
  1: {
    title: '需求描述：[功能名]',
    html:
      '<p><span class="pm-anno-lbl">功能概述：</span>[一句话说明这个功能做什么、给谁用]</p>'
      + '<p><span class="pm-anno-lbl">页面：</span>[P0xx 页面名] <code>[路由]</code>（[本页第 N 步 / 本模块位置]）</p>'
      + '<p><span class="pm-anno-lbl">交互逻辑：</span></p>'
      + '<ol>'
      + '<li>[用户动作 → 系统响应]</li>'
      + '<li>[校验规则、边界、失败提示]</li>'
      + '</ol>'
      + '<p><span class="pm-anno-lbl">字段说明：</span></p>'
      + '<table><tr><th>字段名</th><th>类型</th><th>必填</th><th>校验规则</th><th>说明</th></tr>'
      + '<tr><td>[字段]</td><td>[string/number/date]</td><td>[是/否]</td><td>[规则]</td><td>[用途]</td></tr>'
      + '</table>'
      + '<p><span class="pm-anno-lbl">使用组件：</span><code>[AButton]</code> <code>[ATable]</code></p>'
      + '<p><span class="pm-anno-lbl">关联接口：</span>[R0xx METHOD] <code>[/api/xxx]</code></p>'
  }

  // 2: { ... } —— 按 PRD 功能点继续追加；无表格/无接口的条目可省略对应片段
};
