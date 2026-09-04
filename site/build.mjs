#!/usr/bin/env node
/**
 * PLAYCE（ゲーム制作・プログラミング学習アーカイブ） — 静的サイトジェネレーター
 * 依存パッケージなし（Node 18+ のみ）。 `node build.mjs` で dist/ に全ページを生成します。
 * データ（src/data/ のJSON、game-sources/、public/）を追加するだけでページが自動生成されます。
 * デザイン・遊び要素の「正」は docs/DESIGN_SPEC_V2.md（サイト名 PLAYCE）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';

const ROOT = path.dirname(fileURLToPath(import.meta.url));

// CSS/JS の URL に内容のハッシュを付ける。付けないと、更新してもブラウザが
// 古いキャッシュを使い続けて表示が変わらないことがある。
const assetHash = rel => {
  const h = crypto.createHash('sha1')
    .update(fs.readFileSync(path.join(ROOT, 'src', rel))).digest('hex').slice(0, 8);
  return `/assets/${rel === 'styles.css' ? 'style.css' : rel}?v=${h}`;
};
const SRC = path.join(ROOT, 'src');
const DIST = path.join(ROOT, 'dist');
const GS = path.join(ROOT, 'game-sources');

// ---------- utils ----------
const readJSON = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
// <script> に埋めるJSON（`</script>` 等の誤解釈を防ぐ）
const json = v => JSON.stringify(v).replace(/</g, '\\u003c');
// サブパス公開対応: GitHub Pagesのプロジェクトサイト等では BASE_URL="/リポジトリ名" を指定してビルド
let BASE = '';
const has = v => v !== null && v !== undefined && v !== '' && v !== '要確認' && !(Array.isArray(v) && v.length === 0);
const PAGES = [];
function out(rel, html) {
  if (rel.endsWith('index.html')) PAGES.push('/' + rel.replace(/index\.html$/, ''));
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

// 作品No.: データの並び順（ファイル名順）で自動採番
const ORIGIN = String(site.siteUrl || '').replace(/\/+$/, ''); // OGP/sitemap用（空欄なら出力しない）
const BUILD_DATE = new Date().toISOString().slice(0, 10);
const absUrl = p => ORIGIN ? ORIGIN + p : '';

const dexNo = Object.fromEntries(games.map((g, i) => [g.id, i + 1]));
const dex = id => String(dexNo[id] || 0).padStart(2, '0');

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
const playableGames = games.filter(g => g.play?.playable && g.play.url);

// ソース公開作品（トップの統計にも使うので先に算出）
const sourceGames = games.filter(g => g.source?.available && g.source.dir && fs.existsSync(path.join(GS, g.source.dir)));
const srcFilesOf = dir => fs.readdirSync(dir).filter(f => !f.startsWith('_') && fs.statSync(path.join(dir, f)).isFile());
const sourceStats = sourceGames.reduce((acc, g) => {
  const dir = path.join(GS, g.source.dir);
  for (const f of srcFilesOf(dir)) {
    acc.files++;
    acc.lines += fs.readFileSync(path.join(dir, f), 'utf8').split('\n').length;
  }
  return acc;
}, { files: 0, lines: 0 });

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
const learnByLevel = { 基礎: [], 入門: [], 応用: [] };
for (const t of learnTopics) learnByLevel[t.level].push(t);

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

// ---------- トップのセクション（§1: 深海の演出はやめ、普通の見出しにする） ----------
const LAYERS = [
  { id: 'surface', name: 'ようこそ',     flavor: 'ゲームジャム・授業・高大連携・IDERIAの活動で生まれた作品を、遊んで・読んで・学べます。' },
  { id: 'layer-1', name: 'あそぶ',       flavor: 'まずは触れてみよう。すべてのゲームはブラウザで動く。' },
  { id: 'layer-2', name: 'よむ',         flavor: '遊んだゲームの中身を、そのまま開いて読める。' },
  { id: 'layer-3', name: 'しくみをしる', flavor: '動きのひとつひとつに名前がある。逆引きで仕組みを知る。' },
  { id: 'layer-4', name: 'つくる',       flavor: '読むから作るへ。ブラウザで動かすところまでが一本道。' },
  { id: 'layer-5', name: 'きろく',       flavor: 'ここまでの活動を、すべて記録として残しています。' },
];
// 実績バッジ（表示・トーストの文言はここが唯一の定義。site.js は window.__BADGES__ を読む）
const BADGES = [
  { id: 'first-dive', icon: '🌊', name: 'はじめての訪問', desc: 'このサイトを訪れた' },
  { id: 'first-find', icon: '🔎', name: 'はじめての発見', desc: '作品ページを1つ開いた' },
  { id: 'find5', icon: '🐟', name: '5作品発見', desc: '5作品を見た' },
  { id: 'find10', icon: '🐙', name: '10作品発見', desc: '10作品を見た' },
  { id: 'read-code', icon: '⌨', name: 'コードを読んだ', desc: 'ソースコードのページを開いた' },
  { id: 'all-layers', icon: '🧭', name: '最後まで到達', desc: 'トップページの最後までたどり着いた' },
];

// ---------- layout ----------
const NAV = [
  ['/play/', 'あそぶ'],
  ['/games/', '作品'],
  ['/activities/', '活動'],
  ['/learn/', '学ぶ'],
  ['/about/', 'About'],
];
const MARK = `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
  <circle cx="12" cy="12" r="3" fill="#4fd8c4"/>
  <circle cx="12" cy="12" r="6.5" fill="none" stroke="#4fd8c4" stroke-opacity=".6" stroke-width="1.4"/>
  <circle cx="12" cy="12" r="10" fill="none" stroke="#4fd8c4" stroke-opacity=".3" stroke-width="1.2"/>
</svg>`;
// 関連サイト（フッターの上・全ページ共通。site.json のURLが空欄のカードは出さない）
const RELATED_SITES = [
  { key: 'portfolioUrl', name: '永野斗遠 ポートフォリオ', desc: 'このアーカイブの制作者の業績・活動' },
  { key: 'ideriaOfficialUrl', name: 'IDERIA公式サイト', desc: 'ゲームを生み出している制作団体' },
].map(r => ({ ...r, url: site[r.key] })).filter(r => has(r.url));
const shortUrl = u => String(u).replace(/^https?:\/\//, '').replace(/\/$/, '');
const relatedHTML = RELATED_SITES.length ? `<section class="related" aria-labelledby="related-h">
  <div class="wrap">
    <h2 class="related-h" id="related-h">関連サイト</h2>
    <div class="rel-grid">${RELATED_SITES.map(r => `<a class="rel-card" href="${esc(r.url)}" target="_blank" rel="noopener">
      <span class="rel-name">${esc(r.name)} <span class="rel-ext" aria-hidden="true">↗</span></span>
      <span class="rel-desc">${esc(r.desc)}</span>
      <span class="rel-url">${esc(shortUrl(r.url))}<span class="vh">（外部サイト・新しいタブで開きます）</span></span>
    </a>`).join('')}</div>
  </div>
</section>` : '';

function page({ title, desc, path: cur = '/', content, extraHead = '', bodyClass = '', discover = '', readCode = false, home = false, url = '', image = '', jsonLd = null }) {
  const fullTitle = title ? `${title} | ${site.title}` : `${site.title} — ${site.tagline}`;
  const ogImage = ORIGIN ? absUrl(image || '/images/og-default.png') : '';
  const ogUrl = ORIGIN ? absUrl(url || cur) : '';
  const extLinks = [
    site.ideriaOfficialUrl ? [site.ideriaOfficialUrl, 'IDERIA公式サイト'] : null,
    site.portfolioUrl ? [site.portfolioUrl, 'ポートフォリオ'] : null,
  ].filter(Boolean);
  const bodyAttrs = [
    bodyClass ? ` class="${bodyClass}"` : '',
    discover ? ` data-discover="${esc(discover)}"` : '',
    readCode ? ' data-read-code="1"' : '',
  ].join('');
  return `<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(fullTitle)}</title>
<meta name="description" content="${esc(desc || site.description)}">
<meta property="og:title" content="${esc(fullTitle)}">
<meta property="og:description" content="${esc(desc || site.description)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="${esc(site.title)}">
<meta property="og:locale" content="ja_JP">
${ogUrl ? `<meta property="og:url" content="${esc(ogUrl)}">\n<link rel="canonical" href="${esc(ogUrl)}">` : ''}
${ogImage ? `<meta property="og:image" content="${esc(ogImage)}">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="${esc(ogImage)}">` : '<meta name="twitter:card" content="summary">'}
<meta name="theme-color" content="#040c16">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="${assetHash('styles.css')}">
<script>document.documentElement.className+=' js';if(!document.hidden)document.documentElement.className+=' anim-in';try{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.dataset.theme=t;}catch(e){}</script>
<script>window.__BASE__=${json(BASE)};window.__BADGES__=${json(BADGES)};</script>
${jsonLd ? `<script type="application/ld+json">${json(jsonLd).replace(/</g, '\u003c')}</script>` : ''}
${extraHead}
</head>
<body${bodyAttrs}>
<a class="vh" href="#main">本文へスキップ</a>
<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="/"><span class="brand-mark">${MARK}</span> <span class="brand-text"><span class="brand-name">${esc(site.title)}</span><span class="brand-sub">${esc(site.subtitle || '')}</span></span></a>
    <button type="button" id="nav-toggle" class="nav-toggle js-only" hidden aria-expanded="false" aria-controls="site-nav">メニュー</button>
    <nav class="nav" id="site-nav" aria-label="メインメニュー">
      ${NAV.map(([href, label]) => `<a href="${href}"${cur.startsWith(href) ? ' class="on" aria-current="page"' : ''}>${label}</a>`).join('')}
    </nav>
    <button type="button" id="theme-toggle" class="theme-toggle js-only" hidden aria-label="配色を切りかえ" title="配色を切りかえ">◐</button>
  </div>
</header>
<main id="main" tabindex="-1">${content}</main>
${relatedHTML}
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <p class="foot-title">${esc(site.title)}</p>
      <p class="foot-desc">${esc(site.tagline)}。ゲームジャム・授業・高大連携・IDERIAの制作活動を記録しています。</p>
      ${extLinks.length ? `<p class="foot-links">${extLinks.map(([u, l]) => `<a href="${esc(u)}" target="_blank" rel="noopener">${l} ↗</a>`).join('')}</p>` : ''}
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
  <p class="foot-copy">最終更新（ビルド）: ${BUILD_DATE} ／ © ${new Date().getFullYear()} ${esc(site.title)}</p>
</footer>
<button class="surface-btn js-only" id="surface-btn" type="button" hidden aria-label="ページの最上部へ戻る">
  <span class="up" aria-hidden="true">↑</span>上へ戻る</button>
<div class="toast-wrap" id="toast-wrap" aria-live="polite"></div>
<script src="${assetHash('site.js')}" defer></script>
</body>
</html>`;
}

// ---------- 構造化データ（JSON-LD） ----------
// 検索結果での見え方のため。書けるのは掲載データから確実に言えることだけにする。
const siteLd = () => (ORIGIN ? {
  '@context': 'https://schema.org', '@type': 'WebSite',
  name: site.title, alternateName: site.subtitle, url: absUrl('/'),
  description: site.description, inLanguage: 'ja',
} : null);
function crumbLd(items) {
  if (!ORIGIN) return null;
  return {
    '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: items.map(([name, u], i) => ({
      '@type': 'ListItem', position: i + 1, name, item: absUrl(u),
    })),
  };
}
function gameLd(g) {
  if (!ORIGIN) return null;
  const ld = {
    '@context': 'https://schema.org', '@type': 'VideoGame',
    name: g.title, url: absUrl(`/games/${g.id}/`), inLanguage: 'ja',
  };
  if (has(g.summary)) ld.description = g.summary;
  if (g.thumbnail) ld.image = absUrl(g.thumbnail);
  if (has(g.genre)) ld.genre = g.genre;
  if (has(g.creatorDisplay)) ld.creator = { '@type': 'Organization', name: g.creatorDisplay };
  if (g.play?.playable) { ld.gamePlatform = 'Web browser'; ld.playMode = 'SinglePlayer'; ld.isAccessibleForFree = true; }
  return ld;
}
// ---------- 画像の実寸 ----------
// width/height を出さないと読み込み中にレイアウトがずれる（CLS）。
// 依存を増やさないため、PNG と JPEG のヘッダだけを自前で読む。
const _sizeCache = new Map();
function imgSize(webPath) {
  if (_sizeCache.has(webPath)) return _sizeCache.get(webPath);
  let out = null;
  try {
    const buf = fs.readFileSync(path.join(ROOT, 'public', webPath.replace(/^\//, '')));
    if (buf.length > 24 && buf.toString('ascii', 1, 4) === 'PNG') {
      out = { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
    } else if (buf[0] === 0xFF && buf[1] === 0xD8) {
      for (let i = 2; i + 9 < buf.length;) {
        if (buf[i] !== 0xFF) { i++; continue; }
        const m = buf[i + 1];
        if (m >= 0xC0 && m <= 0xCF && m !== 0xC4 && m !== 0xC8 && m !== 0xCC) {
          out = { h: buf.readUInt16BE(i + 5), w: buf.readUInt16BE(i + 7) }; break;
        }
        i += 2 + buf.readUInt16BE(i + 2);
      }
    }
  } catch { /* 画像が無いときは属性を出さない */ }
  _sizeCache.set(webPath, out);
  return out;
}
const sizeAttr = u => { const d = imgSize(u); return d ? ` width="${d.w}" height="${d.h}"` : ''; };
// ---------- 操作デバイス ----------
// 訪問者の多くはスマートフォンで見るため、開く前にキーボードの要否が分かるようにする。
// 判定は controls の記述だけを根拠にし、勝手な推測はしない。
// 「ダブルタップ」はキーの連打を指す作品があるため、指の操作としては数えない。
function inputKind(g) {
  if (!g.play?.playable) return null;
  const c = g.controls || '';
  const key = /キー|Enter|スペース|矢印|ESC/.test(c);
  const pointer = /クリック|マウス/.test(c);
  // バッジは「キーボードが要るか」だけを答える。内訳は note で説明する
  if (key && pointer) return { label: '⌨ キーボード', note: 'キーボードとマウスの両方を使います。キーボードのない端末では遊べません。' };
  if (key) return { label: '⌨ キーボード', note: 'キーボードで操作します。キーボードのない端末では遊べません。' };
  if (pointer) return { label: '🖱 マウス', note: 'マウス（クリック）だけで操作します。' };
  return null;
}
const inputBadge = g => {
  const k = inputKind(g);
  return k ? `<span class="chip chip-input" title="${esc(k.note)}">${esc(k.label)}</span>` : '';
};
// ---------- partials ----------
const badgePlay = `<span class="badge badge-play">▶ ブラウザで遊べる</span>`;
function gameCard(g) {
  const acts = (g.activities || []).map(id => actById[id]).filter(Boolean);
  const orgNames = (g.organizations || []).map(id => orgById[id]?.name).filter(Boolean);
  const thumb = g.thumbnail
    ? `<img src="${g.thumbnail}" alt="${esc(g.title)}のプレイ画面" loading="lazy" width="640" height="400">`
    : `<div class="thumb-ph" role="img" aria-label="${esc(g.title)}（画像準備中）"><span class="ph-title">${esc(g.title)}</span><small>画像準備中</small></div>`;
  return `<a class="card game-card" href="/games/${g.id}/" data-gid="${g.id}">
  <span class="dex-no">No.${dex(g.id)}</span><span class="stamp">発見済み</span>
  <div class="thumb">${thumb}${g.play?.playable ? badgePlay : ''}</div>
  <div class="card-body">
    <h3 class="card-title">${esc(g.title)}</h3>
    ${has(g.summary) ? `<p class="card-summary">${esc(g.summary)}</p>` : ''}
    <p class="card-meta">
      ${has(g.genre) ? `<span class="chip chip-genre">${esc(g.genre)}</span>` : ''}
      ${g.year != null ? `<span class="chip chip-year">${g.year}年度</span>` : ''}
      ${inputBadge(g)}
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
// セクションの見出し
function layerHead(l) {
  return `<div class="layer-head">
    <h2 class="layer-title" id="${l.id}-h">${esc(l.name)}</h2>
    <p class="layer-flavor">${esc(l.flavor)}</p>
  </div>`;
}
function layer(l, i, inner) {
  return `<section class="layer lay-${i}" id="${l.id}" aria-labelledby="${l.id}-h">
  <div class="wrap">${layerHead(l)}${inner}</div></section>`;
}
const randomBtn = (cls = 'btn') => `<button type="button" class="${cls} js-only" hidden data-random-dive>🎲 ランダムに1本</button>`;
// 泡（座標は固定値。prefers-reduced-motion では CSS 側で非表示）
const playableScript = `<script>window.__PLAYABLE__=${json(playableGames.map(g => g.id))};</script>`;

// ヒーローの背景に敷く作品サムネの帯（§1-4）。文字だけの画面にしないための装飾で、
// 内容は下のカードと重複するため読み上げ対象から外す。
function heroStrip() {
  const shots = games.filter(g => g.thumbnail).map(g => g.thumbnail);
  if (shots.length < 8) return '';
  // 途切れずに流れて見えるよう2周ぶん並べる
  const row = [...shots, ...shots].slice(0, 40);
  return `<div class="hero-strip" aria-hidden="true">${row.map(u =>
    `<img src="${u}" alt="" loading="lazy" decoding="async"${sizeAttr(u)}>`).join('')}</div>`;
}

// ---------- HOME ----------
{
  const [L0, L1, L2, L3, L4, L5] = LAYERS;

  // あそぶ: 遊べる作品のハイライト
  const pickIds = ['ideria-chokopaki', 'gj4-hill-rush', 'gj3-music-game', 'obg-order-recall'];
  const picked = pickIds.map(id => gameById[id]).filter(g => g && g.play?.playable);
  const featured = [...picked, ...playableGames.filter(g => g.thumbnail && !pickIds.includes(g.id))].slice(0, 6);

  // 第2層: コードのプレビュー
  const peekTopic = learnBySlug['r02'] || learnTopics[0];
  const peekCode = peekTopic
    ? fs.readFileSync(path.join(GS, 'reverse', peekTopic.file), 'utf8').split('\n').slice(0, 22).join('\n')
    : '';
  const peek = peekTopic ? `<div class="code-peek">
      <div class="src-toolbar"><span class="src-name">${esc(peekTopic.file)}<small> ・ 冒頭22行</small></span></div>
      ${codeBlockHTML(peekCode, 'python')}
    </div>` : '';

  // 第3層: 基礎/入門/応用
  const levelDesc = {
    基礎: '変数・くり返し・条件分岐・データ構造。プログラムそのものの土台。',
    入門: '画像を出す・キーで動かす・当たり判定。ゲームの部品をひとつずつ。',
    応用: '画面シェイク・なめらか追従・AIの巡回。遊びを面白くする表現。',
  };
  const levelCards = Object.entries(learnByLevel).filter(([, ts]) => ts.length).map(([lv, ts]) =>
    `<a class="level-card" href="/learn/">
      <span class="level-head"><span class="level-name">${lv}</span><span class="level-n">${ts.length} トピック</span></span>
      <span class="level-desc">${esc(levelDesc[lv] || '')}</span>
      <span class="level-eg">${ts.slice(0, 3).map(t => `<span class="chip chip-learn">${esc(t.title)}</span>`).join('')}</span>
    </a>`).join('');

  // 最深部: 活動の記録
  // トップの「きろく」に出すのは ゲームジャム・ゲームコンテスト・
  // ゲームプログラミング授業 の3種別だけ。高大連携やIDERIA制作、
  // VR体験のワークショップはここには出さない（活動一覧には残る）。
  const RECORD_CATS = ['game-jam', 'contest', 'class'];
  // 「新しい順」は年度だけでなく実際の日付で決める。年度だけで並べると
  // 同じ年度内が回数順になり、第3回より第1回が先に出てしまう。
  const actWhen = a => (a.dates || []).slice().sort().pop() || (a.year != null ? a.year + '-00' : '');
  const recentActs = activities
    .filter(a => RECORD_CATS.includes(a.category))
    .sort((x, y) => String(actWhen(y)).localeCompare(String(actWhen(x))))
    .slice(0, 3);
  const catCards = ['game-jam', 'contest', 'class', 'collab', 'ideria'].map(id => {
    const c = catById[id];
    const count = games.filter(g => gameCatsOf(g).includes(id)).length;
    return `<a class="cat-card" href="/${c.slug}/"><span class="cat-name">${esc(c.name)}</span><span class="cat-desc">${esc(c.desc)}</span><span class="cat-count">${count ? `${count} 作品` : '教材のみ'}</span></a>`;
  }).join('');

  const content = `
<section class="layer surface" id="${L0.id}">
  ${heroStrip()}
  <div class="wrap hero-in">
    <p class="hero-eyebrow">PLAY + PLACE</p>
    <h1 class="hero-title">${esc(site.tagline)}。</h1>
    <p class="hero-lead">ここは、ゲームジャム・授業・高大連携・IDERIAの活動で生まれたゲームの置き場所。<br>
    <strong>あそぶ → よむ → しくみをしる → つくる</strong> の順に並べています。</p>
    <p class="hero-cta"><a class="btn btn-primary btn-lg" href="#${L1.id}">作品を見る</a>${randomBtn('btn btn-lg')}<a class="btn btn-lg" href="/games/">作品一覧</a></p>
    <p class="hero-stats"><span><b>${games.length}</b> 作品</span><span><b>${playableGames.length}</b> ブラウザ対応</span><span><b>${sourceGames.length}</b> ソース公開</span><span><b>${activities.length}</b> 活動</span><span><b>${learnTopics.length}</b> 学習トピック</span></p>
  </div>
</section>
${layer(L1, 1, `${cardGrid(featured.map(gameCard))}
  <p class="layer-actions"><a class="btn btn-primary" href="/play/">▶ 遊べる作品をすべて見る</a><a class="btn" href="/games/">作品一覧</a>${randomBtn()}</p>`)}
${layer(L2, 2, `<div class="peek-grid">${peek}
  <ul class="peek-facts">
    <li><b>${sourceGames.length}</b> 作品のソースコードを公開</li>
    <li><b>${sourceStats.lines.toLocaleString('en-US')}</b> 行のコードがそのまま読める</li>
    <li><b>${sourceStats.files}</b> 個のファイルを行番号つきで表示</li>
  </ul></div>
  <p class="layer-actions"><a class="btn btn-primary" href="/source-list/">&lt;/&gt; ソースコードを読む</a></p>`)}
${layer(L3, 3, `<div class="level-grid">${levelCards}</div>
  <p class="layer-actions"><a class="btn btn-primary" href="/learn/">学習トピック ${learnTopics.length} 本を見る</a></p>`)}
${layer(L4, 4, `<ol class="route">
    <li><h3>遊んで決める</h3><p>作品一覧から気になる作品を選んで、ブラウザでそのまま遊ぶ。作りたいものの手ざわりを知る。</p></li>
    <li><h3>コードを読む</h3><p>同じ作品のソースコードを開いて、動きがどう書かれているかを確かめる。</p></li>
    <li><h3>逆引きで作る</h3><p>「学ぶ」の逆引きコードをコピーして動かし、数値や画像を変えながら自分のゲームにする。</p></li>
    <li><h3>Web版にする</h3><p>pygame-ce で作った作品は pygbag でWebAssemblyに変換すれば、ブラウザで遊べる形で公開できる。</p></li>
  </ol>
  <p class="layer-actions"><a class="btn btn-primary" href="/learn/">逆引きコードを見る</a><a class="btn" href="/about/">このサイトの作り方</a></p>`)}
${layer(L5, 5, `<div class="grid grid-3">${recentActs.map(activityCard).join('')}</div>
  <p class="layer-actions"><a class="btn btn-primary" href="/activities/">活動記録をすべて見る</a><a class="btn" href="/game-jams/">ゲームジャム一覧</a><a class="btn" href="/years/">年度別アーカイブ</a></p>
  <div class="cat-grid" style="margin-top:26px">${catCards}</div>`)}
${playableScript}`;
  out('index.html', page({ content, path: '/', home: true, jsonLd: siteLd() }));
}

// ---------- 実施プロジェクトごとのまとまり（§3-1） ----------
// 1作品が複数のプロジェクトに属することがある（例: 第3回ゲームジャムの作品が
// OneButtonGamesにも収録）。その場合は両方のプロジェクトに出す。
function projectGroups() {
  const withGames = activities
    .map(a => ({ act: a, list: sortYearDesc(games.filter(g => (g.activities || []).includes(a.id))) }))
    .filter(x => x.list.length);
  // 新しい順。年の無い活動（IDERIAの制作物など）は最後にまとめる
  withGames.sort((x, y) => (y.act.year || 0) - (x.act.year || 0)
    || String(x.act.id).localeCompare(String(y.act.id)));
  return withGames;
}
function projectHead(a, n) {
  const cat = catById[a.category];
  const meta = [
    a.year != null ? `${a.year}年度` : '',
    cat ? cat.name : '',
    has(a.place) ? a.place : '',
    `${n}作品`,
  ].filter(Boolean);
  return `<div class="proj-head">
    <h3 class="proj-title" id="proj-${a.id}">${esc(a.title)}</h3>
    <p class="proj-meta">${meta.map(m => `<span>${esc(m)}</span>`).join('')}</p>
    ${has(a.summary) ? `<p class="proj-summary">${esc(a.summary)}</p>` : ''}
    <p class="proj-more"><a href="/activities/${a.id}/">この活動の詳細</a></p>
  </div>`;
}
// ---------- 作品一覧 /games/ ----------
{
  const ord = Object.fromEntries(sortYearDesc(games).map((g, i) => [g.id, i]));
  // 検索対象を拡張（制作元・関連活動・使用技術・活動種別も引っかかるようにする）
  const searchText = g => [
    g.title, g.summary, g.genre, g.creatorDisplay,
    ...(g.organizations || []).map(id => orgById[id]?.name),
    ...(g.activities || []).map(id => actById[id]?.title),
    ...(g.tech || []).map(techName),
    ...gameCatsOf(g).map(id => catById[id]?.name),
  ].filter(Boolean).join(' ').toLowerCase();
  const idx = games.map(g => ({
    id: g.id, no: dexNo[g.id], ord: ord[g.id],
    title: g.title, text: searchText(g),
    year: g.year, techs: g.tech || [], orgs: g.organizations || [],
    cats: gameCatsOf(g), genre: g.genre || '', playable: !!(g.play && g.play.playable),
  }));
  const status = `
<div class="dex-status">
  <p class="dex-count" id="stamp-count" data-total="${games.length}"><b>0</b> / ${games.length} 発見</p>
  <div class="dex-bar js-only" id="dex-bar" data-store-only hidden aria-hidden="true"><i></i></div>
  <ul class="badge-shelf" id="badge-shelf">${BADGES.map(b =>
    `<li class="badge-item" data-badge="${b.id}" title="${esc(b.desc)}"><i>${b.icon}</i>${esc(b.name)}</li>`).join('')}</ul>
  <p class="dex-hint">作品ページ・プレイページを開くと「発見済み」のスタンプが付きます（記録はこのブラウザにだけ保存され、送信されません）。</p>
  <div class="dex-tools js-only" data-store-only hidden>
    <label class="check"><input type="checkbox" id="f-silhouette"> 未発見をシルエット表示</label>
    <button type="button" class="btn btn-sm" id="reset-record">発見記録・実績を消す</button>
  </div>
</div>`;
  const filters = `
<div class="filters" id="filters">
  <div class="filters-row">
    <input type="search" id="q" placeholder="タイトル・活動・技術などで検索" aria-label="作品を検索">
    <select id="f-sort" aria-label="並び替え"><option value="no">並び: 作品No.順</option><option value="name">並び: 名前順（辞書順）</option><option value="act">並び: 活動・年度順</option><option value="play">並び: 遊べる作品を先に</option></select>
    <button type="button" class="btn btn-sm js-only" hidden id="filter-toggle" aria-expanded="false" aria-controls="filters-more">絞り込み ▾</button>
    ${randomBtn('btn btn-sm')}
  </div>
  <div class="filters-more" id="filters-more">
    <select id="f-year" aria-label="年度で絞り込み"><option value="">年度: すべて</option>${years.map(y => `<option value="${y}">${y}年度</option>`).join('')}</select>
    <select id="f-cat" aria-label="活動種別で絞り込み"><option value="">活動種別: すべて</option>${categories.map(c => `<option value="${c.id}">${esc(c.name)}</option>`).join('')}</select>
    <select id="f-genre" aria-label="ジャンルで絞り込み"><option value="">ジャンル: すべて</option>${[...new Set(games.map(g => g.genre).filter(has))].map(x => `<option>${esc(x)}</option>`).join('')}</select>
    <select id="f-tech" aria-label="使用技術で絞り込み"><option value="">技術: すべて</option>${[...new Set(games.flatMap(g => g.tech || []))].map(t => `<option value="${t}">${esc(techName(t))}</option>`).join('')}</select>
    <select id="f-org" aria-label="制作元で絞り込み"><option value="">制作元: すべて</option>${organizations.map(o => `<option value="${o.id}">${esc(o.name)}</option>`).join('')}</select>
    <select id="f-found" class="js-only" data-store-only hidden aria-label="発見状態で絞り込み"><option value="">発見状態: すべて</option><option value="new">未発見のみ</option><option value="found">発見済みのみ</option></select>
    <label class="check"><input type="checkbox" id="f-play"> プレイ可能のみ</label>
    <button type="button" class="btn btn-sm js-only" hidden id="f-reset">条件をクリア</button>
  </div>
</div>
<p class="result-count" id="count" role="status">${games.length} / ${games.length} 作品を表示中</p>`;
  const groups = projectGroups();
  // 近道の一覧はゲームジャムとコンテストだけにする。高大連携やIDERIA制作まで並べると11件になり、絞り込みより先に4行を占めていた。
  // 一覧そのもの（下のセクション）は全プロジェクトを出す。ここから外しても作品は消えない。
  const jumpGroups = groups.filter(({ act }) => ['game-jam', 'contest'].includes(act.category));
  const content = `<div class="wrap page-pad">
<h1 class="page-title">作品一覧</h1>
<p class="page-lead">これまでの活動で生まれたゲーム作品 ${games.length} 件を、<strong>実施したプロジェクトごと</strong>にまとめています。1つの作品が複数のプロジェクトに出ることがあります。</p>
<nav class="proj-jump" aria-label="ゲームジャム・コンテストから探す">
  <span class="proj-jump-h">ゲームジャム・コンテストから探す</span>
  ${jumpGroups.map(({ act, list }) => `<a href="#proj-${act.id}">${esc(act.title)}<b>${list.length}</b></a>`).join('')}
</nav>
${filters}
<p class="kbd-hint"><kbd>/</kbd> で検索欄へ移動、<kbd>Esc</kbd> で解除できます。</p>
<h2 class="vh">プロジェクトごとの作品</h2>
<div id="game-grid">
${groups.map(({ act, list }) => `<section class="proj" data-proj="${act.id}">
  ${projectHead(act, list.length)}
  <div class="grid">${list.map(g => `<div class="gi" data-id="${g.id}">${gameCard(g)}</div>`).join('')}</div>
</section>`).join('')}
</div>
<p class="empty" id="empty" hidden>条件にあう作品が見つかりませんでした。</p>
<details class="dex-fold">
  <summary>発見スタンプ・実績（このブラウザだけの記録）</summary>
  ${status}
</details>
</div>
<script>window.__GAMES__=${json(idx)};</script>
${playableScript}`;
  out('games/index.html', page({ title: '作品一覧', path: '/games/', content }));
}

// ---------- 作品詳細 ----------
for (const g of games) {
  const gi = games.indexOf(g);
  const prevG = games[gi - 1], nextG = games[gi + 1];
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
    `<button type="button" class="btn js-only" hidden data-copy-url>🔗 URLをコピー</button>`,
  ].filter(Boolean).join('');
  const content = `<div class="wrap page-pad">
<nav class="crumbs" aria-label="パンくず"><a href="/">HOME</a> › <a href="/games/">作品一覧</a> › <span>${esc(g.title)}</span></nav>
<div class="detail-grid">
  <div class="detail-media">${main}
    <p class="badge-line"><span class="chip chip-tech">作品No.${dex(g.id)}</span>${g.play?.playable ? badgePlay : ''}<span class="found-mark" id="found-mark">発見済み</span></p>
    ${shots.length ? `<div class="shot-row">${shots.map(u => `<img src="${u}" alt="${esc(g.title)}のスクリーンショット" loading="lazy"${sizeAttr(u)}>`).join('')}</div>` : ''}
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
${has(g.controls) ? `<section class="detail-sec"><h2>操作方法</h2><p>${esc(g.controls)}</p>${inputKind(g) ? `<p class="note">${esc(inputKind(g).note)}</p>` : ''}</section>` : ''}
${has(g.background) ? `<section class="detail-sec"><h2>制作背景</h2><p>${esc(g.background)}</p></section>` : ''}
${has(g.highlights) ? `<section class="detail-sec"><h2>工夫した点</h2><p>${esc(g.highlights)}</p></section>` : ''}
${topics.length ? `<section class="detail-sec"><h2>このゲームで使われている技術を学ぶ</h2><p class="chips">${topics.map(t => `<a class="chip chip-learn" href="/learn/${t.slug}/">${esc(t.title)}</a>`).join(' ')}</p></section>` : ''}
${has(g.webVersionNote) ? `<section class="detail-sec"><h2>Web版について</h2><p>${esc(g.webVersionNote)}</p></section>` : ''}
<nav class="pager" aria-label="作品No.順の移動">
  ${prevG ? `<a class="pg-prev" href="/games/${prevG.id}/"><small>← No.${dex(prevG.id)} 前の作品</small><b>${esc(prevG.title)}</b></a>` : ''}
  ${nextG ? `<a class="pg-next" href="/games/${nextG.id}/"><small>No.${dex(nextG.id)} 次の作品 →</small><b>${esc(nextG.title)}</b></a>` : ''}
</nav>
</div>`;
  out(`games/${g.id}/index.html`, page({
    title: g.title, desc: g.summary, path: '/games/', content, discover: g.id,
    url: `/games/${g.id}/`, image: g.thumbnail || '',
    jsonLd: [gameLd(g), crumbLd([['HOME', '/'], ['作品一覧', '/games/'], [g.title, `/games/${g.id}/`]])].filter(Boolean),
  }));
}

// ---------- プレイ一覧 & プレイページ ----------
{
  const content = `<div class="wrap page-pad">
<h1 class="page-title">ゲームを遊ぶ</h1>
<p class="page-lead">ここにある ${playableGames.length} 作品は、インストールなしでブラウザからそのまま遊べます（pygame-ce → WebAssembly変換）。読み込みに少し時間がかかることがあります。</p>
<p class="detail-actions">${randomBtn('btn btn-primary')}</p>
<h2 class="vh">遊べる作品リスト</h2>
${cardGrid(sortYearDesc(playableGames).map(gameCard))}
</div>
${playableScript}`;
  out('play/index.html', page({ title: 'ゲームを遊ぶ', path: '/play/', content }));
}
for (const g of playableGames) {
  const content = `<div class="wrap page-pad play-page">
<nav class="crumbs" aria-label="パンくず"><a href="/">HOME</a> › <a href="/games/">作品一覧</a> › <a href="/games/${g.id}/">${esc(g.title)}</a> › <span>プレイ</span></nav>
<h1 class="page-title">${esc(g.title)} をプレイ</h1>
${inputKind(g) ? `<p class="play-note"><b>${esc(inputKind(g).label)}</b> — ${esc(inputKind(g).note)}</p>` : ''}
<div class="play-frame-wrap">
  <!-- 初回は20MBほど読み込むため、黙って黒い画面を見せない -->
  <div class="play-loading js-only" id="play-loading" role="status" hidden>
    <span class="spin" aria-hidden="true"></span>
    <b>ゲームを読み込んでいます…</b>
    <small>初回は20MBほど読み込むため、少し時間がかかります</small>
  </div>
  <iframe id="game-frame" src="${g.play.url}" title="${esc(g.title)}（ゲーム画面）" allow="autoplay; fullscreen" allowfullscreen loading="eager"></iframe>
</div>
<!-- js-only は付けない。付けると読み込み中から出てしまう（表示は準備完了後にJSが行う） -->
<p class="play-hint" id="play-hint" hidden>▶ ゲーム画面をクリックすると始まります</p>
<p class="play-tools"><button type="button" class="btn js-only" hidden id="fs-btn">⛶ 全画面で遊ぶ</button><a class="btn" href="/games/${g.id}/">作品の詳細へ</a>${g.source?.available ? `<a class="btn" href="/source/${g.id}/">&lt;/&gt; ソースコードを見る</a>` : ''}${randomBtn()}</p>
${has(g.controls) ? `<section class="detail-sec"><h2>操作方法</h2><p>${esc(g.controls)}</p></section>` : ''}
<section class="detail-sec"><h2>うまく動かないとき</h2><p>${esc(g.play.note || '読み込みに時間がかかることがあります。音が出ない場合は一度ゲーム画面をクリックしてください。')} ゲームが始まらない場合はページを再読み込みしてください。</p></section>
</div>
${playableScript}`;
  out(`play/${g.id}/index.html`, page({
    title: `${g.title} をプレイ`, desc: g.summary, path: '/play/', content, discover: g.id,
    url: `/play/${g.id}/`, image: g.thumbnail || '',
  }));
}

// ---------- ソースコード閲覧 ----------
{
  const content = `<div class="wrap page-pad">
<h1 class="page-title">ソースコード閲覧</h1>
<p class="page-lead">公開できる作品のソースコードを、ブラウザ上でそのまま読めます（${sourceGames.length}作品・${sourceStats.lines.toLocaleString('en-US')}行）。</p>
<ul class="src-list">${sortYearDesc(sourceGames).map(g => `<li><a href="/source/${g.id}/">${esc(g.title)}</a><span>${g.year != null ? g.year + '年度' : ''}</span></li>`).join('')}</ul>
</div>`;
  out('source-list/index.html', page({ title: 'ソースコード閲覧', path: '/source-list/', content }));
}
for (const g of sourceGames) {
  const dir = path.join(GS, g.source.dir);
  const files = srcFilesOf(dir);
  const assets = fs.existsSync(path.join(dir, '_assets.json')) ? readJSON(path.join(dir, '_assets.json')) : [];
  const fileData = files.map(f => {
    const text = fs.readFileSync(path.join(dir, f), 'utf8');
    const lang = f.endsWith('.py') ? 'python' : 'text';
    return { name: f, text, lang, lines: text.split('\n').length };
  });
  const panes = fileData.map((f, i) => `<div class="src-pane" id="pane-${i}" ${i ? 'hidden' : ''}>
    <div class="src-toolbar"><span class="src-name">${esc(f.name)}<small> ・ ${f.lines}行</small></span>
    <span class="js-only" hidden><button type="button" class="btn btn-sm copy-btn" data-i="${i}">コピー</button><button type="button" class="btn btn-sm wrap-btn">折り返し</button></span></div>
    ${codeBlockHTML(f.text, f.lang)}</div>`).join('');
  const tree = `<ul class="file-tree" role="tablist">
    ${fileData.map((f, i) => `<li><button type="button" role="tab" class="file-btn${i === 0 ? ' on' : ''}" data-i="${i}" aria-selected="${i === 0}">${esc(f.name)}</button></li>`).join('')}
    ${assets.length ? `<li class="tree-assets"><details><summary>素材ファイル ${assets.length}件</summary><ul>${assets.slice(0, 40).map(a =>
      `<li class="tree-asset" title="${esc(a.path)}">${esc(a.path.split('/').pop())} <small>${(a.size / 1024).toFixed(0)}KB</small></li>`).join('')}${assets.length > 40 ? `<li class="tree-asset">…ほか ${assets.length - 40} ファイル</li>` : ''}</ul></details></li>` : ''}
  </ul>`;
  const content = `<div class="wrap-wide page-pad">
<nav class="crumbs" aria-label="パンくず"><a href="/games/${g.id}/">← ${esc(g.title)} の詳細へ戻る</a>${g.play?.playable ? ` ／ <a href="/play/${g.id}/">▶ このゲームを遊ぶ</a>` : ''}</nav>
<h1 class="page-title">${esc(g.title)} のソースコード</h1>
${has(g.source.note) ? `<p class="note">${esc(g.source.note)}</p>` : ''}
<div class="src-layout">
  <aside class="src-side">${tree}</aside>
  <div class="src-main">${panes}</div>
</div></div>
<script>window.__SRC__=${json(fileData.map(f => f.text))};</script>`;
  out(`source/${g.id}/index.html`, page({ title: `${g.title} のソースコード`, path: '/source-list/', content, bodyClass: 'page-source', readCode: true }));
}

// ---------- 活動記録 ----------
{
  const tabs = `<div class="chips tabs">${['all', ...categories.map(c => c.id)].map(id =>
    `<a class="chip chip-cat${id === 'all' ? ' on' : ''}" href="${id === 'all' ? '/activities/' : '/' + catById[id].slug + '/'}">${id === 'all' ? 'すべて' : esc(catById[id].name)}</a>`).join('')}</div>`;
  const content = `<div class="wrap page-pad">
<h1 class="page-title">活動記録</h1>
<p class="page-lead">ゲームジャム・コンテスト・授業・高大連携など、ゲーム制作にまつわる活動の記録です。</p>
${tabs}
<h2 class="vh">活動リスト</h2>
<div class="grid grid-3">${sortYearDesc(activities).map(activityCard).join('')}</div>
</div>`;
  out('activities/index.html', page({ title: '活動記録', path: '/activities/', content }));
}
for (const a of activities) {
  const ag = gamesOfActivity(a.id);
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
${(a.photos || []).length ? `<section class="detail-sec"><h2>活動写真</h2><div class="shot-row">${a.photos.map(u => `<img src="${u}" alt="${esc(a.title)}の活動写真" loading="lazy"${sizeAttr(u)}>`).join('')}</div></section>` : ''}
${(a.relatedDocs || []).length ? `<section class="detail-sec"><h2>関連資料</h2><ul>${a.relatedDocs.map(d => `<li><a href="${esc(d.url)}"${/^https?:/.test(d.url) ? ' target="_blank" rel="noopener"' : ''}>${esc(d.title)}${/^https?:/.test(d.url) ? ' ↗' : ''}</a></li>`).join('')}</ul></section>` : ''}
</div>`;
  out(`activities/${a.id}/index.html`, page({ title: a.title, desc: a.summary, path: '/activities/', content,
    url: `/activities/${a.id}/`,
    jsonLd: crumbLd([['HOME', '/'], ['活動', '/activities/'], [a.title, `/activities/${a.id}/`]]) }));
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
  const content = `<div class="wrap page-pad">
<h1 class="page-title">学ぶ</h1>
<p class="page-lead">ゲームジャムで実際に配布された「逆引きコード」をベースにした学習トピック集です。それぞれのページでサンプルコードを読み、コピーして手元で動かしながら学べます。作品ページの「このゲームで使われている技術」からもたどれます。</p>
<div class="filters"><div class="filters-row">
  <input type="search" id="learn-q" placeholder="トピック名で検索（例: 当たり判定）" aria-label="学習トピックを検索">
  <p class="result-count" id="learn-count" role="status" style="margin:0">${learnTopics.length} トピック</p>
</div></div>
<p class="learn-empty" id="learn-empty" hidden>条件にあうトピックが見つかりませんでした。</p>
${Object.entries(learnByLevel).map(([lv, ts]) => ts.length ? `<h2 class="year-h">${lv}</h2><div class="learn-grid">${ts.map(t =>
    `<a class="learn-card" href="/learn/${t.slug}/" data-topic="${esc(t.title)}"><span class="learn-num">${String(t.num).padStart(2, '0')}</span><span class="learn-title">${esc(t.title)}</span><span class="chip chip-level">${lv}</span></a>`).join('')}</div>` : '').join('')}
</div>`;
  out('learn/index.html', page({ title: '学ぶ', path: '/learn/', content }));
}
for (const t of learnTopics) {
  const ti = learnTopics.indexOf(t);
  const prevT = learnTopics[ti - 1], nextT = learnTopics[ti + 1];
  const code = fs.readFileSync(path.join(GS, 'reverse', t.file), 'utf8');
  const rel = gamesOfTopic(t.slug);
  const content = `<div class="wrap page-pad">
<nav class="crumbs" aria-label="パンくず"><a href="/">HOME</a> › <a href="/learn/">学ぶ</a> › <span>${esc(t.title)}</span></nav>
<p class="chips"><span class="chip chip-level">${t.level}</span></p>
<h1 class="page-title">${esc(t.title)}</h1>
<p class="page-lead">ゲームジャム参加者に配布された逆引きサンプルコードです。コピーして実行し、数値や画像を変えながら動きを確かめてみましょう（実行には Python と pygame-ce が必要です）。</p>
<div class="src-pane">
  <div class="src-toolbar"><span class="src-name">${esc(t.file)}</span><span class="js-only" hidden><button type="button" class="btn btn-sm copy-btn" data-i="0">コピー</button></span></div>
  ${codeBlockHTML(code, 'python')}
</div>
${rel.length ? `<section class="detail-sec"><h2>この技術を使っている作品</h2>${cardGrid(rel.map(gameCard))}</section>` : ''}
<nav class="pager" aria-label="学習トピックの移動">
  ${prevT ? `<a class="pg-prev" href="/learn/${prevT.slug}/"><small>← ${String(prevT.num).padStart(2, '0')} 前のトピック</small><b>${esc(prevT.title)}</b></a>` : ''}
  ${nextT ? `<a class="pg-next" href="/learn/${nextT.slug}/"><small>${String(nextT.num).padStart(2, '0')} 次のトピック →</small><b>${esc(nextT.title)}</b></a>` : ''}
</nav>
</div>
<script>window.__SRC__=${json([code])};</script>`;
  out(`learn/${t.slug}/index.html`, page({ title: t.title, path: '/learn/', content, bodyClass: 'page-source' }));
}

