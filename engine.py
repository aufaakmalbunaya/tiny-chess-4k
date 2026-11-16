import json,os,sys,random,urllib.request as u
ENV=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
_S='````````leWd\\hT[`bbad_\\[`d_b`_`[`c_c`_`\\`c`_a`dZ^d^_aebXc```````````````v`^]a^ebU`_]_`c`Z____`b``___``a``a^a`_a_c_``a^`_a```````Kjg^nLjUddn[_eY]\\n]cbfY]Yc`e^dYa[bb`b^a\\^bc_a`a[^]eb`b\\`Uj\\cb^b__dVeb^f^^e\\`fc[Xdg``_b_[`aad_`\\__c`aa^__`b```a___b`^aba\\\\d^_a`]bga_bbYca^acab^[cYcaa^dbZ[bbb`a[_^aaba^b\\]ca`b`_]^d`aaa^Xg`bb`_Zb_dd^e__aW^da^i]cW`c`cc_aV`a`bb^`_^b`a```^b_a_ab_[cb_aa^``^ab]__^^k_\\[cdbb\\^a`a[acd]^`cbZa``__aa^^f]^_`b^d`_]`bb_ca^Yccc`]f^Wh[g_Ueb`ac^^`d```c^^`aa_`d`\\]d```a_]^bc```^^_bab`__^^bab`^__[cab]b_^'
_V=[];_p=0
for _c in _S:
 _p+=ord(_c)-96;_V.append(_p*8)
MP,EP,MN,MB,MR,MQ,MK,EK=[_V[i*64:(i+1)*64] for i in range(8)]
MV=(0,82,337,365,477,1025,0);WV=(0,94,281,297,512,936,0)
MGT=[0,MP,MN,MB,MR,MQ,MK];EGT=[0,EP,MN,MB,MR,MQ,EK];PHS=(0,0,1,1,2,4,0)
SQ=[r*16+f for r in range(8) for f in range(8)]
KN=(14,18,31,33,-14,-18,-31,-33)
KG=(1,15,16,17,-1,-15,-16,-17)
BD=(15,17,-15,-17)
RD=(1,16,-1,-16)
MATE=100000
LIM=150000
class Abort(Exception):pass
random.seed(88172645463325252)
R=random.getrandbits
Z=[[R(64) for _ in range(128)] for _ in range(13)]
ZS=R(64);ZC=[R(64) for _ in range(16)];ZE=[R(64) for _ in range(8)]
B=[0]*128;SIDE=1;CAST=0;EP=-1;HALF=0;HASH=0;WK=4;BK=116
MG=0;EG=0;PH=0;NP=0
ST=[];HIST={};TT={}
KILL=[[0,0] for _ in range(128)]
NODES=0
def parse(fen):
    global B,SIDE,CAST,EP,HALF,HASH,WK,BK,MG,EG,PH,NP
    p=fen.split()
    B=[0]*128;HASH=0;MG=0;EG=0;PH=0;NP=0
    r=7;f=0
    for c in p[0]:
        if c=='/':r-=1;f=0
        elif c.isdigit():f+=int(c)
        else:
            sq=r*16+f;pc='PNBRQK'.index(c.upper())+1
            if c.islower():pc=-pc
            B[sq]=pc;HASH^=Z[pc+6][sq]
            a=abs(pc);PH+=PHS[a]
            if a==1:NP+=1
            i=(7-r)*8+f if pc>0 else r*8+f
            s=1 if pc>0 else -1
            MG+=s*(MV[a]+MGT[a][i]);EG+=s*(WV[a]+EGT[a][i])
            if pc==6:WK=sq
            elif pc==-6:BK=sq
            f+=1
    SIDE=1 if p[1]=='w' else -1
    CAST=0
    for c in p[2]:CAST|={'K':1,'Q':2,'k':4,'q':8}.get(c,0)
    EP=-1 if p[3]=='-' else (ord(p[3][0])-97)+(int(p[3][1])-1)*16
    HALF=int(p[4]) if len(p)>4 else 0
    HASH^=ZC[CAST]
    if EP>=0:HASH^=ZE[EP&7]
    if SIDE<0:HASH^=ZS
