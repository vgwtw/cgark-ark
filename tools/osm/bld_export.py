import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import json, hashlib, numpy as np
B=json.load(open('bld-scene.json'))
def rnd(i,a,b):
    h=int(hashlib.md5(str(i).encode()).hexdigest()[:8],16)/0xffffffff; return a+(b-a)*h
SKIP={1056803924,1056803925,1056803922,1056803923,1262810681,1262810682,1262810683,1262810684,1262810685,1262810686,1262810687,1267309762,1267309763,1056803928,1056803929,1056803930,1056803931}
T85={34170948,344740871,344740872,344740873,344740874,345038766,345038767}
WH={444746704,444746705,444746706,444746707,444746708,444746709}
out=[]; lms=[]
grid=json.load(open('harbor-data.json'))['grid']; rows=grid['rows']
def land(x,z):
    i=round((z-grid['z0'])/2); j=round((x-grid['x0'])/2)
    return 0<=i<len(rows) and 0<=j<len(rows[0]) and rows[i][j]=='1'
for o in B:
    i=o['id']
    if i in SKIP: continue
    P=np.array(o['p']); c=P.mean(0)
    if not (-380<c[0]<230 and -220<c[1]<180): continue
    t=o['b']; nm=o['name']
    if i in T85: st='t85'
    elif i==668444820: st='term'
    elif i==913343429: st='kmc'
    elif i==660815346: st='reef'
    elif i in WH: st='whale'
    elif i==6464911: st='expo'
    elif i==239754110: st='lib'
    elif i==198038582: st='csc'
    elif i==8211009: st='kw2'
    elif t=='warehouse' and c[0]<-100: st='brick'
    elif t in ('industrial','warehouse','transportation','transporation'): st='ind'
    elif t in ('apartments','residential','hotel','dormitory'): st='apt'
    elif t in ('commercial','office','retail'): st='com'
    else: st='low'
    if st=='expo' and np.ptp(P[:,0])<5: continue
    if st in('apt','com','low','ind','brick') and not land(c[0],c[1]): continue
    if o['h']: h1=o['h']
    elif o['lv']: h1=o['lv']*3.3
    else: h1={'apt':rnd(i,24,60),'com':rnd(i,18,45),'low':rnd(i,8,22),'ind':rnd(i,7,12),'brick':8,'kw2':10,'whale':9,'reef':14,'kmc':0,'term':16,'expo':27,'lib':40,'csc':135}.get(st,12)
    if t in('school','university') and not (o['h'] or o['lv']): h1=16
    h0=o['mh'] or 0
    pts=[round(v,1) for xy in o['p'] for v in xy]
    out.append([st,round(h0,1),round(h1,1),o['roof'][:4]]+pts)
LM=[['高雄港埠旅運中心',12.3,-12],['音浪塔',-77,-64],['高雄流行音樂中心・海音館',-77,-53],['珊瑚礁群',-51,-79],['鯨魚堤岸',-35,-53],['高雄展覽館',60.5,-1.5],['85 大樓',57.9,-47.1],['高雄市立圖書館總館',80.3,-39],['中鋼集團總部大樓',107.6,10.9],['棧貳庫',-190.5,-14],['駁二藝術特區',-156,-50]]
js='/* 高雄港周邊建築（OpenStreetMap 建築外框與高度，© OpenStreetMap contributors，ODbL）。每筆：[樣式, 底高m, 頂高m, 屋頂, x1,z1, x2,z2, ...]，座標同 ARK_HARBOR。 */\nwindow.ARK_BUILDINGS = '+json.dumps({'b':out,'lm':LM},ensure_ascii=False,separators=(',',':'))+';\n'
open('../../docs/harbor-buildings.js','w').write(js)
import collections; print(len(out),'buildings', len(js)//1024,'KB', collections.Counter(b[0] for b in out))
