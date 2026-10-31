# يولّد ملف PDF للجوال لدورة المعلمين (تجهيز المعلم لفرص التدريس في الخليج)
# التشغيل: python3 tools/gen_teacher_course_pdf.py
import asyncio, os, re
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'courses', 'teacher-course-gulf.pdf')
src = open(os.path.join(ROOT, 'tools', 'gen_ideas_pdf.py'), encoding='utf-8').read()
CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)
CSS += '.cr{background:#fff;border:.5mm solid #E4DFC9;border-inline-start:2.4mm solid var(--c);border-radius:3mm;padding:1.8mm 3.4mm;line-height:1.5}.cr b{font-size:4.3mm;color:#0F4A3A;margin-inline-end:2mm}.cr span{font-size:4.1mm}.cb{gap:2.4mm!important}'

def pg(label, inner, cls='', ic='🎓', c='#0F4A3A', t='#fff', bd='#C8A23A', cnt=''):
    return ('<section class="page %s" style="--c:%s;--t:%s;--bd:%s"><div class="bg1"></div><div class="bg2"></div>'
            '<div class="top"><span class="ic">%s</span><span class="lb">%s</span>%s<span class="lg"></span></div>'
            '<div class="body">%s</div><div class="ft"><span>دورة أنجلومانيا للمعلمين</span></div></section>'
            % (cls, c, t, bd, ic, label, ('<span class="cnt">%s</span>' % cnt) if cnt else '', inner))

def bl(items): return ''.join('<div class="bl"><span>%s</span></div>' % x for x in items)
def row(l, x, hook=False): return '<div class="row%s"><b>%s</b><span>%s</span></div>' % (' hook' if hook else '', l, x)
def h2(x, s=False): return '<div class="h2%s">%s</div>' % (' s' if s else '', x)

P = []
def L(u): return '<bdi dir="ltr" style="font-size:3.4mm;color:#9E7E22">%s</bdi>' % u
P.append('<section class="page cover"><div class="mk"></div><div class="bar"></div><h1>دورة تجهيز المعلم<br>لفرص التدريس في الخليج</h1>'
         '<p>جهّز نفسك لفرصتك<br>مع أساسيات الذكاء الاصطناعي لمعلم الإنجليزية<br>يقدّمها المستر حسام</p>'
         '<div class="k"><span>10 مقاعد فقط</span><span>4 جلسات على الزوم</span><span>الدفعة الأولى</span></div>'
         '<div class="sg">ARAFAT ALRAJHI © 2026</div></section>')

P.append(pg('لماذا ولمن؟', h2('فجوة نريد أن نسدّها', True)
    + bl(['كثير من معلمي الإنجليزية بينهم وبين الذكاء الاصطناعي <b>فجوة كبيرة</b>، وهو يختصر ساعات التحضير ويحسّن التواصل مع الأهل.',
          'والمعلم الذي يريد فرصة في دولة خليجية يحتاج أن يعرف <b>ماذا يُطلب منه</b> وكيف يعرض نفسه ويستعد للمقابلة.',
          '<b>لمن؟</b> معلم الإنجليزية الذي يريد التدريس في إحدى دول الخليج، مقيمًا أو عن بُعد، ولو بدأ مع الذكاء الاصطناعي من الصفر.',
          '<span class="note">الدورة تدريب وتجهيز. القرار النهائي في التوظيف بيد الجهة المُوظِّفة.</span>']), ic='💡'))

P.append(pg('الذكاء الاصطناعي', h2('ست مهارات عملية من الصفر', True)
    + bl(['<b>كتابة الطلب الجيد</b> للأداة بنتيجة تصلح للصف.',
          '<b>تحضير الدرس:</b> خطة درس من وحدة الكتاب في دقائق.',
          '<b>أوراق عمل واختبارات</b> بمستويات مختلفة.',
          '<b>ملاحظات على كتابة الطلاب</b> تراجعها أنت.',
          '<b>رسائل لأولياء الأمور:</b> تقارير وتنبيهات مهذبة وواضحة.',
          '<b>السيرة والمقابلة:</b> تحسين سيرتك والتدرّب على الأسئلة.',
          '<span class="note">بقواعد واضحة: لا بيانات طلاب في الأداة، وكل مخرج تراجعه قبل إرساله.</span>']), ic='🤖', cls='dense'))

