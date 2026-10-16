"""Pixel «Шакалячий експрес» — кіт-автобус (рудий шакал, на спині автобус з вікнами і синьою смугою).
Профіль, дивиться ВПРАВО, сітка 48x32. 2 кадри бігу (лапи в протифазі, хвіст вгору/вниз).
Редька стоїть на даху (верхня лінія тіла y=6).

Writes catbus.json {frames: [rows, rows], pal} and catbus.png (preview). Paste into index.html (BUSGRID/BUSPAL)."""
from PIL import Image
import json, os

DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 48, 32

PAL = {
    'A': '#e8a33a',  # шерсть
    'a': '#c07a22',  # тінь шерсті / дальні лапи
    'D': '#8a4a1e',  # темний кінчик хвоста, вуха, пазурі
    'S': '#f6e6c0',  # кремовий живіт
    'R': '#6a3a22',  # дах
    'r': '#8d5632',  # світлий край даху
    'F': '#5a301c',  # рами вікон
    'g': '#2a1a20',  # скло
    'h': '#8fc7ff',  # блік на склі
    'B': '#4f7fd0',  # синя смуга
    'b': '#3a62ad',  # низ смуги
    'W': '#ffffff',  # зуби, очі, літери
    'K': '#1a141a',  # зіниці, ніс
    'M': '#7a1c2a',  # пащека
    'P': '#e8707c',  # язик
    'Y': '#ffd23a',  # фари
}

# шрифт 3x5 для «ЕКСПРЕС»
FONT = {
    'Е': ['###', '#..', '##.', '#..', '###'],
    'К': ['#.#', '#.#', '##.', '#.#', '#.#'],
    'С': ['.##', '#..', '#..', '#..', '.##'],
    'П': ['###', '#.#', '#.#', '#.#', '#.#'],
    'Р': ['##.', '#.#', '##.', '#..', '#..'],
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

    def ell(s, cx, cy, rx, ry, c):
        for y in range(H):
            for x in range(W):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1:
                    s.px(x, y, c)

    def line(s, x0, y0, x1, y1, c, w=2):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n)
            y = round(y0 + (y1 - y0) * i / n)
            for k in range(w):
                s.px(x + k, y, c)

    def rows(s):
        return [''.join(r) for r in s.g]


# ноги: (x стегна, x стопи, y стопи); 3 дальні (темні) і 3 ближні, дві фази
LEGS = [
    dict(far=[(10, 7, 30), (18, 21, 29), (27, 26, 30)], near=[(8, 11, 29), (15, 12, 30), (24, 29, 29)]),
    dict(far=[(10, 13, 29), (18, 16, 30), (27, 31, 29)], near=[(8, 5, 30), (15, 18, 29), (24, 22, 30)]),
]
TAIL = [0, 1]


