from PIL import Image
import json,math
W,H=20,26
PAL={'K':'#1e1820','F':'#f3c6a0','f':'#d99c72','p':'#f08f86','W':'#ffffff',
'H':'#4a4a55','h':'#22222a','C':'#c9a46a','c':'#9c7a44','P':'#fbfbf2','L':'#8aa0c8','n':'#3b3b46',
'A':'#5a3a22','T':'#d9302c','t':'#9e1b1b','S':'#f4f4ee','s':'#c4c8d0','M':'#f0b93a','m':'#b07d16','N':'#2c3a66',
'B':'#2a2320','G':'#59606c','R':'#d63434','r':'#8f1c1c','D':'#5e6675','d':'#3f4552','Y':'#a8743e',
'O':'#ecc062','o':'#b98a2c','V':'#c22a3a','Q':'#c0303a','X':'#2a9a8c','x':'#1b6660','Z':'#9a9aa4','U':'#9a6a3a',
'J':'#2b6fd6','j':'#1b4a99','I':'#2c2c36','i':'#17171d','E':'#3a3a44','e':'#7cd2ff'}
class G:
    def __init__(s):s.g=[['.']*W for _ in range(H)]
    def px(s,x,y,c):
        if 0<=x<W and 0<=y<H:s.g[y][x]=c
    def rect(s,x0,y0,x1,y1,c):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):s.px(x,y,c)
    def ell(s,cx,cy,rx,ry,c,shade=None,sx=.45):
        for y in range(H):
            for x in range(W):
                if ((x+.5-cx)/rx)**2+((y+.5-cy)/ry)**2<=1:
                    s.px(x,y,shade if shade and (x+.5-cx)>rx*sx else c)
    def get(s,x,y):return s.g[y][x] if 0<=x<W and 0<=y<H else '.'
    def outline(s):
        add=[]
        for y in range(H):
            for x in range(W):
                if s.g[y][x]=='.' and any(s.get(x+dx,y+dy) not in '.K' for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):add.append((x,y))
        for x,y in add:s.g[y][x]='K'
    def rows(s):return [''.join(r) for r in s.g]
def face(g,eyes='norm',mouth='grin',cx=10,ey=8,brows='angry'):
    # eyes
    for ex in (cx-3,cx+2):
        if eyes=='shifty':g.px(ex,ey,'W');g.px(ex+1,ey,'K')
        elif eyes=='squint':g.px(ex,ey,'K');g.px(ex+1,ey,'K')
        else:g.px(ex,ey,'W');g.px(ex,ey+1,'K');g.px(ex+1,ey,'K');g.px(ex+1,ey+1,'K')
    if brows=='angry':g.px(cx-4,ey-2,'K');g.px(cx-3,ey-1,'K');g.px(cx+4,ey-2,'K');g.px(cx+3,ey-1,'K')
    if brows=='raised':g.rect(cx-4,ey-2,cx-3,ey-2,'K');g.rect(cx+2,ey-2,cx+3,ey-2,'K')
    g.px(cx-5,ey+2,'p');g.px(cx+5,ey+2,'p')
    my=ey+4
    if mouth=='grin':g.rect(cx-2,my,cx+1,my,'K');g.px(cx+2,my-1,'K')
    if mouth=='shout':g.rect(cx-2,my-1,cx+1,my+1,'K');g.rect(cx-1,my,cx,my+1,'T')
    if mouth=='flat':g.rect(cx-2,my,cx+1,my,'K')
    if mouth=='smirk':g.rect(cx-1,my,cx+2,my,'K');g.px(cx-2,my-1,'K')
def head(g,cy=8):g.ell(10,cy,6.6,6.2,'F','f',.68)
def legs(g,col):g.rect(6,23,8,24,col);g.rect(11,23,13,24,col);g.rect(5,25,8,25,'K');g.rect(11,25,14,25,'K')

def stuk():
    g=G();head(g)
    g.ell(10,3.2,6,3,'H','H');g.rect(4,4,15,4,'h');g.rect(2,5,17,5,'H')
    face(g,eyes='shifty',mouth='smirk',ey=8,brows='angry')
    g.ell(10,18.5,6.5,5.5,'C','c',.4);g.rect(9,14,10,22,'c');g.rect(8,14,11,15,'S')
    g.rect(14,15,18,20,'P');g.rect(15,16,17,16,'L');g.rect(15,18,17,18,'L');g.px(13,17,'F');g.px(13,18,'F')
    legs(g,'n');g.outline();return g
