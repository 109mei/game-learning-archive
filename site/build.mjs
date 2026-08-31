#!/usr/bin/env node
/**
 * ゲーム制作・プログラミング学習アーカイブ — 静的サイトジェネレーター
 * 依存パッケージなし（Node 18+ のみ）。 `node build.mjs` で dist/ に全ページを生成します。
 * データ（src/data/ のJSON、game-sources/、public/）を追加するだけでページが自動生成されます。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.join(ROOT, 'src');
const DIST = path.join(ROOT, 'dist');
const GS = path.join(ROOT, 'game-sources');

// ---------- utils ----------
const readJSON = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
// サブパス公開対応: GitHub Pagesのプロジェクトサイト等では BASE_URL="/リポジトリ名" を指定してビルド
let BASE = '';
const has = v => v !== null && v !== undefined && v !== '' && v !== '要確認' && !(Array.isArray(v) && v.length === 0);
function out(rel, html) {
  if (BASE) html = html.replace(/(href|src)="\//g, `$1="${BASE}/`);
  const p = path.join(DIST, rel);
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, html);
}
function copyDir(from, to) {
  if (!fs.existsSync(from)) return;
  fs.mkdirSync(to, { recursive: true });
  for (const e of fs.readdirSync(from, { withFileTypes: true })) {
    const f = path.join(from, e.name), t = path.join(to, e.name);
    e.isDirectory() ? copyDir(f, t) : fs.copyFileSync(f, t);
  }
}

// ---------- data ----------
const site = readJSON(path.join(SRC, 'data/site.json'));
BASE = (process.env.BASE_URL || site.baseUrl || '').replace(/\/+$/, '');
if (BASE && !BASE.startsWith('/')) BASE = '/' + BASE;
const categories = readJSON(path.join(SRC, 'data/categories.json'));
const organizations = readJSON(path.join(SRC, 'data/organizations.json'));
const techNames = readJSON(path.join(SRC, 'data/tech.json'));
const games = fs.readdirSync(path.join(SRC, 'data/games')).filter(f => f.endsWith('.json'))
  .map(f => readJSON(path.join(SRC, 'data/games', f)));
const activities = fs.readdirSync(path.join(SRC, 'data/activities')).filter(f => f.endsWith('.json'))
  .map(f => readJSON(path.join(SRC, 'data/activities', f)));

const catById = Object.fromEntries(categories.map(c => [c.id, c]));
const orgById = Object.fromEntries(organizations.map(o => [o.id, o]));
const actById = Object.fromEntries(activities.map(a => [a.id, a]));
const gameById = Object.fromEntries(games.map(g => [g.id, g]));
const techName = t => techNames[t] || t;

// thumbnail auto-detection: public/images/games/<id>.png
for (const g of games) {
  if (!g.thumbnail && fs.existsSync(path.join(ROOT, 'public/images/games', g.id + '.png')))
    g.thumbnail = `/images/games/${g.id}.png`;
  if ((!g.screenshots || !g.screenshots.length)) {
    g.screenshots = ['_a', '_b']
      .map(s => `/images/games/${g.id}${s}.png`)
      .filter(u => fs.existsSync(path.join(ROOT, 'public', u.slice(1))));
  }
}

// activity -> games (many-to-many, 逆引き)
const gamesOfActivity = id => games.filter(g => (g.activities || []).includes(id));
const actCategoriesOf = a => [a.category, ...(a.subCategories || [])].filter(Boolean);
const gameCatsOf = g => {
  const s = new Set();
  for (const aid of g.activities || []) { const a = actById[aid]; if (a) actCategoriesOf(a).forEach(c => s.add(c)); }
  return [...s];
};
const sortYearDesc = arr => [...arr].sort((a, b) => (b.year ?? -1) - (a.year ?? -1) || String(a.title).localeCompare(String(b.title), 'ja'));
const years = [...new Set([...games, ...activities].map(x => x.year).filter(y => y != null))].sort((a, b) => b - a);

// learn topics (auto: game-sources/reverse/NN_タイトル.py)
const LEVELS = { 基礎: [21, 31, 32, 33, 34, 35, 2, 5], 入門: [1, 3, 4, 6, 7, 8, 9, 10, 17, 28, 29] };
const learnTopics = fs.existsSync(path.join(GS, 'reverse')) ? fs.readdirSync(path.join(GS, 'reverse'))
  .filter(f => /^\d+_.*\.py$/.test(f)).sort().map(f => {
    const num = parseInt(f, 10);
    const title = f.replace(/^\d+_/, '').replace(/\.py$/, '').replace(/[.,]$/, '');
    const level = LEVELS.基礎.includes(num) ? '基礎' : LEVELS.入門.includes(num) ? '入門' : '応用';
    return { slug: 'r' + String(num).padStart(2, '0'), num, title, level, file: f };
  }) : [];
const learnBySlug = Object.fromEntries(learnTopics.map(t => [t.slug, t]));
const gamesOfTopic = slug => games.filter(g => (g.learnTopics || []).includes(slug));

// ---------- python highlighter ----------
const PY_KW = new Set(['False','None','True','and','as','assert','async','await','break','class','continue','def','del','elif','else','except','finally','for','from','global','if','import','in','is','lambda','nonlocal','not','or','pass','raise','return','try','while','with','yield','match','case']);
const PY_BUILTIN = new Set(['print','len','range','int','str','float','list','dict','set','tuple','abs','min','max','sum','open','enumerate','zip','map','filter','sorted','round','input','type','isinstance','hasattr','getattr','setattr','super','id','repr','bool','bytes','chr','ord','divmod','pow','all','any','next','iter','vars','format','hex','oct','bin']);
function hlPython(code) {
  let i = 0, outp = '';
  const n = code.length;
  const push = (cls, text) => { outp += cls ? `<span class="${cls}">${esc(text)}</span>` : esc(text); };
  while (i < n) {
    const ch = code[i];
    // comments
    if (ch === '#') { let j = code.indexOf('\n', i); if (j < 0) j = n; push('c', code.slice(i, j)); i = j; continue; }
    // strings (with optional prefix)
    const m = /^[rbufRBUF]{0,2}("""|'''|"|')/.exec(code.slice(i));
    if (m && /[rbufRBUF'"]/.test(ch)) {
      const q = m[1]; const start = i; i += m[0].length;
      if (q.length === 3) { let j = code.indexOf(q, i); if (j < 0) j = n; else j += 3; push('s', code.slice(start, j)); i = j; continue; }
      let j = i;
      while (j < n && code[j] !== q && code[j] !== '\n') { if (code[j] === '\\') j++; j++; }
      if (j < n && code[j] === q) j++;
      push('s', code.slice(start, j)); i = j; continue;
    }
    // words
    if (/[A-Za-z_]/.test(ch)) {
      let j = i; while (j < n && /[A-Za-z0-9_]/.test(code[j])) j++;
      const w = code.slice(i, j);
      if (PY_KW.has(w)) push('k', w);
      else if (PY_BUILTIN.has(w)) push('b', w);
      else if (/^\s*(async\s+)?def\s+$/.test(code.slice(Math.max(0, i - 10), i)) || /(^|\n)\s*(async\s+)?def\s+$/.test(code.slice(Math.max(0, i - 12), i)) || /class\s+$/.test(code.slice(Math.max(0, i - 8), i))) push('f', w);
      else push('', w);
      i = j; continue;
    }
    // numbers
    if (/[0-9]/.test(ch)) { let j = i; while (j < n && /[0-9a-fA-FxXoObB_.eEjJ]/.test(code[j])) j++; push('n', code.slice(i, j)); i = j; continue; }
    push('', ch); i++;
  }
  return outp;
}
function codeBlockHTML(code, lang) {
  const body = lang === 'python' ? hlPython(code) : esc(code);
  const lines = body.split('\n').map(l => `<span class="cl">${l || ' '}</span>`).join('\n');
  return `<pre class="code"><code>${lines}</code></pre>`;
}

// ---------- layout ----------
const NAV = [
  ['/play/', 'ゲームを遊ぶ'],
  ['/games/', '作品一覧'],
  ['/activities/', '活動記録'],
  ['/learn/', '学ぶ'],
  ['/about/', 'About'],
];
function page({ title, desc, path: cur = '/', content, extraHead = '', bodyClass = '' }) {
  const fullTitle = title ? `${title} | ${site.title}` : `${site.title} — ${site.tagline}`;
  const ideria = site.ideriaOfficialUrl
    ? `<a href="${esc(site.ideriaOfficialUrl)}" target="_blank" rel="noopener">IDERIA公式サイト</a>` : '';
  return `<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(fullTitle)}</title>
<meta name="description" content="${esc(desc || site.description)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<script>try{const t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;}catch(e){}</script>
${extraHead}
</head>
<body class="${bodyClass}">
<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="/"><span class="brand-mark">▶</span> <span class="brand-text">${esc(site.title)}</span></a>
    <nav class="nav" aria-label="メインメニュー">
      ${NAV.map(([href, label]) => `<a href="${href}"${cur.startsWith(href) ? ' class="on" aria-current="page"' : ''}>${label}</a>`).join('')}
    </nav>
    <button id="theme-toggle" class="theme-toggle" aria-label="ダークモード切りかえ" title="ダークモード切りかえ">◐</button>
  </div>
</header>
<main>${content}</main>
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <p class="foot-title">${esc(site.title)}</p>
      <p class="foot-desc">${esc(site.tagline)}。ゲームジャム・授業・高大連携・IDERIAの制作活動を記録しています。</p>
      ${ideria ? `<p class="foot-link">${ideria}</p>` : ''}
    </div>
    <nav aria-label="フッターメニュー"><p class="foot-h">見る・遊ぶ</p>
      <a href="/play/">ゲームを遊ぶ</a><a href="/games/">作品一覧</a><a href="/source-list/">ソースコード</a><a href="/years/">年度別アーカイブ</a>
    </nav>
    <nav aria-label="活動"><p class="foot-h">活動</p>
      <a href="/game-jams/">ゲームジャム</a><a href="/contests/">コンテスト</a><a href="/classes/">授業</a><a href="/collabs/">高大連携</a><a href="/ideria/">IDERIA制作</a>
    </nav>
    <nav aria-label="学ぶ"><p class="foot-h">学ぶ</p>
      <a href="/learn/">学習トピック一覧</a><a href="/about/">このサイトについて</a>
    </nav>
  </div>
  <p class="foot-copy">© ${new Date().getFullYear()} ゲーム制作・プログラミング学習アーカイブ</p>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>`;
}

// ---------- partials ----------
const badgePlay = `<span class="badge badge-play">▶ ブラウザで遊べる</span>`;
function gameCard(g) {
  const acts = (g.activities || []).map(id => actById[id]).filter(Boolean);
  const orgNames = (g.organizations || []).map(id => orgById[id]?.name).filter(Boolean);
  const thumb = g.thumbnail
    ? `<img src="${g.thumbnail}" alt="${esc(g.title)}のプレイ画面" loading="lazy" width="640" height="400">`
    : `<div class="thumb-ph" role="img" aria-label="画像準備中"><span>🎮</span><small>画像準備中</small></div>`;
  return `<a class="card game-card" href="/games/${g.id}/">
  <div class="thumb">${thumb}${g.play?.playable ? badgePlay : ''}</div>
  <div class="card-body">
    <h3 class="card-title">${esc(g.title)}</h3>
    ${has(g.summary) ? `<p class="card-summary">${esc(g.summary)}</p>` : ''}
    <p class="card-meta">
      ${has(g.genre) ? `<span class="chip chip-genre">${esc(g.genre)}</span>` : ''}
      ${g.year != null ? `<span class="chip chip-year">${g.year}年度</span>` : ''}
      ${(g.tech || []).slice(0, 2).map(t => `<span class="chip chip-tech">${esc(techName(t))}</span>`).join('')}
    </p>
    ${orgNames.length || acts.length ? `<p class="card-org">${esc([orgNames[0], acts[0]?.title].filter(Boolean).join(' ／ '))}</p>` : ''}
  </div></a>`;
}
function activityCard(a) {
  const n = gamesOfActivity(a.id).length;
  const cat = catById[a.category];
  return `<a class="card act-card" href="/activities/${a.id}/">
  <div class="card-body">
    <p class="card-meta"><span class="chip chip-cat">${esc(cat?.name || '')}</span>${a.year != null ? `<span class="chip chip-year">${a.year}年度</span>` : ''}</p>
    <h3 class="card-title">${esc(a.title)}</h3>
    ${has(a.summary) ? `<p class="card-summary">${esc(a.summary)}</p>` : ''}
    <p class="card-org">${[has(a.dates) ? a.dates.join('・') : null, n ? `作品 ${n}件` : null].filter(Boolean).map(esc).join(' ／ ')}</p>
  </div></a>`;
}
const section = (title, more, inner) =>
  `<section class="sec"><div class="wrap"><div class="sec-head"><h2>${title}</h2>${more ? `<a class="more" href="${more}">すべて見る →</a>` : ''}</div>${inner}</div></section>`;
const cardGrid = items => `<div class="grid">${items.join('')}</div>`;
function defRow(label, value) { return has(value) ? `<div class="def-row"><dt>${label}</dt><dd>${value}</dd></div>` : ''; }

// ---------- HOME ----------
{
  const playable = games.filter(g => g.play?.playable && g.thumbnail);
  const featured = ['ideria-chokopaki', 'gj4-hill-rush', 'gj3-music-game', 'obg-order-recall'].map(id => gameById[id]).filter(Boolean);
  const newest = sortYearDesc(games.filter(g => g.year != null)).slice(0, 4);
  const learnGames = games.filter(g => (g.learnTopics || []).length && g.play?.playable).slice(0, 4);
  const recentActs = sortYearDesc(activities).slice(0, 3);
  const catCards = ['game-jam', 'contest', 'class', 'collab', 'ideria'].map(id => {
    const c = catById[id];
    const count = games.filter(g => gameCatsOf(g).includes(id)).length;
    return `<a class="cat-card" href="/${c.slug}/"><span class="cat-name">${esc(c.name)}</span><span class="cat-desc">${esc(c.desc)}</span><span class="cat-count">${count} 作品</span></a>`;
  }).join('');
  const content = `
<section class="hero"><div class="wrap">
  <p class="hero-eyebrow">GAME × CODE × LEARNING</p>
  <h1>ゲームを遊んで、<br class="sp">コードを見て、<br>ゲーム制作を学ぶ。</h1>
  <p class="hero-lead">ここは、ゲームジャムや授業・高大連携・IDERIAの活動で生まれたゲームのアーカイブ。<br class="pc">気になるゲームをブラウザでそのまま遊んで、そのソースコードを読んで、作り方を学べます。</p>
  <p class="hero-cta"><a class="btn btn-primary" href="/play/">▶ 今すぐ遊ぶ</a><a class="btn" href="/games/">作品を見る</a><a class="btn" href="/learn/">学ぶ</a></p>
  <p class="hero-stats"><span><b>${games.length}</b> 作品</span><span><b>${games.filter(g => g.play?.playable).length}</b> ブラウザ対応</span><span><b>${activities.length}</b> 活動</span><span><b>${learnTopics.length}</b> 学習トピック</span></p>
</div></section>
${section('すぐ遊べるゲーム', '/play/', cardGrid(featured.map(gameCard)))}
${section('新着作品', '/games/', cardGrid(newest.map(gameCard)))}
${section('学習におすすめのゲーム', '/learn/', cardGrid(learnGames.map(gameCard)))}
${section('最近の活動', '/activities/', `<div class="grid grid-3">${recentActs.map(activityCard).join('')}</div>`)}
<section class="sec"><div class="wrap"><div class="sec-head"><h2>カテゴリからさがす</h2></div><div class="cat-grid">${catCards}</div></div></section>`;
  out('index.html', page({ content, path: '/' }));
}

// ---------- 作品一覧 /games/ （絞り込み・検索つき） ----------
{
  const idx = games.map(g => ({
    id: g.id, title: g.title, summary: g.summary || '', genre: g.genre || '',
    year: g.year, techs: g.tech || [], orgs: g.organizations || [],
    cats: gameCatsOf(g), playable: !!(g.play && g.play.playable),
  }));
  const filters = `
<div class="filters" id="filters">
  <input type="search" id="q" placeholder="タイトル・説明で検索" aria-label="作品を検索">
  <select id="f-year" aria-label="年度で絞り込み"><option value="">年度: すべて</option>${years.map(y => `<option value="${y}">${y}年度</option>`).join('')}</select>
  <select id="f-cat" aria-label="活動種別で絞り込み"><option value="">活動種別: すべて</option>${categories.map(c => `<option value="${c.id}">${esc(c.name)}</option>`).join('')}</select>
  <select id="f-genre" aria-label="ジャンルで絞り込み"><option value="">ジャンル: すべて</option>${[...new Set(games.map(g => g.genre).filter(has))].map(x => `<option>${esc(x)}</option>`).join('')}</select>
  <select id="f-tech" aria-label="使用技術で絞り込み"><option value="">技術: すべて</option>${[...new Set(games.flatMap(g => g.tech || []))].map(t => `<option value="${t}">${esc(techName(t))}</option>`).join('')}</select>
  <select id="f-org" aria-label="制作元で絞り込み"><option value="">制作元: すべて</option>${organizations.map(o => `<option value="${o.id}">${esc(o.name)}</option>`).join('')}</select>
  <label class="check"><input type="checkbox" id="f-play"> ブラウザで遊べる</label>
</div>
<p class="result-count" id="count" role="status"></p>`;
  const content = `<div class="wrap page-pad">
<h1 class="page-title">作品一覧</h1>
<p class="page-lead">これまでの活動で生まれたゲーム作品のアーカイブです。カードを選ぶと詳細ページへ移動します。</p>
${filters}
<div class="grid" id="game-grid">${sortYearDesc(games).map(g => `<div class="gi" data-id="${g.id}">${gameCard(g)}</div>`).join('')}</div>
<p class="empty" id="empty" hidden>条件にあう作品が見つかりませんでした。</p>
</div>
<script>window.__GAMES__=${JSON.stringify(idx)};</script>`;
  out('games/index.html', page({ title: '作品一覧', path: '/games/', content }));
}

// ---------- 作品詳細 ----------
for (const g of games) {
  const acts = (g.activities || []).map(id => actById[id]).filter(Boolean);
  const orgNames = (g.organizations || []).map(id => orgById[id]?.name).filter(Boolean);
  const shots = (g.screenshots || []).filter(u => u !== g.thumbnail);
  const topics = (g.learnTopics || []).map(s => learnBySlug[s]).filter(Boolean);
  const main = g.thumbnail
    ? `<img class="detail-hero" src="${g.thumbnail}" alt="${esc(g.title)}のプレイ画面" width="640" height="400">`
    : `<div class="detail-hero thumb-ph"><span>🎮</span><small>画像準備中</small></div>`;
  const buttons = [
    g.play?.playable ? `<a class="btn btn-primary btn-lg" href="/play/${g.id}/">▶ ブラウザで遊ぶ</a>` : '',
    g.source?.available ? `<a class="btn btn-lg" href="/source/${g.id}/">&lt;/&gt; ソースコードを見る</a>` : '',
  ].filter(Boolean).join('');
  const content = `<div class="wrap page-pad">
<nav class="crumbs" aria-label="パンくず"><a href="/">HOME</a> › <a href="/games/">作品一覧</a> › <span>${esc(g.title)}</span></nav>
<div class="detail-grid">
  <div class="detail-media">${main}
    ${g.play?.playable ? `<p class="badge-line">${badgePlay}</p>` : ''}
    ${shots.length ? `<div class="shot-row">${shots.map(u => `<img src="${u}" alt="${esc(g.title)}のスクリーンショット" loading="lazy">`).join('')}</div>` : ''}
  </div>
  <div class="detail-info">
    <h1 class="page-title">${esc(g.title)}</h1>
    ${has(g.summary) ? `<p class="detail-summary">${esc(g.summary)}</p>` : ''}
    <p class="detail-actions">${buttons}</p>
    <dl class="def">
      ${defRow('ジャンル', has(g.genre) ? esc(g.genre) : null)}
      ${defRow('プレイ人数', has(g.players) ? esc(g.players) : null)}
      ${defRow('制作年度', g.year != null ? `<a href="/years/${g.year}/">${g.year}年度</a>` : null)}
      ${defRow('制作元', orgNames.length ? esc(orgNames.join('・')) : null)}
      ${defRow('制作', has(g.creatorDisplay) ? esc(g.creatorDisplay) : null)}
      ${defRow('使用技術', (g.tech || []).length ? (g.tech || []).map(t => `<span class="chip chip-tech">${esc(techName(t))}</span>`).join(' ') : null)}
      ${defRow('関連活動', acts.length ? acts.map(a => `<a class="chip chip-cat" href="/activities/${a.id}/">${esc(a.title)}</a>`).join(' ') : null)}
    </dl>
  </div>
</div>
${has(g.description) ? `<section class="detail-sec"><h2>ゲーム概要</h2><p>${esc(g.description)}</p></section>` : ''}
${has(g.controls) ? `<section class="detail-sec"><h2>操作方法</h2><p>${esc(g.controls)}</p></section>` : ''}
${has(g.background) ? `<section class="detail-sec"><h2>制作背景</h2><p>${esc(g.background)}</p></section>` : ''}
${has(g.highlights) ? `<section class="detail-sec"><h2>工夫した点</h2><p>${esc(g.highlights)}</p></section>` : ''}
${topics.length ? `<section class="detail-sec"><h2>このゲームで使われている技術を学ぶ</h2><p class="chips">${topics.map(t => `<a class="chip chip-learn" href="/learn/${t.slug}/">${esc(t.title)}</a>`).join(' ')}</p></section>` : ''}
${has(g.webVersionNote) ? `<section class="detail-sec"><h2>Web版について</h2><p>${esc(g.webVersionNote)}</p></section>` : ''}
</div>`;
  out(`games/${g.id}/index.html`, page({ title: g.title, desc: g.summary, path: '/games/', content }));
}

// ---------- プレイ一覧 & プレイページ ----------
{
  const playable = games.filter(g => g.play?.playable);
  const content = `<div class="wrap page-pad">
<h1 class="page-title">ゲームを遊ぶ</h1>
<p class="page-lead">ここにある ${playable.length} 作品は、インストールなしでブラウザからそのまま遊べます（pygame-ce → WebAssembly変換）。読み込みに少し時間がかかることがあります。</p>
${cardGrid(sortYearDesc(playable).map(gameCard))}
</div>`;
  out('play/index.html', page({ title: 'ゲームを遊ぶ', path: '/play/', content }));
}
for (const g of games) {
  if (!g.play?.playable || !g.play.url) continue;
  const content = `<div class="wrap page-pad play-page">
<nav class="crumbs" aria-label="パンくず"><a href="/games/${g.id}/">← ${esc(g.title)} の詳細へ戻る</a></nav>
<h1 class="page-title">${esc(g.title)} をプレイ</h1>
<div class="play-frame-wrap">
  <iframe id="game-frame" src="${g.play.url}" title="${esc(g.title)}（ゲーム画面）" allow="autoplay; fullscreen" allowfullscreen loading="eager"></iframe>
</div>
<p class="play-tools"><button class="btn" id="fs-btn">⛶ 全画面で遊ぶ</button><a class="btn" href="/source/${g.id}/" ${g.source?.available ? '' : 'hidden'}>&lt;/&gt; ソースコードを見る</a></p>
${has(g.controls) ? `<section class="detail-sec"><h2>操作方法</h2><p>${esc(g.controls)}</p></section>` : ''}
<section class="detail-sec"><h2>うまく動かないとき</h2><p>${esc(g.play.note || '読み込みに時間がかかることがあります。音が出ない場合は一度ゲーム画面をクリックしてください。')} ゲームが始まらない場合はページを再読み込みしてください。</p></section>
</div>
<script>document.getElementById('fs-btn').addEventListener('click',()=>{const f=document.getElementById('game-frame');(f.requestFullscreen||f.webkitRequestFullscreen||function(){}).call(f);});</script>`;
  out(`play/${g.id}/index.html`, page({ title: `${g.title} をプレイ`, desc: g.summary, path: '/play/', content }));
}

// ---------- ソースコード閲覧 ----------
const sourceGames = games.filter(g => g.source?.available && g.source.dir && fs.existsSync(path.join(GS, g.source.dir)));
{
  const content = `<div class="wrap page-pad">
<h1 class="page-title">ソースコード閲覧</h1>
<p class="page-lead">公開できる作品のソースコードを、ブラウザ上でそのまま読めます。</p>
<ul class="src-list">${sortYearDesc(sourceGames).map(g => `<li><a href="/source/${g.id}/">${esc(g.title)}</a><span>${g.year != null ? g.year + '年度' : ''}</span></li>`).join('')}</ul>
</div>`;
  out('source-list/index.html', page({ title: 'ソースコード閲覧', path: '/source-list/', content }));
}
for (const g of sourceGames) {
  const dir = path.join(GS, g.source.dir);
  const files = fs.readdirSync(dir).filter(f => !f.startsWith('_') && fs.statSync(path.join(dir, f)).isFile());
  const assets = fs.existsSync(path.join(dir, '_assets.json')) ? readJSON(path.join(dir, '_assets.json')) : [];
  const fileData = files.map(f => {
    const text = fs.readFileSync(path.join(dir, f), 'utf8');
    const lang = f.endsWith('.py') ? 'python' : 'text';
    return { name: f, text, lang, lines: text.split('\n').length };
  });
  const panes = fileData.map((f, i) => `<div class="src-pane" id="pane-${i}" ${i ? 'hidden' : ''}>
    <div class="src-toolbar"><span class="src-name">${esc(f.name)}<small> ・ ${f.lines}行</small></span>
    <span><button class="btn btn-sm copy-btn" data-i="${i}">コピー</button><button class="btn btn-sm wrap-btn">折り返し</button></span></div>
    ${codeBlockHTML(f.text, f.lang)}</div>`).join('');
  const tree = `<ul class="file-tree" role="tablist">
    ${fileData.map((f, i) => `<li><button role="tab" class="file-btn${i === 0 ? ' on' : ''}" data-i="${i}" aria-selected="${i === 0}">${esc(f.name)}</button></li>`).join('')}
    ${assets.length ? `<li class="tree-h">素材ファイル</li>${assets.slice(0, 40).map(a => `<li class="tree-asset" title="${esc(a.path)}">${esc(a.path.split('/').pop())} <small>${(a.size / 1024).toFixed(0)}KB</small></li>`).join('')}${assets.length > 40 ? `<li class="tree-asset">…ほか ${assets.length - 40} ファイル</li>` : ''}` : ''}
  </ul>`;
  const content = `<div class="wrap-wide page-pad">
<nav class="crumbs" aria-label="パンくず"><a href="/games/${g.id}/">← ${esc(g.title)} の詳細へ戻る</a>${g.play?.playable ? ` ／ <a href="/play/${g.id}/">▶ このゲームを遊ぶ</a>` : ''}</nav>
<h1 class="page-title">${esc(g.title)} のソースコード</h1>
${has(g.source.note) ? `<p class="note">${esc(g.source.note)}</p>` : ''}
<div class="src-layout">
  <aside class="src-side">${tree}</aside>
  <div class="src-main">${panes}</div>
</div></div>
<script>window.__SRC__=${JSON.stringify(fileData.map(f => f.text))};</script>`;
  out(`source/${g.id}/index.html`, page({ title: `${g.title} のソースコード`, path: '/source-list/', content, bodyClass: 'page-source' }));
}

// ---------- 活動記録 ----------
{
  const tabs = `<div class="chips tabs">${['all', ...categories.map(c => c.id)].map(id =>
    `<a class="chip chip-cat${id === 'all' ? ' on' : ''}" href="${id === 'all' ? '/activities/' : '/' + catById[id].slug + '/'}">${id === 'all' ? 'すべて' : esc(catById[id].name)}</a>`).join('')}</div>`;
  const content = `<div class="wrap page-pad">
<h1 class="page-title">活動記録</h1>
<p class="page-lead">ゲームジャム・コンテスト・授業・高大連携など、ゲーム制作にまつわる活動の記録です。</p>
${tabs}
<div class="grid grid-3">${sortYearDesc(activities).map(activityCard).join('')}</div>
</div>`;
  out('activities/index.html', page({ title: '活動記録', path: '/activities/', content }));
}
for (const a of activities) {
  const ag = gamesOfActivity(a.id);
  const cat = catById[a.category];
  const orgNames = (a.organizations || []).map(id => orgById[id]?.name).filter(Boolean);
  const content = `<div class="wrap page-pad">
<nav class="crumbs" aria-label="パンくず"><a href="/">HOME</a> › <a href="/activities/">活動記録</a> › <span>${esc(a.title)}</span></nav>
<p class="chips">${[a.category, ...(a.subCategories || [])].map(c => catById[c]).filter(Boolean).map(c => `<a class="chip chip-cat" href="/${c.slug}/">${esc(c.name)}</a>`).join(' ')}${a.year != null ? ` <a class="chip chip-year" href="/years/${a.year}/">${a.year}年度</a>` : ''}</p>
<h1 class="page-title">${esc(a.title)}</h1>
${has(a.summary) ? `<p class="detail-summary">${esc(a.summary)}</p>` : ''}
<dl class="def def-wide">
  ${defRow('開催日', has(a.dates) ? esc(a.dates.join('・')) + (has(a.dateNote) ? `<small class="mut">（${esc(a.dateNote)}）</small>` : '') : (has(a.dateNote) ? esc(a.dateNote) : null))}
  ${defRow('場所', has(a.place) ? esc(a.place) : null)}
  ${defRow('対象', has(a.target) ? esc(a.target) : null)}
  ${defRow('参加人数', a.participants != null ? `${a.participants}名${a.id === 'game-jam-2' ? '以上' : ''}` : null)}
  ${defRow('チーム数', a.teams != null ? `${a.teams}チーム` : null)}
  ${defRow('テーマ', has(a.theme) ? esc(a.theme) : null)}
  ${defRow('制作形式', has(a.format) ? esc(a.format) : null)}
  ${defRow('使用技術', (a.tech || []).length ? (a.tech || []).map(t => `<span class="chip chip-tech">${esc(techName(t))}</span>`).join(' ') : null)}
  ${defRow('関係団体', orgNames.length ? esc(orgNames.join('・')) : null)}
</dl>
${has(a.description) ? `<section class="detail-sec"><h2>概要</h2><p>${esc(a.description)}</p></section>` : ''}
${ag.length ? `<section class="detail-sec"><h2>制作された作品（${ag.length}）</h2>${cardGrid(ag.map(gameCard))}</section>` : ''}
${(a.photos || []).length ? `<section class="detail-sec"><h2>活動写真</h2><div class="shot-row">${a.photos.map(u => `<img src="${u}" alt="${esc(a.title)}の活動写真" loading="lazy">`).join('')}</div></section>` : ''}
${(a.relatedDocs || []).length ? `<section class="detail-sec"><h2>関連資料</h2><ul>${a.relatedDocs.map(d => `<li><a href="${esc(d.url)}">${esc(d.title)}</a></li>`).join('')}</ul></section>` : ''}
</div>`;
  out(`activities/${a.id}/index.html`, page({ title: a.title, desc: a.summary, path: '/activities/', content }));
}

// ---------- ゲームジャム一覧（年度→開催回） ----------
{
  const jams = activities.filter(a => actCategoriesOf(a).includes('game-jam'))
    .sort((x, y) => (y.series?.number ?? -1) - (x.series?.number ?? -1));
  const byYear = {};
  for (const j of jams) (byYear[j.year ?? '年度未確認'] ??= []).push(j);
  const yearsKeys = Object.keys(byYear).sort((a, b) => (b === '年度未確認' ? -1 : a === '年度未確認' ? 1 : Number(b) - Number(a)));
  const inner = yearsKeys.map(y => `<h2 class="year-h">${y === '年度未確認' ? y : y + '年度'}</h2><div class="grid grid-3">${byYear[y].map(activityCard).join('')}</div>`).join('');
  const content = `<div class="wrap page-pad">
<h1 class="page-title">ゲームジャム一覧</h1>
<p class="page-lead">これまでに開催したゲームジャムを年度・開催回ごとにまとめています。</p>
${inner}</div>`;
  out('game-jams/index.html', page({ title: 'ゲームジャム一覧', path: '/game-jams/', content }));
}

// ---------- カテゴリページ（自動生成） ----------
for (const c of categories) {
  if (c.id === 'game-jam') continue; // 専用ページあり
  const acts = sortYearDesc(activities.filter(a => actCategoriesOf(a).includes(c.id)));
  const cg = sortYearDesc(games.filter(g => gameCatsOf(g).includes(c.id)));
  const content = `<div class="wrap page-pad">
<h1 class="page-title">${esc(c.name)}</h1>
<p class="page-lead">${esc(c.desc)}${c.id === 'ideria' ? '。IDERIAはこのアーカイブの掲載元のひとつです' : ''}。</p>
${acts.length ? `<h2 class="year-h">活動</h2><div class="grid grid-3">${acts.map(activityCard).join('')}</div>` : ''}
${cg.length ? `<h2 class="year-h">作品</h2>${cardGrid(cg.map(gameCard))}` : ''}
${!acts.length && !cg.length ? `<p class="empty">この分類の活動・作品はまだ登録されていません。データを追加すると自動的にここへ表示されます。</p>` : ''}
</div>`;
  out(`${c.slug}/index.html`, page({ title: c.name, path: `/${c.slug}/`, content }));
}

// ---------- 年度別アーカイブ ----------
{
  const content = `<div class="wrap page-pad">
<h1 class="page-title">年度別アーカイブ</h1>
<p class="page-lead">活動と作品を年度ごとに振り返ることができます。</p>
<div class="year-list">${years.map(y => {
    const gc = games.filter(g => g.year === y).length, ac = activities.filter(a => a.year === y).length;
    return `<a class="year-card" href="/years/${y}/"><span class="year-num">${y}<small>年度</small></span><span>活動 ${ac} ／ 作品 ${gc}</span></a>`;
  }).join('')}</div></div>`;
  out('years/index.html', page({ title: '年度別アーカイブ', path: '/years/', content }));
}
for (const y of years) {
  const acts = activities.filter(a => a.year === y);
  const yg = games.filter(g => g.year === y);
  const byCat = categories.map(c => ({ c, acts: acts.filter(a => actCategoriesOf(a).includes(c.id)) })).filter(x => x.acts.length);
  const content = `<div class="wrap page-pad">
<nav class="crumbs"><a href="/years/">← 年度別アーカイブ</a></nav>
<h1 class="page-title">${y}年度</h1>
${byCat.map(({ c, acts }) => `<h2 class="year-h">${esc(c.name)}</h2><div class="grid grid-3">${acts.map(activityCard).join('')}</div>`).join('')}
${yg.length ? `<h2 class="year-h">この年度の作品（${yg.length}）</h2>${cardGrid(yg.map(gameCard))}` : ''}
</div>`;
  out(`years/${y}/index.html`, page({ title: `${y}年度アーカイブ`, path: '/years/', content }));
}

// ---------- 学ぶ ----------
{
  const byLevel = { 基礎: [], 入門: [], 応用: [] };
  for (const t of learnTopics) byLevel[t.level].push(t);
  const content = `<div class="wrap page-pad">
<h1 class="page-title">学ぶ</h1>
<p class="page-lead">ゲームジャムで実際に配布された「逆引きコード」をベースにした学習トピック集です。それぞれのページでサンプルコードを読み、コピーして手元で動かしながら学べます。作品ページの「このゲームで使われている技術」からもたどれます。</p>
${Object.entries(byLevel).map(([lv, ts]) => ts.length ? `<h2 class="year-h">${lv}</h2><div class="learn-grid">${ts.map(t =>
    `<a class="learn-card" href="/learn/${t.slug}/"><span class="learn-num">${String(t.num).padStart(2, '0')}</span><span class="learn-title">${esc(t.title)}</span><span class="chip chip-level">${lv}</span></a>`).join('')}</div>` : '').join('')}
</div>`;
  out('learn/index.html', page({ title: '学ぶ', path: '/learn/', content }));
}
for (const t of learnTopics) {
  const code = fs.readFileSync(path.join(GS, 'reverse', t.file), 'utf8');
  const rel = gamesOfTopic(t.slug);
  const content = `<div class="wrap page-pad">
<nav class="crumbs"><a href="/learn/">← 学習トピック一覧</a></nav>
<p class="chips"><span class="chip chip-level">${t.level}</span></p>
<h1 class="page-title">${esc(t.title)}</h1>
<p class="page-lead">ゲームジャム参加者に配布された逆引きサンプルコードです。コピーして実行し、数値や画像を変えながら動きを確かめてみましょう（実行には Python と pygame-ce が必要です）。</p>
<div class="src-pane">
  <div class="src-toolbar"><span class="src-name">${esc(t.file)}</span><span><button class="btn btn-sm copy-btn" data-i="0">コピー</button></span></div>
  ${codeBlockHTML(code, 'python')}
</div>
${rel.length ? `<section class="detail-sec"><h2>この技術を使っている作品</h2>${cardGrid(rel.map(gameCard))}</section>` : ''}
</div>
<script>window.__SRC__=${JSON.stringify([code])};</script>`;
  out(`learn/${t.slug}/index.html`, page({ title: t.title, path: '/learn/', content, bodyClass: 'page-source' }));
}

// ---------- About / 404 ----------
{
  const content = `<div class="wrap page-pad prose">
<h1 class="page-title">このサイトについて</h1>
<p>「${esc(site.title)}」は、ゲームジャム・ゲームコンテスト・ゲームプログラミング授業・高大連携・IDERIAの制作活動などで生まれたゲーム作品を記録し、<b>遊んで・コードを読んで・学べる</b>かたちで公開しているアーカイブサイトです。</p>
<h2>できること</h2>
<p>pygame-ceで作られた作品はpygbagでWebAssemblyに変換し、ブラウザからそのまま遊べます。多くの作品はソースコードも公開しており、「学ぶ」ページでは実際のゲームジャムで配布された逆引きサンプルコードで学習できます。</p>
<h2>掲載している活動</h2>
<p><a href="/game-jams/">ゲームジャム</a>、<a href="/contests/">ゲームコンテスト</a>、<a href="/classes/">ゲームプログラミング授業</a>、<a href="/collabs/">高大連携</a>、<a href="/ideria/">IDERIA制作</a>などの活動を記録しています。作品と活動は相互にリンクしています。</p>
<h2>作品・データについて</h2>
<p>学生作品の制作者名は原則として匿名（学校名・チーム表記）で掲載しています。掲載内容に問題がある場合や、確認できていない情報（「要確認」表記）について情報をお持ちの場合は、運営までお知らせください。ゲームのWeb版はブラウザで動かすための最小限の変更（フルスクリーン解除・音声形式変換など）のみを行っており、ゲーム内容は変更していません。</p>
<h2>IDERIAについて</h2>
<p>IDERIAは本アーカイブの掲載元のひとつで、ゲーム制作・ワークショップ・高大連携などの活動を行っています。${site.ideriaOfficialUrl ? `詳しくは<a href="${esc(site.ideriaOfficialUrl)}">IDERIA公式サイト</a>をご覧ください。` : 'IDERIA公式サイトは現在準備中です。'}</p>
</div>`;
  out('about/index.html', page({ title: 'About', path: '/about/', content }));
}
out('404.html', page({
  title: 'ページが見つかりません', path: '/404',
  content: `<div class="wrap page-pad" style="text-align:center"><h1 class="page-title">404</h1><p class="page-lead">お探しのページが見つかりませんでした。</p><p><a class="btn btn-primary" href="/">HOMEへ戻る</a></p></div>`,
}));

// ---------- static assets ----------
copyDir(path.join(ROOT, 'public'), DIST);
fs.mkdirSync(path.join(DIST, 'assets'), { recursive: true });
fs.copyFileSync(path.join(SRC, 'styles.css'), path.join(DIST, 'assets/style.css'));
fs.copyFileSync(path.join(SRC, 'site.js'), path.join(DIST, 'assets/site.js'));

console.log(BASE ? `base: ${BASE}` : 'base: /' );
console.log(`build OK: ${games.length} games / ${activities.length} activities / ${learnTopics.length} learn topics / years: ${years.join(',')}`);
