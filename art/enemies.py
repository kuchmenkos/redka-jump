"""Hater bodies: costume + props, no pixel faces (PNG overlay). cancel keeps a pixel head as fallback."""
from PIL import Image
import json, os

DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 20, 26
PAL = {
    'K': '#1e1820', 'F': '#f3c6a0', 'f': '#d99c72', 'p': '#f08f86', 'W': '#ffffff',
    'H': '#4a4a55', 'h': '#22222a', 'C': '#c9a46a', 'c': '#9c7a44', 'P': '#fbfbf2', 'L': '#8aa0c8', 'n': '#3b3b46',
    'A': '#5a3a22', 'T': '#d9302c', 't': '#9e1b1b', 'S': '#f4f4ee', 's': '#c4c8d0', 'M': '#f0b93a', 'm': '#b07d16', 'N': '#2c3a66',
    'B': '#2a2320', 'G': '#59606c', 'R': '#d63434', 'r': '#8f1c1c', 'D': '#5e6675', 'd': '#3f4552', 'Y': '#a8743e',
    'O': '#ecc062', 'o': '#b98a2c', 'V': '#c22a3a', 'Q': '#c0303a', 'X': '#2a9a8c', 'x': '#1b6660', 'Z': '#9a9aa4', 'U': '#9a6a3a',
    'J': '#2b6fd6', 'j': '#1b4a99', 'I': '#2c2c36', 'i': '#17171d', 'E': '#3a3a44', 'e': '#7cd2ff'
}