// ---------- About / 404 ----------
{
  const content = `<div class="wrap page-pad prose">
<h1 class="page-title">このサイトについて</h1>
<p>「${esc(site.title)}」は、ゲームジャム・ゲームコンテスト・ゲームプログラミング授業・高大連携・IDERIAの制作活動などで生まれたゲーム作品を記録し、<b>遊んで・コードを読んで・学べる</b>かたちで公開しているアーカイブサイトです。</p>
<h2>できること</h2>
<p>pygame-ceで作られた作品はpygbagでWebAssemblyに変換し、ブラウザからそのまま遊べます。多くの作品はソースコードも公開しており、「学ぶ」ページでは実際のゲームジャムで配布された逆引きサンプルコードで学習できます。</p>
<h2 id="route">サイトの構成</h2>
<p>トップページは <strong>あそぶ → よむ → しくみをしる → つくる → きろく</strong> の順に並べています。目的のページには上のメニューからも移動できます。</p>
<h2 id="record">発見スタンプ・実績について</h2>
<p>開いた作品には「発見済み」のスタンプが付き、<a href="/games/">作品一覧ページ</a>で発見数と実績バッジを確認できます。これらの記録は<b>お使いのブラウザ（localStorage）にのみ保存され、サーバーへ送信されることはありません</b>。ブラウザの設定で保存が使えない場合は、スタンプ表示を行わないだけで、ほかの機能は通常どおり動作します。</p>
<ul class="badge-shelf">${BADGES.map(b =>
  `<li class="badge-item" data-badge="${b.id}" title="${esc(b.desc)}"><i>${b.icon}</i>${esc(b.name)}</li>`).join('')}</ul>
<p class="js-only" data-store-only hidden><button type="button" class="btn btn-sm" id="reset-record">発見記録・実績を消す</button></p>
<h2>掲載している活動</h2>
<p><a href="/game-jams/">ゲームジャム</a>、<a href="/contests/">ゲームコンテスト</a>、<a href="/classes/">ゲームプログラミング授業</a>、<a href="/collabs/">高大連携</a>、<a href="/ideria/">IDERIA制作</a>などの活動を記録しています。作品と活動は相互にリンクしています。</p>
<h2>作品・データについて</h2>
<p>学生作品の制作者名は原則として匿名（学校名・チーム表記）で掲載しています。掲載内容に問題がある場合や、確認できていない情報（「要確認」表記）について情報をお持ちの場合は、${site.repoUrl ? `<a href="${esc(site.repoUrl)}/issues">GitHubのIssues</a>からお知らせください。` : '運営までお知らせください。'}ゲームのWeb版はブラウザで動かすための最小限の変更（フルスクリーン解除・音声形式変換など）のみを行っており、ゲーム内容は変更していません。</p>
<h2>IDERIAについて</h2>
<p>IDERIAは本アーカイブの掲載元のひとつで、ゲーム制作・ワークショップ・高大連携などの活動を行っています。${site.ideriaOfficialUrl ? `詳しくは<a href="${esc(site.ideriaOfficialUrl)}">IDERIA公式サイト</a>をご覧ください。` : 'IDERIA公式サイトは現在準備中です。'}</p>
</div>`;
  out('about/index.html', page({ title: 'About', path: '/about/', content }));
}
out('404.html', page({
  title: 'ページが見つかりません', path: '/404', url: '/404.html',
  content: `<div class="wrap page-pad" style="text-align:center"><h1 class="page-title">404</h1><p class="page-lead">お探しのページが見つかりませんでした。</p><p class="detail-actions" style="justify-content:center"><a class="btn btn-primary" href="/">HOMEへ戻る</a><a class="btn" href="/games/">作品一覧</a></p></div>`,
}));

