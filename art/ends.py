"""Collage exact PNG faces onto empty end environments. Felix is always felix-fail."""
from PIL import Image, ImageFilter, ImageChops
import os

DIR = os.path.dirname(os.path.abspath(__file__))
FACE = os.path.join(DIR, 'faces')
EMPTY = os.path.join(DIR, 'ends', '_empty')
OUT = os.path.join(DIR, 'ends')
W, H = 1280, 720


def load_face(name):
    return Image.open(os.path.join(FACE, name + '.png')).convert('RGBA')


def scale_h(im, h):
    r = h / im.height
    return im.resize((max(1, round(im.width * r)), h), Image.Resampling.NEAREST)


def shadow(im, ox=5, oy=7, blur=3, alpha=110):
    a = im.getchannel('A').filter(ImageFilter.MaxFilter(3))
    sh = Image.new('RGBA', (im.width + abs(ox) + blur * 2, im.height + abs(oy) + blur * 2), (0, 0, 0, 0))
    sil = Image.new('RGBA', im.size, (20, 12, 14, alpha))
    sil.putalpha(ImageChops.multiply(a, Image.new('L', im.size, alpha)))
    px, py = blur + max(ox, 0), blur + max(oy, 0)
    sh.paste(sil, (px, py), sil)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    return sh, px, py


def paste(canvas, face, cx, cy, h, rot=0, flip=False):
    im = scale_h(face, h)
    if flip:
        im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if rot:
        # 90°-multiples stay nearest; other angles need bicubic or the pixels smear.
        resample = Image.Resampling.NEAREST if abs(rot) % 90 < 1 else Image.Resampling.BICUBIC
        im = im.rotate(rot, expand=True, resample=resample)
    sh, sx, sy = shadow(im)
    x = int(cx - im.width / 2)
    y = int(cy - im.height / 2)
    canvas.paste(sh, (x - sx, y - sy), sh)
    canvas.paste(im, (x, y), im)
    return canvas


def plate(kind):
    bg = Image.open(os.path.join(EMPTY, kind + '.webp')).convert('RGBA').resize((W, H), Image.Resampling.LANCZOS)
    felix = load_face('felix-fail')
    if kind == 'fall':
        paste(bg, load_face('stuk'), 270, 250, 200)
        paste(bg, load_face('threads'), 640, 228, 210)
        paste(bg, load_face('koms'), 1010, 250, 200)
        paste(bg, felix, 640, 505, 270, rot=180)
    elif kind == 'stuk':
        paste(bg, felix, 380, 390, 340)
        paste(bg, load_face('stuk'), 980, 360, 300)
    elif kind == 'threads':
        paste(bg, felix, 430, 430, 300)
        paste(bg, load_face('threads'), 980, 340, 280, flip=True)
    elif kind == 'koms':
        paste(bg, load_face('koms'), 220, 430, 240)
        paste(bg, felix, 640, 430, 300)
        paste(bg, load_face('koms'), 1060, 430, 240, flip=True)
    elif kind == 'cancel':
        paste(bg, felix, 280, 430, 280)
        paste(bg, load_face('cancel'), 1000, 430, 280, flip=True)
    elif kind == 'lang':
        paste(bg, felix, 980, 400, 320)
    else:
        raise SystemExit('unknown kind ' + kind)
    rgb = Image.new('RGB', (W, H), (248, 241, 227))
    rgb.paste(bg, mask=bg.split()[-1])
    path = os.path.join(OUT, kind + '.webp')
    rgb.save(path, 'WEBP', quality=88, method=6)
    print('wrote', path)


if __name__ == '__main__':
    for k in ('fall', 'stuk', 'threads', 'koms', 'cancel', 'lang'):
        plate(k)
