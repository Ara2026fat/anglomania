#!/usr/bin/env python3
"""books-covers.html: all Foundation Corner books with first-page thumbnail + sections (single file, offline)."""
import json,os,subprocess,base64,io,html
from PIL import Image
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cat=json.load(open(R+'/catalog.json',encoding='utf-8'))['files']
SN={'preschool':'ما قبل المدرسة','primary':'الابتدائية','intermediate':'المتوسطة','secondary':'الثانوية والكبار'}
KN={'phonics':'الأصوات','grammar':'القواعد','handwriting':'الخط','letters':'الحروف','translation':'الترجمة','writing':'الكتابة','reading':'القراءة'}
tmp='/tmp/claude-0/-home-claude/1b6ebfa6-f935-56bb-b42e-b0a79fcfb8ba/scratchpad/covers';os.makedirs(tmp,exist_ok=True)
cards=[]
for i,f in enumerate(cat,1):
    out=f'{tmp}/{f["id"]}'
    subprocess.run(['pdftoppm','-f','1','-l','1','-r','60','-jpeg','-singlefile',f'{R}/pdf/{f["id"]}.pdf',out],check=True)
    im=Image.open(out+'.jpg').convert('RGB');im.thumbnail((300,420));b=io.BytesIO();im.save(b,'JPEG',quality=70)
    img='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    by={}
    for p in f['place']:
        s,k=p.split(':');by.setdefault(s,[]).append(KN[k])
    pl=''.join(f'<div class="pl"><b>{SN[s]}</b> ← {"، ".join(v)}</div>' for s,v in by.items()) or '<div class="pl no">⚠ بلا قسم</div>'
    tier='<span class="t p">مدفوع '+str(f['price'])+' ريال</span>' if f['tier']=='paid' else '<span class="t f">مجاني</span>'
    cards.append(f'<div class="c" data-s="{html.escape(" ".join(f["place"])+" "+f["ar"]+" "+f["en"]+" "+f["id"])}"><img src="{img}" alt=""><div class="b"><div class="n">{i}</div><h3>{html.escape(f["ar"])}</h3><div class="e">{html.escape(f["en"])}</div><div class="m">{f["pages"]} صفحة · {f["mb"]}MB · {tier}</div>{pl}<div class="id">{f["id"]}</div></div></div>')
H='''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>كتب ركن التأسيس · Anglomania</title>
<style>*{box-sizing:border-box;margin:0}body{font-family:Cairo,Tahoma,sans-serif;background:#FBF7EA;color:#17302A;line-height:1.5}
header{background:#0E5E3E;color:#fff;padding:14px 16px;border-bottom:4px solid #D4A72C;position:sticky;top:0;z-index:3}header h1{font-size:19px}
input{width:100%;margin-top:8px;padding:9px 12px;border-radius:10px;border:0;font:700 15px Cairo,Tahoma}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px;padding:12px}
.c{display:flex;gap:10px;background:#fff;border:2px solid #eadfb8;border-radius:14px;padding:10px}.c img{width:110px;height:auto;align-self:flex-start;border:1px solid #ddd;border-radius:6px}
.b{flex:1;min-width:0;position:relative}.n{position:absolute;left:0;top:0;background:#D4A72C;color:#fff;font-weight:900;border-radius:99px;min-width:28px;text-align:center;font-size:13px}
h3{font-size:15px;padding-left:34px}.e{font-size:12px;color:#5B6C65;direction:ltr;text-align:right}.m{font-size:12px;margin:4px 0}
.t{padding:1px 8px;border-radius:99px;color:#fff;font-weight:700}.t.f{background:#1FA571}.t.p{background:#D4A72C}
.pl{font-size:13px;background:#E8F5EE;border-radius:8px;padding:3px 8px;margin-top:4px}.pl.no{background:#fde8e6;color:#b3261e}.id{font-size:11px;color:#999;direction:ltr;text-align:right;margin-top:4px}
</style></head><body><header><h1>كتب ركن التأسيس — __N__ كتابًا</h1><input id="q" placeholder="ابحث باسم الكتاب أو القسم…"></header><div class="g" id="g">__C__</div>
<script>q.oninput=()=>{const v=q.value.trim().toLowerCase();document.querySelectorAll('.c').forEach(c=>c.style.display=!v||c.textContent.toLowerCase().includes(v)||c.dataset.s.toLowerCase().includes(v)?'':'none')}</script></body></html>'''
open(R+'/books-covers.html','w',encoding='utf-8').write(H.replace('__N__',str(len(cat))).replace('__C__','\n'.join(cards)))
print(os.path.getsize(R+'/books-covers.html')//1024,'KB')