// ---------- static assets ----------
copyDir(path.join(ROOT, 'public'), DIST);
// GitHub Pages が万一「ブランチから公開」に切り替わってもJekyll処理を通さない保険
fs.writeFileSync(path.join(DIST, '.nojekyll'), '');
fs.mkdirSync(path.join(DIST, 'assets'), { recursive: true });
fs.copyFileSync(path.join(SRC, 'styles.css'), path.join(DIST, 'assets/style.css'));
fs.copyFileSync(path.join(SRC, 'site.js'), path.join(DIST, 'assets/site.js'));

// ---------- sitemap.xml / robots.txt（siteUrl 未設定なら出力しない） ----------
if (ORIGIN) {
  const urls = [...new Set(PAGES)].sort();
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url><loc>${esc(ORIGIN + u)}</loc><lastmod>${BUILD_DATE}</lastmod></url>`).join('\n')}
</urlset>
`;
  fs.writeFileSync(path.join(DIST, 'sitemap.xml'), xml);
  fs.writeFileSync(path.join(DIST, 'robots.txt'),
    `User-agent: *\nAllow: /\nSitemap: ${ORIGIN}/sitemap.xml\n`);
  console.log(`sitemap: ${urls.length} URLs (${ORIGIN})`);
} else {
  console.log('sitemap: skipped (site.json の siteUrl が未設定)');
}

console.log(BASE ? `base: ${BASE}` : 'base: /' );
console.log(`build OK: ${games.length} games / ${playableGames.length} playable / ${sourceGames.length} sources / ${activities.length} activities / ${learnTopics.length} learn topics / years: ${years.join(',')}`);
