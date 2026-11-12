"""Search-engine step: canonical + Open Graph tags, robots.txt, sitemap.xml, _headers, share image.
Nothing visible on the page changes.
Usage: python3 -I tools/seo.py site <canonical-url> "<og:title>" <share-image.png>
The sitemap date is the date of the last commit that changed the game's inputs (source/, tools/, build.sh),
or today if those inputs have uncommitted changes.
"""
import sys, os, re, html, shutil, subprocess, datetime

site, url, og_title, image = sys.argv[1:5]
url = url.rstrip('/') + '/'
path = os.path.join(site, 'index.html')
src = open(path, encoding='utf-8').read()

# date the page last changed, from git
inputs = ['source', 'tools', 'build.sh']
dirty = subprocess.run(['git', 'status', '--porcelain', '--'] + inputs, capture_output=True, text=True).stdout.strip()
lastmod = datetime.date.today().isoformat() if dirty else \
    subprocess.run(['git', 'log', '-1', '--format=%cs', '--'] + inputs, capture_output=True, text=True).stdout.strip()
assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', lastmod), lastmod

# head tags (only the missing ones; the existing <title> and description stay)
m = re.search(r'<meta name="description" content="([^"]*)">', src)
assert m, 'description meta missing'
desc = m.group(1)
assert 'rel="canonical"' not in src and 'property="og:' not in src
assert not re.search(r'<meta[^>]+name="robots"[^>]+noindex', src, re.I), 'noindex found'
shutil.copy(image, os.path.join(site, 'og-image.png'))
tags = ('\n<link rel="canonical" href="%s">'
        '\n<meta property="og:type" content="website">'
        '\n<meta property="og:title" content="%s">'
        '\n<meta property="og:description" content="%s">'
        '\n<meta property="og:url" content="%s">'
        '\n<meta property="og:image" content="%sog-image.png">'
        '\n<meta property="og:image:width" content="1200">'
        '\n<meta property="og:image:height" content="630">') % (
    url, html.escape(og_title, quote=True), desc, url, url)
src = src[:m.end()] + tags + src[m.end():]
open(path, 'w', encoding='utf-8').write(src)

open(os.path.join(site, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % url)
open(os.path.join(site, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n  </url>\n'
    '</urlset>\n' % (url, lastmod))
# Cloudflare Pages: real files already win over the "unknown path -> index.html" fallback; pin their types
open(os.path.join(site, '_headers'), 'w').write(
    '/robots.txt\n  Content-Type: text/plain; charset=utf-8\n'
    '/sitemap.xml\n  Content-Type: application/xml; charset=utf-8\n')
print('seo: canonical %s, sitemap lastmod %s' % (url, lastmod))
