"""Key art for The Sericum Via I, composited only from the game's own artwork.
Run: python3 keyart.py <portfolio-images dir> <sericum-via repo dir> <cover png>
Pixel art is scaled only by whole numbers with nearest-neighbour."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT, REPO, COVER = sys.argv[1:4]
A = os.path.join(REPO, 'source', 'assets')
sys.path.insert(0, os.path.dirname(__file__))
from frame import parchment  # same parchment as the screenshot package

GOLD = (214, 168, 66)


def tinted_parchment(w, h, tint=None):
    p = parchment(w, h)
    if tint:
        p = Image.blend(p, Image.new('RGB', (w, h), tint), 0.35)
    return p


# ---------- pixel map: white -> transparent, routes -> gold, glow ----------
def map_layers():
    m = Image.open(os.path.join(A, 'main-map.png')).convert('RGB')
    a = np.array(m).astype(int)
    h, w, _ = a.shape
    # background = white region connected to the border (flood fill)
    white = (a.min(axis=2) >= 250)
    bg = np.zeros((h, w), bool)
    stack = [(0, x) for x in range(w)] + [(h - 1, x) for x in range(w)] + [(y, 0) for y in range(h)] + [(y, w - 1) for y in range(h)]
    while stack:
        y, x = stack.pop()
        if 0 <= y < h and 0 <= x < w and white[y, x] and not bg[y, x]:
            bg[y, x] = True
            stack += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    grey = (abs(r - g) < 6) & (abs(g - b) < 6) & (r > 80) & (r < 130)          # route fill
    outline = (r < 40) & (g < 40) & (b < 40)                                    # route / marker outlines
    marker = (r > 190) & (g < 70) & (b < 80)                                    # red caravanserai markers
    land = ~bg & ~grey & ~outline & ~marker
    out = a.copy()
    # sit the land on the paper: soften zone colours 22% toward parchment
    paper = np.array([236, 222, 190])
    out[land] = (out[land] * 0.78 + paper * 0.22).astype(int)
    out[grey] = GOLD
    out[outline] = (92, 58, 24)
    rgba = np.dstack([out.clip(0, 255), np.where(bg, 0, 255)]).astype(np.uint8)
    mp = Image.fromarray(rgba, 'RGBA')
    route = Image.fromarray(((grey | outline | marker) * 255).astype(np.uint8), 'L')
    glow = route.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(7))
    glow = glow.point(lambda v: int(v * 0.75))
    return mp, glow


def sprite(scale_num=1, scale_den=1):
    s = Image.open(os.path.join(A, 'man-cammel.png')).convert('RGBA')
    s = s.crop(s.getbbox())
    if scale_num != 1 or scale_den != 1:
        s = s.resize((s.width * scale_num // scale_den, s.height * scale_num // scale_den), Image.NEAREST)
    return s


def map_scene(W, H, name):
    c = tinted_parchment(W, H).convert('RGBA')
    mp, glow = map_layers()
    mx, my = (W - mp.width) // 2, (H - mp.height) // 2
    gold = Image.new('RGBA', mp.size, GOLD + (0,))
    gold.putalpha(glow)
    c.alpha_composite(gold, (mx, my))
    c.alpha_composite(mp, (mx, my))
    sp = sprite()
    # walking across the middle of the country, facing east along the route
    sx = mx + mp.width // 2 - sp.width // 2 + 20
    sy = my + mp.height // 2 - sp.height // 2 + 40
    sh = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sh).ellipse((sx + 10, sy + sp.height - 14, sx + sp.width - 6, sy + sp.height + 10), fill=90)
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    c.paste(Image.new('RGBA', (W, H), (90, 60, 30, 255)), (0, 0), sh)
    c.alpha_composite(sp, (sx, sy))
    for (x0, y0, x1, y1) in [(mx, my, mx + mp.width, my + mp.height), (sx, sy, sx + sp.width, sy + sp.height)]:
        assert x0 >= W * .1 and y0 >= H * .1 and x1 <= W * .9 and y1 <= H * .9, (name, x0, y0, x1, y1)
    c.convert('RGB').save(os.path.join(OUT, name), optimize=True)
    print(name, (W, H), 'map at', (mx, my), 'sprite at', (sx, sy), sp.size)


# ---------- store: cover crop, title and map labels removed ----------
def inpaint(img, mask):
    """Fill masked pixels from mask-aware blurs of the surrounding paper (wider blurs for bigger gaps),
    then add grain with the same strength as the real paper."""
    a = np.array(img).astype(float)
    m = (np.array(mask) > 0).astype(float)
    paper_only = (a.mean(axis=2) > 175).astype(float)   # learn the fill from paper only, never from ink
    known = (1 - m) * paper_only
    est = np.zeros_like(a); done = np.zeros(m.shape, bool)
    for r in (8, 16, 32, 64, 128):
        num = np.array(Image.fromarray((a * known[..., None]).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(float)
        den = np.array(Image.fromarray((known * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(float) / 255
        ok = (den > 0.25) & ~done
        est[ok] = num[ok] / den[ok][:, None]
        done |= ok
    if not done.all():
        est[~done] = np.median(a[(paper_only > 0) & (m == 0)], axis=0)
    # paper grain: measure the fine noise of a plain paper area of the cover, then generate the same
    ref = a[330:430, 960:1020]
    sd = (ref - np.array(Image.fromarray(ref.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(float)).std()
    rng = np.random.default_rng(3)
    noise = rng.normal(0, sd, m.shape)
    noise = np.array(Image.fromarray(((noise + 64).clip(0, 255)).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(float) - 64
    est = est + noise[..., None] * np.array([1.0, 0.95, 0.85])
    soft = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(float)[..., None] / 255
    out = a * (1 - soft) + est * soft
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def store():
    cov = Image.open(COVER).convert('RGB')
    a = np.array(cov).astype(int)
    lum = a.mean(axis=2)
    mask = np.zeros(lum.shape, bool)
    # label and title boxes (cover pixel coordinates), plus the dotted route between them
    # label and title boxes (cover pixel coordinates); all sit on open paper, so the whole box is refilled
    boxes = [(150, 388, 300, 478),   # Tabriz, Ardebil
             (222, 506, 812, 593),   # Iran's Caravanserais
             (340, 594, 455, 628),   # Qazvin
             (488, 612, 625, 650),   # Hamadan
             (448, 704, 570, 748),   # Ispahan
             (640, 462, 840, 512)]   # Iran
    for x0, y0, x1, y1 in boxes:
        mask[y0:y1, x0:x1] = True
    # dotted route: dark specks on open paper between Tabriz and Ispahan (not on buildings)
    route = np.zeros(lum.shape, bool)
    route[380:760, 225:700] = True
    route[600:900, 0:435] = False      # left caravanserai
    route[690:900, 590:1024] = False   # right caravanserai
    route[640:760, 280:470] = False    # faint mountains left of Ispahan
    mask |= route & (lum < 165)
    mimg = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
    clean = inpaint(cov, mimg)
    crop = clean.crop((0, 430, 588, 1024))            # caravanserai + caravan (stops before the second building)
    S = 720
    inner = 560                                         # artwork height inside the square
    art = crop.resize((round(crop.width * inner / crop.height), inner), Image.LANCZOS)
    paper_tint = tuple(int(v) for v in np.array(cov.crop((520, 860, 700, 1010))).reshape(-1, 3).mean(0))
    c = tinted_parchment(S, S, paper_tint)
    fade = Image.new('L', art.size, 0)
    f = 46
    ImageDraw.Draw(fade).rounded_rectangle((f, f, art.width - f, art.height - f), 30, fill=255)
    fade = fade.filter(ImageFilter.GaussianBlur(f * .55))
    x0, y0 = (S - art.width) // 2, (S - art.height) // 2
    c.paste(art, (x0, y0), fade)
    c.save(os.path.join(OUT, 'store-720x720.png'), optimize=True)
    clean.save(os.path.join(os.path.dirname(__file__), 'cover-cleaned-preview.png'))
    print('store-720x720.png', (S, S), 'art', art.size, 'at', (x0, y0))


def icon():
    S = 192
    c = tinted_parchment(S, S).convert('RGBA')
    sp = sprite(1, 2)                                   # exactly half size, nearest-neighbour
    x0, y0 = (S - sp.width) // 2, (S - sp.height) // 2
    assert x0 >= S * .1 and y0 >= S * .1, (x0, y0, sp.size)
    c.alpha_composite(sp, (x0, y0))
    c.convert('RGB').save(os.path.join(OUT, 'icon-192x192.png'), optimize=True)
    print('icon-192x192.png', (S, S), 'sprite', sp.size, 'at', (x0, y0))


map_scene(1200, 750, 'card-1200x750.png')
map_scene(1200, 630, 'og-1200x630.png')
store()
icon()
