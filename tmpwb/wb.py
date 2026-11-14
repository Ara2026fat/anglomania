import sys,os,json,math,subprocess,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import soundfile as sf
W,H,FPS=1280,720,24
D=os.path.dirname(os.path.abspath(__file__))
F=lambda n,s:ImageFont.truetype(f'{D}/fonts/{n}',s)
PM='PermanentMarker-Regular.ttf';PH='PatrickHand-Regular.ttf'
EM=(14,94,62);EMD=(10,74,49);GOLD=(200,162,58);CREAM=(250,246,234)
BOARD=(253,253,251);INK=(34,38,44);GREY=(96,102,112)
ROLE={'S':(22,128,74),'V':(206,52,52),'O':(32,92,206),'T':(224,122,22),'N':INK}
BX0,BY0,BX1,BY1=50,86,1230,640
LM,RM=105,1185
def chrome():
    im=Image.new('RGB',(W,H),CREAM);d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,66],fill=EM);d.rectangle([0,66,W,70],fill=GOLD)
    d.text((40,33),'ANGLOMANIA EDU',font=F(PM,30),fill=(255,255,255),anchor='lm')
    d.text((W-40,33),'MORE THAN ENGLISH',font=F(PM,26),fill=GOLD,anchor='rm')
    d.rectangle([0,H-50,W,H],fill=EM);d.rectangle([0,H-54,W,H-50],fill=GOLD)
    d.text((W//2,H-25),'anglomaniaedu.com',font=F(PH,28),fill=(255,255,255),anchor='mm')
    d.rounded_rectangle([BX0-12,BY0-12,BX1+12,BY1+12],radius=14,fill=(196,201,208),outline=(140,146,155),width=3)
    d.rectangle([BX0,BY0,BX1,BY1],fill=BOARD)
    d.rounded_rectangle([BX0+60,BY1+12,BX1-60,BY1+26],radius=6,fill=(170,176,184))
    for i,c in enumerate([(30,30,30),(32,92,206),(206,52,52),(22,128,74)]):
        x=BX0+120+i*70;d.rounded_rectangle([x,BY1+4,x+54,BY1+14],radius=4,fill=c)
    return im
def segs(markup):
    out=[];pos=0
    for m in re.finditer(r'\{([SVOTN]):([^}]*)\}',markup):
        if m.start()>pos:out.append((markup[pos:m.start()],'N'))
        out.append((m.group(2),m.group(1)));pos=m.end()
    if pos<len(markup):out.append((markup[pos:],'N'))
    return out
def text_img(markup,font,color=None,ar=False,pad=8):
    if ar:
        tmp=Image.new('RGBA',(10,10));d=ImageDraw.Draw(tmp)
        w=int(d.textlength(markup,font=font,direction='rtl',language='ar'))
        asc,desc=font.getmetrics()
        im=Image.new('RGBA',(w+2*pad,asc+desc+2*pad),(0,0,0,0));d=ImageDraw.Draw(im)
        d.text((pad,pad),markup,font=font,fill=color+(255,),direction='rtl',language='ar')
        return im
    parts=segs(markup);tmp=ImageDraw.Draw(Image.new('RGBA',(10,10)))
    ws=[tmp.textlength(t,font=font) for t,_ in parts];asc,desc=font.getmetrics()
    im=Image.new('RGBA',(int(sum(ws))+2*pad,asc+desc+2*pad),(0,0,0,0));d=ImageDraw.Draw(im);x=pad
    for (t,r),w in zip(parts,ws):
        d.text((x,pad),t,font=font,fill=(color or ROLE[r])+(255,));x+=w
    return im
def icon_img(kind,size=44):
    im=Image.new('RGBA',(size+12,size+12),(0,0,0,0));d=ImageDraw.Draw(im)
    if kind=='wrong':
        d.line([(8,8),(size,size)],fill=ROLE['V']+(255,),width=7);d.line([(size,8),(8,size)],fill=ROLE['V']+(255,),width=7)
    else:
        d.line([(6,size*0.55),(size*0.38,size),(size+2,8)],fill=ROLE['S']+(255,),width=8,joint='curve')
    return im
class Item:
    def __init__(s,img,x,y,ar=False,color=INK,deco=None):
        s.img=img;s.x=x;s.y=y;s.ar=ar;s.color=color;s.deco=deco
def pen(fr,x,y,color):
    d=ImageDraw.Draw(fr)
    d.line([(x+14,y-14),(x+66,y-88)],fill=(64,70,82),width=22)
    d.line([(x+4,y-3),(x+16,y-19)],fill=tuple(color[:3]),width=15)
    d.ellipse([x-5,y-5,x+7,y+7],fill=color)
SIZES={'line':50,'ex':45,'wrong':45,'right':45,'sub':38,'note':36}
def layout(page_items,ar_on,title,y0=122):
    items=[];y=y0
    for it in page_items:
        k=it[0]
        if k=='head':
            im=text_img(it[1],F(PM,34),GREY,pad=6);items.append(Item(im,LM-8,y-20,color=GREY))
            ln=Image.new('RGBA',(RM-LM,10),(0,0,0,0));ImageDraw.Draw(ln).rounded_rectangle([0,2,RM-LM,7],radius=3,fill=GOLD+(255,))
            items.append(Item(ln,LM,y-20+im.height,color=GOLD));y+=im.height-6;continue
        if k=='title':
            im=text_img(it[1],F(PM,76),EM,pad=8);items.append(Item(im,(W-im.width)//2,y,color=EM));y+=im.height+2;continue
        if k=='sub':
            im=text_img(it[1],F(PH,SIZES['sub']),GREY,pad=8);items.append(Item(im,(W-im.width)//2,y,color=GREY));y+=im.height
            if len(it)>2 and ar_on:
                ai=text_img(it[2],F('Tajawal-Medium.ttf',30),(78,84,92),ar=True,pad=8)
                items.append(Item(ai,(W-ai.width)//2,y,ar=True,color=(78,84,92)));y+=ai.height
            y+=10;continue
        font=F(PH,SIZES[k]);col=None;ex_w=0
        if k in('wrong','right'):
            rc=ROLE['V'] if k=='wrong' else ROLE['S']
            items.append(Item(icon_img(k),LM-8,y+4,color=rc))
            im=text_img(it[1],font,(90,96,104) if k=='wrong' else ROLE['S'],pad=8)
            en=Item(im,LM+52,y,color=rc,deco='strike' if k=='wrong' else None);ex_w=52
        elif k=='note':
            im=text_img(it[1],font,EMD,pad=8);en=Item(im,LM-8,y,color=EMD)
        else:
            im=text_img(it[1],font,None,pad=8);en=Item(im,LM-8,y,color=INK)
        items.append(en);rowh=im.height
        ar=it[2] if len(it)>2 else None
        if ar and ar_on:
            ai=text_img(ar,F('Tajawal-Medium.ttf',30),(78,84,92),ar=True,pad=8)
            if LM+ex_w+im.width+30<RM-ai.width:
                items.append(Item(ai,RM-ai.width+8,y+(im.height-ai.height)//2+4,ar=True,color=(78,84,92)))
            else:
                items.append(Item(ai,RM-ai.width+8,y+im.height-10,ar=True,color=(78,84,92)));rowh=im.height+ai.height-10
        y+=rowh+4
    if y>BY1-10:print('OVERFLOW',title,y,flush=True)
    return items,y
def build_audio(lesson,voice='am_puck',speed=0.85):
    from kokoro_onnx import Kokoro
    speed=float(os.environ.get('SPEED',speed))
    k=Kokoro(f'{D}/models/kokoro.onnx',f'{D}/models/voices.bin');SR=24000
    ia,_=k.create(os.environ.get('INTRO',"Welcome to Anglomania! More than English!"),voice=os.environ.get('IVOICE','am_puck'),speed=speed,lang='en-us');ia=ia.astype(np.float32)
    lead=1.2;tail=0.9;Ti=lead+len(ia)/SR+tail
    out=[np.zeros(int(lead*SR),dtype=np.float32),ia,np.zeros(int(tail*SR),dtype=np.float32),np.zeros(int(0.2*SR),dtype=np.float32)];t=Ti+0.2;tl=[('intro',0,Ti)]
    for st in lesson['steps']:
        if st.get('page'):
            tl.append(('erase',t,t+0.7));out.append(np.zeros(int(0.7*SR),dtype=np.float32));t+=0.7
        a,_=k.create(st['say'],voice=st.get('v',voice),speed=st.get('sp',speed),lang='en-us');a=a.astype(np.float32)
        d=len(a)/SR;out.append(a);out.append(np.zeros(int(0.45*SR),dtype=np.float32))
        tl.append(('step',t,t+d,st));t+=d+0.45
    out.append(np.zeros(int(1.8*SR),dtype=np.float32));t+=1.8
    return np.concatenate(out),SR,tl,t
def pad_music(n,SR):
    t=np.arange(n)/SR;m=np.zeros(n)
    for f,ph in((196,0),(246.9,1),(293.7,2),(392,3)):m+=np.sin(2*np.pi*f*t+ph)*(0.5+0.5*np.sin(2*np.pi*0.07*t+ph))
    m*=0.012/4*4;env=np.minimum(1,np.minimum(t/2,(n/SR-t)/2));return (m*env).astype(np.float32)
def render(lesson,out,ar_on):
    vox,SR,tl,total=build_audio(lesson)
    mus=pad_music(len(vox),SR);mix=np.clip(vox+mus,-1,1)
    sf.write(out+'.wav',mix,SR)
    base=chrome();cur=base.copy();blank=base.copy()
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',out+'.wav','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-shortest',out],stdin=subprocess.PIPE)
    state=dict(t=0.0,fr=0)
    def hold(until):
        n=int(round(until*FPS))-state['fr']
        if n>0:
            b=cur.tobytes()
            for _ in range(n):ff.stdin.write(b)
            state['fr']+=n
    def anim(t0,t1,fn):
        hold(t0)
        n=max(1,int(round((t1-t0)*FPS)))
        for i in range(n):
            fr=fn((i+1)/n);ff.stdin.write(fr.tobytes());state['fr']+=1
    ypage=[122]
    LOGO=Image.open(f'{D}/logo.png').convert('RGB').crop((95,105,417,405));IV=(254,253,245)
    def intro_img(tm):
        fr=Image.new('RGB',(W,H),IV);d=ImageDraw.Draw(fr)
        d.rectangle([0,0,W,14],fill=EM);d.rectangle([0,14,W,20],fill=GOLD);d.rectangle([0,H-20,W,H-14],fill=GOLD);d.rectangle([0,H-14,W,H],fill=EM)
        p=min(1,tm/0.8);e=1-(1-p)**3;sh=int(330+50*e);sw=int(sh*LOGO.width/LOGO.height);lg=LOGO.resize((sw,sh),Image.LANCZOS)
        fr.paste(lg,((W-sw)//2,36+(380-sh)//2))
        def txt(t0,y,text,font,col,ar=False):
            a=max(0,min(1,(tm-t0)/0.5))
            if a<=0:return
            lay=Image.new('RGBA',(W,H),(0,0,0,0));dd=ImageDraw.Draw(lay)
            kw=dict(direction='rtl',language='ar') if ar else {}
            dd.text((W//2,y+int((1-a)*14)),text,font=font,fill=col+(int(255*a),),anchor='mm',**kw)
            fr.paste(lay,(0,0),lay)
        a=max(0,min(1,(tm-0.9)/0.5))
        if a>0:
            for xx,x2 in((330,500),(780,950)):d.line([(xx,408),(x2,408)],fill=GOLD,width=4)
            txt(0.9,408,'MORE THAN ENGLISH',F(PM,34),(158,126,34))
        txt(1.4,470,'Welcome to Anglomania!',F(PM,58),EM)
        if ar_on:txt(1.9,535,'أهلاً بكم في أنجلومانيا',F('Tajawal-Bold.ttf',44),(158,126,34),ar=True)
        a=max(0,min(1,(tm-2.3)/0.5))
        if a>0:
            lay=Image.new('RGBA',(W,H),(0,0,0,0));dd=ImageDraw.Draw(lay)
            dd.rounded_rectangle([W//2-190,600,W//2+190,656],radius=28,fill=EM+(int(255*a),),outline=GOLD+(int(255*a),),width=3)
            dd.text((W//2,628),'anglomaniaedu.com',font=F(PH,34),fill=(255,255,255,int(255*a)),anchor='mm')
            fr.paste(lay,(0,0),lay)
        return fr
    for ev in tl:
        if ev[0]=='intro':
            n=int(round(ev[2]*FPS));fo=int(0.5*FPS)
            for i in range(n):
                fr=intro_img(i/FPS)
                if i>=n-fo:fr=Image.blend(fr,base,(i-(n-fo)+1)/fo)
                ff.stdin.write(fr.tobytes());state['fr']+=1
            continue
        if ev[0]=='erase':
            def er(p):
                fr=cur.copy();x=int(BX0+(BX1-BX0+160)*p)-80
                fr.paste(blank.crop((BX0,BY0,min(x,BX1),BY1)),(BX0,BY0)) if x>BX0 else None
                d=ImageDraw.Draw(fr);d.rounded_rectangle([x,BY0+160,x+80,BY0+330],radius=12,fill=(80,86,96))
                d.rectangle([x,BY0+300,x+80,BY0+330],fill=(210,170,70))
                return fr
            anim(ev[1],ev[2],er)
            cur.paste(blank.crop((BX0,BY0,BX1,BY1)),(BX0,BY0));ypage[0]=122;continue
        _,t0,t1,st=ev
        items,ypage[0]=layout(st['write'],ar_on,lesson['en'],ypage[0])
        avail=max(1.0,(t1-t0)-0.5);nat=[]
        for it in items:
            w=it.img.width;nat.append(max(0.45,w/430))
        tot=sum(nat);sc=min(1.0,avail/tot) if tot>0 else 1
        tt=t0+0.25
        for it,nd in zip(items,nat):
            dur=max(0.35,nd*sc);a0,a1=tt,tt+dur;tt=a1+0.04
            def wr(p,it=it):
                fr=cur.copy();w,h=it.img.size
                if it.ar:
                    cx=int(w*p);crop=it.img.crop((w-cx,0,w,h));px=it.x+w-cx
                else:
                    cx=int(w*p);crop=it.img.crop((0,0,cx,h));px=it.x
                if cx>0:fr.paste(crop,(px,it.y),crop)
                tipx=(px if it.ar else px+cx);tipy=it.y+int(h*0.62)
                pen(fr,tipx,tipy,it.color)
                return fr
            anim(a0,a1,wr)
            cur.paste(it.img,(it.x,it.y),it.img)
            if it.deco=='strike':
                d=ImageDraw.Draw(cur);y=it.y+it.img.height//2+4;d.line([(it.x+14,y),(it.x+it.img.width-14,y)],fill=ROLE['V'],width=5)
    hold(total)
    ff.stdin.close();ff.wait()
    os.remove(out+'.wav')
if __name__=='__main__':
    import importlib
    sys.path.insert(0,D)
    lessons=importlib.import_module(os.environ.get('LMOD','lessons_final')).LESSONS
    mode=sys.argv[1];ids=[int(x) for x in sys.argv[2:]]
    os.makedirs(f'{D}/out',exist_ok=True)
    for n in ids:
        L=[l for l in lessons if l['n']==n][0]
        for st in L['steps']:
            if st.get('page') and not any(w[0]=='head' for w in st['write']):st['write']=[('head',L['en'])]+st['write']
        name=f"Anglomania-Grammar-{n:02d}-{L['en'].replace(' ','-')}"+('' if mode=='ar' else '-EN')+'.mp4'
        render(L,f'{D}/out/{name}',mode=='ar');print('done',name,flush=True)
