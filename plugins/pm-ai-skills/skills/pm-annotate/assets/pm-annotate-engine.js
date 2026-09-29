/**
 * pm-annotate · 原型标注引擎
 * 功能：为原型页面注入编号角标（1-999）与可拖拽的悬浮说明，与 PRD 需求编号一一对应。
 * 角标锚点约定：页面内放置 <i class="pm-anno-anchor" data-n="N" style="display:none"></i>，
 * 其 nextElementSibling 即被标注的模块元素。引擎据此把角标悬浮到该模块右上角。
 */
;(function (window, document) {
  'use strict';
  /*
   * 引擎为静态资产，不含项目内容；标注数据由同目录 pm-annotate-data.js 提供。
   * 加载顺序：pm-annotate-data.js 必须先于本文件加载。
   */
  var TOOLTIPS = window.PM_ANNOTATE_TOOLTIPS || {};
  var layer = null;
  var tipLayer = null;
  var markers = {};
  var openTips = {};
  var drag = null;

  function scrollX() { return window.scrollX || window.pageXOffset || document.documentElement.scrollLeft || 0; }
  function scrollY() { return window.scrollY || window.pageYOffset || document.documentElement.scrollTop || 0; }

  function ensureLayers() {
    if (!layer) {
      layer = document.createElement('div');
      layer.id = 'pm-anno-layer';
      document.body.appendChild(layer);
    }
    if (!tipLayer) {
      tipLayer = document.createElement('div');
      tipLayer.id = 'pm-anno-tip-layer';
      document.body.appendChild(tipLayer);
    }
  }

  function createMarker(n) {
    var m = document.createElement('span');
    m.className = 'pm-anno-marker';
    m.setAttribute('data-n', n);
    m.textContent = n;
    m.addEventListener('mouseenter', function () { openTooltip(n, m); });
    m.addEventListener('click', function (e) { e.stopPropagation(); openTooltip(n, m); });
    layer.appendChild(m);
    markers[n] = m;
    return m;
  }

  function positionMarkers() {
    ensureLayers();
    var anchors = Array.prototype.slice.call(document.querySelectorAll('.pm-anno-anchor'));
    var seen = {};
    anchors.forEach(function (a) {
      var n = a.getAttribute('data-n');
      var target = a.nextElementSibling;
      var visible = target && target.offsetParent !== null;
      if (!visible) {
        if (markers[n]) markers[n].style.display = 'none';
        return;
      }
      var m = markers[n] || createMarker(n);
      m.style.display = 'inline-block';
      m.style.visibility = 'hidden';
      var rect = target.getBoundingClientRect();
      var w = m.offsetWidth || 16;
      m.style.left = (rect.right + scrollX() + 4 - w) + 'px';
      m.style.top = (rect.top + scrollY() - 8) + 'px';
      m.style.visibility = 'visible';
      seen[n] = true;
    });
    for (var k in markers) {
      if (!seen[k]) markers[k].style.display = 'none';
    }
  }

  function openTooltip(n, marker) {
    if (openTips[n]) closeTooltip(n);
    var t = TOOLTIPS[n];
    if (!t) return;
    var tip = document.createElement('div');
    tip.className = 'pm-anno-tooltip';
    tip.setAttribute('data-n', n);
    tip.innerHTML =
      '<div class="pm-anno-tooltip-header">'
      + '<span class="pm-anno-tooltip-title"><span class="pm-anno-tooltip-num">' + n + '</span>' + t.title + '</span>'
      + '<button class="pm-anno-tooltip-close" data-n="' + n + '" title="关闭">✕</button>'
      + '</div>'
      + '<div class="pm-anno-tooltip-body">' + t.html + '</div>';
    var r = marker.getBoundingClientRect();
    tip.style.left = (r.left + scrollX()) + 'px';
    tip.style.top = (r.top + scrollY() + r.height + 8) + 'px';
    tipLayer.appendChild(tip);
    var tw = tip.offsetWidth;
    var th = tip.offsetHeight;
    var vw = window.innerWidth || document.documentElement.clientWidth;
    var vh = window.innerHeight || document.documentElement.clientHeight;
    var left = r.left;
    var topBelow = r.top + r.height + 8;
    var topAbove = r.top - th - 8;
    if (left + tw > vw - 8) left = vw - tw - 8;
    if (left < 8) left = 8;
    var top;
    if (topBelow + th <= vh) top = topBelow;
    else if (topAbove >= 0) top = topAbove;
    else top = Math.max(8, vh - th - 8);
    tip.style.left = (left + scrollX()) + 'px';
    tip.style.top = (top + scrollY()) + 'px';
    openTips[n] = tip;
  }

  function closeTooltip(n) {
    var tip = openTips[n];
    if (tip && tip.parentNode) tip.parentNode.removeChild(tip);
    delete openTips[n];
  }

  function onTipMouseDown(e) {
    e.stopPropagation();
    var tip = e.target.closest ? e.target.closest('.pm-anno-tooltip') : null;
    if (!tip) return;
    if (e.target.closest && e.target.closest('.pm-anno-tooltip-close')) return;
    drag = { tip: tip, sx: e.clientX, sy: e.clientY, ox: tip.offsetLeft, oy: tip.offsetTop };
    e.preventDefault();
  }

  function onDocMouseMove(e) {
    if (!drag) return;
    drag.tip.style.left = (drag.ox + (e.clientX - drag.sx)) + 'px';
    drag.tip.style.top = (drag.oy + (e.clientY - drag.sy)) + 'px';
  }

  function onDocMouseUp() { drag = null; }

  function init() {
    ensureLayers();
    tipLayer.addEventListener('mousedown', onTipMouseDown);
    tipLayer.addEventListener('click', function (e) {
      e.stopPropagation();
      var btn = e.target.closest ? e.target.closest('.pm-anno-tooltip-close') : null;
      if (btn) closeTooltip(btn.getAttribute('data-n'));
    });
    document.addEventListener('mousemove', onDocMouseMove);
    document.addEventListener('mouseup', onDocMouseUp);

    positionMarkers();

    var app = document.getElementById('app');
    if (app && window.MutationObserver) {
      var timer = null;
      var mo = new MutationObserver(function () {
        if (timer) clearTimeout(timer);
        timer = setTimeout(positionMarkers, 60);
      });
      mo.observe(app, { childList: true, subtree: true });
    }
    var resizeTimer = null;
    window.addEventListener('resize', function () {
      if (resizeTimer) clearTimeout(resizeTimer);
      resizeTimer = setTimeout(positionMarkers, 100);
    });
    window.addEventListener('load', positionMarkers);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})(window, document);
