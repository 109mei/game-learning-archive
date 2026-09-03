/* ============================================================
   共通クライアントスクリプト
   テーマ切替 / メニュー / メニュー / 作品一覧スタンプ・実績
   / ランダム表示 / 上へ戻るボタン / 作品一覧の絞り込み・並び替え・URL反映
   / 記録リセット / シルエット表示 / 学習トピック検索 / コードビューア
   すべて localStorage 無効環境・JS無効環境でエラーを出さずに動作する。
   ============================================================ */
(function () {
  'use strict';

  var BASE = window.__BASE__ || '';
  var doc = document;
  var body = doc.body;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var suppressAuto = false; // 記録リセット直後に自動獲得を止める

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
      },
      del: function (key) {
        if (!ok) return;
        try { window.localStorage.removeItem(key); } catch (e) { }
      }
    };
  })();
  var K_FOUND = 'dive:found', K_BADGE = 'dive:badges', K_SIL = 'dive:silhouette';
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

  // ---------------------------------------------------------- JS専用UIを出す
  [].forEach.call(doc.querySelectorAll('.js-only'), function (el) {
    if (el.hasAttribute('data-store-only') && !store.ok) return;
    el.hidden = false;
  });

  // ---------------------------------------------------------- トースト（1件ずつ順に表示）
  var toastQ = [], toastBusy = false;
  function toast(icon, title, note) {
    toastQ.push([icon, title, note]);
    pumpToast();
  }
  function pumpToast() {
    if (toastBusy || !toastQ.length) return;
    var wrap = doc.getElementById('toast-wrap');
    if (!wrap) { toastQ.length = 0; return; }
    toastBusy = true;
    var args = toastQ.shift();
    var el = doc.createElement('div');
    el.className = 'toast';
    el.setAttribute('role', 'status');
    var i = doc.createElement('i'); i.textContent = args[0] || '◎';
    var b = doc.createElement('div');
    var t = doc.createElement('span'); t.textContent = args[1];
    b.appendChild(t);
    if (args[2]) { var s = doc.createElement('small'); s.textContent = args[2]; b.appendChild(s); }
    el.appendChild(i); el.appendChild(b);
    wrap.appendChild(el);
    setTimeout(function () {
      if (el.parentNode) el.parentNode.removeChild(el);
      toastBusy = false;
      pumpToast();
    }, toastQ.length ? 2000 : 3800);
  }

  // ---------------------------------------------------------- 実績バッジ
  function hasBadge(id) { return earned.indexOf(id) >= 0; }
  function unlock(id) {
    if (!store.ok || suppressAuto || hasBadge(id)) return;
    var b = badgeById(id);
    if (!b) return;
    earned.push(id);
    store.set(K_BADGE, earned);
    paintBadges();
    toast(b.icon, '実績「' + b.name + '」を獲得', b.desc);
  }
  function paintBadges() {
    [].forEach.call(doc.querySelectorAll('.badge-shelf'), function (shelf) {
      if (!store.ok) { shelf.hidden = true; return; }
      [].forEach.call(shelf.querySelectorAll('[data-badge]'), function (el) {
        el.classList.toggle('on', hasBadge(el.dataset.badge));
      });
    });
  }
  function checkFindBadges() {
    if (found.length >= 1) unlock('first-find');
    if (found.length >= 5) unlock('find5');
    if (found.length >= 10) unlock('find10');
  }

  // ---------------------------------------------------------- 作品一覧スタンプ（発見記録）
  function paintStamps() {
    [].forEach.call(doc.querySelectorAll('[data-gid]'), function (el) {
      el.classList.toggle('found', store.ok && found.indexOf(el.dataset.gid) >= 0);
    });
    var mark = doc.getElementById('found-mark');
    if (mark) mark.style.display = (store.ok && found.indexOf(body.dataset.discover || '') >= 0) ? 'inline-block' : 'none';
  }
  function updateStampCount() {
    var el = doc.getElementById('stamp-count');
    var bar = doc.getElementById('dex-bar');
    if (!el) return;
    if (!store.ok) { el.hidden = true; if (bar) bar.hidden = true; return; }
    var total = Number(el.dataset.total || 0);
    el.innerHTML = '';
    var b = doc.createElement('b'); b.textContent = String(found.length);
    el.appendChild(b);
    el.appendChild(doc.createTextNode(' / ' + total + ' 発見'));
    if (bar && total) bar.style.setProperty('--p', String(Math.min(1, found.length / total)));
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

  // ---------------------------------------------------------- 記録のリセット
  [].forEach.call(doc.querySelectorAll('#reset-record'), function (btn) {
    btn.addEventListener('click', function () {
      if (!store.ok) return;
      if (!window.confirm('このブラウザに保存された「発見記録」と「実績」をすべて消します。よろしいですか？')) return;
      store.del(K_FOUND); store.del(K_BADGE);
      found = []; earned = [];
      suppressAuto = true;
      paintStamps(); updateStampCount(); paintBadges();
      if (typeof applyDex === 'function') applyDex();
      toast('🧹', '記録を消しました', '発見スタンプと実績が初期状態に戻りました');
    });
  });

  // ---------------------------------------------------------- 未発見のシルエット表示
  var silBox = doc.getElementById('f-silhouette');
  function applySilhouette(on) {
    doc.documentElement.classList.toggle('silhouette', !!on);
  }
  if (store.ok) applySilhouette(store.get(K_SIL, false) === true);
  if (silBox) {
    silBox.checked = store.ok && store.get(K_SIL, false) === true;
    silBox.addEventListener('change', function () {
      applySilhouette(silBox.checked);
      store.set(K_SIL, silBox.checked);
    });
  }

  // ---------------------------------------------------------- テーマ切替
  var themeBtn = doc.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.setAttribute('aria-pressed', doc.documentElement.dataset.theme === 'light' ? 'true' : 'false');
    themeBtn.addEventListener('click', function () {
      var next = doc.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
      doc.documentElement.dataset.theme = next;
      themeBtn.setAttribute('aria-pressed', next === 'light' ? 'true' : 'false');
      try { window.localStorage.setItem('theme', next); } catch (e) { }
    });
  }

  // ---------------------------------------------------------- メニュー（スマホ）
  var navBtn = doc.getElementById('nav-toggle'), nav = doc.getElementById('site-nav');
  if (navBtn && nav) navBtn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // ---------------------------------------------------------- 上へ戻るボタン
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
  [].forEach.call(doc.querySelectorAll('[data-copy-url]'), function (btn) {
    btn.addEventListener('click', function () {
      copyText(window.location.href).then(function () { flash(btn, '✓ コピーしました'); },
        function () { flash(btn, 'コピーできませんでした'); });
    });
  });

  // ---------------------------------------------------------- 作品一覧（作品一覧）
  var applyDex = null;
  var grid = doc.getElementById('game-grid');
  if (grid && window.__GAMES__) {
    var games = window.__GAMES__;
    var items = {};
    [].forEach.call(grid.querySelectorAll('.gi'), function (el) { items[el.dataset.id] = el; });
    var q = doc.getElementById('q');
    var fy = doc.getElementById('f-year'), fc = doc.getElementById('f-cat'),
      fg = doc.getElementById('f-genre'), ft = doc.getElementById('f-tech'),
      fo = doc.getElementById('f-org'), fp = doc.getElementById('f-play'),
      fs = doc.getElementById('f-sort'), ff = doc.getElementById('f-found');
    var count = doc.getElementById('count'), empty = doc.getElementById('empty');
    var collator = (window.Intl && Intl.Collator)
      ? new Intl.Collator('ja', { numeric: true, ignorePunctuation: true })
      : null;

    // --- URL との同期 ---
    var PARAMS = [['q', q], ['sort', fs], ['year', fy], ['cat', fc], ['genre', fg],
      ['tech', ft], ['org', fo], ['found', ff]];
    function readUrl() {
      if (!window.URLSearchParams) return;
      var sp = new URLSearchParams(window.location.search);
      PARAMS.forEach(function (pair) {
        var v = sp.get(pair[0]);
        if (v != null && pair[1]) pair[1].value = v;
      });
      if (fp) fp.checked = sp.get('play') === '1';
    }
    function writeUrl() {
      if (!window.URLSearchParams || !window.history || !history.replaceState) return;
      var sp = new URLSearchParams();
      PARAMS.forEach(function (pair) {
        var el = pair[1];
        // 既定値（作品一覧No.順・すべて）はURLに載せず、共有URLを短く保つ
        if (el && el.value && !(pair[0] === 'sort' && el.value === 'no')) sp.set(pair[0], el.value);
      });
      if (fp && fp.checked) sp.set('play', '1');
      var s = sp.toString();
      history.replaceState(null, '', s ? location.pathname + '?' + s : location.pathname);
    }

    function sortedGames() {
      var mode = fs ? fs.value : 'no';
      var arr = games.slice();
      arr.sort(function (a, b) {
        if (mode === 'name') {
          return collator ? collator.compare(a.title, b.title)
            : String(a.title).localeCompare(String(b.title), 'ja');
        }
        if (mode === 'act') return a.ord - b.ord;
        return a.no - b.no;
      });
      return arr;
    }
    applyDex = function () {
      var kw = (q && q.value || '').trim().toLowerCase();
      var fstate = (ff && store.ok) ? ff.value : '';
      var n = 0;
      sortedGames().forEach(function (g, i) {
        var ok = true;
        if (kw && String(g.text).indexOf(kw) < 0) ok = false;
        if (ok && fy && fy.value && String(g.year) !== fy.value) ok = false;
        if (ok && fc && fc.value && g.cats.indexOf(fc.value) < 0) ok = false;
        if (ok && fg && fg.value && g.genre !== fg.value) ok = false;
        if (ok && ft && ft.value && g.techs.indexOf(ft.value) < 0) ok = false;
        if (ok && fo && fo.value && g.orgs.indexOf(fo.value) < 0) ok = false;
        if (ok && fp && fp.checked && !g.playable) ok = false;
        if (ok && fstate) {
          var isFound = found.indexOf(g.id) >= 0;
          if (fstate === 'new' && isFound) ok = false;
          if (fstate === 'found' && !isFound) ok = false;
        }
        var el = items[g.id];
        if (el) { el.hidden = !ok; el.style.order = String(i); }
        if (ok) n++;
      });
      if (count) count.textContent = n + ' / ' + games.length + ' 作品を表示中';
      if (empty) empty.hidden = n !== 0;
    };
    function onChange() { applyDex(); writeUrl(); }
    [q, fy, fc, fg, ft, fo, fp, fs, ff].forEach(function (el) {
      if (!el) return;
      el.addEventListener('input', onChange);
      el.addEventListener('change', onChange);
    });
    var reset = doc.getElementById('f-reset');
    if (reset) reset.addEventListener('click', function () {
      if (q) q.value = '';
      [fy, fc, fg, ft, fo, ff].forEach(function (el) { if (el) el.value = ''; });
      if (fp) fp.checked = false;
      if (fs) fs.value = 'no';
      onChange();
    });
    // 絞り込みの開閉（スマホ）
    var fToggle = doc.getElementById('filter-toggle'), fMore = doc.getElementById('filters-more');
    if (fToggle && fMore) fToggle.addEventListener('click', function () {
      var open = fMore.classList.toggle('open');
      fToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      fToggle.textContent = open ? '絞り込み ▴' : '絞り込み ▾';
    });
    readUrl();
    applyDex();

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

  // ---------------------------------------------------------- 学習トピックの絞り込み
  var lq = doc.getElementById('learn-q');
  if (lq) {
    var lCount = doc.getElementById('learn-count'), lEmpty = doc.getElementById('learn-empty');
    var lGrids = [].slice.call(doc.querySelectorAll('.learn-grid'));
    var total = doc.querySelectorAll('[data-topic]').length;
    lq.addEventListener('input', function () {
      var kw = lq.value.trim().toLowerCase();
      var n = 0;
      lGrids.forEach(function (gridEl) {
        var shown = 0;
        [].forEach.call(gridEl.querySelectorAll('[data-topic]'), function (card) {
          var hit = !kw || String(card.dataset.topic).toLowerCase().indexOf(kw) >= 0;
          card.hidden = !hit;
          if (hit) { shown++; n++; }
        });
        gridEl.hidden = shown === 0;
        var h = gridEl.previousElementSibling;
        if (h && h.classList.contains('year-h')) h.hidden = shown === 0;
      });
      if (lCount) lCount.textContent = kw ? (n + ' / ' + total + ' トピック') : (total + ' トピック');
      if (lEmpty) lEmpty.hidden = n !== 0;
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
  // 全画面（プレイページ）
  var fsBtn = doc.getElementById('fs-btn');
  if (fsBtn) fsBtn.addEventListener('click', function () {
    var f = doc.getElementById('game-frame');
    if (!f) return;
    (f.requestFullscreen || f.webkitRequestFullscreen || function () { }).call(f);
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
