"""Pixel jackals for the Jackal Express (Шакалячий експрес). Side view facing RIGHT, 34x20 grid.
Lean body, dark saddle, pointed ears, long snout, bushy tail. 4 gallop frames x (mouth shut | barking).

Writes jackals.json {frames: [shut[4], bark[4]], pals: {gold, grey, dark}} and jackals.png (preview).
Paste into index.html (JACKAL)."""
from PIL import Image
import json, os

DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 34, 20

PALS = {
    'gold': {'A': '#d9953f', 'a': '#a8692a', 'D': '#5b3a1c', 'S': '#f6e6c0', 'W': '#ffffff', 'B': '#1a141a', 'P': '#e8707c', 'R': '#7a1c2a', 'E': '#ffd23a'},
    'grey': {'A': '#b3a590', 'a': '#857866', 'D': '#3d3832', 'S': '#ece4d4', 'W': '#ffffff', 'B': '#1a141a', 'P': '#e8707c', 'R': '#7a1c2a', 'E': '#ffd23a'},
    'dark': {'A': '#8e6c48', 'a': '#614932', 'D': '#2a2018', 'S': '#dccaa6', 'W': '#ffffff', 'B': '#1a141a', 'P': '#e8707c', 'R': '#7a1c2a', 'E': '#ffd23a'},
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


# gallop: (front far, front near, hind far, hind near) as (hip_x, foot_x, foot_y, knee_dx)
GAIT = [
    dict(ff=(20, 26, 17), fn=(19, 24, 18), hf=(8, 2, 17), hn=(9, 4, 18)),    # fully stretched
    dict(ff=(20, 22, 18), fn=(19, 20, 18), hf=(8, 6, 18), hn=(9, 8, 18)),    # gathering
    dict(ff=(20, 15, 17), fn=(19, 14, 18), hf=(8, 14, 17), hn=(9, 12, 18)),  # tucked under
    dict(ff=(20, 22, 18), fn=(19, 20, 18), hf=(8, 10, 18), hn=(9, 8, 18)),   # pushing off
]
TAIL_DY = [0, -1, 0, 1]
BOB = [0, 1, 0, -1]


def jackal(frame, bark):
    g = G()
    dy = BOB[frame]
    gt = GAIT[frame]
    # far legs (darker)
    for (hx, fx, fy), c in ((gt['ff'], 'a'), (gt['hf'], 'a')):
        g.line(hx, 11 + dy, fx, fy, c, 2)
        g.px(fx, fy, 'D'); g.px(fx + 1, fy, 'D')
    # tail (bushy, trails behind)
    ty = TAIL_DY[frame]
    g.ell(3.5, 8 + ty, 3.6, 2.2, 'A')
    g.rect(0, 7 + ty, 2, 9 + ty, 'D')
    g.px(1, 8 + ty, 'D')
    # body
    g.ell(13, 9 + dy, 8.6, 3.5, 'A')
    g.ell(19.5, 9 + dy, 3.6, 3.9, 'A')            # chest
    g.rect(7, 6 + dy, 20, 7 + dy, 'D')            # dark saddle
    g.rect(9, 5 + dy, 17, 5 + dy, 'D')
    g.px(11, 7 + dy, 'A'); g.px(15, 7 + dy, 'A'); g.px(13, 6 + dy, 'A')
    g.rect(8, 11 + dy, 20, 12 + dy, 'S')          # cream belly
    g.rect(21, 10 + dy, 22, 12 + dy, 'S')
    # neck + head
    g.ell(22, 6 + dy, 2.6, 3.2, 'A')
    g.ell(24.5, 5 + dy, 3.3, 2.7, 'A')
    # snout
    g.rect(26, 5 + dy, 31, 6 + dy, 'A')
    g.rect(26, 7 + dy, 30, 7 + dy, 'S')
    if bark:
        # jaw dropped: dark mouth, tongue, teeth
        g.rect(26, 7 + dy, 31, 8 + dy, 'R')
        g.rect(26, 9 + dy, 30, 9 + dy, 'S')
        g.rect(27, 8 + dy, 29, 8 + dy, 'P')
        g.px(27, 7 + dy, 'W'); g.px(30, 7 + dy, 'W'); g.px(28, 9 + dy, 'W')
    g.px(32, 5 + dy, 'B'); g.px(32, 6 + dy, 'B')   # nose
    # ears (tall, pointed)
    for (x, y) in ((22, 3), (22, 2), (22, 1), (23, 0), (23, 1), (23, 2), (23, 3), (24, 1), (24, 2), (24, 3), (24, 4), (21, 3), (21, 4)):
        g.px(x, y + dy, 'A')
    g.px(23, 1 + dy, 'P'); g.px(23, 2 + dy, 'P'); g.px(23, 3 + dy, 'P')
    g.px(26, 2 + dy, 'a'); g.px(26, 3 + dy, 'a'); g.px(25, 3 + dy, 'a'); g.px(26, 1 + dy, 'a')
    # eye
    g.px(26, 4 + dy, 'E'); g.px(27, 4 + dy, 'B')
    # near legs (lighter, on top)
    for (hx, fx, fy), c in ((gt['fn'], 'A'), (gt['hn'], 'A')):
        g.line(hx, 11 + dy, fx, fy, c, 2)
        g.px(fx, fy, 'D'); g.px(fx + 1, fy, 'D')
    return g


SC = 8
frames = [[jackal(f, b).rows() for f in range(4)] for b in (0, 1)]
json.dump({'frames': frames, 'pals': PALS}, open(os.path.join(DIR, 'jackals.json'), 'w'))

img = Image.new('RGB', (4 * (W * SC + 12) + 12, 2 * (H * SC + 12) + 12 + 3 * 0), (239, 230, 211))
def paint(rows, pal, ox, oy):
    # 1px outline like buildSprite(..., '#1a141a')
    filled = lambda x, y: 0 <= y < H and 0 <= x < W and rows[y][x] in pal
    for y in range(-1, H + 1):
        for x in range(-1, W + 1):
            if filled(x, y):
                continue
            if any(filled(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                img.paste((26, 20, 26), (ox + x * SC, oy + y * SC, ox + x * SC + SC, oy + y * SC + SC))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c in pal:
                col = tuple(int(pal[c][j:j + 2], 16) for j in (1, 3, 5))
                img.paste(col, (ox + x * SC, oy + y * SC, ox + x * SC + SC, oy + y * SC + SC))
for b in range(2):
    for f in range(4):
        paint(frames[b][f], PALS['gold' if b == 0 else 'grey'], 12 + f * (W * SC + 12), 12 + b * (H * SC + 12))
img.save(os.path.join(DIR, 'jackals.png'))
print('wrote jackals.json, jackals.png')
