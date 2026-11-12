"""Step 1: make the original 2020 game self-contained.
Replaces the external image links (ImgBB, olgoirani.com) with local files in assets/,
removes a stray ImgBB link wrapper, and replaces the lost third-party background image.
Usage: python3 -I tools/localize.py source/original/<game>.html source/assets site
"""
import re, os, shutil, sys

src_html, asset_dir, out = sys.argv[1:4]
src = open(src_html, encoding='utf-8').read()
os.makedirs(out + '/assets', exist_ok=True)

urls = sorted(set(re.findall(r'https?://(?:i\.ibb\.co|files\.olgoirani\.com)/[^"&\s]+', src)))
for u in urls:
    name = u.rsplit('/', 1)[1]
    shutil.copy(os.path.join(asset_dir, name), out + '/assets/' + name)
    src = src.replace(u, 'assets/' + name)

# clicking Rajab's picture used to leave the game (link to imgbb.com); stray </a> after the camel
src = src.replace('&lt;a href=&quot;https://imgbb.com/&quot;&gt;', '')
src = src.replace('border=&quot;0&quot;&gt;&lt;/a&gt;', 'border=&quot;0&quot;&gt;')
# original background (third-party mars.jpg) no longer exists online; ux.py sets a white background
src = src.replace('background-image: url("http://www.ohiofi.com/img/mars.jpg");', 'background-image: none;')

for k in ('ohiofi', 'ibb.co/', 'imgbb.com', 'olgoirani'):
    assert k not in src, k
open(out + '/index.html', 'w', encoding='utf-8').write(src)
print('localized %d images' % len(urls))