def koms():
    g=G();head(g)
    g.ell(10,3,6.6,3,'A','A');g.rect(4,2,16,4,'A');g.px(15,5,'A');g.px(4,5,'A')
    face(g,mouth='shout',brows='angry')
    g.ell(10,19,6,5,'S','s',.4);g.rect(8,15,12,15,'T');g.rect(9,16,11,17,'T');g.px(10,18,'t')
    g.rect(15,15,18,19,'M');g.rect(17,14,19,20,'M');g.rect(17,18,19,20,'m');g.px(14,17,'F')
    legs(g,'N');g.outline();return g
def cancel():
    g=G();head(g)
    g.ell(10,3.4,6.2,2.8,'B','B');g.rect(4,3,16,4,'B')
    g.rect(3,6,3,10,'G');g.rect(16,6,16,10,'G');g.rect(4,2,15,2,'G');g.px(3,4,'G');g.px(3,5,'G');g.px(16,4,'G');g.px(16,5,'G')
    g.rect(14,11,15,11,'G');g.px(13,12,'K')
    face(g,mouth='flat',brows='angry')
    g.ell(10,19,6.2,5,'D','d',.4);g.rect(9,14,10,22,'d');g.rect(8,14,11,14,'S')
    g.rect(15,12,16,17,'Y');g.rect(13,18,19,21,'R');g.rect(13,21,19,21,'r');g.px(14,15,'F');g.px(14,16,'F')
    legs(g,'d');g.outline();return g
def lang():
    g=G();head(g)
    g.ell(10,1.8,3,2.2,'O','o');g.ell(10,4.5,7,3.3,'O','o',.5);g.rect(3,5,4,11,'O');g.rect(16,5,16,11,'o')
    face(g,mouth='shout',brows='raised')
    for ex in (6,11):g.rect(ex,7,ex+3,7,'V');g.px(ex,8,'V');g.px(ex+3,8,'V');g.px(ex,9,'V');g.px(ex+3,9,'V');g.rect(ex,10,ex+3,10,'V')
    g.ell(10,19.3,6.6,5,'X','x',.4);g.rect(9,14,11,15,'S')
    g.rect(1,15,4,19,'U');g.rect(2,16,4,19,'P');g.rect(2,15,3,15,'Z');g.px(5,17,'F')
    g.rect(15,13,16,15,'F');g.px(16,12,'F')
    legs(g,'x');g.outline();return g
def threads():
    g=G();head(g)
    g.ell(10,3.5,7,3.2,'J','j',.5);g.rect(3,5,16,5,'J');g.rect(14,5,18,5,'j')
    face(g,eyes='squint',mouth='smirk',brows='none')
    g.ell(10,19.2,6.8,5.2,'I','i',.4);g.rect(7,14,13,14,'I');g.px(8,15,'W');g.px(12,15,'W')
    g.rect(14,15,17,20,'E');g.rect(15,16,16,19,'e');g.px(13,17,'F');g.px(13,18,'F')
    g.rect(9,17,11,17,'W');g.px(8,18,'W');g.px(12,18,'W');g.px(10,18,'e');g.rect(9,19,11,19,'W');g.px(12,19,'W')
    legs(g,'i');g.outline();return g
S={'stuk':stuk(),'koms':koms(),'cancel':cancel(),'lang':lang(),'threads':threads()}
s=10;img=Image.new('RGB',(len(S)*(W*s+20)+20,H*s+40),(239,230,211))
for i,(k,g) in enumerate(S.items()):
    for y,r in enumerate(g.rows()):
        for x,c in enumerate(r):
            if c!='.':img.paste(PAL[c],(20+i*(W*s+20)+x*s,20+y*s,20+i*(W*s+20)+x*s+s,20+y*s+s))
img.save('/tmp/claude-0/art/enemies.png')
json.dump({k:g.rows() for k,g in S.items()},open('/tmp/claude-0/art/enemies.json','w'))
json.dump(PAL,open('/tmp/claude-0/art/pal.json','w'))
