import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import json, math, re, numpy as np, hashlib
d=json.load(open('coast.json'))
lat0,lon0=22.6125,120.287
kx=111320*math.cos(math.radians(lat0)); ky=110540
def en(lat,lon): return np.array([(lon-lon0)*kx,(lat-lat0)*ky])
segs=[]
for e in d['elements']:
    pts=[en(p['lat'],p['lon']) for p in e['geometry']]
    for a,b in zip(pts,pts[1:]): segs.append((a,b))
A=np.array([s[0] for s in segs]); B=np.array([s[1] for s in segs])
T=en(22.611011,120.2935352)
AB=B-A; t=np.clip(((T-A)*AB).sum(1)/(AB*AB).sum(1),0,1); C=A+AB*t[:,None]; i=np.linalg.norm(C-T,axis=1).argmin()
dvec=AB[i]/np.linalg.norm(AB[i]); water=np.array([dvec[1],-dvec[0]]); O=C[i]+water*46; S=10.0
def scene(lat,lon): r=en(lat,lon)-O; return (float(r@dvec)/S, float(r@water)/S)
b=json.load(open('bldg.json'))['elements']
def num(v):
    m=re.match(r'\s*([\d.]+)',str(v)); return float(m.group(1)) if m else None
out=[]
for e in b:
    t=e.get('tags',{})
    rings=[]
    if e['type']=='way': rings=[e['geometry']]
    else:
        # stitch outer member ways that share end points into closed rings
        segs=[[(q['lat'],q['lon']) for q in m['geometry']] for m in e.get('members',[]) if m.get('role')=='outer' and 'geometry' in m]
        rings=[]
        while segs:
            ring=segs.pop(0)
            changed=True
            while changed and ring[0]!=ring[-1]:
                changed=False
                for k,sg in enumerate(segs):
                    if sg[0]==ring[-1]: ring+=sg[1:]; segs.pop(k); changed=True; break
                    if sg[-1]==ring[-1]: ring+=sg[::-1][1:]; segs.pop(k); changed=True; break
            rings.append([{'lat':a,'lon':b} for a,b in ring])
    for g in rings:
        p=[scene(q['lat'],q['lon']) for q in g]
        if len(p)>1 and p[0]==p[-1]: p=p[:-1]
        if len(p)<3: continue
        out.append({'id':e['id'],'type':e['type'],'name':t.get('name',''),'b':t.get('building',''),'part':t.get('building:part',''),
            'h':num(t['height']) if 'height' in t else None,'mh':num(t['min_height']) if 'min_height' in t else None,
            'lv':num(t['building:levels']) if 'building:levels' in t else None,'roof':t.get('roof:shape',''),'p':p})
json.dump(out,open('bld-scene.json','w'),ensure_ascii=False)
def info(o):
    P=np.array(o['p']); c=P.mean(0); ext=P.max(0)-P.min(0)
    return f"{o['type'][0]}{o['id']} {o['name'][:14]:14s} b={o['b']} part={o['part']} h={o['h']} mh={o['mh']} lv={o['lv']} roof={o['roof']} c=({c[0]:.1f},{c[1]:.1f}) ext=({ext[0]:.1f},{ext[1]:.1f}) n={len(P)}"
for o in out:
    if re.search('85|旅運|流行|海音|音浪|鯨魚|礁|展覽|圖書館總館|中鋼總部|棧貳|駁二', o['name']) or o['part']: print(info(o))
