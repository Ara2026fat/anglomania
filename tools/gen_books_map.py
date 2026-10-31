#!/usr/bin/env python3
"""Generate books-map.html: editable inventory of every Foundation Corner book
(location on the site, free/paid, SAR price, file path). Data embedded from catalog.json."""
import json, os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cat=json.load(open(os.path.join(R,'catalog.json'),encoding='utf-8'))
STAGES=[['preschool','ما قبل المدرسة',[['phonics','الأصوات'],['grammar','القواعد والجمل'],['handwriting','الخط'],['letters','الحروف']]],
['primary','الابتدائية',[['translation','الترجمة'],['grammar','القواعد'],['writing','الكتابة'],['reading','القراءة']]],
['intermediate','المتوسطة',[['translation','الترجمة'],['grammar','القواعد'],['writing','الكتابة'],['reading','القراءة']]],
['secondary','الثانوية والكبار',[['translation','الترجمة'],['grammar','القواعد'],['writing','الكتابة'],['reading','القراءة']]]]
HTML=r'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#0E5E3E"><title>خريطة الكتب · Anglomania</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
<style>
:root{--em:#0E5E3E;--gold:#D4A72C;--ink:#17302A;--mut:#5B6C65;--line:#eadfb8}
*{box-sizing:border-box;margin:0}body{font-family:Cairo,Tahoma,sans-serif;background:#FBF7EA;color:var(--ink);padding-bottom:110px;line-height:1.6}
header{background:var(--em);color:#fff;padding:14px 16px;border-bottom:4px solid var(--gold);position:sticky;top:0;z-index:5}
header h1{font-size:19px}header p{font-size:13px;opacity:.9}
.bar{display:flex;gap:8px;padding:10px 12px;overflow-x:auto}.bar button{flex:none;padding:6px 14px;border-radius:99px;border:2px solid var(--line);background:#fff;font:700 14px Cairo}
.bar button.on{background:var(--em);color:#fff;border-color:var(--em)}
.card{background:#fff;border:2px solid var(--line);border-radius:16px;margin:10px 12px;padding:12px}.card.dirty{border-color:var(--gold);background:#FFFBEA}
.t{font-weight:900;font-size:16px}.m{font-size:12px;color:var(--mut);direction:ltr;text-align:right}
.path{font-size:12px;background:#f3efe0;border-radius:8px;padding:4px 8px;margin:6px 0;direction:ltr;text-align:left;word-break:break-all}
.st{font-weight:900;font-size:13px;margin-top:8px;color:var(--em)}.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:4px}
.chip{padding:5px 12px;border-radius:99px;border:2px solid var(--line);background:#fff;font:700 13px Cairo;color:var(--ink)}.chip.on{background:var(--em);border-color:var(--em);color:#fff}
.row{display:flex;gap:8px;align-items:center;margin-top:10px;flex-wrap:wrap}
.tier{padding:7px 16px;border-radius:12px;border:2px solid var(--line);background:#fff;font:900 14px Cairo}.tier.f.on{background:#1FA571;color:#fff;border-color:#1FA571}.tier.p.on{background:var(--gold);color:#fff;border-color:var(--gold)}
input[type=number]{width:90px;padding:7px;border:2px solid var(--line);border-radius:10px;font:700 15px Cairo}
.foot{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:3px solid var(--gold);padding:10px 12px;display:flex;gap:8px;align-items:center}
.foot .s{flex:1;font-weight:700;font-size:14px}.btn{padding:10px 16px;border-radius:12px;border:0;font:900 15px Cairo;background:var(--em);color:#fff}.btn.w{background:#fff;color:var(--em);border:2px solid var(--em)}
</style></head><body>
<header><h1>خريطة كتب ركن التأسيس</h1><p>كل ملف: مكانه الآن، مجاني أو مدفوع، والسعر. عدّل ثم نزّل الملف وأرسله لي.</p></header>
<div class="bar" id="bar"></div><main id="main"></main>
<div class="foot"><div class="s" id="stat"></div><button class="btn w" id="rst">تراجع</button><button class="btn" id="dl">⬇ تنزيل التعديلات</button></div>
<script>
const STAGES=__STAGES__;const ORIG=__DATA__;const KEY='ang.booksmap.v1';
let S=JSON.parse(JSON.stringify(ORIG));try{const k=JSON.parse(localStorage.getItem(KEY)||'null');if(k&&k.files)S=k}catch(e){}
let flt='map';const N=n=>String(n).replace(/\d/g,d=>'٠١٢٣٤٥٦٧٨٩'[d]);
const SN={};STAGES.forEach(s=>{SN[s[0]]=s[1];s[2].forEach(k=>SN[s[0]+':'+k[0]]=s[1]+' · '+k[1])});
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
const orig=id=>ORIG.files.find(f=>f.id===id);
const key=f=>JSON.stringify([f.ar,f.tier,f.tier==='paid'?f.price:0,[...f.place].sort()]);
const dirty=f=>key(f)!==key(orig(f.id));
function path(f){return f.tier==='paid'?'private: paid/'+f.id+'.pdf<br>public sample: pdf/samples/'+f.id+'.pdf':'public: pdf/'+f.id+'.pdf'}
function card(f){const d=dirty(f);let h=`<div class="card${d?' dirty':''}" data-id="${f.id}"><div class="t">${f.ar}</div><div class="m">${f.en} · ${f.pages}p · ${f.mb}MB · ${f.id}</div><div class="path">${path(f)}</div>`;
STAGES.forEach(s=>{h+=`<div class="st">${s[1]}</div><div class="chips">`+s[2].map(k=>{const p=s[0]+':'+k[0];return `<button class="chip${f.place.includes(p)?' on':''}" data-p="${p}">${k[1]}</button>`}).join('')+`</div>`});
h+=`<div class="row"><button class="tier f${f.tier==='free'?' on':''}" data-t="free">مجاني</button><button class="tier p${f.tier==='paid'?' on':''}" data-t="paid">مدفوع</button>`;
if(f.tier==='paid')h+=`<input type="number" min="1" inputmode="numeric" value="${f.price||''}" placeholder="اختياري"> ريال <small>(فارغ = السعر عبر واتساب)</small>`;
h+=`</div>${!f.place.length?'<div style="color:#b3261e;font-size:13px;margin-top:6px">⚠ غير موجود في أي قسم</div>':''}</div>`;return h}
function mapView(){let h='<p style="padding:6px 14px;font-size:13px;color:var(--mut)">كل أيقونة في الموقع وعدد الكتب تحتها. اضغط على اسم كتاب لتعديله.</p>';
STAGES.forEach(s=>{h+=`<div class="card"><div class="t" style="font-size:18px;color:var(--em)">${s[1]}</div>`;
s[2].forEach(k=>{const p=s[0]+':'+k[0];const L=S.files.filter(f=>f.place.includes(p));if(!L.length){h+=`<div class="st" style="font-size:15px;color:#9aa5a0;opacity:.7;pointer-events:none">${k[1]} — ٠ كتب (فارغ)</div>`;return}h+=`<div class="st" style="font-size:15px">${k[1]} — ${N(L.length)} ${L.length>10||L.length===0?'كتاب':L.length===1?'كتاب':L.length===2?'كتابان':'كتب'}</div><div class="chips">`+(L.map(f=>`<button class="chip" data-one="${f.id}">${f.ar}${f.tier==='paid'?' 💰':''}</button>`).join('')||'<span style="color:var(--mut);font-size:13px">فارغ</span>')+'</div>'});h+='</div>'});
const no=S.files.filter(f=>!f.place.length);if(no.length)h+=`<div class="card"><div class="t" style="color:#b3261e">بلا قسم</div><div class="chips">`+no.map(f=>`<button class="chip" data-one="${f.id}">${f.ar}</button>`).join('')+'</div></div>';return h}
function render(){if(flt==='map'){$('#main').innerHTML=mapView();bar();render_stat();return}const L=S.files.filter(f=>flt.startsWith('one:')?f.id===flt.slice(4):flt==='all'||(flt==='paid'&&f.tier==='paid')||(flt==='free'&&f.tier==='free')||(flt==='chg'&&dirty(f))||(flt==='none'&&!f.place.length)||f.place.some(p=>p.split(':')[0]===flt));
$('#main').innerHTML=L.map(card).join('')||'<p style="padding:24px;text-align:center">لا يوجد</p>';
render_stat();bar()}
function bar(){const T=[['map','🗺 الأقسام'],['all','كل الكتب'],['chg','المعدَّل'],['none','بلا قسم'],['free','مجاني'],['paid','مدفوع']].concat(STAGES.map(s=>[s[0],s[1]]));
$('#bar').innerHTML=T.map(t=>`<button class="${flt===t[0]?'on':''}" data-f="${t[0]}">${t[1]}</button>`).join('')}
const $=q=>document.querySelector(q);
$('#bar').onclick=e=>{const b=e.target.closest('button');if(b){flt=b.dataset.f;render()}};
$('#main').onclick=e=>{const o=e.target.closest('[data-one]');if(o){flt='one:'+o.dataset.one;render();scrollTo(0,0);return}const c=e.target.closest('.card');if(!c)return;const f=S.files.find(x=>x.id===c.dataset.id);const b=e.target.closest('button');if(!b)return;
if(b.dataset.p){const i=f.place.indexOf(b.dataset.p);i<0?f.place.push(b.dataset.p):f.place.splice(i,1)}else if(b.dataset.t){f.tier=b.dataset.t;if(f.tier==='free')f.price=0}else return;save();rerender(c,f)};
$('#main').oninput=e=>{const c=e.target.closest('.card');if(!c)return;const f=S.files.find(x=>x.id===c.dataset.id);f.price=Math.max(0,+e.target.value||0);save();c.classList.toggle('dirty',dirty(f));const cc=S.files.filter(dirty).length;$('#stat').textContent=N(S.files.length)+' ملف · '+N(S.files.filter(f=>f.tier==='paid').length)+' مدفوع · '+N(cc)+' تعديل'};
function rerender(c,f){const t=document.createElement('div');t.innerHTML=card(f);c.replaceWith(t.firstElementChild);render_stat()}
function render_stat(){const c=S.files.filter(dirty).length;$('#stat').textContent=N(S.files.length)+' ملف · '+N(S.files.filter(f=>f.tier==='paid').length)+' مدفوع · '+N(c)+' تعديل'}
$('#rst').onclick=()=>{if(confirm('إلغاء كل تعديلاتك؟')){S=JSON.parse(JSON.stringify(ORIG));save();render()}};
$('#dl').onclick=()=>{const out={app:'anglomania-books-map',date:new Date().toISOString().slice(0,10),waNumber:S.waNumber,changes:S.files.filter(dirty).map(f=>({id:f.id,from:{ar:orig(f.id).ar,tier:orig(f.id).tier,price:orig(f.id).price,place:orig(f.id).place},to:{ar:f.ar,tier:f.tier,price:f.tier==='paid'?f.price:0,place:f.place}})),files:S.files};
const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(out,null,1)],{type:'application/json'}));a.download='anglomania-books-edit.json';a.click()};
render();
</script></body></html>'''
out=HTML.replace('__STAGES__',json.dumps(STAGES,ensure_ascii=False)).replace('__DATA__',json.dumps(cat,ensure_ascii=False))
open(os.path.join(R,'books-map.html'),'w',encoding='utf-8').write(out)
print('ok',len(out))
