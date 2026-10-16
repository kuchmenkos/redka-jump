"""Pixel bodies for Redka looks. Every look shares ONE silhouette (the clown's: big ruff, wide torso,
hands out, pants, shoes) and differs by palette and torso pattern. Look 0 is the same body shirtless.
Headless: the face is felix*.png laid on top by makeChar() in index.html.

Writes looks.json {grids, grids_side (hands slightly out, while jumping), grids_up (hands raised, while flying on the rocket), pals, head} and looks.png (preview). Paste grids/pals/head into index.html
(LOOKGRID, LOOKPAL, HEADPH)."""
from PIL import Image
import json, os

DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 30, 35


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


def ruff(g):
    """Gathered collar (S light, s shade, W highlight). Same on every dressed look."""
    g.ell(15, 14.2, 9.2, 3.4, 'S', 's', .5)
    g.ell(15, 15.6, 7.4, 2.2, 'W', 's', .45)
    g.rect(12, 16, 18, 16, 'S')


def torso_base(g, c, shade):
    g.rect(9, 17, 21, 29, c)
    g.rect(20, 17, 21, 29, shade)
    for x, y in ((9, 17), (21, 17), (9, 29), (21, 29)):
        g.px(x, y, '.')


def dia(g, cx, cy, s, lite, dark):
    for y in range(-s, s + 1):
        w = s - abs(y)
        for x in range(-w, w + 1):
            g.px(cx + x, cy + y, dark if x > 0 else lite)


def pat_diamond(g):
    cols = [('A', 'a'), ('B', 'b'), ('C', 'c')]
    for cy, shift in ((19, 0), (22, 1), (25, 0), (28, 1)):
        for j in range(3):
            lite, dark = cols[(j + shift) % 3]
            dia(g, 10 + j * 4 + (1 if shift else 0), cy, 2, lite, dark)