def atk(sq,by):
    if by>0:
        for t in (sq-15,sq-17):
            if not t&0x88 and B[t]==1:return 1
    else:
        for t in (sq+15,sq+17):
            if not t&0x88 and B[t]==-1:return 1
    for o in KN:
        t=sq+o
        if not t&0x88 and B[t]==by*2:return 1
    for o in KG:
        t=sq+o
        if not t&0x88 and B[t]==by*6:return 1
    for o in (1,16,-1,-16,15,17,-15,-17):
        d=4 if abs(o) in (1,16) else 3
        t=sq+o
        while not t&0x88:
            pc=B[t]
            if pc:
                if pc==by*d or pc==by*5:return 1
                break
            t+=o
    return 0
def mk(f,t,p=0,fl=0):return f|t<<7|p<<14|fl<<17
def gen(cap_only=0):
    ms=[]
    def pm(o):
        for pr in (5,4,3,2):ms.append(mk(sq,o,pr))
    for sq in SQ:
        pc=B[sq]
        if not pc or (pc>0)!=(SIDE>0):continue
        t=abs(pc)
        if t==1:
            d=16*SIDE
            o=sq+d
            if not o&0x88 and not B[o] and not cap_only:
                if (o>>4)==(7 if SIDE>0 else 0):pm(o)
                else:
                    ms.append(mk(sq,o))
            if (sq>>4)==(1 if SIDE>0 else 6) and not B[o] and not B[o+d] and not cap_only:ms.append(mk(sq,o+d,0,1))
            elif not o&0x88 and not B[o] and (o>>4)==(7 if SIDE>0 else 0):pm(o)
            for o in (sq+d-1,sq+d+1):
                if o&0x88:continue
                if B[o] and (B[o]>0)!=(SIDE>0):
                    if (o>>4)==(7 if SIDE>0 else 0):pm(o)
                    else:ms.append(mk(sq,o))
                elif o==EP and not B[o]:
                    ms.append(mk(sq,o,0,2))
        elif t==2 or t==6:
            for o in (KN if t==2 else KG):
                x=sq+o
                if x&0x88:continue
                q=B[x]
                if not q:
                    if not cap_only:ms.append(mk(sq,x))
                elif (q>0)!=(SIDE>0):ms.append(mk(sq,x))
            if t==6 and not cap_only:
                for cb,es,rs,kf,kt,fl in ((1,(5,6),7,4,6,4),(2,(3,2,1),0,4,2,8),(4,(117,118),119,116,118,4),(8,(115,114,113),112,116,114,8)):
                    if CAST&cb and B[rs]==4*SIDE and not any(B[s] for s in es) and not any(atk(s,-SIDE) for s in (kf,)+es[:2]):ms.append(mk(kf,kt,0,fl))
        else:
            for o in (BD if t==3 else RD if t==4 else BD+RD):
                x=sq+o
                while not x&0x88:
                    q=B[x]
                    if not q:
                        if not cap_only:ms.append(mk(sq,x))
                    else:
                        if (q>0)!=(SIDE>0):ms.append(mk(sq,x))
                        break
                    x+=o
    return ms
