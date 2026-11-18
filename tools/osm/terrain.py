import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import json, math, numpy as np
d=json.load(open('coast.json')); g=json.load(open('geo.json'))
lat0,lon0=22.6125,120.287
kx=111320*math.cos(math.radians(lat0)); ky=110540
def en(lat,lon): return np.array([(lon-lon0)*kx,(lat-lat0)*ky])
segs=[]
for e in d['elements']:
    pts=[en(p['lat'],p['lon']) for p in e['geometry']]
    for a,b in zip(pts,pts[1:]): segs.append((a,b))
A=np.array([s[0] for s in segs]); B=np.array([s[1] for s in segs])
T=en(22.611011,120.2935352)                  # 旅運中心
# nearest coastline segment to the terminal = our quay
def nearest(P):
    AB=B-A; t=np.clip(((P-A)*AB).sum(1)/(AB*AB).sum(1),0,1); C=A+AB*t[:,None]; dd=np.linalg.norm(C-P,axis=1); i=dd.argmin(); return i,C[i],t[i]
i,C,_=nearest(T)
dvec=(B[i]-A[i]); dvec/=np.linalg.norm(dvec)
water=np.array([dvec[1],-dvec[0]])           # right of way direction = water (OSM: land on the left)
S=10.0                                        # metres per scene unit
O=C+water*46                                  # ark centre line sits 46 m off the quay edge
def scene(P): r=P-O; return [round(float(r@dvec)/S,2), round(float(r@water)/S,2)]
print('quay dir (E,N)',dvec,'angle deg',math.degrees(math.atan2(dvec[1],dvec[0])))
# land mask on a grid in scene units
xs=np.arange(-380,231,2.0); zs=np.arange(-220,181,2.0)
X,Z=np.meshgrid(xs,zs)
P=O+X[...,None]*S*dvec+Z[...,None]*S*water   # (nz,nx,2)
Pf=P.reshape(-1,2)
AB=B-A; L2=(AB*AB).sum(1)
land=np.zeros(len(Pf),bool)
for k in range(0,len(Pf),4000):
    Q=Pf[k:k+4000][:,None,:]
    t=np.clip(((Q-A)*AB).sum(2)/L2,0,1); Cc=A+AB*t[...,None]; dist=np.linalg.norm(Cc-Q,axis=2); j=dist.argmin(1)
    ab=AB[j]; aq=Pf[k:k+4000]-A[j]; cross=ab[:,0]*aq[:,1]-ab[:,1]*aq[:,0]
    land[k:k+4000]=cross>0
mask=land.reshape(Z.shape)
# keep only water connected to the harbour (stray inland "water" far from any coastline becomes land)
from collections import deque as _dq
_nz,_nx=mask.shape; seen=np.zeros(mask.shape,bool)
_s=(int(round((2-zs[0])/2)), int(round((0-xs[0])/2))); _q=_dq([_s]); seen[_s]=True
while _q:
    _a,_b=_q.popleft()
    for _da,_db in ((1,0),(-1,0),(0,1),(0,-1)):
        _u,_v=_a+_da,_b+_db
        if 0<=_u<_nz and 0<=_v<_nx and not seen[_u,_v] and not mask[_u,_v]: seen[_u,_v]=True; _q.append((_u,_v))
mask=~seen
# drop tiny islets (a few cells) that would look like boxes floating in the water
_lab=np.zeros(mask.shape,int); _id=0
for _a in range(_nz):
    for _b in range(_nx):
        if mask[_a,_b] and not _lab[_a,_b]:
            _id+=1; _cells=[(_a,_b)]; _lab[_a,_b]=_id; _k=0
            while _k<len(_cells):
                _u0,_v0=_cells[_k]; _k+=1
                for _da,_db in ((1,0),(-1,0),(0,1),(0,-1)):
                    _u,_v=_u0+_da,_v0+_db
                    if 0<=_u<_nz and 0<=_v<_nx and mask[_u,_v] and not _lab[_u,_v]: _lab[_u,_v]=_id; _cells.append((_u,_v))
            if len(_cells)<6:
                for _u,_v in _cells: mask[_u,_v]=False
print('grid',mask.shape,'land frac',mask.mean().round(3))
rows=[''.join('1' if v else '0' for v in r) for r in mask]
names={'高雄流行音樂中心':'kmc','真愛碼頭':'zhenai','光榮碼頭':'guangrong','高雄85大樓':'t85','高雄市立圖書館總館':'library','高雄展覽館':'expo','駁二藝術特區':'pier2','大港橋':'dagang','壽山':'shoushan','旗後燈塔':'lighthouse','棧貳庫':'kw2','中鋼大樓':'csc','新光碼頭':'xinguang','夢時代購物中心':'dream','高雄軟體園區':'ksp','旗津':'cijin','哈瑪星':'hamasen'}
pts={}
for k,v in g.items():
    if k in names and v and not isinstance(v,str): pts[names[k]]=scene(en(v[0],v[1]))
