"""Піксельні «лукалайки» хейтерів: stuk, koms, threads, cancel.
Намальовані вручну на низькій сітці (фігури, не фото), потім x2 nearest → art/faces/<id>.png.
Схожість лише в ключових рисах (волосся, борода, навушники, каре); облич реальних людей тут немає.
Запуск: python3 art/faces.py  (з кореня репозиторію; PNG перезаписуються)."""
from PIL import Image, ImageDraw
import os, sys

SCALE = 2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'faces')


def hx(s):
    s = s.lstrip('#')
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


class Canvas:
    def __init__(self, w, h):
        self.im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.w, self.h = w, h

    def ell(self, x0, y0, x1, y1, c):
        self.d.ellipse([x0, y0, x1, y1], fill=hx(c))

    def rect(self, x0, y0, x1, y1, c):
        self.d.rectangle([x0, y0, x1, y1], fill=hx(c))

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.im.putpixel((x, y), hx(c))

    def pts(self, lst, c):
        for x, y in lst:
            self.px(x, y, c)

    def clip(self, x0, y0, x1, y1):
        """Прибрати все поза прямокутником (для обрізання волосся/бороди)."""
        m = Image.new('L', (self.w, self.h), 0)
        ImageDraw.Draw(m).rectangle([x0, y0, x1, y1], fill=255)
        a = self.im.getchannel('A')
        from PIL import ImageChops
        self.im.putalpha(ImageChops.multiply(a, m))

    def save(self, name):
        big = self.im.resize((self.w * SCALE, self.h * SCALE), Image.NEAREST)
        big.save(os.path.join(OUT, name + '.png'), optimize=True)
        return big


def stuk():
    c = Canvas(22, 34)
    skin, shade, hair, beard = '#e6b690', '#cf9a74', '#5a3a22', '#3b2418'
    c.ell(2, 11, 3, 18, skin); c.ell(18, 11, 19, 18, skin)             # вуха
    c.ell(3, 3, 18, 31, skin)                                            # обличчя
    # борода по щелепі: нижня частина овалу, крім рота
    b = Canvas(22, 34); b.ell(3, 3, 18, 31, beard); b.clip(0, 21, 22, 34)
    c.im.alpha_composite(b.im)
    c.rect(8, 24, 13, 26, skin)                                          # просвіт рота
    c.rect(9, 25, 12, 25, '#8a3d3a')                                     # губи
    c.rect(7, 22, 14, 23, beard)                                         # вуса
    c.pts([(5, 21), (16, 21), (4, 20), (17, 20)], beard)                 # бакенбарди
    # волосся: шапка + чубчик
    h = Canvas(22, 34); h.ell(2, 1, 19, 17, hair); h.clip(0, 0, 22, 11)
    c.im.alpha_composite(h.im)
    c.rect(2, 8, 4, 14, hair); c.rect(17, 8, 19, 14, hair)               # скроні
    c.rect(5, 10, 16, 11, hair)
    # очі, брови, ніс
    c.rect(6, 12, 9, 12, '#2a1a10'); c.rect(12, 12, 15, 12, '#2a1a10')   # брови
    c.rect(7, 14, 8, 14, '#ffffff'); c.rect(13, 14, 14, 14, '#ffffff')
    c.px(8, 14, '#3d2a1c'); c.px(14, 14, '#3d2a1c')
    c.rect(7, 15, 8, 15, shade); c.rect(13, 15, 14, 15, shade)           # повіки
    c.rect(10, 16, 11, 20, shade)                                        # ніс
    c.pts([(9, 20), (12, 20)], '#b98466')
    return c.save('stuk')


def koms():
    c = Canvas(24, 36)
    skin, shade, hair, stub = '#e0ad88', '#c58f6a', '#6b4a2a', '#8a6a52'
    c.ell(3, 13, 4, 20, skin); c.ell(19, 13, 20, 20, skin)
    c.ell(4, 6, 19, 33, skin)
    # щетина: шахова розкладка по щелепі
    for y in range(24, 33):
        for x in range(5, 19):
            if (x + y) % 2 == 0 and ((x - 11.5) ** 2) / 49 + ((y - 14) ** 2) / 380 < 1:
                c.px(x, y, stub)
    # кучеряве волосся: купол + «кучері» по краю
    h = Canvas(24, 36); h.ell(2, 1, 21, 17, hair); h.clip(0, 0, 24, 11)
    c.im.alpha_composite(h.im)
    c.pts([(3, 6), (2, 8), (4, 5), (6, 3), (9, 1), (13, 1), (16, 2), (19, 4), (21, 7), (20, 5)], hair)
    for x in range(6, 18, 2):
        c.px(x, 0 + (x % 4 == 0), '#4f3519')
    c.rect(5, 9, 18, 11, hair); c.rect(3, 9, 5, 14, hair); c.rect(18, 9, 20, 14, hair)
    c.pts([(8, 10), (11, 10), (14, 10)], '#8a6a3c')                      # відблиски
    # навушники
    c.rect(2, 4, 3, 12, '#1d1d22'); c.rect(20, 4, 21, 12, '#1d1d22')
    c.rect(1, 12, 4, 19, '#26262c'); c.rect(19, 12, 22, 19, '#26262c')
    c.rect(2, 1, 21, 2, '#1d1d22')
    # брови (одна вище), очі: праве примружене
    c.rect(7, 13, 10, 13, '#3b2a1a'); c.rect(14, 12, 17, 12, '#3b2a1a')
    c.rect(7, 16, 10, 16, '#ffffff'); c.px(9, 16, '#3a2a1c')
    c.rect(14, 16, 17, 16, '#2a1a10')                                    # примружене око
    c.rect(11, 17, 13, 22, shade)                                        # ніс
    # губи «качечкою»
    c.rect(9, 26, 14, 28, '#d98a85'); c.rect(10, 27, 13, 27, '#a8524f')
    return c.save('koms')


