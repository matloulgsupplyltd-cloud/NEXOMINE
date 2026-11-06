"""Procedural scene renderer: produces photographic-style JPEG renders for each photo slot."""
import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFilter

def fbm(w, h, seed, octaves=5, base=4):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w)); amp = 1.0; tot = 0
    for o in range(octaves):
        n = base * 2 ** o
        a = rng.random((n + 1, max(2, int(n * h / w)) + 1))
        im = Image.fromarray((a * 255).astype("uint8")).resize((w, h), Image.BICUBIC)
        out += np.asarray(im, dtype=float) / 255 * amp; tot += amp; amp *= .5
    return out / tot

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def sky(w, h, hor, top, bot, seed, clouds=.35):
    y = np.linspace(0, 1, h)[:, None, None]
    t = np.clip(y / max(hor / h, .01), 0, 1)
    top, bot = np.array(top), np.array(bot)
    img = top * (1 - t) + bot * t
    img = np.broadcast_to(img, (h, w, 3)).copy()
    c = fbm(w, h, seed, 5, 3)
    c = np.clip((c - .5) / .25, 0, 1) * clouds * (1 - np.clip(y[:, :, 0] / (hor / h), 0, 1) * .6)
    img = img * (1 - c[..., None]) + np.array([255, 250, 245]) * c[..., None]
    return img

def ridge(w, h, base, amp, seed, rough=6):
    rng = np.random.default_rng(seed)
    xs = np.arange(w)
    prof = np.zeros(w)
    for o in range(1, 6):
        k = rough * 2 ** o
        pts = rng.random(k + 2)
        prof += np.interp(xs, np.linspace(0, w, k + 2), pts) * (.5 ** o)
    prof = (prof - prof.min()) / (prof.max() - prof.min())
    return base - prof * amp

def fill_ridge(img, prof, color, tex_seed, light=0.0, texamp=14):
    h, w, _ = img.shape
    yy = np.arange(h)[:, None]
    mask = yy >= prof[None, :]
    tex = (fbm(w, h, tex_seed, 5, 8) - .5) * texamp
    col = np.array(color)[None, None, :] + tex[..., None]
    img[mask] = col[mask]
    return img

def haze(img, color, strength):
    return img * (1 - strength) + np.array(color) * strength

def finish(img, seed, grain=7, vig=.28, warm=(1.0, 1.0, 1.0)):
    h, w, _ = img.shape
    rng = np.random.default_rng(seed)
    img = img * np.array(warm)
    img += rng.normal(0, grain, (h, w, 1))
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - vig * np.clip(d - .5, 0, 1) ** 1.5)[..., None]
    img = (img - 128) * 1.06 + 128
    return Image.fromarray(np.clip(img, 0, 255).astype("uint8"))

def poly_layer(w, h, drawfn, blur=0):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    drawfn(ImageDraw.Draw(im))
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    return im

def paste(base, layer):
    b = Image.fromarray(np.clip(base, 0, 255).astype("uint8")).convert("RGBA")
    b.alpha_composite(layer)
    return np.asarray(b.convert("RGB"), dtype=float)

