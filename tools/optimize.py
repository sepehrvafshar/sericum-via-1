"""Make the images lighter without visible loss (runs after localize.py).
- PNG artwork (pixel characters, maps): reduced to a 64-colour palette (about half the size).
- The caravanserai photo stored as PNG: saved as a JPEG instead (120 KB -> 45 KB).
- JPEG photos and animated GIFs are left as they are.
A file is only replaced when the new version is smaller. Needs Pillow; without it the step is skipped.
Usage: python3 tools/optimize.py site
"""
import io, os, sys

site = sys.argv[1]
try:
    from PIL import Image
except ImportError:
    print('optimize: Pillow not installed, images left unchanged (pip install pillow)')
    sys.exit(0)

assets = os.path.join(site, 'assets')
index = os.path.join(site, 'index.html')
html = open(index, encoding='utf-8').read()
TO_JPEG = {'Ghofrani-M-Sabet-M-M-Sahaf-S-M-K.png'}   # photo, not pixel art

before = after = 0
for name in sorted(os.listdir(assets)):
    path = os.path.join(assets, name)
    if not (os.path.isfile(path) and name.endswith('.png')):
        continue
    orig = os.path.getsize(path)
    im = Image.open(path)
    buf = io.BytesIO()
    if name in TO_JPEG:
        im.convert('RGB').save(buf, 'JPEG', quality=82, optimize=True, progressive=True)
        new_name = name[:-4] + '.jpg'
    else:
        im.convert('RGBA').quantize(colors=64, method=Image.Quantize.FASTOCTREE).save(buf, 'PNG', optimize=True)
        new_name = name
    data = buf.getvalue()
    before += orig
    if len(data) < orig:
        os.remove(path)
        open(os.path.join(assets, new_name), 'wb').write(data)
        if new_name != name:
            html = html.replace('assets/' + name, 'assets/' + new_name)
        after += len(data)
    else:
        after += orig

open(index, 'w', encoding='utf-8').write(html)
print('optimize: PNG images %d KB -> %d KB' % (before // 1024, after // 1024))