def make(m):
    global SIDE,CAST,EP,HALF,HASH,WK,BK,MG,EG,PH,NP
    f=m&127;t=(m>>7)&127;p=(m>>14)&7;fl=(m>>17)&15
    pc=B[f];cap=B[t]
    ST.append((m,cap,CAST,EP,HALF,HASH,MG,EG,PH,NP))
    HASH^=Z[pc+6][f]
    if cap:HASH^=Z[cap+6][t]
    B[f]=0
    a=abs(pc);oi=(7-(f>>4))*8+(f&7) if SIDE>0 else (f>>4)*8+(f&7);ni=(7-(t>>4))*8+(t&7) if SIDE>0 else (t>>4)*8+(t&7)
    if p:
        MG+=SIDE*((MV[p]+MGT[p][ni])-(MV[1]+MGT[1][oi]));EG+=SIDE*((WV[p]+EGT[p][ni])-(WV[1]+EGT[1][oi]));PH+=PHS[p];NP-=1
    else:
        MG+=SIDE*(MGT[a][ni]-MGT[a][oi]);EG+=SIDE*(EGT[a][ni]-EGT[a][oi])
    if cap:
        c=abs(cap);ci=(7-(t>>4))*8+(t&7) if cap>0 else (t>>4)*8+(t&7)
        MG+=SIDE*(MV[c]+MGT[c][ci]);EG+=SIDE*(WV[c]+EGT[c][ci]);PH-=PHS[c]
        if c==1:NP-=1
    if fl&2:
        e=t-16*SIDE;HASH^=Z[-SIDE+6][e];B[e]=0
        ei=(7-(e>>4))*8+(e&7) if SIDE<0 else (e>>4)*8+(e&7)
        MG+=SIDE*(MV[1]+MGT[1][ei]);EG+=SIDE*(WV[1]+EGT[1][ei]);NP-=1
    np=p*SIDE if p else pc
    if p:HASH^=Z[np+6][t]
    else:HASH^=Z[pc+6][t]
    B[t]=np
    if abs(pc)==6:
        if SIDE>0:WK=t
        else:BK=t
    if fl&12:
        rf=(112 if SIDE<0 else 0)+(7 if fl&4 else 0);rt=rf-2 if fl&4 else rf+3
        B[rf]=0;B[rt]=4*SIDE;HASH^=Z[4*SIDE+6][rf]^Z[4*SIDE+6][rt]
        MG+=SIDE*(MGT[4][61 if fl&4 else 59]-MGT[4][63 if fl&4 else 56]);EG+=SIDE*(EGT[4][61 if fl&4 else 59]-EGT[4][63 if fl&4 else 56])
    nc=CAST
    if abs(pc)==6:nc&=~(3 if SIDE>0 else 12)
    if f==0 or t==0:nc&=~2
    if f==7 or t==7:nc&=~1
    if f==112 or t==112:nc&=~8
    if f==119 or t==119:nc&=~4
    if nc!=CAST:HASH^=ZC[CAST]^ZC[nc];CAST=nc
    if EP>=0:HASH^=ZE[EP&7]
    if fl&1:EP=(f+t)//2;HASH^=ZE[EP&7]
    else:EP=-1
    HALF=0 if abs(pc)==1 or cap or fl&2 else HALF+1
    SIDE=-SIDE;HASH^=ZS
def unmake():
    global SIDE,CAST,EP,HALF,HASH,WK,BK,MG,EG,PH,NP
    m,cap,oc,oe,oh,ohash,mg,eg,ph,np=ST.pop()
    if m==0:
        SIDE=-SIDE;EP=oe;HASH=ohash;MG,EG,PH,NP=mg,eg,ph,np;return
    f=m&127;t=(m>>7)&127;p=(m>>14)&7;fl=(m>>17)&15
    SIDE=-SIDE
    pc=B[t]
    if p:pc=SIDE
    B[f]=pc;B[t]=cap
    if fl&2:B[t-16*SIDE]=-SIDE
    if fl&12:
        rf=(112 if SIDE<0 else 0)+(7 if fl&4 else 0);rt=rf-2 if fl&4 else rf+3
        B[rf]=4*SIDE;B[rt]=0
    if abs(pc)==6:
        if SIDE>0:WK=f
        else:BK=f
    CAST,EP,HALF,HASH,MG,EG,PH,NP=oc,oe,oh,ohash,mg,eg,ph,np
def mnull():
    global SIDE,EP,HASH
    ST.append((0,0,CAST,EP,HALF,HASH,MG,EG,PH,NP))
    if EP>=0:HASH^=ZE[EP&7]
    EP=-1;SIDE=-SIDE;HASH^=ZS
def ev():
    if NP==0 and PH<=1:return 0
    ph=min(PH,24)
    return (MG*ph+EG*(24-ph))//24*SIDE+8
def order(ms,ttm,ply):
    def sc(m):
        if m==ttm:return 1<<20
        t=(m>>7)&127;cap=B[t]
        if cap:return 10000+10*MV[abs(cap)]-MV[abs(B[m&127])]
        if (m>>14)&7:return 9000+MV[(m>>14)&7]
        if ply<128:
            if m==KILL[ply][0]:return 8000
            if m==KILL[ply][1]:return 7000
        return 0
    ms.sort(key=lambda m:(-sc(m),m))
def qs(a,b,ply):
    global NODES
    NODES+=1
    if NODES>=LIM:raise Abort
    me=SIDE;ksq=WK if me>0 else BK
    if atk(ksq,-me):
        ms=gen();order(ms,0,ply);best=-MATE+ply;legal=0
        for m in ms:
            make(m)
            if atk(WK if me>0 else BK,SIDE):unmake();continue
            legal+=1
            v=-qs(-b,-a,ply+1)
            unmake()
            if v>=b:return b
            if v>best:best=v
            if v>a:a=v
        return best if legal else -MATE+ply
    st=ev()
    if st>=b:return b
    if st>a:a=st
    if ply>64:return a
    ms=gen(1);order(ms,0,ply)
    for m in ms:
        make(m)
        if atk(WK if me>0 else BK,SIDE):unmake();continue
        v=-qs(-b,-a,ply+1)
        unmake()
        if v>=b:return b
        if v>a:a=v
    return a
