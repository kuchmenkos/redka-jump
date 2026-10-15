"""Pixel bodies for Redka looks. Jacket grid + unique clown / Odysseus costumes."""
from PIL import Image
import json, os

DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 30, 35

# Jacket / shirt / mic (same keys as index.html lookPal)
PAL = {
    'K': '#1a141a', 'G': '#4ca038', 'g': '#1d6626',
    'R': '#e2452a', 'r': '#b0241c', 'W': '#fafafa', 'P': '#c8281e', 'T': '#8f1a1a',
    'Y': '#f1ede4', 'y': '#cfc7b8', 'Z': '#fff0a0', 'M': '#b4b4ba', 'H': '#8f5f08',
    'n': '#2a2230', 'F': '#f2c9a0', 'h': '#ff9a7a',
    # clown
    'A': '#e22b2b', 'a': '#9e1212', 'B': '#2ea043', 'b': '#1a6b32',
    'C': '#f5cb26', 'c': '#c88e12', 'S': '#fff8ee', 's': '#e4d4b8',
    # odyssey
    'D': '#4a3a32', 'd': '#2e241e', 'U': '#6a6560', 'u': '#3e3a38',
    'O': '#c4a35a', 'o': '#8a6a28', 'N': '#3a322c', 'E': '#c9b08a',
}