def bus(frame):
    g = G()
    ly = LEGS[frame]
    # дальні лапи
    for hx, fx, fy in ly['far']:
        g.line(hx, 22, fx, fy - 1, 'a', 2)
        g.rect(fx - 1, fy, fx + 2, fy, 'D')
    # хвіст: піднятий пухнастий серпанок за кабіною (зліва)
    ty = TAIL[frame]
    for (cx, cy, rx, ry, c) in ((3.5, 18, 3.4, 3.2, 'A'), (2.6, 13 + ty, 2.8, 3.4, 'A'), (3.2, 8 + ty, 3.0, 3.4, 'A'), (4.5, 3 + ty, 2.6, 3.0, 'A')):
        g.ell(cx, cy, rx, ry, c)
    g.rect(3, 1 + ty, 6, 3 + ty, 'D')
    g.px(2, 12 + ty, 'a'); g.px(2, 14 + ty, 'a'); g.px(3, 9 + ty, 'a')
    # корпус
    g.rect(5, 6, 34, 24, 'A')
    for x, y in ((5, 6), (34, 6), (5, 24), (34, 24)):
        g.px(x, y, '.')
    # дах
    g.rect(6, 6, 33, 6, 'r')
    g.rect(5, 7, 34, 8, 'R')
    # вікна: 4 штуки з рамами і блікомзі
    for i in range(4):
        x0 = 7 + i * 7
        g.rect(x0, 9, x0 + 5, 14, 'F')
        g.rect(x0 + 1, 10, x0 + 4, 13, 'g')
        g.px(x0 + 1, 10, 'h'); g.px(x0 + 2, 10, 'h'); g.px(x0 + 1, 11, 'h')
    # світла смуга-розділювач
    g.rect(5, 15, 34, 15, 'a')
    # синя смуга з написом
    g.rect(5, 16, 34, 22, 'B')
    g.rect(5, 22, 34, 22, 'b')
    word = 'ЕКСПРЕС'
    x = 7
    for ch in word:
        for yy, row in enumerate(FONT[ch]):
            for xx, c in enumerate(row):
                if c == '#':
                    g.px(x + xx, 17 + yy, 'W')
        x += 4
    # живіт
    g.rect(5, 23, 34, 24, 'S')
    g.rect(5, 23, 34, 23, 'a')
    # шия/голова (спереду, справа)
    g.ell(41.5, 15, 6.6, 10, 'A')
    g.rect(35, 7, 38, 23, 'A')
    # вуха (два трикутники над головою)
    g.rect(36, 3, 38, 5, 'A'); g.px(37, 2, 'A'); g.px(37, 1, 'D'); g.px(37, 3, 'D'); g.px(37, 4, 'D')
    g.rect(43, 2, 45, 5, 'A'); g.px(44, 1, 'A'); g.px(44, 0, 'D'); g.px(44, 2, 'D'); g.px(44, 3, 'D')
    # очі: великі білі кола зі зіницями
    for ex in (38, 43):
        g.rect(ex, 7, ex + 3, 11, 'W')
        g.px(ex, 7, 'A'); g.px(ex + 3, 7, 'A')
        g.rect(ex + 1, 8, ex + 2, 10, 'K')
        g.px(ex + 1, 8, 'W')
    # ніс
    g.rect(45, 13, 46, 14, 'K')
    # пащека з зубами
    g.rect(38, 17, 46, 22, 'M')
    g.rect(40, 20, 44, 22, 'P')
    for x in (38, 41, 44):
        g.rect(x, 17, x + 1, 18, 'W')
    for x in (39, 42, 45):
        g.rect(x, 21, x + 1, 22, 'W')
    # фара-щока
    g.px(39, 14, 'Y'); g.px(40, 14, 'Y')
    # ближні лапи
    for hx, fx, fy in ly['near']:
        g.line(hx, 22, fx, fy - 1, 'A', 2)
        g.rect(fx - 1, fy, fx + 2, fy, 'D')
    return g


frames = [bus(f).rows() for f in range(2)]
json.dump({'frames': frames, 'pal': PAL}, open(os.path.join(DIR, 'catbus.json'), 'w'))

SC = 10
img = Image.new('RGB', (2 * (W * SC + 12) + 12, H * SC + 24), (150, 120, 170))


def paint(rows, ox, oy):
    filled = lambda x, y: 0 <= y < H and 0 <= x < W and rows[y][x] in PAL
    for y in range(-1, H + 1):
        for x in range(-1, W + 1):
            if filled(x, y):
                continue
            if any(filled(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                img.paste((26, 20, 26), (ox + x * SC, oy + y * SC, ox + x * SC + SC, oy + y * SC + SC))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c in PAL:
                col = tuple(int(PAL[c][j:j + 2], 16) for j in (1, 3, 5))
                img.paste(col, (ox + x * SC, oy + y * SC, ox + x * SC + SC, oy + y * SC + SC))


for f in range(2):
    paint(frames[f], 12 + f * (W * SC + 12), 12)
img.save(os.path.join(DIR, 'catbus.png'))
print('wrote catbus.json, catbus.png')
