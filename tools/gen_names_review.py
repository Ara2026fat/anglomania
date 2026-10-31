#!/usr/bin/env python3
"""names-review.html: final Arabic/English names review for the 38 books (after the owner's classification)."""
import json,re,sys
R='/home/claude/anglomania'
E=json.load(open('/home/claude/review/edit.json',encoding='utf-8'))['files']
EN={ # proposed English names (only where the Arabic name changed or the English was empty/wrong)
'grammar-intermediate-secondary':'Comprehensive Course · Intermediate & Secondary',
'grammar-present-simple-course':'Comprehensive Grammar Course · Intermediate & Secondary',
'translation-course':'Grammar Exercises · Secondary',
'to-be-to-have':'Translation Course',
'adjectives':'Comprehensive Course · Level 2',
'present-simple-continuous':'Tenses Comparison',
'about-yourself-family':'Writing Course · Level 1',
'farm-food':'Translation Course · Level 2',
'tenses-intro':'Dealing with Tenses',
'prepositions':'Comprehensive Grammar Course',
'cvc-dictionary':'Phonics Course for Kids',
'phonics-stories':'Advanced Pronunciation Course',
'sight-words':'Phonics Course · Level 2',
'have-got':'Comprehensive Course · Level 4',
'body-parts-articles':'Comprehensive Course · Level 1',
'indefinite-articles':'Grammar Course · Level 1',
'my-body':'Translation Course · Level 1',
'animals-vocab':'Comprehensive Course · Level 3',
'present-simple-summary':'Tenses Made Simple'}
SP=[('الكتابه','الكتابة'),('الترجمه','الترجمة'),('الاول','الأول'),('الازمنه','الأزمنة'),('الازمنة','الأزمنة'),('مقارنه','مقارنة'),('فونيكس','فونكس'),('للاطفال','للأطفال'),('الاطفال','الأطفال')]
def fix(s):
    s=s.strip()
    for a,b in SP:s=s.replace(a,b)
    return s
rows=[]
for i,f in enumerate(E,1):
    rows.append(dict(n=i,id=f['id'],ar=f['ar'].strip(),sp=fix(f['ar']),en=EN.get(f['id'],f['en']).strip(),tier=f['tier'],place=f['place'],pages=f['pages'],chg=f['id'] in EN))
SEC={'preschool':'ما قبل المدرسة','primary':'ابتدائي','intermediate':'متوسط','secondary':'ثانوي','phonics':'أصوات','grammar':'قواعد','handwriting':'خط','letters':'حروف','translation':'ترجمة','writing':'كتابة','reading':'قراءة'}
H=open(R+'/tools/names_tpl.html',encoding='utf-8').read().replace('__DATA__',json.dumps(rows,ensure_ascii=False)).replace('__SEC__',json.dumps(SEC,ensure_ascii=False))
open(R+'/names-review.html','w',encoding='utf-8').write(H);print(len(rows),sum(r['chg'] for r in rows))