class G:
    def __init__(s, w=W, h=H):
        s.w, s.h = w, h
        s.g = [['.'] * w for _ in range(h)]
    def px(s, x, y, c):
        if 0 <= x < s.w and 0 <= y < s.h:
            s.g[y][x] = c
    def rect(s, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.px(x, y, c)
    def ell(s, cx, cy, rx, ry, c, shade=None, sx=.45):
        for y in range(s.h):
            for x in range(s.w):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1:
                    s.px(x, y, shade if shade and (x + .5 - cx) > rx * sx else c)
    def get(s, x, y):
        return s.g[y][x] if 0 <= x < s.w and 0 <= y < s.h else '.'
    def outline(s):
        add = []
        for y in range(s.h):
            for x in range(s.w):
                if s.g[y][x] == '.' and any(s.get(x + dx, y + dy) not in '.K' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    add.append((x, y))
        for x, y in add:
            s.g[y][x] = 'K'
    def rows(s):
        return [''.join(r) for r in s.g]


def redka():
    """Sharper lapels, buttons, trousers, shoes. Radish head kept for no-face fallback."""
    g = G()
    # leaves
    g.ell(7, 4, 4.2, 4.4, 'G', 'g', .4)
    g.ell(15, 3.2, 4.6, 4.8, 'G', 'g', .35)
    g.ell(23, 4, 4.2, 4.4, 'G', 'g', .55)
    g.rect(12, 7, 18, 9, 'G')
    # radish
    g.ell(15, 16, 7.2, 7.4, 'R', 'r', .55)
    g.rect(10, 11, 20, 12, 'R')
    # face placeholders (overwritten by photo)
    g.rect(11, 13, 13, 15, 'W'); g.px(12, 14, 'P')
    g.rect(16, 13, 18, 15, 'W'); g.px(17, 14, 'P')
    g.rect(13, 17, 17, 18, 'T')
    # mic (cols 0-6)
    g.rect(1, 12, 5, 16, 'K')
    g.rect(2, 13, 4, 15, 'W')
    g.px(3, 14, 'M')
    g.rect(3, 17, 3, 22, 'K')
    g.px(2, 19, 'R'); g.px(4, 19, 'R')
    # collar / shirt
    g.rect(11, 20, 19, 27, 'R')
    g.rect(12, 20, 18, 20, 'r')
    g.rect(14, 21, 16, 26, 'T')  # tie
    g.px(15, 22, 'K'); g.px(15, 24, 'K'); g.px(15, 26, 'K')  # buttons
    # jacket — slimmer lapels + body (2 cells in from each side)
    g.rect(8, 20, 11, 30, 'Y')
    g.rect(19, 20, 22, 30, 'Y')
    g.rect(9, 21, 11, 29, 'Y')
    g.rect(19, 21, 21, 29, 'Y')
    g.rect(10, 22, 12, 22, 'y')   # left lapel
    g.rect(18, 22, 20, 22, 'y')
    g.rect(10, 23, 12, 23, 'y')
    g.rect(18, 23, 20, 23, 'y')
    g.rect(7, 24, 9, 30, 'Y')
    g.rect(21, 24, 23, 30, 'Y')
    g.rect(8, 28, 22, 30, 'Y')
    g.rect(7, 29, 9, 30, 'y')
    g.rect(21, 29, 23, 30, 'y')
    # trousers
    g.rect(10, 31, 13, 32, 'n')
    g.rect(17, 31, 20, 32, 'n')
    # shoes
    g.rect(9, 33, 13, 34, 'K')
    g.rect(17, 33, 21, 34, 'K')
    g.outline()
    return g


def clown():
    """Harlequin diamonds, white ruff, white pants. Headless — face is felix.png."""
    g = G()
    # ruff
    g.ell(15, 14.2, 9.2, 3.4, 'S', 's', .5)
    g.ell(15, 15.6, 7.4, 2.2, 'W', 's', .45)
    g.rect(12, 16, 18, 16, 'S')
    # diamonds on torso
    def dia(cx, cy, s, lite, dark):
        for y in range(-s, s + 1):
            w = s - abs(y)
            for x in range(-w, w + 1):
                g.px(cx + x, cy + y, dark if x > 0 else lite)
    cols = [('A', 'a'), ('B', 'b'), ('C', 'c')]
    for i, (cy, shift) in enumerate(((19, 0), (22, 1), (25, 0), (28, 1))):
        for j in range(3):
            lite, dark = cols[(j + shift) % 3]
            dia(10 + j * 4 + (1 if shift else 0), cy, 2, lite, dark)
    # belt
    g.rect(9, 29, 21, 29, 'K')
    g.px(15, 29, 'C')
    # arms
    g.rect(6, 18, 8, 26, 'A')
    g.rect(22, 18, 24, 26, 'B')
    g.rect(5, 26, 8, 27, 'F')
    g.rect(22, 26, 25, 27, 'F')
    # pants
    g.rect(10, 30, 13, 32, 'S')
    g.rect(17, 30, 20, 32, 'S')
    g.rect(10, 32, 13, 32, 's')
    g.rect(17, 32, 20, 32, 's')
    # shoes
    g.rect(9, 33, 13, 34, 'K')
    g.rect(17, 33, 21, 34, 'K')
    g.px(11, 33, 'A'); g.px(19, 33, 'B')
    g.outline()
    return g


def odyssey():
    """Leather cuirass, grey cloak, bronze brooch, bare arms. Headless."""
    g = G()
    # cloak behind, right shoulder
    g.ell(19, 22, 8.2, 12, 'U', 'u', .35)
    g.rect(16, 13, 26, 32, 'U')
    g.rect(21, 18, 27, 33, 'u')
    g.rect(17, 14, 23, 16, 'U')
    # neck
    g.rect(13, 12, 17, 14, 'F')
    # cuirass
    g.ell(14, 21, 6.2, 8.2, 'D', 'd', .5)
    g.rect(9, 16, 18, 27, 'D')
    g.rect(10, 17, 17, 18, 'd')  # muscle bands
    g.rect(10, 21, 17, 21, 'd')
    g.rect(10, 24, 17, 24, 'd')
    g.px(14, 19, 'O'); g.px(14, 22, 'O')
    # brooch + drape
    g.rect(17, 14, 20, 17, 'O')
    g.px(18, 15, 'o'); g.px(19, 16, 'o')
    g.rect(19, 14, 21, 15, 'E')
    # left bare arm
    g.rect(6, 16, 8, 24, 'F')
    g.rect(5, 24, 7, 25, 'F')
    g.px(7, 17, 'h')
    # skirt / pteruges
    g.rect(9, 28, 18, 30, 'N')
    for x in range(9, 19, 2):
        g.rect(x, 29, x, 31, 'D')
    # sandals
    g.rect(9, 32, 12, 32, 'N')
    g.rect(16, 32, 19, 32, 'N')
    g.rect(8, 33, 12, 34, 'K')
    g.rect(16, 33, 20, 34, 'K')
    g.px(9, 33, 'O'); g.px(18, 33, 'O')
    g.outline()
    return g


def nomic(rows):
    out = []
    for y, r in enumerate(rows):
        if 12 <= y <= 22:
            out.append('......' + r[6:])
        else:
            out.append(r)
    return out


S = {'redka': redka(), 'clown': clown(), 'odyssey': odyssey()}
data = {k: g.rows() for k, g in S.items()}
data['redka_nomic'] = nomic(data['redka'])
json.dump(data, open(os.path.join(DIR, 'looks.json'), 'w'))

scale = 10
names = ['redka', 'clown', 'odyssey']
img = Image.new('RGB', (len(names) * (W * scale + 24) + 24, H * scale + 48), (239, 230, 211))
for i, k in enumerate(names):
    g = S[k]
    ox = 16 + i * (W * scale + 24)
    for y, r in enumerate(g.rows()):
        for x, c in enumerate(r):
            if c != '.':
                col = tuple(int(PAL[c][j:j + 2], 16) for j in (1, 3, 5))
                img.paste(col, (ox + x * scale, 24 + y * scale, ox + x * scale + scale, 24 + y * scale + scale))
img.save(os.path.join(DIR, 'looks.png'))
print('wrote', os.path.join(DIR, 'looks.json'), 'and looks.png')
for k, g in S.items():
    print(k, len(g.rows()), 'x', len(g.rows()[0]))
