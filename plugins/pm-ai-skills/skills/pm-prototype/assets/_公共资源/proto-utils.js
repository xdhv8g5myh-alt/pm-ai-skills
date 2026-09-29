/**
 * PM 原型库 · 公共工具
 * 提供：原型调试工具条、状态切换、Mock 数据生成器
 */

;(function(window) {
  'use strict';

  const Proto = {};

  // ─── 原型调试工具条 ───────────────────────────────────────────
  // 用法：Proto.initToolbar({ page: '列表页', section: '管理后台' })
  Proto.initToolbar = function(opts) {
    opts = opts || {};
    const bar = document.createElement('div');
    bar.className = 'proto-toolbar';
    bar.innerHTML = `
      <span class="proto-badge">PROTO</span>
      <span>${opts.section || ''} · ${opts.page || document.title}</span>
      <span class="proto-sep">|</span>
      <button onclick="Proto.toggleState('loading')">⏳ 加载中</button>
      <button onclick="Proto.toggleState('empty')">📭 空数据</button>
      <button onclick="Proto.toggleState('error')">⚠️ 加载失败</button>
      <button onclick="Proto.toggleState('normal')">✅ 正常</button>
      <span class="proto-sep">|</span>
      <span style="opacity:.5;font-size:11px">点击按钮切换页面状态 · 仅原型调试用</span>
    `;
    document.body.appendChild(bar);
    // 为底部 TabBar 保留工具条空间（H5/小程序端）
    const tabBar = document.querySelector('.proto-tab-bar');
    if (tabBar) {
      tabBar.style.bottom = '32px';
    }
  };

  // ─── 页面状态切换 ─────────────────────────────────────────────
  // 依赖各页面在 Vue setup 中暴露 window.__protoApp = { pageState }
  Proto.toggleState = function(state) {
    const app = window.__protoApp;
    if (app && app.pageState !== undefined) {
      app.pageState.value = state;
      return;
    }
    // 备用：触发自定义事件
    document.dispatchEvent(new CustomEvent('proto-state-change', { detail: state }));
    console.log('[Proto] State changed to:', state);
  };

  // ─── Mock 数据生成器 ──────────────────────────────────────────
  // 生成带中文的真实感 Mock 数据
  Proto.mock = {
    // 中文姓名
    names: ['张伟','李芳','王磊','赵静','刘洋','陈敏','杨帆','周婷','吴刚','郑海'],
    // 部门
    depts: ['技术部','产品部','运营部','市场部','财务部','人事部','销售部','客服部'],
    // 状态
    statuses: [
      { label: '正常', color: 'green' },
      { label: '禁用', color: 'default' },
      { label: '待审核', color: 'blue' },
      { label: '已过期', color: 'orange' },
    ],
    // 生成随机 ID（6位）
    id: function() {
      return String(Math.floor(Math.random() * 900000) + 100000);
    },
    // 从数组随机取一项
    pick: function(arr) {
      return arr[Math.floor(Math.random() * arr.length)];
    },
    // 生成日期字符串 YYYY-MM-DD（近30天内）
    date: function(offsetDays) {
      const d = new Date();
      d.setDate(d.getDate() - (offsetDays !== undefined ? offsetDays : Math.floor(Math.random() * 30)));
      return d.toISOString().slice(0, 10);
    },
    // 生成日期时间字符串
    datetime: function(offsetDays) {
      const d = new Date();
      d.setDate(d.getDate() - (offsetDays !== undefined ? offsetDays : Math.floor(Math.random() * 30)));
      return d.toISOString().slice(0, 16).replace('T', ' ');
    },
    // 生成用户列表数据（n 条）
    userList: function(n) {
      const list = [];
      for (let i = 0; i < (n || 8); i++) {
        const name = this.names[i % this.names.length];
        list.push({
          id: this.id(),
          name: name,
          phone: '1' + String(3 + Math.floor(Math.random() * 6)) + String(Math.floor(Math.random() * 1e9)).padStart(9, '0'),
          dept: this.pick(this.depts),
          status: this.statuses[i % this.statuses.length],
          createdAt: this.datetime(i * 3),
        });
      }
      return list;
    },
    // 生成通用列表数据（n 条）
    list: function(n, template) {
      const list = [];
      for (let i = 0; i < (n || 8); i++) {
        list.push(typeof template === 'function' ? template(i) : {
          id: this.id(),
          name: '数据项 ' + (i + 1),
          status: this.statuses[i % this.statuses.length],
          createdAt: this.datetime(i * 2),
        });
      }
      return list;
    },
  };

  // ─── 导航高亮（根据当前文件名标记菜单项）───────────────────────
  Proto.highlightNav = function(menuItemKey) {
    document.querySelectorAll('[data-nav-key]').forEach(el => {
      el.classList.remove('proto-nav-active');
      if (el.dataset.navKey === menuItemKey) {
        el.classList.add('proto-nav-active');
      }
    });
  };

  window.Proto = Proto;
})(window);