def threads():
    c = Canvas(29, 35)
    skin, shade, hair, hl = '#f1c6a3', '#dba482', '#e2bd78', '#f4dca0'
    # каре: гладкий блок волосся до підборіддя
    c.ell(3, 1, 25, 28, hair); c.rect(3, 14, 25, 27, hair)
    c.ell(7, 6, 21, 31, skin)                                            # обличчя
    c.rect(3, 12, 7, 27, hair); c.rect(21, 12, 25, 27, hair)             # пасма по боках
    # чубчик набік
    h = Canvas(29, 35); h.ell(3, 1, 25, 21, hair); h.clip(0, 0, 29, 12)
    c.im.alpha_composite(h.im)
    c.rect(9, 11, 20, 12, hair); c.pts([(8, 13), (9, 13), (8, 14), (21, 13)], hair)
    c.rect(10, 13, 11, 13, hair)
    for (x, y) in [(9, 3), (10, 3), (16, 2), (17, 2), (5, 18), (5, 19), (23, 18), (23, 19), (7, 7)]:
        c.px(x, y, hl)
    # очі, брови, ніс, губи
    c.rect(9, 14, 12, 14, '#8a6a42'); c.rect(16, 14, 19, 14, '#8a6a42')
    c.rect(10, 16, 12, 16, '#ffffff'); c.rect(16, 16, 18, 16, '#ffffff')
    c.px(11, 16, '#4aa0a8'); c.px(17, 16, '#4aa0a8')
    c.rect(10, 17, 12, 17, shade); c.rect(16, 17, 18, 17, shade)
    c.rect(14, 18, 14, 22, shade); c.pts([(13, 23), (15, 23)], '#c48a68')
    c.rect(11, 26, 17, 27, '#e08a8c'); c.rect(12, 27, 16, 27, '#c4666d')
    return c.save('threads')


def cancel():
    c = Canvas(25, 34)
    skin, shade, hair = '#f0cdb6', '#d8ae94', '#b9a07c'
    c.ell(2, 12, 3, 19, skin); c.ell(21, 12, 22, 19, skin)
    c.ell(3, 5, 21, 32, skin)
    # коротка світло-русява стрижка, лінія росту рівна
    h = Canvas(25, 34); h.ell(2, 1, 22, 17, hair); h.clip(0, 0, 25, 9)
    c.im.alpha_composite(h.im)
    c.rect(3, 7, 5, 11, hair); c.rect(19, 7, 21, 11, hair)
    c.rect(6, 8, 18, 8, hair)
    c.pts([(10, 2), (11, 2), (15, 3), (8, 4), (17, 4)], '#d2bf9a')
    c.rect(7, 11, 10, 11, '#a08a68'); c.rect(14, 11, 17, 11, '#a08a68')  # брови
    c.rect(7, 13, 10, 13, '#ffffff'); c.rect(14, 13, 17, 13, '#ffffff')
    c.px(8, 13, '#5a7a96'); c.px(15, 13, '#5a7a96')
    c.rect(7, 14, 10, 14, shade); c.rect(14, 14, 17, 14, shade)
    c.rect(11, 15, 13, 21, shade)                                        # ніс
    c.rect(9, 25, 15, 26, '#cf8f88'); c.rect(9, 26, 15, 26, '#b0706c')   # нейтральний рот
    return c.save('cancel')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    outs = [f() for f in (stuk, koms, threads, cancel)]
    if len(sys.argv) > 1:   # контактний лист: python3 art/faces.py sheet.png
        W = sum(o.width * 3 for o in outs) + 30
        sheet = Image.new('RGB', (W, 330), (120, 160, 200))
        x = 10
        for o in outs:
            g = o.resize((o.width * 3, o.height * 3), Image.NEAREST)
            sheet.paste(g, (x, 10), g)
            x += g.width + 10
        sheet.save(sys.argv[1])