def cr(n, t, u): return '<div class="cr"><b>%s</b><span>%s</span> %s</div>' % (n, t, L(u))
P.append(pg('متطلبات التدريس', h2('ما تأكدنا منه رسميًا', True)
    + cr('🇦🇪 الإمارات', 'بكالوريوس في التخصص، ورخصة معلم مهنية، وتصديق الشهادات، وحسن سيرة.', 'u.ae')
    + cr('🇴🇲 عُمان', 'المدرسة تقدّم الطلب. مؤهلات وخبرة موثقة وIELTS أو TOEFL.', 'gov.om')
    + cr('🇧🇭 البحرين', 'المدرسة تقدّم الطلب. تحقق من المؤهلات والخبرة وحسن سيرة.', 'bahrain.bh')
    + cr('🇸🇦 السعودية', 'رخصة مهنية من هيئة تقويم التعليم. تحقق هل تلزمك.', 'etec.gov.sa')
    + cr('🇰🇼 الكويت', 'خدمة «التعاقد للهيئة التعليمية» في بوابة الوزارة.', 'eservices.moe.edu.kw')
    + cr('🇶🇦 قطر', 'وظائف لغير القطريين ورخصة مهنية عبر الوزارة.', 'edu.gov.qa')
    + '<span class="note">آخر مراجعة: 27 أكتوبر 2026. تأكد من الجهة الرسمية قبل أي خطوة.</span>', ic='🧭', cls='cb'))

P.append(pg('الجلسات', h2('4 جلسات على الزوم، 90 دقيقة للجلسة', True)
    + bl(['<b>1 — الفرص والمتطلبات:</b> أنواع المدارس، وكيف تتحقق من متطلبات دولتك وتبحث عن فرصة.',
          '<b>2 — الذكاء الاصطناعي من الصفر:</b> الأساسيات وتحضير الدروس.',
          '<b>3 — الأوراق والاختبارات وأولياء الأمور:</b> نبني ورقة عمل واختبارًا ورسائل جاهزة.',
          '<b>4 — ملفك ومقابلتك:</b> السيرة، وأسئلة المقابلة، ودرس تجريبي مع ملاحظاتنا.']), ic='🗓️'))

P.append(pg('ماذا تخرج به؟', h2('ستة أشياء بين يديك', True)
    + bl(['قائمة تحقق لمتطلبات التدريس في الخليج وطريقة تحديثها.',
          'سيرة ذاتية محسّنة للتقديم في الخليج.',
          '10 أسئلة مقابلة مع إجاباتك المجهّزة.',
          'حزمة وحدة جاهزة: درس وورقة عمل واختبار قصير.',
          '5 قوالب رسائل لأولياء الأمور.',
          'مكتبة أوامر جاهزة، وشهادة حضور من أنجلومانيا.']), ic='🎁', cls='dense'))

P.append(pg('التسجيل', h2('الدفعة الأولى', True)
    + bl(['<b>المقاعد:</b> 10 فقط، والأولوية بحسب التسجيل.',
          '<b>المقدّم:</b> المستر حسام، بالشراكة مع أنجلومانيا.',
          '<b>الجلسات:</b> مباشرة على الزوم مع تسجيل للمشاركين، وتمرين بعد كل جلسة، ومجموعة متابعة.',
          '<b>الرسوم:</b> رمزية للدفعة الأولى، وتُعلن مع فتح التسجيل.',
          '<b>الدفع:</b> بالتحويل البنكي، والتأكيد عبر واتساب.',
          '<span class="note">anglomaniaedu.com</span>']), ic='📝', cls='dense'))

async def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc = '<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(P))
    tmp = os.path.join(ROOT, 'courses', '_c.html')
    open(tmp, 'w', encoding='utf-8').write(doc)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg_ = await b.new_page()
        await pg_.goto('file://' + tmp); await pg_.evaluate("document.fonts.ready"); await pg_.wait_for_timeout(400)
        await pg_.evaluate("document.querySelectorAll('.page').forEach(p=>{const b=p.querySelector('.body'); if(b && b.scrollHeight>b.clientHeight+1) p.classList.add('tight')})")
        await pg_.evaluate("document.querySelectorAll('.page.tight').forEach(p=>{const b=p.querySelector('.body'); if(b && b.scrollHeight>b.clientHeight+1) p.classList.add('tighter')})")
        bad = await pg_.evaluate("[...document.querySelectorAll('.page')].map((p,i)=>{const b=p.querySelector('.body');return b&&b.scrollHeight>b.clientHeight+1?i+1:null}).filter(Boolean)")
        await pg_.pdf(path=OUT, width='120mm', height='213mm', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
        print('pages', await pg_.evaluate("document.querySelectorAll('.page').length"), 'overflow', bad)
        await b.close()
    os.remove(tmp)
asyncio.run(main())
