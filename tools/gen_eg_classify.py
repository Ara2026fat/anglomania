#!/usr/bin/env python3
"""egypt-classify.html: all books, cover + name + section chips + free/paid/price; exports JSON of changes."""
import json,os,subprocess,base64,io
from PIL import Image
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files=[f for f in json.load(open(R+'/catalog.json',encoding='utf-8'))['files'] if f['code'].startswith('EG')]
PV='/home/claude/anglomania-private/paid/'
tmp='/tmp/claude-0/-home-claude/1b6ebfa6-f935-56bb-b42e-b0a79fcfb8ba/scratchpad/covers'
IMG={}
for f in files:
    import glob
    o=f'{tmp}/c5-{f["id"]}'
    if not glob.glob(o+'-*.jpg'):
        subprocess.run(['pdftoppm','-f','1','-l','5','-r','75','-jpeg',f'{PV}{f["id"]}.pdf',o],check=True,stderr=subprocess.DEVNULL)
        subprocess.run(['pdftoppm','-f',str(f['pages']),'-l',str(f['pages']),'-r','75','-jpeg',f'{PV}{f["id"]}.pdf',o+'z'],check=True,stderr=subprocess.DEVNULL)
    L=[]
    for x in sorted(glob.glob(o+'-*.jpg'))+sorted(glob.glob(o+'z-*.jpg')):
        im=Image.open(x).convert('RGB');im.thumbnail((440,620));b=io.BytesIO();im.save(b,'JPEG',quality=62);L.append('data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode())
    IMG[f['id']]=L
GR=[['eg-g%d'%n,t] for n,t in [(1,'الأول الابتدائي'),(2,'الثاني الابتدائي'),(3,'الثالث الابتدائي'),(4,'الرابع الابتدائي'),(5,'الخامس الابتدائي'),(6,'السادس الابتدائي'),(7,'الأول الإعدادي'),(8,'الثاني الإعدادي'),(9,'الثالث الإعدادي'),(10,'الأول الثانوي')]]
SK=[['grammar','القواعد'],['writing','الكتابة'],['translation','الترجمة'],['reading','القراءة'],['book','الكتاب المدرسي']]
STAGES=[GR,SK]
H=r'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>تصنيف الكتب المصرية · Anglomania</title>
<style>*{box-sizing:border-box;margin:0}body{font-family:Cairo,Tahoma,sans-serif;background:#FBF7EA;color:#17302A;padding-bottom:84px;line-height:1.5}
header{background:#0E5E3E;color:#fff;padding:12px 16px;border-bottom:4px solid #D4A72C;position:sticky;top:0;z-index:5}header h1{font-size:18px}header p{font-size:12px;opacity:.9}
.f{display:flex;gap:6px;overflow-x:auto;margin-top:8px}.f button{flex:none;padding:5px 13px;border-radius:99px;border:0;background:#fff;color:#0E5E3E;font:700 13px Cairo,Tahoma}.f button.on{background:#D4A72C;color:#fff}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:12px;padding:12px}
.c{display:block;background:#fff;border:2px solid #eadfb8;border-radius:16px;padding:10px}.c.d{border-color:#D4A72C;background:#FFFBEA}
.ps{display:flex;gap:8px;overflow-x:auto;padding:4px 0 8px;direction:rtl}.ps img{height:260px;width:auto;flex:none;border:1px solid #ddd;border-radius:6px;cursor:zoom-in}.op{display:block;text-align:center;padding:8px;border-radius:10px;background:#E8F5EE;color:#0E5E3E;font:900 13px Cairo,Tahoma;text-decoration:none;margin-bottom:4px}.nm{display:flex;flex-direction:column;gap:4px;margin:4px 0}.nm input{width:100%;padding:5px 8px;border:2px solid #eadfb8;border-radius:10px;font:700 14px Cairo,Tahoma}.nm input.en{direction:ltr;text-align:left;font-size:13px}
.h{font-weight:900;font-size:15px}.e{font-size:11px;color:#5B6C65;direction:ltr;text-align:right}.n{display:inline-block;background:#D4A72C;color:#fff;border-radius:99px;padding:0 8px;font-size:12px;font-weight:900;margin-left:4px}
.st{font-weight:900;font-size:12px;color:#0E5E3E;margin-top:5px}.ch{display:flex;flex-wrap:wrap;gap:4px;margin-top:2px}
.chip{padding:3px 10px;border-radius:99px;border:2px solid #eadfb8;background:#fff;font:700 12px Cairo,Tahoma}.chip.on{background:#0E5E3E;border-color:#0E5E3E;color:#fff}
.r{display:flex;gap:6px;align-items:center;margin-top:8px;flex-wrap:wrap}.t{padding:6px 14px;border-radius:12px;border:2px solid #eadfb8;background:#fff;font:900 13px Cairo,Tahoma}.t.f.on{background:#1FA571;border-color:#1FA571;color:#fff}.t.p.on{background:#D4A72C;border-color:#D4A72C;color:#fff}
input{width:80px;padding:5px;border:2px solid #eadfb8;border-radius:10px;font:700 14px Cairo,Tahoma}
.lb{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;align-items:center;justify-content:center;z-index:9}.lb.on{display:flex}.lb img{max-width:96vw;max-height:96vh}
.foot{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:3px solid #D4A72C;padding:10px 12px;display:flex;gap:8px;align-items:center;z-index:6}.foot span{flex:1;font-weight:700;font-size:14px}
.btn{padding:10px 14px;border-radius:12px;border:0;font:900 14px Cairo,Tahoma;background:#0E5E3E;color:#fff}.btn.w{background:#fff;color:#0E5E3E;border:2px solid #0E5E3E}
</style></head><body><header><h1>تصنيف كتب المنهج المصري (الفصل الأول) — __N__ كتابًا</h1><p>أول ٥ صفحات + صفحة الختام (اسحب). عدّل الاسم والأقسام ومجاني/مدفوع. اضغط الصورة لتكبيرها.</p><div class="f" id="f"></div></header><div class="g" id="g"></div><div class="lb" id="lb"><img id="li"></div>
<div class="foot"><span id="stat"></span><button class="btn w" id="rst">تراجع</button><button class="btn" id="dl">⬇ تنزيل التعديلات</button></div>
<script>
const STAGES=__ST__,ORIG=__DATA__,IMG=__IMG__,KEY='ang.classify.eg.v1';
let S=JSON.parse(JSON.stringify(ORIG)),flt='all';try{const k=JSON.parse(localStorage.getItem(KEY)||'null');if(k&&k.length===S.length)S=k}catch(e){}
const $=q=>document.querySelector(q),N=n=>String(n).replace(/\d/g,d=>'٠١٢٣٤٥٦٧٨٩'[d]);
const orig=id=>ORIG.find(f=>f.id===id),key=f=>JSON.stringify([f.ar,f.en,f.tier,f.tier==='paid'?+f.price||0:0,[...f.place].sort()]),dirty=f=>key(f)!==key(orig(f.id));
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
function card(f){const i=ORIG.findIndex(x=>x.id===f.id)+1;let h=`<div class="c${dirty(f)?' d':''}" data-id="${f.id}"><div class="h"><span class="n">${N(i)}</span>${f.pages} صفحة · ${f.id}</div><div class="ps">${IMG[f.id].map(s=>`<img src="${s}" loading="lazy">`).join('')}</div><div class="nm"><input class="ar" value="${f.ar.replace(/"/g,'&quot;')}" placeholder="الاسم بالعربي"><input class="en" value="${f.en.replace(/"/g,'&quot;')}" placeholder="English name"></div>`;
const cur=(f.place[0]||'').split(':');h+='<div class="st">الصف</div><div class="ch">'+STAGES[0].map(g=>`<button class="chip${cur[0]===g[0]?' on':''}" data-g="${g[0]}">${g[1]}</button>`).join('')+'</div><div class="st">القسم</div><div class="ch">'+STAGES[1].map(k=>`<button class="chip${cur[2]===k[0]?' on':''}" data-k="${k[0]}">${k[1]}</button>`).join('')+'</div>';
h+=`<div class="r"><button class="t f${f.tier==='free'?' on':''}" data-t="free">مجاني</button><button class="t p${f.tier==='paid'?' on':''}" data-t="paid">مدفوع</button>`+(f.tier==='paid'?`<input type="number" min="1" inputmode="numeric" value="${f.price||''}" placeholder="اختياري"> ريال <small>(فارغ = السعر عبر واتساب)</small>`:'')+'</div></div>';return h}
function stat(){$('#stat').textContent=N(S.length)+' كتابًا · '+N(S.filter(f=>f.tier==='paid').length)+' مدفوع · '+N(S.filter(f=>f.tier==='free').length)+' مجاني · '+N(S.filter(f=>f.tier==='pending').length)+' غير مصنّف · '+N(S.filter(dirty).length)+' تعديل'}
function bar(){const T=[['all','الكل'],['chg','المعدَّل'],['pend','غير مصنّف'],['paid','مدفوع'],['free','مجاني']];$('#f').innerHTML=T.map(t=>`<button class="${flt===t[0]?'on':''}" data-f="${t[0]}">${t[1]}</button>`).join('')}
function render(){const L=S.filter(f=>flt==='all'||(flt==='chg'&&dirty(f))||(flt==='pend'&&f.tier==='pending')||(flt==='paid'&&f.tier==='paid')||(flt==='free'&&f.tier==='free'));$('#g').innerHTML=L.map(card).join('')||'<p style="padding:24px">لا يوجد</p>';bar();stat()}
$('#f').onclick=e=>{const b=e.target.closest('button');if(b){flt=b.dataset.f;render()}};
$('#g').onclick=e=>{if(e.target.tagName==='IMG'){$('#li').src=e.target.src;$('#lb').classList.add('on');return}
const c=e.target.closest('.c'),b=e.target.closest('button');if(!c||!b)return;const f=S.find(x=>x.id===c.dataset.id);
if(b.dataset.g||b.dataset.k){const c0=(f.place[0]||'::').split(':');if(b.dataset.g)c0[0]=b.dataset.g;if(b.dataset.k)c0[2]=b.dataset.k;c0[1]='t1';f.place=[c0.join(':')]}else if(b.dataset.t){f.tier=(f.tier===b.dataset.t?'pending':b.dataset.t);if(f.tier!=='paid')f.price=0}else return;
save();const t=document.createElement('div');t.innerHTML=card(f);c.replaceWith(t.firstElementChild);stat()};
$('#g').oninput=e=>{const c=e.target.closest('.c');if(!c)return;const f=S.find(x=>x.id===c.dataset.id);if(e.target.classList.contains('ar'))f.ar=e.target.value;else if(e.target.classList.contains('en'))f.en=e.target.value;else f.price=Math.max(0,+e.target.value||0);save();c.classList.toggle('d',dirty(f));stat()};
$('#lb').onclick=()=>$('#lb').classList.remove('on');
$('#rst').onclick=()=>{if(confirm('إلغاء كل تعديلاتك؟')){S=JSON.parse(JSON.stringify(ORIG));save();render()}};
$('#dl').onclick=()=>{const out={app:'anglomania-books-map',source:'egypt',date:new Date().toISOString().slice(0,10),changes:S.filter(dirty).map(f=>({id:f.id,from:{ar:orig(f.id).ar,en:orig(f.id).en,tier:orig(f.id).tier,price:orig(f.id).price,place:orig(f.id).place},to:{ar:f.ar,en:f.en,tier:f.tier,price:f.tier==='paid'?+f.price||0:0,place:f.place}})),files:S};
const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(out,null,1)],{type:'application/json'}));a.download='anglomania-egypt-edit.json';a.click()};
render();
</script></body></html>'''
J=lambda x:json.dumps(x,ensure_ascii=False)
open(R+'/egypt-classify.html','w',encoding='utf-8').write(H.replace('__N__',str(len(files))).replace('__ST__',J(STAGES)).replace('__DATA__',J(files)).replace('__IMG__',J(IMG)))
print(os.path.getsize(R+'/egypt-classify.html')//1024,'KB')
