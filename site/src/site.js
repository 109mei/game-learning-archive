/* 共通クライアントスクリプト（テーマ切替・作品フィルタ・コードビューア） */
(function () {
  // ---- テーマ切替 ----
  var btn = document.getElementById('theme-toggle');
  if (btn) btn.addEventListener('click', function () {
    var cur = document.documentElement.dataset.theme;
    var next = cur === 'dark' ? 'light'
      : cur === 'light' ? 'dark'
      : (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'light' : 'dark');
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) { }
  });

  // ---- 作品一覧フィルタ・検索 ----
  var grid = document.getElementById('game-grid');
  if (grid && window.__GAMES__) {
    var games = window.__GAMES__;
    var items = {};
    grid.querySelectorAll('.gi').forEach(function (el) { items[el.dataset.id] = el; });
    var q = document.getElementById('q');
    var fy = document.getElementById('f-year'), fc = document.getElementById('f-cat'),
      fg = document.getElementById('f-genre'), ft = document.getElementById('f-tech'),
      fo = document.getElementById('f-org'), fp = document.getElementById('f-play');
    var count = document.getElementById('count'), empty = document.getElementById('empty');
    function apply() {
      var kw = (q.value || '').trim().toLowerCase();
      var n = 0;
      games.forEach(function (g) {
        var ok = true;
        if (kw && (g.title + ' ' + g.summary + ' ' + g.genre).toLowerCase().indexOf(kw) < 0) ok = false;
        if (ok && fy.value && String(g.year) !== fy.value) ok = false;
        if (ok && fc.value && g.cats.indexOf(fc.value) < 0) ok = false;
        if (ok && fg.value && g.genre !== fg.value) ok = false;
        if (ok && ft.value && g.techs.indexOf(ft.value) < 0) ok = false;
        if (ok && fo.value && g.orgs.indexOf(fo.value) < 0) ok = false;
        if (ok && fp.checked && !g.playable) ok = false;
        var el = items[g.id];
        if (el) el.hidden = !ok;
        if (ok) n++;
      });
      count.textContent = n + ' / ' + games.length + ' 作品を表示中';
      empty.hidden = n !== 0;
    }
    [q, fy, fc, fg, ft, fo, fp].forEach(function (el) {
      el.addEventListener('input', apply);
      el.addEventListener('change', apply);
    });
    apply();
  }

  // ---- コードビューア（ファイル切替・コピー・折り返し） ----
  document.querySelectorAll('.file-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.file-btn').forEach(function (x) { x.classList.remove('on'); x.setAttribute('aria-selected', 'false'); });
      document.querySelectorAll('.src-pane').forEach(function (p) { p.hidden = true; });
      b.classList.add('on'); b.setAttribute('aria-selected', 'true');
      var pane = document.getElementById('pane-' + b.dataset.i);
      if (pane) pane.hidden = false;
    });
  });
  document.querySelectorAll('.copy-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var i = Number(b.dataset.i || 0);
      var text = (window.__SRC__ || [])[i] || '';
      navigator.clipboard.writeText(text).then(function () {
        var t = b.textContent; b.textContent = 'コピーしました';
        setTimeout(function () { b.textContent = t; }, 1400);
      });
    });
  });
  document.querySelectorAll('.wrap-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var pre = b.closest('.src-pane').querySelector('pre.code');
      if (pre) pre.classList.toggle('wrapped');
    });
  });
})();