def pat_plain(g):
    """Suit jacket: small white shirt V, bow tie, lapel seams, gold buttons."""
    torso_base(g, 'A', 'a')
    for i in range(6):
        g.rect(13 + i // 2, 17 + i, 17 - i // 2, 17 + i, 'W')
        g.px(12 + i // 2, 17 + i, 'a'); g.px(18 - i // 2, 17 + i, 'a')
    g.px(14, 17, 'R'); g.px(15, 17, 'K'); g.px(16, 17, 'R')
    for y in (24, 26, 28):
        g.px(15, y, 'M')
    g.px(15, 23, 'a')
    g.rect(9, 29, 21, 29, 'K')


def pat_stripes(g):
    torso_base(g, 'A', 'a')
    for x in range(9, 22):
        if ((x - 9) // 2) % 2:
            g.rect(x, 17, x, 29, 'B')
    g.rect(9, 29, 21, 29, 'K'); g.px(15, 29, 'M')


def pat_dots(g):
    torso_base(g, 'A', 'a')
    for x, y in ((11, 19), (15, 19), (19, 19), (13, 22), (17, 22), (11, 25), (15, 25), (19, 25), (13, 28), (17, 28)):
        g.rect(x, y, x + 1, y + 1, 'C')
        g.px(x + 1, y + 1, 'c')
    g.rect(9, 29, 21, 29, 'K'); g.px(15, 29, 'M')


def pat_tunic(g):
    torso_base(g, 'A', 'a')
    for y in (19, 22, 25):
        g.rect(10, y, 20, y, 'a')
    g.rect(19, 17, 21, 19, 'O'); g.px(20, 18, 'o'); g.px(21, 19, 'o')
    g.px(14, 20, 'O'); g.px(14, 23, 'O'); g.px(14, 26, 'O')
    g.rect(9, 29, 21, 29, 'K')


def pat_bare(g):
    """Shirtless: neck, pecs, belly button. The motivation to buy a suit."""
    g.rect(13, 16, 17, 19, 'F')
    g.rect(9, 18, 21, 29, 'F')
    g.rect(20, 18, 21, 29, 'f')
    for x, y in ((9, 18), (21, 18), (9, 29), (21, 29)):
        g.px(x, y, '.')
    g.rect(10, 22, 13, 22, 'f'); g.rect(17, 22, 20, 22, 'f')   # under the pecs
    g.px(12, 20, 'q'); g.px(18, 20, 'q')                       # nipples
    g.px(15, 26, 'f'); g.px(15, 27, 'f')                       # belly button
    g.rect(9, 29, 21, 29, 'K')                                 # belt


def arms(g, left, right, skin=False, up=False, side=False):
    if side:
        # micro-gesture while jumping: arms swing a little outward and the hands lift to waist height
        cl, cr = ('F', 'F') if skin else (left, right)
        sl, sr = ('f', 'f') if skin else (left.lower(), right.lower())
        for y in range(18, 26):
            xl = 7 - round((y - 18) * 3 / 7)
            xr = 29 - xl
            g.rect(xl - 1, y, xl + 1, y, cl)
            g.px(xl + 1, y, sl)
            g.rect(xr - 1, y, xr + 1, y, cr)
            g.px(xr - 1, y, sr)
        g.rect(1, 24, 4, 26, 'F'); g.rect(25, 24, 28, 26, 'F')
        g.rect(1, 26, 4, 26, 'f'); g.rect(25, 26, 28, 26, 'f')
        return
    if up:
        # hands raised: arms go diagonally up and out beside the face (face spans x 7.5..22.5)
        cl, cr = ('F', 'F') if skin else (left, right)
        sl, sr = ('f', 'f') if skin else (left.lower(), right.lower())
        for y in range(9, 20):
            xl = 7 - round((19 - y) * 5 / 10)
            xr = 29 - xl
            g.rect(xl - 1, y, xl + 1, y, cl)
            g.px(xl + 1, y, sl)
            g.rect(xr - 1, y, xr + 1, y, cr)
            g.px(xr - 1, y, sr)
        g.rect(1, 5, 4, 8, 'F'); g.rect(25, 5, 28, 8, 'F')
        g.rect(1, 8, 4, 8, 'f'); g.rect(25, 8, 28, 8, 'f')
        return
    if skin:
        g.rect(6, 18, 8, 26, 'F'); g.rect(22, 18, 24, 26, 'F')
        g.rect(8, 18, 8, 26, 'f'); g.rect(22, 18, 22, 26, 'f')
    else:
        g.rect(6, 18, 8, 26, left); g.rect(22, 18, 24, 26, right)
        g.rect(8, 18, 8, 26, left.lower()); g.rect(22, 18, 22, 26, right.lower())
    g.rect(5, 26, 8, 27, 'F')
    g.rect(22, 26, 25, 27, 'F')


def lower(g, shoe_l='A', shoe_r='B', skirt=False):
    if skirt:
        g.rect(9, 30, 21, 31, 'P')
        for x in range(9, 22, 2):
            g.rect(x, 31, x, 32, 'p')
    else:
        g.rect(10, 30, 13, 32, 'P'); g.rect(17, 30, 20, 32, 'P')
        g.rect(10, 32, 13, 32, 'p'); g.rect(17, 32, 20, 32, 'p')
    g.rect(9, 33, 13, 34, 'K'); g.rect(17, 33, 21, 34, 'K')
    g.px(11, 33, shoe_l); g.px(19, 33, shoe_r)


def suit(pat, arm=('A', 'A'), dressed=True, skin_arms=False, skirt=False, shoes=('A', 'B'), up=False, side=False):
    g = G()
    if dressed:
        ruff(g)
    if (up or side) and pat is pat_diamond:  # the diamond pattern leaves ragged edges that only the lowered arms used to hide
        torso_base(g, 'A', 'a')
    pat(g)
    if up or side:  # pattern cells that poked out under the lowered arms must not show when the arms are raised
        for y in range(17, 30):
            for x in list(range(0, 9)) + list(range(22, 30)):
                g.g[y][x] = '.'
    arms(g, arm[0], arm[1], skin_arms, up, side)
    lower(g, shoes[0], shoes[1], skirt)
    g.outline()
    return g


# name, pattern, extra kwargs, palette (letters used above), outline override, gold flag
SKIN = {'F': '#f2c9a0', 'f': '#d99c72', 'q': '#c97a62'}
LOOKS = [
    dict(name='Жебрак', pat=pat_bare, kw=dict(dressed=False, skin_arms=True),
         pal=dict(SKIN, P='#4a68a8', p='#324a80', A='#c8281e', B='#c8281e')),
    dict(name='Перший піджак', pat=pat_plain, kw=dict(arm=('A', 'A'), shoes=('M', 'M')),
         pal=dict(SKIN, A='#2b2b38', a='#17171f', S='#ffffff', s='#d9dcea', W='#fafafa', R='#d63434', M='#e2b33a', P='#3a3a46', p='#25252e')),
    dict(name='Жовтий піджак', pat=pat_plain, kw=dict(arm=('A', 'A'), shoes=('M', 'M')),
         pal=dict(SKIN, A='#f5cb26', a='#c88e12', S='#fff8ee', s='#e8d6a0', W='#fafafa', R='#d63434', M='#8f5f08', P='#7a5a1a', p='#573e10')),
    dict(name='Синій оксамит', pat=pat_stripes, kw=dict(arm=('A', 'A'), shoes=('B', 'B')),
         pal=dict(SKIN, A='#2f5fd0', a='#1b3a8a', B='#4b80f0', b='#2f5fd0', S='#e6edff', s='#aebfee', W='#ffffff', M='#e2b33a', P='#1b3a8a', p='#12276b')),
    dict(name='Малиновий смокінг', pat=pat_plain, kw=dict(arm=('A', 'A'), shoes=('M', 'M')),
         pal=dict(SKIN, A='#b81f52', a='#6e0d2b', S='#fff0f4', s='#e8b8c8', W='#fafafa', R='#1a141a', M='#ffd75a', P='#2a1018', p='#18080e')),
    dict(name='Клоун', pat=pat_diamond, kw=dict(arm=('A', 'B'), shoes=('A', 'B')),
         pal=dict(SKIN, A='#e22b2b', a='#9e1212', B='#2ea043', b='#1a6b32', C='#f5cb26', c='#c88e12', S='#fff8ee', s='#e4d4b8', W='#ffffff', M='#f5cb26', P='#fff8ee', p='#e4d4b8')),
    dict(name='Смарагдовий костюм', pat=pat_dots, kw=dict(arm=('A', 'A'), shoes=('C', 'C')),
         pal=dict(SKIN, A='#18946a', a='#0b553d', C='#7ff0c4', c='#3fc79a', S='#e8fff6', s='#a9e4cc', W='#ffffff', M='#e2b33a', P='#0b553d', p='#073a29')),
    dict(name='Одіссей', pat=pat_tunic, kw=dict(arm=('A', 'A'), skin_arms=True, skirt=True, shoes=('O', 'O')),
         pal=dict(SKIN, A='#4a3a32', a='#2e241e', O='#c4a35a', o='#8a6a28', S='#a8a39e', s='#6f6a66', W='#c9c4be', P='#3a322c', p='#2e241e')),
    dict(name='Біле пальто', pat=pat_plain, kw=dict(arm=('A', 'A'), shoes=('M', 'M')),
         pal=dict(SKIN, A='#f4f4f0', a='#c4c9d6', S='#d6e4f7', s='#9fb6d6', W='#ffffff', R='#b81f52', M='#e2b33a', P='#8a93a6', p='#646c7e')),
    dict(name='Золотий костюм', pat=pat_diamond, kw=dict(arm=('A', 'B'), shoes=('A', 'B')), out='#ffe08a', gold=1,
         pal=dict(SKIN, A='#c8860e', a='#8f5f08', B='#ffd75a', b='#d9a52a', C='#fff4b8', c='#f0cf66', S='#fff4b8', s='#e2c36a', W='#ffffff', M='#fff4b8', P='#c88e12', p='#8f5f08')),
]

# Placeholder head for the frames before felix.png has loaded (rows 2..10 of the 30-wide grid).
HEAD = G()
HEAD.ell(15, 7, 5.2, 5.4, 'F', 'f', .5)
HEAD.px(13, 6, 'K'); HEAD.px(17, 6, 'K'); HEAD.rect(14, 10, 16, 10, 'p')
HEAD.outline()

BASE_PAL = {'K': '#1a141a'}
SC = 10
grids = [suit(L['pat'], **L['kw']) for L in LOOKS]
grids_up = [suit(L['pat'], up=True, **L['kw']) for L in LOOKS]
grids_side = [suit(L['pat'], side=True, **L['kw']) for L in LOOKS]
json.dump({'grids': [g.rows() for g in grids], 'grids_up': [g.rows() for g in grids_up], 'grids_side': [g.rows() for g in grids_side], 'pals': [L['pal'] for L in LOOKS], 'head': HEAD.rows()[:12]},
          open(os.path.join(DIR, 'looks.json'), 'w'))

cols = 5
cell = W * SC + 24
img = Image.new('RGB', (cols * cell + 24, 6 * (H * SC + 36) + 12), (239, 230, 211))
for i, (L, g) in enumerate(zip(LOOKS * 3, grids + grids_side + grids_up)):
    pal = dict(BASE_PAL, **L['pal'])
    ox, oy = 16 + (i % cols) * cell, 12 + (i // cols) * (H * SC + 36)
    for y, r in enumerate(g.rows()):
        for x, c in enumerate(r):
            if c != '.' and c in pal:
                col = tuple(int(pal[c][j:j + 2], 16) for j in (1, 3, 5))
                img.paste(col, (ox + x * SC, oy + y * SC, ox + x * SC + SC, oy + y * SC + SC))
img.save(os.path.join(DIR, 'looks.png'))
print('wrote looks.json, looks.png;', len(LOOKS), 'looks', W, 'x', H)