pts['terminal']=scene(T)
# harbour exit route: BFS through water with clearance from land
from collections import deque
nz,nx=mask.shape
dist=np.full(mask.shape,10**9); q=deque()
for a in range(nz):
    for b in range(nx):
        if mask[a,b]: dist[a,b]=0; q.append((a,b))
while q:
    a,b=q.popleft()
    for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
        u,v=a+da,b+db
        if 0<=u<nz and 0<=v<nx and dist[u,v]>dist[a,b]+1: dist[u,v]=dist[a,b]+1; q.append((u,v))
def cell(x,z): return (int(round((z-zs[0])/2)), int(round((x-xs[0])/2)))
start=cell(0,2); prev={start:None}; q=deque([start]); goal=None
while q:
    a,b=q.popleft()
    if b<=2: goal=(a,b); break
    for da,db in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
        u,v=a+da,b+db
        if 0<=u<nz and 0<=v<nx and (u,v) not in prev and not mask[u,v] and dist[u,v]>=4: prev[(u,v)]=(a,b); q.append((u,v))
path=[]
c=goal
while c: path.append(c); c=prev[c]
path=path[::-1]
print('path cells',len(path),'goal',goal)
route=[[float(xs[b]),float(zs[a])] for a,b in path[::6]]+[[float(xs[path[-1][1]])-60,float(zs[path[-1][0]])]]
json.dump({'grid':{'x0':-380,'z0':-220,'step':2,'nx':len(xs),'nz':len(zs),'rows':rows},'pts':pts,'route':route,'quayAngle':math.degrees(math.atan2(dvec[1],dvec[0]))},open('harbor-data.json','w'),ensure_ascii=False)
for k,v in pts.items(): print(k,v)
print('route',route)

# debug overlay: land cells on the coastline map (5 m/px, north up)
W,Hh=1400,1100; cx,cy=W/2,Hh/2
sv=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" style="background:#cfe3f0">']
for a in range(0,mask.shape[0],2):
    for b in range(0,mask.shape[1],2):
        if mask[a,b]:
            p=O+xs[b]*S*dvec+zs[a]*S*water
            sv.append(f'<rect x="{cx+p[0]/5-2:.0f}" y="{cy-p[1]/5-2:.0f}" width="4" height="4" fill="#9a9" />')
for e in d['elements']:
    pp=' '.join(f'{cx+en(p["lat"],p["lon"])[0]/5:.1f},{cy-en(p["lat"],p["lon"])[1]/5:.1f}' for p in e['geometry'])
    sv.append(f'<polyline points="{pp}" fill="none" stroke="#c00" stroke-width="1.5"/>')
for (x,z) in route:
    p=O+x*S*dvec+z*S*water; sv.append(f'<circle cx="{cx+p[0]/5:.0f}" cy="{cy-p[1]/5:.0f}" r="4" fill="#00f"/>')
p=O; sv.append(f'<circle cx="{cx+p[0]/5:.0f}" cy="{cy-p[1]/5:.0f}" r="7" fill="#f80"/>')
sv.append('</svg>'); open('mask-debug.svg','w').write('\n'.join(sv))

# write the compact map used by the page
def _rle(r):
    out=[];c=r[0];n=0
    for ch in r:
        if ch==c: n+=1
        else: out.append(n); c=ch; n=1
    out.append(n); return (int(r[0]), out)
_g=json.load(open('harbor-data.json'))
_data={'x0':_g['grid']['x0'],'z0':_g['grid']['z0'],'step':_g['grid']['step'],'nx':_g['grid']['nx'],'nz':_g['grid']['nz'],'rows':[_rle(r) for r in _g['grid']['rows']],'route':_g['route']}
open('../../docs/harbor-data.js','w').write('/* 高雄港岸線（OpenStreetMap 海岸線資料，© OpenStreetMap contributors，ODbL）\n   轉成方舟場景座標：1 單位 = 10 公尺，x 沿旅運中心碼頭方向（東南東），z 朝港內水面。 */\nwindow.ARK_HARBOR = '+json.dumps(_data,separators=(',',':'))+';\n')
print('wrote docs/harbor-data.js')