# ----------------------------------------------------------------- scenes
def scene_pit(w, h, seed):
    rng = random.Random(seed); nrng = np.random.default_rng(seed)
    hor = int(h * .36)
    img = sky(w, h, hor, (58, 112, 176), (226, 214, 196), seed)
    img = fill_ridge(img, ridge(w, h, hor + 20, 55, seed + 1), (150, 132, 120), seed + 2)
    img = haze(img, (226, 214, 196), .35)
    img = fill_ridge(img, ridge(w, h, hor + 40, 30, seed + 3), (168, 120, 88), seed + 4)
    # plain / ground
    gy = hor + 46
    ground = np.array((176, 124, 90)); tex = (fbm(w, h, seed + 5, 6, 10) - .5) * 26
    img[gy:] = ground + tex[gy:, :, None]
    # pit: concentric jittered benches, drawn outer to inner
    cx, cy = w * (.5 + rng.uniform(-.05, .05)), h * .70
    n = 11
    jit = [np.interp(np.linspace(0, 1, 361), np.linspace(0, 1, 24), nrng.random(24)) for _ in range(n)]
    rings = []
    def draw(d):
        for i in range(n):
            rx = w * .56 * (1 - i / (n + 1) * 1.02); ry = rx * .27
            oy = i * h * .017
            pts_o, pts_i = [], []
            for a in range(361):
                t = math.radians(a)
                j = 1 + (jit[i][a] - .5) * .08
                pts_o.append((cx + math.cos(t) * rx * j, cy + math.sin(t) * ry * j + oy))
            rx2 = rx * .955; ry2 = ry * .955
            for a in range(361):
                t = math.radians(a)
                j = 1 + (jit[i][a] - .5) * .08
                pts_i.append((cx + math.cos(t) * rx2 * j, cy + math.sin(t) * ry2 * j + oy + h * .016))
            wall = lerp((120, 78, 56), (84, 54, 42), i / n)
            d.polygon(pts_o, fill=wall + (255,))
            top = lerp((196, 146, 108), (150, 108, 84), i / n)
            d.polygon(pts_i, fill=top + (255,))
        # pit floor water
        rx = w * .56 * (1 - n / (n + 1) * 1.02)
        d.ellipse((cx - rx * .8, cy + n * h * .017 - rx * .2, cx + rx * .8, cy + n * h * .017 + rx * .2), fill=(88, 120, 150, 255))
    img = paste(img, poly_layer(w, h, draw))
    # haul road spiral + trucks
    road = poly_layer(w, h, lambda d: d.line([(cx + math.cos(t / 20) * w * .5 * (1 - t / 900) * 1.0, cy + math.sin(t / 20) * w * .12 * (1 - t / 900) + t * .05) for t in range(0, 700, 2)], fill=(220, 190, 160, 140), width=max(3, w // 260)))
    img = paste(img, road)
    def trucks(d):
        for k in range(4):
            t = rng.randint(80, 600)
            x = cx + math.cos(t / 20) * w * .5 * (1 - t / 900); y = cy + math.sin(t / 20) * w * .12 * (1 - t / 900) + t * .05
            s = w / 120 * (.6 + y / h * .5)
            d.rectangle((x - s, y - s * .9, x + s, y), fill=(238, 190, 40, 255))
            d.rectangle((x - s * .2, y - s * 1.3, x + s * .5, y - s * .9), fill=(230, 230, 230, 255))
            d.ellipse((x - s * .9, y - s * .4, x - s * .3, y + s * .2), fill=(30, 30, 30, 255))
            d.ellipse((x + s * .3, y - s * .4, x + s * .9, y + s * .2), fill=(30, 30, 30, 255))
    img = paste(img, poly_layer(w, h, trucks))
    # dust plumes
    dust = fbm(w, h, seed + 9, 5, 5)
    mask = np.exp(-(((np.arange(w)[None, :] - cx * 1.1) / (w * .25)) ** 2 + ((np.arange(h)[:, None] - h * .6) / (h * .13)) ** 2))
    img = haze(img, (232, 214, 190), (np.clip(dust - .35, 0, 1) * mask * .8)[..., None])
    # foreground berm
    fg = ridge(w, h, h * .94, 30, seed + 11)
    img = fill_ridge(img, fg, (86, 58, 44), seed + 12, texamp=22)
    return finish(img, seed, warm=(1.02, 1.0, .96))

def scene_hills(w, h, seed, tint=(1, 1, 1)):
    hor = int(h * .38)
    img = sky(w, h, hor, (70, 124, 186), (232, 222, 206), seed)
    cols = [(150, 160, 170), (128, 142, 150), (118, 124, 108), (104, 108, 82), (88, 86, 62), (66, 62, 46)]
    for i, c in enumerate(cols):
        img = fill_ridge(img, ridge(w, h, hor + i * h * .08 + 10, 70 - i * 6, seed + i * 7), c, seed + i * 3, texamp=10 + i * 3)
        if i < 3: img = haze(img, (232, 222, 206), .32 - i * .08)
    return finish(img, seed, warm=tint)

def scene_green(w, h, seed):
    rng = random.Random(seed)
    hor = int(h * .34)
    img = sky(w, h, hor, (74, 128, 190), (230, 226, 210), seed, .45)
    greens = [(126, 150, 124), (110, 140, 98), (112, 138, 70), (122, 140, 58), (140, 146, 66)]
    for i, c in enumerate(greens):
        img = fill_ridge(img, ridge(w, h, hor + 20 + i * h * .12, 60, seed + i * 5), c, seed + i, texamp=18)
        if i < 2: img = haze(img, (230, 226, 210), .3)
    def trees(d):
        for _ in range(120):
            x = rng.randint(0, w); y = rng.randint(int(h * .55), h)
            s = (y / h) * w / 70
            d.ellipse((x - s, y - s * 1.4, x + s, y), fill=(46 + rng.randint(0, 22), 78 + rng.randint(0, 24), 40, 255))
    img = paste(img, poly_layer(w, h, trees, 1))
    return finish(img, seed, warm=(1.0, 1.02, .98))

def scene_plant(w, h, seed):
    rng = random.Random(seed)
    hor = int(h * .48)
    img = sky(w, h, hor, (46, 82, 140), (242, 190, 140), seed, .3)
    img = fill_ridge(img, ridge(w, h, hor + 5, 60, seed + 2), (96, 98, 118), seed + 3)
    img = haze(img, (242, 190, 140), .3)
    img = fill_ridge(img, ridge(w, h, h * .72, 20, seed + 4), (86, 74, 66), seed + 5, texamp=20)
    def s(d):
        base = int(h * .74)
        for x, wd, hh in [(.12, .09, .26), (.24, .07, .18), (.58, .10, .32), (.72, .08, .22)]:
            X = int(w * x); W = int(w * wd); H = int(h * hh)
            d.rectangle((X, base - H, X + W, base + 60), fill=(150, 160, 170, 255))
            d.rectangle((X + W * .55, base - H, X + W, base + 60), fill=(100, 110, 124, 255))
            d.rectangle((X, base - H - 10, X + W, base - H), fill=(70, 78, 90, 255))
        for x in (.42, .46, .88):
            X = int(w * x); d.rectangle((X, base - int(h * .4), X + w // 60, base + 40), fill=(92, 98, 110, 255))
        d.line([(w * .22, base - h * .18), (w * .6, base - h * .34)], fill=(60, 66, 78, 255), width=max(6, w // 150))
        d.line([(w * .22, base - h * .18 - 8), (w * .6, base - h * .34 - 8)], fill=(120, 130, 144, 255), width=3)
        for k in range(30):
            X = rng.randint(int(w * .1), int(w * .9)); Y = rng.randint(base - int(h * .3), base)
            d.ellipse((X - 3, Y - 3, X + 3, Y + 3), fill=(255, 220, 140, 255))
        for cx_, r in [(.2, .12), (.7, .14)]:
            d.polygon([(w * cx_ - w * r, h * .88), (w * cx_, h * .8), (w * cx_ + w * r, h * .88)], fill=(120, 94, 76, 255))
    img = paste(img, poly_layer(w, h, s))
    glow = np.exp(-(((np.arange(w)[None, :] - w * .55) / (w * .3)) ** 2 + ((np.arange(h)[:, None] - h * .55) / (h * .2)) ** 2))
    img = haze(img, (255, 200, 130), (glow * .18)[..., None])
    img = fill_ridge(img, ridge(w, h, h * .92, 20, seed + 8), (50, 44, 40), seed + 9)
    return finish(img, seed, warm=(1.03, 1.0, .96))

def scene_underground(w, h, seed):
    rng = random.Random(seed)
    img = np.zeros((h, w, 3)) + (24, 24, 28)
    cx, cy = w * .5, h * .5
    def d_(d):
        for i in range(26, 0, -1):
            t = i / 26
            rw, rh = w * .6 * t ** 1.4 + 20, h * .55 * t ** 1.4 + 14
            v = int(28 + (1 - t) * 190)
            d.rounded_rectangle((cx - rw, cy - rh * .9, cx + rw, cy + rh * .8), radius=int(rh * .5), fill=(int(v * .9), int(v * .82), int(v * .7), 255))
            # support rings
            if i % 3 == 0:
                d.rounded_rectangle((cx - rw, cy - rh * .9, cx + rw, cy + rh * .8), radius=int(rh * .5), outline=(150, 150, 150, 220), width=max(2, int(6 * t)))
        d.ellipse((cx - 36, cy - 28, cx + 36, cy + 28), fill=(255, 244, 214, 255))
    img = paste(img, poly_layer(w, h, d_))
    rock = fbm(w, h, seed, 6, 12)
    img = img * (.72 + rock[..., None] * .5)
    glow = np.exp(-(((np.arange(w)[None, :] - cx) / (w * .22)) ** 2 + ((np.arange(h)[:, None] - cy) / (h * .26)) ** 2))
    img = haze(img, (255, 236, 190), (glow * .55)[..., None])
    def veh(d):
        d.rounded_rectangle((w * .40, h * .62, w * .48, h * .68), radius=6, fill=(236, 186, 36, 255))
        d.ellipse((w * .405, h * .665, w * .42, h * .695), fill=(20, 20, 20, 255)); d.ellipse((w * .455, h * .665, w * .47, h * .695), fill=(20, 20, 20, 255))
        d.ellipse((w * .478, h * .635, w * .488, h * .65), fill=(255, 250, 230, 255))
    img = paste(img, poly_layer(w, h, veh))
    return finish(img, seed, grain=9, vig=.45, warm=(1.0, .98, .94))

def scene_solar(w, h, seed):
    hor = int(h * .40)
    img = sky(w, h, hor, (50, 108, 180), (222, 226, 224), seed, .4)
    img = fill_ridge(img, ridge(w, h, hor + 6, 50, seed + 1), (118, 128, 138), seed + 2)
    img = haze(img, (222, 226, 224), .35)
    gy = hor + 10
    img[gy:] = np.array((156, 126, 92)) + ((fbm(w, h, seed + 3, 6, 10) - .5) * 24)[gy:, :, None]
    def panels(d):
        rows = 9
        for r in range(rows):
            t = (r + 1) / rows
            y = hor + 20 + (h - hor - 40) * t ** 1.9
            ph = 6 + 70 * t ** 1.9; pw_ = 40 + 190 * t ** 1.9
            x = -pw_
            while x < w + pw_:
                d.polygon([(x, y), (x + pw_ * .94, y), (x + pw_ * .94 - ph * .12, y + ph), (x - ph * .12, y + ph)], fill=(26, 52, 98, 255), outline=(170, 190, 215, 255))
                x += pw_
    img = paste(img, poly_layer(w, h, panels))
    refl = fbm(w, h, seed + 7, 4, 3)
    msk = (np.arange(h)[:, None] > hor + 20) * np.ones((1, w))
    img = img + (refl[..., None] * 40) * msk[..., None] * np.array([.6, .7, 1])
    return finish(img, seed, warm=(1.0, 1.0, 1.02))

def scene_water(w, h, seed):
    hor = int(h * .46)
    img = sky(w, h, hor, (64, 116, 182), (230, 224, 208), seed, .4)
    img = fill_ridge(img, ridge(w, h, hor, 70, seed + 1), (126, 134, 142), seed + 2)
    img = haze(img, (230, 224, 208), .3)
    img = fill_ridge(img, ridge(w, h, hor + 14, 30, seed + 3), (100, 106, 90), seed + 4)
    ref = img[:hor + 10][::-1][: h - hor - 10]
    ref = np.pad(ref, ((0, h - hor - 10 - ref.shape[0]), (0, 0), (0, 0)), mode="edge")
    rip = (fbm(w, h - hor - 10, seed + 5, 5, 3) - .5) * 40
    ref = ref * .55 + np.array((40, 80, 110)) * .45 + rip[..., None]
    img[hor + 10:] = ref[: h - hor - 10]
    fg = ridge(w, h, h * .94, 24, seed + 8)
    img = fill_ridge(img, fg, (82, 84, 60), seed + 9, texamp=24)
    return finish(img, seed)

def scene_portrait(w, h, seed):
    rng = random.Random(seed)
    bg = lerp((222, 234, 246), (190, 210, 232), rng.random())
    img = np.zeros((h, w, 3)) + bg
    img = img * (.94 + fbm(w, h, seed, 3, 2)[..., None] * .1)
    sil = (58, 86, 120)
    def p(d):
        d.polygon([(w * .04, h), (w * .10, h * .80), (w * .34, h * .70), (w * .66, h * .70), (w * .90, h * .80), (w * .96, h)], fill=sil + (255,))
        d.rectangle((w * .44, h * .56, w * .56, h * .72), fill=sil + (255,))
        d.ellipse((w * .33, h * .22, w * .67, h * .62), fill=sil + (255,))
    img = paste(img, poly_layer(w, h, p, 2))
    return finish(img, seed, grain=3, vig=.15)

KINDS = {"pit": scene_pit, "hills": scene_hills, "green": scene_green, "plant": scene_plant, "underground": scene_underground,
         "solar": scene_solar, "water": scene_water, "portrait": scene_portrait}

def render(kind, seed, path, size=(1600, 900)):
    fn = KINDS.get(kind, scene_hills)
    fn(size[0], size[1], seed).save(path, "JPEG", quality=80, optimize=True, progressive=True)
