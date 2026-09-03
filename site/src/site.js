/* ============================================================
   共通クライアントスクリプト
   テーマ切替 / メニュー / 深度メーター・層ジャンプ / 図鑑スタンプ・実績
   / ランダム潜行 / 浮上ボタン / 作品フィルタ・並び替え / コードビューア
   すべて localStorage 無効環境でも例外を出さずに動作する。
   ============================================================ */
(function () {
  'use strict';

  var BASE = window.__BASE__ || '';
  var doc = document;
  var body = doc.body;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------------------------------------------------------- 保存領域（安全ラッパー）
  var store = (function () {
    var ok = false;
    try {
      var k = '__dive_probe__';
      window.localStorage.setItem(k, '1');
      window.localStorage.removeItem(k);
      ok = true;
    } catch (e) { ok = false; }
    return {
      ok: ok,
      get: function (key, fallback) {
        if (!ok) return fallback;
        try {
          var v = window.localStorage.getItem(key);
          return v == null ? fallback : JSON.parse(v);
        } catch (e) { return fallback; }
      },
      set: function (key, value) {
        if (!ok) return;
        try { window.localStorage.setItem(key, JSON.stringify(value)); } catch (e) { }
      }
    };
  })();
  var K_FOUND = 'dive:found', K_BADGE = 'dive:badges';
  function uniq(arr) {
    var seen = {}, out = [];
    if (!Array.isArray(arr)) return out; // 壊れた保存値でも落ちないようにする
    arr.forEach(function (v) { if (typeof v === 'string' && !seen[v]) { seen[v] = 1; out.push(v); } });
    return out;
  }
  var found = uniq(store.get(K_FOUND, []));
  var earned = uniq(store.get(K_BADGE, []));
  var BADGES = window.__BADGES__ || [];
  function badgeById(id) {
    for (var i = 0; i < BADGES.length; i++) if (BADGES[i].id === id) return BADGES[i];
    return null;
  }

  // ---------------------------------------------------------- トースト
  function toast(icon, title, note) {
    var wrap = doc.getElementById('toast-wrap');
    if (!wrap) return;
    var el = doc.createElement('div');
    el.className = 'toast';
    el.setAttribute('role', 'status');
    var i = doc.createElement('i'); i.textContent = icon || '◎';
    var b = doc.createElement('div');
    var strong = doc.createElement('span'); strong.textContent = title;
    b.appendChild(strong);
    if (note) { var s = doc.createElement('small'); s.textContent = note; b.appendChild(s); }
    el.appendChild(i); el.appendChild(b);
    wrap.appendChild(el);
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 4200);
  }

  // ---------------------------------------------------------- 実績バッジ
  function hasBadge(id) { return earned.indexOf(id) >= 0; }
  function unlock(id) {
    if (!store.ok || hasBadge(id)) return;
    var b = badgeById(id);
    if (!b) return;
    earned.push(id);
    store.set(K_BADGE, earned);
    paintBadges();
    toast(b.icon, '実績「' + b.name + '」を獲得', b.desc);
  }
  function paintBadges() {
    var shelf = doc.getElementById('badge-shelf');
    if (!shelf) return;
    if (!store.ok) { shelf.hidden = true; return; }
    [].forEach.call(shelf.querySelectorAll('[data-badge]'), function (el) {
      if (hasBadge(el.dataset.badge)) el.classList.add('on');
    });
  }
  function checkFindBadges() {
    if (found.length >= 1) unlock('first-find');
    if (found.length >= 5) unlock('find5');
    if (found.length >= 10) unlock('find10');
  }

  // ---------------------------------------------------------- 図鑑スタンプ（発見記録）
  function paintStamps() {
    if (!store.ok) return;
    [].forEach.call(doc.querySelectorAll('[data-gid]'), function (el) {
      if (found.indexOf(el.dataset.gid) >= 0) el.classList.add('found');
    });
    var mark = doc.getElementById('found-mark');
    if (mark && found.indexOf(body.dataset.discover || '') >= 0) mark.style.display = 'inline-block';
  }
  function updateStampCount() {
    var el = doc.getElementById('stamp-count');
    if (!el) return;
    if (!store.ok) { el.hidden = true; return; }
    var total = Number(el.dataset.total || 0);
    el.innerHTML = '';
    var b = doc.createElement('b'); b.textContent = String(found.length);
    el.appendChild(b);
    el.appendChild(doc.createTextNode(' / ' + total + ' 発見'));
  }
  function discover(id) {
    if (!store.ok || !id) return;
    if (found.indexOf(id) < 0) {
      found.push(id);
      store.set(K_FOUND, found);
      var t = doc.querySelector('h1.page-title');
      toast('🔎', '新しい作品を発見！', t ? t.textContent : '');
    }
    checkFindBadges();
  }

  // ---------------------------------------------------------- テーマ切替
  var themeBtn = doc.getElementById('theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var next = doc.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    doc.documentElement.dataset.theme = next;
    themeBtn.setAttribute('aria-pressed', next === 'light' ? 'true' : 'false');
    try { window.localStorage.setItem('theme', next); } catch (e) { }
  });

  // ---------------------------------------------------------- メニュー（スマホ）
  var navBtn = doc.getElementById('nav-toggle'), nav = doc.getElementById('site-nav');
  if (navBtn && nav) navBtn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // ---------------------------------------------------------- 深度メーター・層ジャンプ
  var hud = doc.getElementById('hud');
  if (hud) {
    var hudNum = doc.getElementById('hud-num');
    var hudLayer = doc.getElementById('hud-layer');
    var sections = [].slice.call(doc.querySelectorAll('.layer[data-depth]'));
    var jumpLinks = [].slice.call(hud.querySelectorAll('.hud-jump a'));
    var baseFrom = Number(hud.dataset.depthFrom || 0);
    var baseTo = Number(hud.dataset.depthTo || 0);
    var pageLayer = hud.dataset.layerName || '';
    var ticking = false;

    function topOf(el) {
      return el.getBoundingClientRect().top + (window.pageYOffset || doc.documentElement.scrollTop);
    }
    function updateHud() {
      ticking = false;
      var y = window.pageYOffset || doc.documentElement.scrollTop || 0;
      var vh = window.innerHeight || doc.documentElement.clientHeight;
      var docH = Math.max(doc.body.scrollHeight, doc.documentElement.scrollHeight);
      var prog = docH > vh ? Math.min(1, Math.max(0, y / (docH - vh))) : 1;
      var depth = 0, name = pageLayer, active = -1;
      if (sections.length) {
        // 読み取り線は画面の42%付近。ページ先頭では 0m から始まるように立ち上げる
        var pos = y + Math.min(y, vh * 0.42), idx = 0;
        for (var i = 0; i < sections.length; i++) if (topOf(sections[i]) <= pos) idx = i;
        var cur = sections[idx], next = sections[idx + 1];
        var t0 = topOf(cur), t1 = next ? topOf(next) : docH;
        var f = t1 > t0 ? Math.min(1, Math.max(0, (pos - t0) / (t1 - t0))) : 0;
        var d0 = Number(cur.dataset.depth || 0);
        var d1 = next ? Number(next.dataset.depth || 0) : d0;
        depth = d0 + (d1 - d0) * f;
        name = cur.dataset.layer || '';
        active = idx;
        if (idx === sections.length - 1 && f > 0.3) unlock('all-layers');
      } else {
        depth = baseFrom + (baseTo - baseFrom) * prog;
      }
      if (hudNum) hudNum.textContent = String(Math.round(depth));
      if (hudLayer) hudLayer.textContent = name;
      hud.style.setProperty('--p', String(prog));
      for (var j = 0; j < jumpLinks.length; j++) jumpLinks[j].classList.toggle('on', j === active);
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      if (window.requestAnimationFrame) {
        window.requestAnimationFrame(updateHud);
        // rAF が来ない環境（描画が止まっているタブ等）でも表示が固まらないようにする保険
        setTimeout(function () { if (ticking) updateHud(); }, 120);
      } else {
        setTimeout(updateHud, 32);
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    updateHud();

    var jumpBtn = doc.getElementById('hud-jump-btn');
    var jumpNav = doc.getElementById('hud-jump');
    if (jumpBtn && jumpNav) {
      jumpBtn.addEventListener('click', function () {
        var open = jumpNav.classList.toggle('open');
        jumpBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      jumpNav.addEventListener('click', function (e) {
        if (e.target.closest('a')) {
          jumpNav.classList.remove('open');
          jumpBtn.setAttribute('aria-expanded', 'false');
        }
      });
    }
  }

  // ---------------------------------------------------------- 浮上ボタン
  var surf = doc.getElementById('surface-btn');
  if (surf) {
    var toggleSurf = function () {
      var y = window.pageYOffset || doc.documentElement.scrollTop || 0;
      surf.classList.toggle('show', y > 520);
    };
    window.addEventListener('scroll', toggleSurf, { passive: true });
    toggleSurf();
    surf.addEventListener('click', function () {
      if (!reduceMotion) {
        surf.classList.add('rise');
        setTimeout(function () { surf.classList.remove('rise'); }, 1000);
      }
      try {
        window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      } catch (e) { window.scrollTo(0, 0); }
    });
  }

  // ---------------------------------------------------------- ランダムに1本潜る
  [].forEach.call(doc.querySelectorAll('[data-random-dive]'), function (btn) {
    btn.addEventListener('click', function () {
      var list = window.__PLAYABLE__ || [];
      if (!list.length) return;
      var id = list[Math.floor(Math.random() * list.length)];
      window.location.href = BASE + '/play/' + id + '/';
    });
  });

  // ---------------------------------------------------------- コピー（共通）
  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      try {
        var ta = doc.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.style.position = 'fixed';
        ta.style.top = '-1000px';
        doc.body.appendChild(ta);
        ta.select();
        var ok = doc.execCommand('copy');
        doc.body.removeChild(ta);
        ok ? resolve() : reject();
      } catch (e) { reject(e); }
    });
  }
  function flash(btn, msg) {
    var t = btn.textContent;
    btn.textContent = msg;
    setTimeout(function () { btn.textContent = t; }, 1400);
  }

  // URLをコピー
  [].forEach.call(doc.querySelectorAll('[data-copy-url]'), function (btn) {
    btn.addEventListener('click', function () {
      copyText(window.location.href).then(function () { flash(btn, '✓ コピーしました'); },
        function () { flash(btn, 'コピーできませんでした'); });
    });
  });

  // ---------------------------------------------------------- 図鑑（作品一覧）
  var grid = doc.getElementById('game-grid');
  if (grid && window.__GAMES__) {
    var games = window.__GAMES__;
    var items = {};
    [].forEach.call(grid.querySelectorAll('.gi'), function (el) { items[el.dataset.id] = el; });
    var q = doc.getElementById('q');
    var fy = doc.getElementById('f-year'), fc = doc.getElementById('f-cat'),
      fg = doc.getElementById('f-genre'), ft = doc.getElementById('f-tech'),
      fo = doc.getElementById('f-org'), fp = doc.getElementById('f-play'),
      fs = doc.getElementById('f-sort');
    var count = doc.getElementById('count'), empty = doc.getElementById('empty');

    function sortedIds() {
      var mode = fs ? fs.value : 'no';
      var arr = games.slice();
      arr.sort(function (a, b) {
        if (mode === 'name') return String(a.title).localeCompare(String(b.title), 'ja');
        if (mode === 'act') return a.ord - b.ord;
        return a.no - b.no;
      });
      return arr;
    }
    function apply() {
      var kw = (q && q.value || '').trim().toLowerCase();
      var n = 0;
      sortedIds().forEach(function (g, i) {
        var ok = true;
        if (kw && (g.title + ' ' + g.summary + ' ' + g.genre).toLowerCase().indexOf(kw) < 0) ok = false;
        if (ok && fy.value && String(g.year) !== fy.value) ok = false;
        if (ok && fc.value && g.cats.indexOf(fc.value) < 0) ok = false;
        if (ok && fg.value && g.genre !== fg.value) ok = false;
        if (ok && ft.value && g.techs.indexOf(ft.value) < 0) ok = false;
        if (ok && fo.value && g.orgs.indexOf(fo.value) < 0) ok = false;
        if (ok && fp.checked && !g.playable) ok = false;
        var el = items[g.id];
        if (el) { el.hidden = !ok; el.style.order = String(i); }
        if (ok) n++;
      });
      if (count) count.textContent = n + ' / ' + games.length + ' 作品を表示中';
      if (empty) empty.hidden = n !== 0;
    }
    [q, fy, fc, fg, ft, fo, fp, fs].forEach(function (el) {
      if (!el) return;
      el.addEventListener('input', apply);
      el.addEventListener('change', apply);
    });
    var reset = doc.getElementById('f-reset');
    if (reset) reset.addEventListener('click', function () {
      if (q) q.value = '';
      [fy, fc, fg, ft, fo].forEach(function (el) { if (el) el.value = ''; });
      if (fp) fp.checked = false;
      if (fs) fs.value = 'no';
      apply();
    });
    apply();

    // キーボードショートカット: / で検索欄へ、Esc で解除
    doc.addEventListener('keydown', function (e) {
      var tag = (e.target && e.target.tagName || '').toLowerCase();
      var typing = tag === 'input' || tag === 'textarea' || tag === 'select' || e.target.isContentEditable;
      if (e.key === '/' && !typing && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        if (q) { q.focus(); q.select(); }
      } else if (e.key === 'Escape' && q && doc.activeElement === q) {
        q.blur();
      }
    });
  }

  // ---------------------------------------------------------- コードビューア
  [].forEach.call(doc.querySelectorAll('.file-btn'), function (b) {
    b.addEventListener('click', function () {
      [].forEach.call(doc.querySelectorAll('.file-btn'), function (x) {
        x.classList.remove('on'); x.setAttribute('aria-selected', 'false');
      });
      [].forEach.call(doc.querySelectorAll('.src-pane'), function (p) { p.hidden = true; });
      b.classList.add('on'); b.setAttribute('aria-selected', 'true');
      var pane = doc.getElementById('pane-' + b.dataset.i);
      if (pane) pane.hidden = false;
    });
  });
  [].forEach.call(doc.querySelectorAll('.copy-btn'), function (b) {
    b.addEventListener('click', function () {
      var i = Number(b.dataset.i || 0);
      var text = (window.__SRC__ || [])[i] || '';
      copyText(text).then(function () { flash(b, 'コピーしました'); },
        function () { flash(b, 'コピーできませんでした'); });
    });
  });
  [].forEach.call(doc.querySelectorAll('.wrap-btn'), function (b) {
    b.addEventListener('click', function () {
      var pre = b.closest('.src-pane').querySelector('pre.code');
      if (pre) pre.classList.toggle('wrapped');
    });
  });

  // ---------------------------------------------------------- 初期化
  paintStamps();
  updateStampCount();
  paintBadges();
  unlock('first-dive');
  if (body.dataset.discover) {
    discover(body.dataset.discover);
    paintStamps();
    updateStampCount();
  }
  if (body.dataset.readCode) unlock('read-code');
  checkFindBadges();
})();
