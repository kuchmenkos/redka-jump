import json
from PIL import Image
def mk(w,h):return [['.']*w for _ in range(h)]
def R(g,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if 0<=y<len(g) and 0<=x<len(g[0]):g[y][x]=c
def outline(g):
    h,w=len(g),len(g[0]);add=[]
    for y in range(h):
        for x in range(w):
            if g[y][x]=='.' and any(0<=y+dy<h and 0<=x+dx<w and g[y+dy][x+dx] not in '.K' for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):add.append((x,y))
    for x,y in add:g[y][x]='K'
rows=lambda g:[''.join(r) for r in g]
# rocket 12x19
r=mk(12,19)
R(r,5,0,6,0,'R');R(r,4,1,7,2,'R');R(r,3,3,8,11,'W');R(r,7,3,8,11,'w');R(r,4,5,7,8,'B');R(r,5,5,6,6,'b')
R(r,4,9,7,9,'R');R(r,1,10,2,14,'R');R(r,9,10,10,14,'R');R(r,3,12,8,14,'R');R(r,4,15,7,15,'K')
R(r,4,16,7,16,'O');R(r,5,17,6,18,'Y')
outline(r)
# train 24x15
t=mk(24,15)
R(t,3,1,7,1,'k');R(t,4,2,6,4,'k');R(t,9,3,11,4,'Y');R(t,9,3,11,3,'Z')
R(t,3,5,15,10,'Y');R(t,3,5,15,5,'Z');R(t,3,6,15,6,'Z');R(t,3,10,15,10,'y');R(t,8,5,8,10,'y');R(t,12,5,12,10,'y')
R(t,14,1,22,1,'k');R(t,15,2,21,10,'Y');R(t,15,2,21,2,'Z');R(t,17,4,19,6,'L');R(t,21,3,21,10,'y')
R(t,0,10,2,11,'k');R(t,1,9,2,9,'k');R(t,2,11,22,11,'k')
for cx in (6,11):R(t,cx-1,12,cx+2,14,'k');R(t,cx,12,cx+1,13,'Z')
R(t,18,12,20,14,'k');R(t,19,12,19,13,'Z')
outline(t)
# envelope 14x10
e=mk(14,10)
R(e,0,0,13,9,'W');R(e,0,9,13,9,'s')
for i in range(6):e[1+i][1+i]='K';e[1+i][12-i]='K'
R(e,6,6,7,7,'R')
outline(e)
# thread bubble 26x12
th=mk(26,12)
R(th,1,0,24,8,'I');R(th,0,1,25,7,'I');R(th,3,9,5,9,'I');R(th,3,10,3,10,'I')
outline(th)
P={'R':'#d63434','W':'#f6f6f0','w':'#c9ccd4','B':'#2b6fd6','b':'#9fd6ff','O':'#ff9a2a','Y':'#ffd23a','K':'#1e1820','Z':'#fff3b0','y':'#a8740f','L':'#7cc4f0','k':'#4a320a','s':'#c9c2b0','I':'#1e1e26','e':'#7cd2ff'}
TP=dict(P);TP['Y']='#e8b524'
out={'ROCKET':rows(r),'TRAIN':rows(t),'ENV':rows(e),'THREAD':rows(th)}
json.dump(out,open('items.json','w'))
s=10;img=Image.new('RGB',(900,220),(239,230,211));ox=20
for k,g in out.items():
    pal=TP if k=='TRAIN' else P
    for y,row in enumerate(g):
        for x,c in enumerate(row):
            if c!='.':img.paste(pal[c],(ox+x*s,20+y*s,ox+x*s+s,20+y*s+s))
    ox+=len(g[0])*s+30
img.save('items.png')
