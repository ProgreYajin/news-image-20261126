"""Build entry.png: a newspaper front page for Thursday 26 November 2026.

Drawn at 2x and downsampled for smooth shapes. Deterministic: no randomness,
no timestamps, no metadata in the PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont

S = 2
W = H = 1024
FD = "/usr/share/fonts/truetype/dejavu/"
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (246, 241, 228)
INK = (28, 26, 24)
GREY = (95, 90, 84)
RED = (196, 38, 38)
BLUE = (38, 84, 150)
GOLD = (214, 160, 40)
GREEN = (52, 128, 82)
STEEL = (150, 160, 172)

img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)


def font(name, size):
    return ImageFont.truetype(FD + name, int(size * S))


def p(*xy):
    return [v * S for v in xy]


def rect(x0, y0, x1, y1, fill=None, outline=None, width=0):
    d.rectangle(p(x0, y0, x1, y1), fill=fill, outline=outline, width=int(width * S))


def rrect(x0, y0, x1, y1, r, fill=None, outline=None, width=0):
    d.rounded_rectangle(p(x0, y0, x1, y1), r * S, fill=fill, outline=outline, width=int(width * S))


def ell(x0, y0, x1, y1, fill=None, outline=None, width=0):
    d.ellipse(p(x0, y0, x1, y1), fill=fill, outline=outline, width=int(width * S))


def poly(pts, fill=None):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill)


def line(pts, fill, width):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=int(width * S))


def text_w(s, f):
    return d.textlength(s, font=f) / S


def text(x, y, s, f, fill=INK, anchor="la"):
    d.text((x * S, y * S), s, font=f, fill=fill, anchor=anchor)


def wrap(s, f, maxw):
    words, lines, cur = s.split(" "), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    return lines


def block(x, y, maxw, s, fname, size, max_lines, fill=INK, lead=1.18):
    """Wrap s into at most max_lines; shrink the font if needed. Returns new y."""
    while True:
        f = font(fname, size)
        ls = wrap(s, f, maxw)
        if len(ls) <= max_lines and all(text_w(l, f) <= maxw for l in ls):
            break
        size -= 1
        assert size >= 20, s
    for l in ls:
        text(x, y, l, f, fill)
        y += size * lead
    return y


# ---------------------------------------------------------------- masthead
M = 28  # page margin
text(W / 2, 22, "THE WORLD DAILY", font("DejaVuSerif-Bold.ttf", 74), anchor="ma")
rect(M, 112, W - M, 116, fill=INK)
rect(M, 122, W - M, 184, fill=INK)
text(W / 2, 153, "THURSDAY 26 NOVEMBER 2026", font("DejaVuSans-Bold.ttf", 44), fill=PAPER, anchor="mm")
rect(M, 190, W - M, 192, fill=INK)

# ---------------------------------------------------------------- lead story
LY0, LY1 = 206, 452


def illo_tariffs(x, y):
    # sea, container ship, and two "up to" tariff bars
    rrect(x, y, x + 380, y + 230, 10, fill=(214, 228, 240))
    rect(x, y + 168, x + 380, y + 230, fill=(120, 160, 205))
    poly([(x + 18, y + 150), (x + 232, y + 150), (x + 214, y + 184), (x + 36, y + 184)], fill=INK)
    cols = [RED, BLUE, GOLD, GREEN, (200, 110, 50)]
    for i in range(5):
        rect(x + 40 + i * 36, y + 118, x + 72 + i * 36, y + 148, fill=cols[i])
    for i in range(3):
        rect(x + 76 + i * 36, y + 86, x + 108 + i * 36, y + 116, fill=cols[(i + 2) % 5])
    rect(x + 196, y + 96, x + 222, y + 148, fill=STEEL)
    # bars
    base = y + 150
    bf = font("DejaVuSans-Bold.ttf", 24)
    lf = font("DejaVuSans-Bold.ttf", 16)
    for bx, hgt, col, val, lab in ((x + 232, 62, GOLD, "25%", "INDIA+6"), (x + 312, 100, RED, "40%", "CHINA")):
        rect(bx, base - hgt, bx + 56, base, fill=col)
        text(bx + 28, base - hgt - 6, val, bf, anchor="md")
        text(bx + 28, y + 200, lab, lf, fill=PAPER, anchor="mm")


illo_tariffs(M, LY0 + 6)
tx = M + 404
text(tx, LY0 + 4, "LEAD STORY", font("DejaVuSans-Bold.ttf", 22), fill=RED)
y = block(tx, LY0 + 36, W - M - tx, "US readies plan for new tariffs", "DejaVuSerif-Bold.ttf", 52, 2, lead=1.12)
y = block(tx, y + 14, W - M - tx, "Up to 25% on goods from India and six other nations; China up to 40%",
          "DejaVuSans.ttf", 28, 3, fill=GREY, lead=1.25)
rect(M, LY1 + 6, W - M, LY1 + 9, fill=INK)

# ---------------------------------------------------------------- small stories
def illo_swiss(x, y, s):
    # Swiss flag on a building + 48h clock
    rect(x + 6, y + 40, x + 86, y + 124, fill=STEEL)
    poly([(x, y + 42), (x + 46, y + 10), (x + 92, y + 42)], fill=GREY)
    rect(x + 32, y + 84, x + 60, y + 124, fill=INK)
    rect(x + 22, y + 48, x + 70, y + 78, fill=RED)
    rect(x + 42, y + 52, x + 50, y + 74, fill="white")
    rect(x + 35, y + 59, x + 57, y + 67, fill="white")
    ell(x + 92, y + 56, x + 130, y + 94, fill="white", outline=INK, width=3)
    line([(x + 111, y + 75), (x + 111, y + 62)], INK, 3)
    line([(x + 111, y + 75), (x + 121, y + 75)], INK, 3)
    text(x + 111, y + 110, "48h", font("DejaVuSans-Bold.ttf", 20), fill=RED, anchor="mm")


def illo_station(x, y, s):
    ell(x, y, x + 130, y + 130, fill=(30, 40, 70))
    for sx, sy in ((x + 20, y + 24), (x + 104, y + 30), (x + 30, y + 104), (x + 98, y + 100)):
        ell(sx - 2, sy - 2, sx + 2, sy + 2, fill="white")
    rect(x + 50, y + 56, x + 80, y + 74, fill=STEEL)
    rect(x + 60, y + 30, x + 70, y + 100, fill=(200, 205, 212))
    for px in (x + 12, x + 84):
        rect(px, y + 50, px + 34, y + 80, fill=BLUE)
        line([(px + 17, y + 50), (px + 17, y + 80)], (180, 200, 230), 2)
    line([(x + 46, y + 65), (x + 84, y + 65)], STEEL, 3)
    poly([(x + 58, y + 100), (x + 72, y + 100), (x + 76, y + 118), (x + 54, y + 118)], fill=GOLD)


def illo_probe(x, y, s):
    rect(x + 10, y + 12, x + 86, y + 118, fill="white", outline=INK, width=3)
    for i in range(5):
        rect(x + 22, y + 30 + i * 16, x + 74 - (i % 2) * 18, y + 36 + i * 16, fill=GREY)
    ell(x + 56, y + 48, x + 112, y + 104, fill=(210, 230, 245), outline=RED, width=7)
    line([(x + 104, y + 98), (x + 128, y + 124)], RED, 11)


def illo_candle(x, y, s):
    ell(x + 20, y + 104, x + 110, y + 124, fill=GREY)
    rect(x + 48, y + 46, x + 82, y + 114, fill="white", outline=INK, width=3)
    line([(x + 65, y + 46), (x + 65, y + 36)], INK, 3)
    poly([(x + 65, y + 4), (x + 76, y + 26), (x + 65, y + 38), (x + 54, y + 26)], fill=GOLD)
    poly([(x + 65, y + 16), (x + 70, y + 28), (x + 65, y + 34), (x + 60, y + 28)], fill=(240, 120, 40))


def illo_cart(x, y, s):
    line([(x + 4, y + 30), (x + 24, y + 30), (x + 40, y + 92), (x + 112, y + 92)], INK, 6)
    poly([(x + 26, y + 42), (x + 124, y + 42), (x + 112, y + 82), (x + 36, y + 82)], fill=STEEL)
    for i in range(4):
        line([(x + 46 + i * 20, y + 44), (x + 48 + i * 18, y + 80)], (120, 128, 138), 2)
    ell(x + 42, y + 98, x + 62, y + 118, fill=INK)
    ell(x + 92, y + 98, x + 112, y + 118, fill=INK)
    # police light
    rrect(x + 64, y + 2, x + 96, y + 26, 6, fill=BLUE)
    rect(x + 60, y + 24, x + 100, y + 30, fill=INK)


def illo_shirt(x, y, s):
    poly([(x + 30, y + 30), (x + 52, y + 20), (x + 78, y + 20), (x + 100, y + 30), (x + 118, y + 56),
          (x + 100, y + 66), (x + 96, y + 60), (x + 96, y + 124), (x + 34, y + 124), (x + 34, y + 60),
          (x + 30, y + 66), (x + 12, y + 56)], fill=GREEN)
    ell(x + 52, y + 14, x + 78, y + 30, fill=PAPER)
    poly([(x + 65, y + 50), (x + 86, y + 76), (x + 73, y + 76), (x + 73, y + 108), (x + 57, y + 108),
          (x + 57, y + 76), (x + 44, y + 76)], fill="white")


stories = [
    (illo_swiss, "N. Korea orders Swiss office shut",
     "Senior Swiss diplomat told to leave Pyongyang within 48 hours"),
    (illo_station, "Pakistani astronaut visits Tiangong",
     "Muhammad Zeeshan Ali is first foreign crew member, on Shenzhou-24"),
    (illo_probe, "China probes Shanghai party chief",
     "Graft investigation into Politburo member Chen\u00a0Jining"),
    (illo_candle, "Russia's war losses near 500,000",
     "Russian figures on its toll in the war in Ukraine"),
    (illo_cart, "Colombia police free 20 hostages",
     "Supermarket stormed after 17-hour hostage ordeal"),
    (illo_shirt, "Bangladesh lifts garment wage 36%",
     "Minimum pay raised after weeks of protests"),
]

GX0, GY0, GY1 = M, LY1 + 20, H - 18
CW = (W - 2 * M) / 2
CH = (GY1 - GY0) / 3
for i, (illo, head, sub) in enumerate(stories):
    c, r = i % 2, i // 2
    cx, cy = GX0 + c * CW, GY0 + r * CH
    pad = 14 if c == 1 else 0
    illo(cx + pad, cy + 14, None)
    tx0 = cx + pad + 142
    maxw = cx + CW - tx0 - (0 if c == 1 else 14)
    y = block(tx0, cy + 10, maxw, head, "DejaVuSerif-Bold.ttf", 31, 2, lead=1.1)
    block(tx0, y + 6, maxw, sub, "DejaVuSans.ttf", 23, 3, fill=GREY, lead=1.2)
    if r < 2:
        rect(cx + pad, cy + CH - 2, cx + CW - (14 if c == 0 else 0), cy + CH, fill=(180, 172, 160))
rect(W / 2 - 1, GY0, W / 2 + 1, GY1 - 6, fill=INK)

out = img.resize((W, H), Image.LANCZOS)
out = out.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
out.save(os.path.join(HERE, "entry.png"), optimize=True)
