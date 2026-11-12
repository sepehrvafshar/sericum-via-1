"""Frames the real screenshots on a parchment background (no added text). Run: python3 frame.py <portfolio-images dir>"""
import sys, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

D = sys.argv[1]
SRC = os.path.join(D, 'source-screenshots')
random.seed(7)


def parchment(w, h):
    base = Image.new('RGB', (w, h), (236, 222, 190))
    # grain
    noise = Image.effect_noise((w, h), 22).convert('L')
    grain = Image.merge('RGB', [noise.point(lambda v: 236 + (v - 128) * 0.10)] * 1 +
                        [noise.point(lambda v: 222 + (v - 128) * 0.10), noise.point(lambda v: 190 + (v - 128) * 0.10)])
    base = Image.blend(base, grain, 0.6)
    # soft sepia stains
    stains = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(stains)
    for _ in range(9):
        r = random.randint(int(min(w, h) * .12), int(min(w, h) * .35))
        x, y = random.randint(-r // 2, w), random.randint(-r // 2, h)
        d.ellipse((x - r, y - r, x + r, y + r), fill=random.randint(18, 40))
    stains = stains.filter(ImageFilter.GaussianBlur(min(w, h) * .08))
    sepia = Image.new('RGB', (w, h), (150, 105, 60))
    base = Image.composite(sepia, base, stains)
    # faint fibres
    fib = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(fib)
    for _ in range(int(w * h / 9000)):
        x, y = random.randint(0, w), random.randint(0, h)
        dx, dy = random.randint(-30, 30), random.randint(-6, 6)
        d.line((x, y, x + dx, y + dy), fill=random.randint(10, 26), width=1)
    base = Image.composite(Image.new('RGB', (w, h), (120, 85, 50)), base, fib)
    # vignette
    vig = Image.new('L', (w, h), 0)
    ImageDraw.Draw(vig).ellipse((-w * .15, -h * .2, w * 1.15, h * 1.2), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(min(w, h) * .12))
    dark = Image.new('RGB', (w, h), (120, 82, 45))
    base = Image.composite(base, Image.blend(base, dark, .45), vig)
    return base


def shadow(canvas, box, radius, blur, offset=(0, 12), alpha=110):
    w, h = canvas.size
    m = Image.new('L', (w, h), 0)
    x0, y0, x1, y1 = box
    ImageDraw.Draw(m).rounded_rectangle((x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]), radius, fill=alpha)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    canvas.paste(Image.new('RGB', (w, h), (70, 45, 20)), (0, 0), m)


def rounded_paste(canvas, img, xy, radius):
    m = Image.new('L', img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius, fill=255)
    canvas.paste(img, xy, m)


def browser(shot, out, W, H, win_w):
    shot = Image.open(os.path.join(SRC, shot)).convert('RGB')
    bar = round(win_w * 0.03)
    cw, ch = win_w, round(win_w * shot.height / shot.width)
    wh = ch + bar
    x0, y0 = (W - cw) // 2, (H - wh) // 2
    assert x0 >= W * .1 - 1 and y0 >= H * .1 - 1, (x0, y0)
    c = parchment(W, H)
    rad = round(win_w * .012)
    shadow(c, (x0, y0, x0 + cw, y0 + wh), rad, round(win_w * .025))
    win = Image.new('RGB', (cw, wh), (250, 247, 240))
    d = ImageDraw.Draw(win)
    d.rectangle((0, 0, cw, bar), fill=(234, 226, 210))
    d.line((0, bar - 1, cw, bar - 1), fill=(205, 192, 168), width=1)
    r = bar * .17
    for k, col in enumerate([(224, 108, 90), (226, 180, 80), (120, 180, 110)]):
        cx, cy = bar * .55 + k * bar * .5, bar / 2
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
    pill_w = cw * .42
    d.rounded_rectangle(((cw - pill_w) / 2, bar * .22, (cw + pill_w) / 2, bar * .78), bar * .28, fill=(248, 244, 236))
    win.paste(shot.resize((cw, ch), Image.LANCZOS), (0, bar))
    rounded_paste(c, win, (x0, y0), rad)
    ImageDraw.Draw(c).rounded_rectangle((x0, y0, x0 + cw - 1, y0 + wh - 1), rad, outline=(150, 115, 75), width=2)
    c.save(os.path.join(D, out), optimize=True)
    print(out, c.size)


def phone(shot, out, W=1080, H=1920):
    shot = Image.open(os.path.join(SRC, shot)).convert('RGB')
    sh = 1440
    sw = round(sh * shot.width / shot.height)
    bz = 22
    bw, bh = sw + 2 * bz, sh + 2 * bz
    x0, y0 = (W - bw) // 2, (H - bh) // 2
    c = parchment(W, H)
    shadow(c, (x0, y0, x0 + bw, y0 + bh), 86, 40, (0, 18), 130)
    body = Image.new('RGB', (bw, bh), (27, 31, 42))
    rounded_paste(c, body, (x0, y0), 86)
    ImageDraw.Draw(c).rounded_rectangle((x0, y0, x0 + bw - 1, y0 + bh - 1), 86, outline=(70, 76, 92), width=3)
    rounded_paste(c, shot.resize((sw, sh), Image.LANCZOS), (x0 + bz, y0 + bz), 64)
    c.save(os.path.join(D, out), optimize=True)
    print(out, c.size, 'phone', (bw, bh), 'margins', x0, y0)


browser('desktop-01-climatic-zone-map.png', 'cover-1600x1000.png', 1600, 1000, 1220)
browser('desktop-02-season-choice.png', 'gallery-season-1200x750.png', 1200, 750, 915)
browser('desktop-04-map-yellow-point.png', 'gallery-journey-1200x750.png', 1200, 750, 915)
browser('desktop-05-ending-score.png', 'gallery-ending-1200x750.png', 1200, 750, 915)
phone('phone-01-season-choice.png', 'phone-1080x1920.png')