class G:
    def __init__(s):
        s.g = [['.'] * W for _ in range(H)]
    def px(s, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            s.g[y][x] = c
    def rect(s, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.px(x, y, c)
    def ell(s, cx, cy, rx, ry, c, shade=None, sx=.45):
        for y in range(H):
            for x in range(W):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1:
                    s.px(x, y, shade if shade and (x + .5 - cx) > rx * sx else c)
    def get(s, x, y):
        return s.g[y][x] if 0 <= x < W and 0 <= y < H else '.'
    def outline(s):
        add = []
        for y in range(H):
            for x in range(W):
                if s.g[y][x] == '.' and any(s.get(x + dx, y + dy) not in '.K' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    add.append((x, y))
        for x, y in add:
            s.g[y][x] = 'K'
    def rows(s):
        return [''.join(r) for r in s.g]


def neck(g, y=12):
    g.rect(8, y, 11, y + 1, 'F')
    g.px(8, y, 'f'); g.px(11, y, 'f')


def legs(g, col):
    g.rect(6, 23, 8, 24, col)
    g.rect(11, 23, 13, 24, col)
    g.rect(5, 25, 8, 25, 'K')
    g.rect(11, 25, 14, 25, 'K')


def face(g, eyes='norm', mouth='grin', cx=10, ey=8, brows='angry'):
    for ex in (cx - 3, cx + 2):
        if eyes == 'shifty':
            g.px(ex, ey, 'W'); g.px(ex + 1, ey, 'K')
        elif eyes == 'squint':
            g.px(ex, ey, 'K'); g.px(ex + 1, ey, 'K')
        else:
            g.px(ex, ey, 'W'); g.px(ex, ey + 1, 'K'); g.px(ex + 1, ey, 'K'); g.px(ex + 1, ey + 1, 'K')
    if brows == 'angry':
        g.px(cx - 4, ey - 2, 'K'); g.px(cx - 3, ey - 1, 'K'); g.px(cx + 4, ey - 2, 'K'); g.px(cx + 3, ey - 1, 'K')
    if brows == 'raised':
        g.rect(cx - 4, ey - 2, cx - 3, ey - 2, 'K'); g.rect(cx + 2, ey - 2, cx + 3, ey - 2, 'K')
    g.px(cx - 5, ey + 2, 'p'); g.px(cx + 5, ey + 2, 'p')
    my = ey + 4
    if mouth == 'grin':
        g.rect(cx - 2, my, cx + 1, my, 'K'); g.px(cx + 2, my - 1, 'K')
    if mouth == 'shout':
        g.rect(cx - 2, my - 1, cx + 1, my + 1, 'K'); g.rect(cx - 1, my, cx, my + 1, 'T')
    if mouth == 'flat':
        g.rect(cx - 2, my, cx + 1, my, 'K')
    if mouth == 'smirk':
        g.rect(cx - 1, my, cx + 2, my, 'K'); g.px(cx - 2, my - 1, 'K')


def head(g, cy=8):
    g.ell(10, cy, 6.6, 6.2, 'F', 'f', .68)


def stuk():
    g = G()
    # fedora brim sitting on the shoulders; PNG face covers the centre
    g.ell(10, 11.4, 6.4, 1.8, 'H', 'h', .5)
    g.rect(6, 11, 13, 11, 'h')
    neck(g, 12)
    g.ell(10, 18.4, 6.8, 5.6, 'C', 'c', .4)
    g.rect(9, 14, 11, 15, 'S')
    g.rect(9, 16, 10, 22, 'c')
    # dossier
    g.rect(14, 14, 18, 21, 'P')
    g.rect(15, 15, 17, 15, 'L')
    g.rect(15, 17, 17, 17, 'L')
    g.rect(15, 19, 17, 19, 'T')
    g.px(13, 16, 'F'); g.px(13, 17, 'F')
    legs(g, 'n')
    g.outline()
    return g


def koms():
    g = G()
    neck(g, 12)
    g.ell(10, 19, 6.2, 5.2, 'S', 's', .4)
    g.rect(8, 14, 12, 15, 'T')
    g.rect(9, 16, 11, 17, 'T')
    g.px(10, 18, 't')
    # red scarf tails
    g.rect(7, 14, 8, 18, 'T')
    g.rect(12, 14, 13, 17, 't')
    # megaphone
    g.rect(15, 15, 16, 18, 'M')
    g.rect(17, 14, 19, 19, 'M')
    g.rect(18, 15, 19, 18, 'm')
    g.px(14, 16, 'F'); g.px(14, 17, 'F')
    legs(g, 'N')
    g.outline()
    return g


def cancel():
    """No PNG — keep a pixel head as fallback."""
    g = G()
    head(g)
    g.ell(10, 3.4, 6.2, 2.8, 'B', 'B')
    g.rect(4, 3, 16, 4, 'B')
    g.rect(3, 6, 3, 10, 'G')
    g.rect(16, 6, 16, 10, 'G')
    g.rect(4, 2, 15, 2, 'G')
    g.px(3, 4, 'G'); g.px(3, 5, 'G'); g.px(16, 4, 'G'); g.px(16, 5, 'G')
    g.rect(14, 11, 15, 11, 'G'); g.px(13, 12, 'K')
    face(g, mouth='flat', brows='angry')
    g.ell(10, 19, 6.4, 5.2, 'D', 'd', .4)
    g.rect(9, 14, 11, 14, 'S')
    g.rect(9, 15, 10, 22, 'd')
    # stamp
    g.rect(14, 12, 16, 17, 'Y')
    g.rect(13, 18, 19, 21, 'R')
    g.rect(13, 21, 19, 21, 'r')
    g.px(14, 15, 'F'); g.px(14, 16, 'F')
    legs(g, 'd')
    g.outline()
    return g


def lang():
    """Teal blazer + clipboard only. Head is art/faces/lang.png."""
    g = G()
    neck(g, 13)
    g.ell(10, 19.5, 6.4, 5.0, 'X', 'x', .42)
    g.rect(8, 15, 12, 16, 'S')
    g.rect(9, 16, 11, 17, 'S')
    # clipboard
    g.rect(2, 16, 5, 21, 'U')
    g.rect(3, 17, 5, 20, 'P')
    g.px(4, 16, 'Z')
    g.px(4, 18, 'K'); g.px(4, 20, 'V')
    g.px(6, 18, 'F')
    g.rect(14, 16, 15, 18, 'F')
    legs(g, 'x')
    g.outline()
    return g


def threads():
    g = G()
    neck(g, 12)
    g.ell(10, 19.2, 7.0, 5.4, 'I', 'i', .4)
    g.rect(7, 14, 13, 14, 'I')
    g.px(8, 15, 'W'); g.px(12, 15, 'W')
    # phone
    g.rect(14, 14, 17, 21, 'E')
    g.rect(15, 15, 16, 20, 'e')
    g.px(13, 17, 'F'); g.px(13, 18, 'F')
    g.rect(9, 17, 11, 17, 'W')
    g.px(8, 18, 'W'); g.px(12, 18, 'W'); g.px(10, 18, 'e')
    g.rect(9, 19, 11, 19, 'W'); g.px(12, 19, 'W')
    legs(g, 'i')
    g.outline()
    return g


S = {'stuk': stuk(), 'koms': koms(), 'cancel': cancel(), 'lang': lang(), 'threads': threads()}
json.dump({k: g.rows() for k, g in S.items()}, open(os.path.join(DIR, 'enemies.json'), 'w'))
json.dump(PAL, open(os.path.join(DIR, 'pal.json'), 'w'))

scale = 10
img = Image.new('RGB', (len(S) * (W * scale + 20) + 20, H * scale + 40), (239, 230, 211))
for i, (k, g) in enumerate(S.items()):
    for y, r in enumerate(g.rows()):
        for x, c in enumerate(r):
            if c != '.':
                col = tuple(int(PAL[c][j:j + 2], 16) for j in (1, 3, 5))
                ox = 20 + i * (W * scale + 20)
                img.paste(col, (ox + x * scale, 20 + y * scale, ox + x * scale + scale, 20 + y * scale + scale))
img.save(os.path.join(DIR, 'enemies.png'))
print('wrote enemies.json / enemies.png')
for k, g in S.items():
    nonempty = sum(1 for r in g.rows() if r.strip('.'))
    print(k, 'rows with pixels', nonempty, 'first', next((i for i, r in enumerate(g.rows()) if r.strip('.')), None))
