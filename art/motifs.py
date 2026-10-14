import json
from PIL import Image
M={}
M['pavilion']=["....XXXX....","..XXXXXXXX..",".XXXXXXXXXX.","XXXXXXXXXXXX","............","X.X.X..X.X.X","X.X.X..X.X.X","X.X.X..X.X.X","X.X.X..X.X.X","XXXXXXXXXXXX","............","............"]
M['mic']=["....XXXX....","...X.XX.X...","...XX..XX...","...X.XX.X...","....XXXX....",".....XX.....",".....XX.....",".....XX.....",".....XX.....","....XXXX....","...XXXXXX...","............"]
M['tower']=[".....XX.....","....XXXX....","....X..X....","....XXXX....","...XXXXXX...","...X.XX.X...","...XXXXXX...","...X.XX.X...","..XXXXXXXX..","..X.XX.X.X..","..XXXXXXXX..","XXXXXXXXXXXX"]
M['lion']=["..XXXX......",".XX..XX.....","XX.X..XX....","X......X....","XX.XX.XX....",".XXXXXXXXXX.","...XXXXXXXXX","...XX....XX.","...XX....XX.","..XXX...XXX.","............","............"]
M['crown']=["............","X....X....X.","XX..XXX..XX.","XXXXXXXXXXX.","X.X.X.X.X.X.","XXXXXXXXXXX.","XXXXXXXXXXX.","............","...X.X.X....","....X.X.....","............","............"]
M['shield']=["XXXXXXXXXXX.","X.........X.","X..X.X.X..X.","X..X.X.X..X.","X..XXXXX..X.","X....X....X.",".X...X...X..",".X.......X..","..X.....X...","...X...X....","....XXX.....","............"]
M['helmet']=["............","....XXXX....","..XXXXXXXX..",".XXXXXXXXXX.",".XX.XX.XXXX.","XXXXXXXXXXXX","XXXXXXXXXXXX","X..........X","............","............","............","............"]
M['headph']=["...XXXXXX...","..X......X..",".X........X.",".X........X.","XX........XX","XXX......XXX","XXX......XXX","XXX......XXX",".X........X.","............","............","............"]
M['candle']=[".....X......","....XXX.....","....XXX.....",".....X......","....XXXX....","....X.XX....","....XXXX....","....XXXX....","....X.XX....","....XXXX....","..XXXXXXXX..","............"]
M['chestnut']=["....X.X.....","...XX.XX....","X.XXX.XXX.X.","XXXXX.XXXXX.",".XXXX.XXXX..","..XXX.XXX...","XX..X.X..XX.","XXXX...XXXX.",".XXXX.XXXX..","....XXX.....",".....X......",".....X......"]
M['ship']=[".....X......",".....XX.....",".....XXX....",".....XXXX...",".....XXXXX..",".....X......","XXXXXXXXXXXX",".XXXXXXXXXX.","..XXXXXXXX..","............","XX.XX.XX.XX.","............"]
M['ticket']=["............","XXXXXXXXXXXX","X....X.....X","X.XX.X.XXX.X","X....X.....X","X.XX.X.XX..X","X....X.....X","XXXXXXXXXXXX","............","............","............","............"]
M['spot']=["XX..........","XXX.........","XXXX........",".XXXX.......","..XXXX......","...X..X.....","...X...X....","....X...X...",".....X...X..","......X...X.",".......XXXX.","............"]
M['star']=[".....X......",".....X......","....XXX.....","XXXXXXXXXXX.",".XXXXXXXXX..","..XXXXXXX...","..XXXXXXX...",".XXX...XXX..",".XX.....XX..","............","............","............"]
for k,v in M.items():
    for r in v:assert len(r)==12,(k,r)
json.dump(M,open('motifs.json','w'))
s=8;img=Image.new('RGB',(len(M)*110,120),(239,230,211))
for i,(k,v) in enumerate(M.items()):
    for y,r in enumerate(v):
        for x,c in enumerate(r):
            if c=='X':img.paste((150,110,80),(10+i*110+x*s,10+y*s,10+i*110+x*s+s,10+y*s+s))
img.save('motifs.png')
