#!/usr/bin/env python3
"""books-preschool.html: preschool books with first 5 pages each + classification chips (export JSON)."""
import json,os,subprocess,base64,io,html,glob
from PIL import Image
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cat=json.load(open(R+'/catalog.json',encoding='utf-8'))
files=[f for f in cat['files'] if any(p.startswith('preschool:') for p in f['place'])]
ORDER=['phonics','grammar','handwriting','letters']
files.sort(key=lambda f:(min(ORDER.index(p.split(':')[1]) for p in f['place'] if p.startswith('preschool:')),f['ar']))
tmp='/tmp/claude-0/-home-claude/1b6ebfa6-f935-56bb-b42e-b0a79fcfb8ba/scratchpad/ps';os.makedirs(tmp,exist_ok=True)
for f in files:
    for x in glob.glob(f'{tmp}/{f["id"]}-*'):os.remove(x)
    subprocess.run(['pdftoppm','-f','1','-l','5','-r','80','-jpeg',f'{R}/pdf/{f["id"]}.pdf',f'{tmp}/{f["id"]}'],check=True)
    pgs=[]
    for x in sorted(glob.glob(f'{tmp}/{f["id"]}-*.jpg')):
        im=Image.open(x).convert('RGB');im.thumbnail((520,760));b=io.BytesIO();im.save(b,'JPEG',quality=62)
        pgs.append('data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode())
    f['_pgs']=pgs
data=[{k:v for k,v in f.items() if k!='_pgs'} for f in files]
pg={f['id']:f['_pgs'] for f in files}
STAGES=[['preschool','ما قبل المدرسة',[['phonics','الأصوات'],['grammar','القواعد والجمل'],['handwriting','الخط'],['letters','الحروف']]],['primary','الابتدائية',[['translation','الترجمة'],['grammar','القواعد'],['writing','الكتابة'],['reading','القراءة']]],['intermediate','المتوسطة',[['translation','الترجمة'],['grammar','القواعد'],['writing','الكتابة'],['reading','القراءة']]],['secondary','الثانوية والكبار',[['translation','الترجمة'],['grammar','القواعد'],['writing','الكتابة'],['reading','القراءة']]]]
H=r'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>كتب ما قبل المدرسة · Anglomania</title>
<style>*{box-sizing:border-box;margin:0}body{font-family:Cairo,Tahoma,sans-serif;background:#FBF7EA;color:#17302A;padding-bottom:90px;line-height:1.5}
header{background:#0E5E3E;color:#fff;padding:12px 16px;border-bottom:4px solid #D4A72C;position:sticky;top:0;z-index:5}header h1{font-size:18px}header p{font-size:12px;opacity:.9}
.card{background:#fff;border:2px solid #eadfb8;border-radius:16px;margin:12px;padding:12px}.card.d{border-color:#D4A72C;background:#FFFBEA}
.h{font-weight:900;font-size:17px}.e{font-size:12px;color:#5B6C65;direction:ltr;text-align:right}.cur{font-size:12px;background:#E8F5EE;border-radius:8px;padding:3px 8px;margin:6px 0;display:inline-block}
.ps{display:flex;gap:8px;overflow-x:auto;padding:8px 0;scroll-snap-type:x mandatory;direction:rtl}.ps img{height:300px;width:auto;border:1px solid #ddd;border-radius:6px;flex:none;scroll-snap-align:start;cursor:zoom-in}
.st{font-weight:900;font-size:12px;color:#0E5E3E;margin-top:6px}.ch{display:flex;flex-wrap:wrap;gap:5px;margin-top:3px}
.chip{padding:4px 11px;border-radius:99px;border:2px solid #eadfb8;background:#fff;font:700 13px Cairo,Tahoma}.chip.on{background:#0E5E3E;border-color:#0E5E3E;color:#fff}
.lb{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;align-items:center;justify-content:center;z-index:9}.lb.on{display:flex}.lb img{max-width:96vw;max-height:96vh}
.foot{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:3px solid #D4A72C;padding:10px 12px;display:flex;gap:8px;align-items:center}.foot span{flex:1;font-weight:700;font-size:14px}
.btn{padding:10px 16px;border-radius:12px;border:0;font:900 15px Cairo,Tahoma;background:#0E5E3E;color:#fff}
</style></head><body><header><h1>كتب ما قبل المدرسة — __N__ كتابًا</h1><p>تصفّح أول ٥ صفحات (اسحب الصور)، واضغط الصورة لتكبيرها. صنّف بالأزرار ثم نزّل.</p></header><main id="m"></main>
<div class="lb" id="lb"><img id="li"></div>
<div class="foot"><span id="stat"></span><button class="btn" id="dl">⬇ تنزيل التصنيف</button></div>
<script>
const STAGES=__ST__,ORIG=__DATA__,PG=__PG__,KEY='ang.preschool.v1';
let S=JSON.parse(JSON.stringify(ORIG));try{const k=JSON.parse(localStorage.getItem(KEY)||'null');if(k&&k.length===S.length)S=k}catch(e){}
const $=q=>document.querySelector(q),N=n=>String(n).replace(/\d/g,d=>'٠١٢٣٤٥٦٧٨٩'[d]);
const SN={};STAGES.forEach(s=>s[2].forEach(k=>SN[s[0]+':'+k[0]]=s[1]+' ← '+k[1]));
const orig=id=>ORIG.find(f=>f.id===id),key=f=>JSON.stringify([...f.place].sort()),dirty=f=>key(f)!==key(orig(f.id));
function card(f){let h=`<div class="card${dirty(f)?' d':''}" data-id="${f.id}"><div class="h">${f.ar}</div><div class="e">${f.en} · ${f.pages}p</div><div class="cur">الآن: ${f.place.map(p=>SN[p]).join(' | ')||'بلا قسم'}</div><div class="ps">${PG[f.id].map(s=>`<img src="${s}" loading="lazy">`).join('')}</div>`;
STAGES.forEach(s=>{h+=`<div class="st">${s[1]}</div><div class="ch">`+s[2].map(k=>{const p=s[0]+':'+k[0];return `<button class="chip${f.place.includes(p)?' on':''}" data-p="${p}">${k[1]}</button>`}).join('')+'</div>'});return h+'</div>'}
function stat(){$('#stat').textContent=N(S.length)+' كتابًا · '+N(S.filter(dirty).length)+' تعديل'}
function render(){$('#m').innerHTML=S.map(card).join('');stat()}
$('#m').onclick=e=>{if(e.target.tagName==='IMG'){$('#li').src=e.target.src;$('#lb').classList.add('on');return}
const b=e.target.closest('.chip');if(!b)return;const c=b.closest('.card'),f=S.find(x=>x.id===c.dataset.id),i=f.place.indexOf(b.dataset.p);i<0?f.place.push(b.dataset.p):f.place.splice(i,1);
try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}const t=document.createElement('div');t.innerHTML=card(f);const sc=c.querySelector('.ps').scrollLeft;c.replaceWith(t.firstElementChild);stat()};
$('#lb').onclick=()=>$('#lb').classList.remove('on');
$('#dl').onclick=()=>{const out={app:'anglomania-books-map',source:'preschool',date:new Date().toISOString().slice(0,10),changes:S.filter(dirty).map(f=>({id:f.id,from:{ar:orig(f.id).ar,tier:orig(f.id).tier,price:orig(f.id).price,place:orig(f.id).place},to:{ar:f.ar,tier:f.tier,price:f.price,place:f.place}}))};
const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(out,null,1)],{type:'application/json'}));a.download='anglomania-preschool-edit.json';a.click()};
render();
</script></body></html>'''
J=lambda x:json.dumps(x,ensure_ascii=False)
open(R+'/books-preschool.html','w',encoding='utf-8').write(H.replace('__N__',str(len(files))).replace('__ST__',J(STAGES)).replace('__DATA__',J(data)).replace('__PG__',J(pg)))
print(len(files),os.path.getsize(R+'/books-preschool.html')//1024,'KB')
