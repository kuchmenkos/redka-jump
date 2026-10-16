"""Піксельні іконки ачивок (96x96, сітка 48x48 x2, кремовий фон): kyiv, chain3, armor, bus10, lang5 + exp3 (кіт-автобус).
Решта іконок (art/achs/*.png) — старі ілюстрації, цей скрипт їх не чіпає.
Запуск: python3 art/achs.py  → art/achs/<id>.png і art/achs_new.png (прев'ю)."""
from PIL import Image
import json, os

DIR = os.path.dirname(os.path.abspath(__file__))
N, SC = 48, 2
BG = (254, 242, 210)
INK = '#2a1e18'

def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

class Cv:
    def __init__(s, frame=True):
        s.p = [[None] * N for _ in range(N)]
        s.frame = frame

    def px(s, x, y, c):
        if 0 <= x < N and 0 <= y < N:
            s.p[y][x] = c

    def rect(s, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.px(x, y, c)

    def ell(s, cx, cy, rx, ry, c):
        for y in range(N):
            for x in range(N):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1:
                    s.px(x, y, c)

    def line(s, x0, y0, x1, y1, c, w=1):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
            for a in range(w):
                for b in range(w):
                    s.px(x + a, y + b, c)

    def grid(s, rows, pal, ox, oy, k=1):
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch in pal:
                    for a in range(k):
                        for b in range(k):
                            s.px(ox + x * k + a, oy + y * k + b, pal[ch])

    def outline(s, c=INK):
        f = lambda x, y: 0 <= x < N and 0 <= y < N and s.p[y][x] is not None
        add = [(x, y) for y in range(N) for x in range(N) if not f(x, y) and any(f(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)]
        for x, y in add:
            s.p[y][x] = c

    def stamp(s):
        # пунктирна «марка» по краю, як на старих іконках
        for i in range(2, N - 2):
            if i % 3 != 2:
                for (x, y) in ((i, 2), (i, N - 3), (2, i), (N - 3, i)):
                    if s.p[y][x] is None:
                        s.px(x, y, '#d9c79a')

    def save(s, name):
        if s.frame:
            s.stamp()
        im = Image.new('RGB', (N * SC, N * SC), BG)
        for y in range(N):
            for x in range(N):
                c = s.p[y][x]
                if c:
                    im.paste(rgb(c), (x * SC, y * SC, x * SC + SC, y * SC + SC))
        im.save(os.path.join(DIR, 'achs', name + '.png'))
        return im

FONT = {
    '×': ['...', '#.#', '.#.', '#.#', '...'],
    '1': ['.#.', '##.', '.#.', '.#.', '###'],
    '0': ['###', '#.#', '#.#', '#.#', '###'],
    '3': ['###', '..#', '.##', '..#', '###'],
}
def text(c, s, x, y, col):
    for ch in s:
        for yy, row in enumerate(FONT[ch]):
            for xx, v in enumerate(row):
                if v == '#':
                    c.px(x + xx, y + yy, col)
        x += 4

def badge(c, s, cx, cy):
    w = len(s) * 4 + 3
    x0, y0 = cx - w // 2, cy - 4
    c.rect(x0, y0, x0 + w - 1, y0 + 8, '#d63434')
    c.rect(x0 + 1, y0 - 1, x0 + w - 2, y0 - 1, INK); c.rect(x0 + 1, y0 + 9, x0 + w - 2, y0 + 9, INK)
    c.rect(x0 - 1, y0, x0 - 1, y0 + 8, INK); c.rect(x0 + w, y0, x0 + w, y0 + 8, INK)
    text(c, s, x0 + 2, y0 + 2, '#ffffff')

BUS = json.load(open(os.path.join(DIR, 'catbus.json')))
def bus_icon(c, oy=7):
    rows = [r for y, r in enumerate(BUS['frames'][0]) if y % 6 != 2]
    rows = [''.join(ch for x, ch in enumerate(r) if x % 6 != 3) for r in rows]
    c.grid(rows, BUS['pal'], 3, oy, 1)

def kyiv():
    c = Cv()
    c.rect(4, 36, 43, 40, '#6fa04a')                       # трава
    c.rect(12, 26, 35, 36, '#f6f0e0'); c.rect(12, 26, 14, 36, '#d8cfb8')   # стіни
    for x in (16, 22, 28):                                 # арки-вікна
        c.rect(x, 29, x + 3, 36, '#3a6fbf'); c.rect(x + 1, 28, x + 2, 28, '#3a6fbf')
    c.rect(10, 24, 37, 25, '#3a6fbf')                      # синій пояс
    c.ell(24, 17, 7, 8.5, '#f2b928'); c.rect(21, 14, 22, 19, '#fff0a0')   # головна баня
    c.rect(23, 5, 24, 10, '#f2b928'); c.rect(21, 7, 26, 8, '#f2b928')    # хрест
    for cx in (13, 35):
        c.ell(cx, 22, 3.6, 4.4, '#f2b928'); c.px(cx, 17, '#f2b928'); c.px(cx, 16, '#f2b928')
    c.ell(41, 32, 4.5, 6, '#4f8f3a'); c.rect(40, 36, 41, 40, '#6a4a2a')   # каштан
    c.px(41, 27, '#fff0a0'); c.px(39, 30, '#fff0a0')
    c.outline(); return c

def chain3():
    c = Cv()
    c.rect(6, 38, 41, 42, '#2ea043'); c.rect(6, 42, 41, 42, '#1d7a30')    # ярлик-латка
    for x in range(9, 39, 4): c.px(x, 40, '#ffffff'); c.px(x + 1, 40, '#ffffff')
    c.rect(11, 12, 24, 30, '#7a4a28'); c.rect(11, 12, 15, 30, '#5b3419')   # халява
    c.rect(11, 28, 33, 34, '#7a4a28'); c.rect(25, 30, 36, 34, '#7a4a28')  # носак
    c.rect(10, 35, 37, 37, '#222222'); c.rect(14, 15, 21, 15, '#f0d8a0')  # підошва, шнурки
    c.rect(14, 19, 21, 19, '#f0d8a0'); c.rect(14, 23, 21, 23, '#f0d8a0')
    for (x, y) in ((8, 33), (6, 29), (39, 33), (41, 29)): c.px(x, y, '#ffd23a'); c.px(x + 1, y, '#ffd23a'); c.px(x, y + 1, '#ffd23a')
    for i, (cx, cy) in enumerate(((31, 8), (37, 13), (41, 20))):          # ланцюг ×3
        c.ell(cx, cy, 4.6, 3.2 if i % 2 == 0 else 4.6, '#9aa0aa'); c.ell(cx, cy, 2.6, 1.4 if i % 2 == 0 else 2.6, None)
    c.outline(); return c

def armor():
    c = Cv()
    S = ["..KKKKKKKKKKK..", ".KBBBBBBBBBBBK.", "KBbbBBBBBBBBBBK", "KBbBBBBBBBBBBBK", "KBBBBBBBBBBBBBK", "KBBBBBBBBBBBBBK", "KBBBBBBBBBBBBBK", "KBBBBBBBBBBBBBK",
         ".KBBBBBBBBBBBK.", ".KBBBBBBBBBBBK.", "..KBBBBBBBBBK..", "...KBBBBBBBK...", "....KBBBBBK....", ".....KBBBK.....", "......KKK......"]
    c.grid(S, {'K': '#1e1820', 'B': '#2b6fd6', 'b': '#9fd6ff'}, 5, 12, 2)
    for (x0, y0, x1, y1) in ((14, 20, 18, 24), (18, 24, 15, 28), (15, 28, 20, 31)):
        c.line(x0, y0, x1, y1, '#14306e', 1)                                  # тріщина від удару
    c.rect(32, 6, 43, 15, '#fffaf0'); c.rect(31, 7, 31, 14, INK); c.rect(44, 7, 44, 14, INK); c.rect(32, 5, 43, 5, INK); c.rect(32, 16, 43, 16, INK)
    c.line(32, 6, 37, 11, '#d63434'); c.line(43, 6, 38, 11, '#d63434')       # лист-скарга
    c.line(31, 17, 29, 21, '#ffd23a'); c.line(35, 18, 33, 23, '#ffd23a'); c.line(39, 18, 37, 23, '#ffd23a')   # відскок
    c.outline(); return c

def bus(n):
    c = Cv()
    bus_icon(c, 6)
    badge(c, '×' + str(n), 35, 39)
    c.outline(); return c

def lang5():
    c = Cv()
    c.rect(6, 22, 12, 30, '#d9302c'); c.rect(6, 22, 12, 23, '#f6f6f0')
    for i in range(0, 15):
        y0, y1 = 20 - i // 2, 32 + i // 2
        c.rect(13 + i, y0, 13 + i, y1, '#f6f6f0' if i % 5 < 2 else '#d9302c')
    c.rect(10, 31, 12, 36, '#444a55')
    c.line(21, 20, 25, 28, INK, 1); c.line(25, 28, 22, 33, INK, 1)           # тріщина
    c.ell(35, 14, 10.5, 9, '#ffffff'); c.rect(30, 21, 32, 25, '#ffffff')     # бульбашка
    c.rect(30, 12, 39, 13, '#2d6fd6'); c.rect(30, 12, 31, 20, '#2d6fd6'); c.rect(38, 12, 39, 20, '#2d6fd6')   # «Ї»
    c.rect(31, 8, 32, 9, '#2d6fd6'); c.rect(37, 8, 38, 9, '#2d6fd6')
    c.outline(); return c

def exp3():
    c = Cv()
    bus_icon(c, 6); badge(c, '×3', 35, 39); c.outline(); return c

icons = [('kyiv', kyiv()), ('chain3', chain3()), ('armor', armor()), ('bus10', bus(10)), ('lang5', lang5()), ('exp3', exp3())]
ims = [c.save(n) for n, c in icons]
m = Image.new('RGB', (len(ims) * 108, 108 * 2), (245, 235, 210))
for i, im in enumerate(ims):
    m.paste(im, (i * 108 + 6, 6)); m.paste(im.resize((96, 96)), (i * 108 + 6, 110))
m.save(os.path.join(DIR, 'achs_new.png'))
print('ok')
