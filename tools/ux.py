"""Step 3b: user-experience improvements that keep the original look.
- viewport meta + mobile layout (the passage box used to overflow off-screen on phones)
- self-hosted Press Start 2P font (no Google Fonts dependency; works offline)
- favicon + description
- keyboard: number keys 1-9 pick the Nth choice, Tab/Enter work on links
- new passage always starts scrolled to the top
Usage: python3 -I ux.py index.html fontdir icon.png
"""
import sys, shutil, os

path, fontdir, icon = sys.argv[1:4]
site = os.path.dirname(path)
src = open(path, encoding='utf-8').read()

os.makedirs(site + '/assets/fonts', exist_ok=True)
for f in ('PressStart2P-latin.woff2', 'PressStart2P-latin-ext.woff2'):
    shutil.copy(os.path.join(fontdir, f), site + '/assets/fonts/' + f)
shutil.copy(icon, site + '/assets/icon.png')

def once(s, old, new):
    assert s.count(old) == 1, (old[:60], s.count(old))
    return s.replace(old, new)

HEAD = ('<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="description" content="The Sericum Via: a serious game about the Safavid caravanserais of Iran on the Silk Road (ASCAAD 2021).">\n'
        '<link rel="icon" type="image/png" href="assets/icon.png">\n')
src = src.replace('<meta charset="utf-8">\n', HEAD, 1)

FONT = ('@font-face { font-family: "Press Start 2P"; font-style: normal; font-weight: 400; font-display: swap;\n'
        '  src: url(assets/fonts/PressStart2P-latin-ext.woff2) format("woff2");\n'
        '  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF; }\n'
        '@font-face { font-family: "Press Start 2P"; font-style: normal; font-weight: 400; font-display: swap;\n'
        '  src: url(assets/fonts/PressStart2P-latin.woff2) format("woff2");\n'
        '  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }')
src = once(src, '@import url(https://fonts.googleapis.com/css?family=Press+Start+2P);', FONT)

EXTRA_CSS = '''
/* ---- preservation edition: usability additions ---- */
tw-story { line-height: 1.6em; background: #fff; background-image: none; }
html, body { background: #fff; }
/* compact layout so a page fits on one screen */
tw-story { padding: 3vh 12%; font-size: 15px; }
tw-passage { overflow-wrap: break-word; padding: 18px 26px; }
/* centred pictures; the script below sizes them to the free space on screen */
tw-passage img { display: block; margin: 6px auto; width: auto; height: auto; max-width: 100%; max-height: 32vh; image-rendering: pixelated;
  opacity: 0; transition: opacity .4s ease-out; }
tw-passage img.sv-ready { opacity: 1; }
/* each new page fades in softly instead of appearing all at once */
@keyframes sv-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
tw-passage { animation: sv-in .45s ease-out both; }
@media (prefers-reduced-motion: reduce) { tw-passage { animation: none; } tw-passage img { transition: none; } }
tw-passage img[alt="1"], tw-passage img[alt="2"], tw-passage img[alt="E"], tw-passage img[alt^="Screen-Shot"],
tw-passage img[alt^="Ghofrani"], tw-passage img[alt="vuuranimatie2"], tw-passage img:not([alt]) { image-rendering: auto; }
tw-passage img + br, tw-passage br:has(+ img) { display: none; }
tw-passage a { color: darkblue; transition: color .5s ease-in-out; }
tw-passage a:hover { color: orange; }
tw-link, .enchantment-link { cursor: pointer; }
tw-link:focus-visible { outline: 2px dashed orange; outline-offset: 3px; }
/* Home + Back toolbar, pulled up close to the top edge of the box */
.sv-bar { display: flex; gap: 8px; align-items: center; margin: -10px 0 8px -8px; min-height: 0; }
.sv-bar:not(:has(tw-link, .sv-back)) { display: none; }
.sv-bar + br { display: none; }
.sv-back, .sv-bar tw-link { display: inline-block; margin: 0; padding: 5px 11px 4px; font: inherit; font-size: 0.7em; line-height: 1.4;
  color: darkblue; background: rgba(255,255,255,0.8); border: 3px groove gray; border-radius: 14px; cursor: pointer;
  text-shadow: none; transition: color .3s ease-in-out, border-color .3s ease-in-out; }
.sv-back:hover, .sv-back:focus-visible, .sv-bar tw-link:hover, .sv-bar tw-link:focus-visible { color: orange; border-color: orange; outline: none; }
/* About page: small text in separate cards */
.sv-about { font-size: 0.72em; line-height: 1.75; text-shadow: none; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 4px; }
.sv-about > .sv-card:first-child, .sv-about > .sv-card:last-child { grid-column: 1 / -1; }
.sv-card { background: rgba(255,255,255,0.75); border: 2px groove gray; border-radius: 14px; padding: 8px 14px; margin: 0; }
.sv-h { color: darkgreen; text-shadow: 1px 1px lightgreen; font-size: 1.15em; margin-bottom: 6px; }
.sv-dim { color: gray; margin-top: 6px; }
.sv-award { color: #b8860b; margin-top: 6px; }
.sv-ext { display: inline-block; margin-top: 4px; }
.sv-row { margin: 4px 0; }
.sv-k { display: block; color: gray; font-size: 0.85em; }
@media (max-width: 900px) { .sv-about { grid-template-columns: 1fr; } }
@media (max-width: 700px) {
  tw-story { padding: 12px 10px; font-size: 12px; }
  tw-passage { padding: 14px; border-width: 3px; border-radius: 16px; }
  tw-passage img { max-height: 28vh; }
}
</style>'''
i = src.index('<style role="stylesheet"')
j = src.index('</style>', i)
src = src[:j] + EXTRA_CSS + src[j + len('</style>'):]