def S(d,a,b,ply):
    global NODES
    NODES+=1
    if NODES>=LIM:raise Abort
    if HALF>=100:return 0
    me=SIDE;ksq=WK if me>0 else BK
    chk=atk(ksq,-me)
    if chk:d+=1
    if d<=0:return qs(a,b,ply)
    e=TT.get(HASH)
    if e and e[0]>=d:
        if e[1]==0:return e[2]
        if e[1]==1 and e[2]>=b:return e[2]
        if e[1]==2 and e[2]<=a:return e[2]
    if d>=3 and ply>0 and not chk and PH>0:
        st=ev()
        if st>=b:
            mnull()
            v=-S(d-3,-b,-b+1,ply+1)
            unmake()
            if v>=b:return b
    ms=gen();order(ms,e[3] if e else 0,ply)
    best=-MATE;bm=0;fl=2;legal=0
    for m in ms:
        t=(m>>7)&127;cap=B[t]
        make(m)
        if atk(WK if me>0 else BK,SIDE):unmake();continue
        legal+=1
        if HASH in HIST:v=0
        elif legal==1:v=-S(d-1,-b,-a,ply+1)
        else:
            r=2 if d>=3 and legal>3 and not chk and not cap and not (m>>14)&7 else 0
            v=-S(d-1-r,-a-1,-a,ply+1)
            if v>a:v=-S(d-1,-b,-a,ply+1)
        unmake()
        if v>best:best=v;bm=m
        if v>a:a=v;fl=0
        if a>=b:
            fl=1
            t=(m>>7)&127
            if not B[t] and not (m>>14)&7 and ply<128:
                if m!=KILL[ply][0]:KILL[ply][1]=KILL[ply][0];KILL[ply][0]=m
            break
    if not legal:return -MATE+ply if chk else 0
    if len(TT)>300000:TT.clear()
    TT[HASH]=(d,fl,best if fl==0 else a,bm)
    return best
def root():
    global NODES
    NODES=0
    ms=gen()
    me=SIDE
    best=ms[0]
    for d in range(1,12):
        cur=None;curv=-MATE;a=-MATE;b=MATE;i=0
        try:
            order(ms,0,0)
            ms.sort(key=lambda m:m!=best)
            for m in ms:
                make(m)
                if atk(WK if me>0 else BK,SIDE):unmake();continue
                if HASH in HIST:v=0
                elif i==0:v=-S(d-1,-b,-a,1)
                else:
                    v=-S(d-1,-a-1,-a,1)
                    if v>a:v=-S(d-1,-b,-a,1)
                unmake()
                i+=1
                if cur is None or v>curv:cur=m;curv=v
                if v>a:a=v
            if cur is not None:best=cur
        except Abort:break
    return best
def greedy():
    ms=gen()
    return max(ms,key=lambda m:MV[abs(B[(m>>7)&127])]) if ms else 0
def post(p,body):
    r=u.Request(ENV+p,json.dumps(body).encode(),{"content-type":"application/json"})
    try:
        with u.urlopen(r) as x:return json.load(x)
    except Exception as e:sys.exit(f"{p}: {e}")
def uci(m):
    return "abcdefgh"[m&7]+str((m&127)//16+1)+"abcdefgh"[(m>>7)&7]+str(((m>>7)&127)//16+1)+("nbrq"[(m>>14)-2] if (m>>14)&7 else "")
cur=None
while True:
    g=post("/game",{})
    if g["status"]=="done":break
    while g["status"]=="your_move":
        if g["game"]!=cur:cur=g["game"];HIST.clear()
        parse(g["fen"])
        HIST[HASH]=HIST.get(HASH,0)+1
        try:m=root()
        except Exception:m=greedy()
        mv=uci(m)
        lm=g["legal_moves"]
        if mv not in lm:
            mv=next((uci(x) for x in gen() if uci(x) in lm),lm[0])
        g=post("/move",{"game":g["game"],"move":mv})
    print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