SCRIPT = r'''<script role="script" id="twine-user-script" type="text/twine-javascript">
/* Preservation edition: keyboard shortcuts + scroll to top on each new passage */
(function () {
  /* story choices only (the Home button in the toolbar is not a numbered choice) */
  function links() { return Array.prototype.slice.call(document.querySelectorAll('tw-passage tw-link')).filter(function (l) { return !l.closest('.sv-bar'); }); }
  function undoIcon() { return document.querySelector('tw-passage tw-icon.undo'); }
  function canGoBack() { var u = undoIcon(); return !!u && u.style.visibility !== 'hidden'; }
  function goBack() { if (canGoBack()) undoIcon().click(); }
  function addBack() {
    var p = document.querySelector('tw-passage');
    if (!p || p.querySelector('.sv-back') || !canGoBack()) return;
    var home = p.querySelector('.sv-bar');
    if (home && !home.querySelector('tw-link')) return;  /* home page: the header has no Home link, and no Back either */
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'sv-back'; b.title = 'Back (Esc)';
    b.textContent = '◀ Back';
    b.addEventListener('click', goBack);
    var bar = p.querySelector('.sv-bar');
    if (!bar) {
      bar = document.createElement('div'); bar.className = 'sv-bar';
      var side = p.querySelector('tw-sidebar');
      p.insertBefore(bar, side ? side.nextSibling : p.firstChild);
    }
    bar.appendChild(b);  /* Back goes to the right of Home */
  }
  /* Grow pictures into the empty space below the passage (pixel art up to 3x, photos up to 1.6x, at most 55% of the screen),
     without making the page scroll; never shrink below a readable size. */
  function fitImages() {
    var p = document.querySelector('tw-passage'); if (!p) return;
    var imgs = Array.prototype.slice.call(p.querySelectorAll('img')); if (!imgs.length) return;
    if (imgs.some(function (i) { return !i.complete || !i.naturalWidth; })) return;
    imgs.forEach(function (i) { i.style.maxHeight = 'none'; i.style.width = 'auto'; i.style.height = '40px'; });
    var ps = getComputedStyle(p), story = document.querySelector('tw-story');
    var padB = story ? parseFloat(getComputedStyle(story).paddingBottom) || 0 : 0;
    var rest = p.getBoundingClientRect().bottom + window.scrollY + padB - 40 * imgs.length;
    var share = (window.innerHeight - rest - 10) / imgs.length;
    var cw = p.clientWidth - parseFloat(ps.paddingLeft) - parseFloat(ps.paddingRight);
    imgs.forEach(function (i) {
      var nw = i.naturalWidth, nh = i.naturalHeight, byWidth = cw * nh / nw;
      var grow = getComputedStyle(i).imageRendering === 'auto' ? 1.6 : 3;  /* photos blur sooner than pixel art */
      var maxH = Math.min(byWidth, window.innerHeight * 0.55, nh * grow);
      var minH = Math.min(nh, byWidth, 160);
      i.style.height = Math.round(Math.max(minH, Math.min(share, maxH))) + 'px';
      i.classList.add('sv-ready');  /* fade in only once sized, so nothing jumps */
    });
  }
  function showAnyway() { Array.prototype.forEach.call(document.querySelectorAll('tw-passage img'), function (i) { i.classList.add('sv-ready'); }); }
  /* Preload every picture of the game in the background, so later pages open without waiting. */
  function preloadAll() {
    var sd = document.querySelector('tw-storydata'); if (!sd) return;
    var seen = {}, rx = /src=(?:"|&quot;)(assets\/[^"&]+)/g, m;
    while ((m = rx.exec(sd.innerHTML))) { if (!seen[m[1]]) { seen[m[1]] = 1; new Image().src = m[1]; } }
  }
  setTimeout(preloadAll, 800);
  var fitTimer;
  function scheduleFit() { clearTimeout(fitTimer); fitTimer = setTimeout(fitImages, 30); }
  window.addEventListener('resize', scheduleFit);
  function prep() {
    addBack();
    links().forEach(function (l) { if (!l.hasAttribute('tabindex')) l.setAttribute('tabindex', '0'); });
    Array.prototype.forEach.call(document.querySelectorAll('tw-passage img'), function (i) {
      if (!i.svFit) { i.svFit = true; i.addEventListener('load', scheduleFit); i.addEventListener('error', showAnyway); }
    });
    scheduleFit();
    clearTimeout(prep.safety); prep.safety = setTimeout(showAnyway, 2500);  /* never leave a picture hidden */
  }
  new MutationObserver(function (muts) {
    prep();
    muts.forEach(function (m) {
      Array.prototype.forEach.call(m.addedNodes, function (n) { if (n.tagName === 'TW-PASSAGE') window.scrollTo(0, 0); });
    });
  }).observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var t = e.target;
    if (t && t.tagName === 'TW-LINK' && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); t.click(); return; }
    if (e.key === 'Escape' || e.key === 'Backspace') { e.preventDefault(); goBack(); return; }
    if (/^[1-9]$/.test(e.key)) { var l = links()[+e.key - 1]; if (l) { e.preventDefault(); l.click(); } }
  });
  prep();
})();
</script>'''
src = once(src, '<script role="script" id="twine-user-script" type="text/twine-javascript"></script>', SCRIPT)

open(path, 'w', encoding='utf-8').write(src)
print('ux applied')
