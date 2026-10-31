# يولّد PDF للجوال (صفحة لكل فكرة) من بيانات ideas-partners/index.html
# التشغيل: python3 tools/gen_ideas_pdf.py
import asyncio, html, os
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'ideas-partners', 'index.html')
OUT = os.path.join(ROOT, 'ideas-partners', 'anglomania-ideas.pdf')
e = html.escape
EF = {'S': 'سهلة', 'M': 'متوسطة', 'L': 'كبيرة'}
COL = {'start': '#C8A23A', 'dev': '#0F4A3A', 'mkt': '#166B53', 'bold': '#C8A23A', 'risk': '#8A6D17', 'cur': '#0F4A3A'}
INK = {'start': '#2b2204', 'bold': '#2b2204'}  # لون نص على الذهبي
BD = {'start': '#0F4A3A', 'bold': '#0F4A3A'}   # خط سفلي للشريط العلوي
LOGO = 'file:///home/claude/fonts/logo.png'
ICO = {'start': '🚀', 'dev': '🛠️', 'mkt': '📣', 'bold': '💡', 'risk': '🛡️', 'cur': '📚'}

CSS = """
@font-face{font-family:Cairo;src:url("file:///home/claude/fonts/Cairo.ttf");font-weight:200 1000;font-style:normal}
@page{size:120mm 213mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html{direction:rtl}
body{font-family:Cairo,'DejaVu Sans',system-ui,sans-serif;color:#17302A;counter-reset:pg}
.page{width:120mm;height:213mm;overflow:hidden;position:relative;break-after:page;page-break-after:always;background:#FEFDF5;counter-increment:pg;display:flex;flex-direction:column}
.page:last-child{break-after:auto;page-break-after:auto}
.bg1,.bg2{position:absolute;border-radius:50%;background:var(--c);opacity:.10;pointer-events:none}
.bg1{width:90mm;height:90mm;top:-30mm;left:-35mm}
.bg2{width:70mm;height:70mm;bottom:-22mm;right:-25mm}
.top{background:var(--c);color:var(--t,#fff);padding:7mm 8mm 6mm;position:relative;display:flex;align-items:center;gap:3mm;border-bottom:2mm solid var(--bd,#C8A23A)}
.top .ic{font-size:8mm;line-height:1}
.top .lg{width:11mm;height:11mm;border-radius:50%;background:#FEFDF5 url("file:///home/claude/fonts/logo.png") center 42%/235% no-repeat;border:.6mm solid rgba(255,255,255,.6);flex:none}
.top .lb{font-weight:800;font-size:4.6mm;flex:1}
.top .cnt{background:rgba(255,255,255,.25);border-radius:99px;padding:.6mm 3.4mm;font-weight:800;font-size:3.8mm}
.body{flex:1;padding:7mm 8mm 3mm;display:flex;flex-direction:column;gap:4.6mm;position:relative;min-height:0}
.num{width:15mm;height:15mm;border-radius:50%;background:#C8A23A;color:#3b2f06;font-weight:800;font-size:7mm;display:grid;place-items:center;box-shadow:0 1.2mm 0 #9E7E22}
.hd{display:flex;gap:4mm;align-items:center}
h1.t{font-size:8.6mm;line-height:1.35;font-weight:800;color:#0F4A3A}
.desc{font-size:5.4mm;line-height:1.65;color:#2c4a42}
.chips{display:flex;flex-wrap:wrap;gap:2mm}
.chip{font-size:4.3mm;font-weight:800;padding:1mm 3.6mm;border-radius:99px;background:#F6EFD6;color:#9E7E22}
.chip.g{background:#E3F1EB;color:#166B53}.chip.r{background:#F3E3B5;color:#7A5F12}.chip.b{background:#DDEBE4;color:#0F4A3A}.chip.s{background:#C8A23A;color:#3b2f06}
.imp{display:flex;align-items:center;gap:2.4mm;font-weight:800;font-size:4.5mm;color:#5C6B66}
.imp i{width:5.4mm;height:5.4mm;border-radius:50%;background:#E4DFC9;display:block}
.imp i.on{background:var(--c)}
.row{background:#fff;border:.5mm solid #E4DFC9;border-inline-start:2.4mm solid var(--c);border-radius:3.8mm;padding:3.4mm 4.6mm}
.row b{display:block;font-size:4.1mm;color:#9E7E22;margin-bottom:.4mm}
.row span{font-size:5.2mm;line-height:1.6}
.row.hook{background:var(--c);color:var(--t,#fff);border-color:var(--c);position:relative}
.row.hook b{color:var(--t,#fff);opacity:.85}
.row.hook span{font-weight:800;font-size:5.7mm}
.row.hook::after{content:"”";position:absolute;inset-inline-start:2mm;top:-1.5mm;font-size:16mm;line-height:1;opacity:.22}
.ft{padding:2.4mm 8mm 4mm;display:flex;justify-content:space-between;font-size:3.3mm;color:#5C6B66;font-weight:700;position:relative}
.ft::after{content:counter(pg);background:#0F4A3A;color:#C8A23A;border-radius:99px;padding:0 3mm;font-weight:800}
/* غلاف وفواصل */
.cover{background:linear-gradient(160deg,#0F4A3A,#0b3a2d);color:#fff;justify-content:center;align-items:center;text-align:center;gap:6mm;padding:12mm}
.cover .mk{width:62mm;height:62mm;border-radius:9mm;background:#FEFDF5 url("file:///home/claude/fonts/logo.png") center/112% no-repeat;box-shadow:0 2mm 0 #C8A23A}
.cover h1{font-size:11mm;line-height:1.25;font-weight:800}
.cover p{font-size:4.6mm;color:#E9E2C8;line-height:1.7}
.cover .k{display:flex;flex-wrap:wrap;gap:2.5mm;justify-content:center}
.cover .k span{background:rgba(255,255,255,.14);border:.4mm solid rgba(200,162,58,.6);border-radius:99px;padding:1.2mm 4mm;font-size:4mm;font-weight:800}
.cover .sg{font-size:3.6mm;color:#C8A23A;font-weight:800;letter-spacing:.3mm;margin-top:6mm}
.cover .bar{width:40mm;height:1.6mm;background:#C8A23A;border-radius:9px}
.div{background:var(--c);color:var(--t,#fff);justify-content:center;align-items:center;text-align:center;padding:14mm;gap:6mm}
.div .big{font-size:30mm;line-height:1}
.div h1{font-size:11mm;font-weight:800;line-height:1.3}
.div p{font-size:5mm;line-height:1.7;opacity:.95}
.div .cn{background:rgba(255,255,255,.25);border-radius:99px;padding:1.2mm 6mm;font-size:5mm;font-weight:800}
.div .ft{position:absolute;bottom:0;inset-inline:0;color:var(--t,#fff)}
.div .ft::after{background:rgba(0,0,0,.25);color:var(--t,#fff)}
/* قوائم كبيرة */
.li{display:flex;gap:3.5mm;align-items:center;background:#fff;border:.5mm solid #E4DFC9;border-inline-start:2.2mm solid var(--c);border-radius:3.5mm;padding:3mm 4mm}
.li .n{flex:none;width:9.5mm;height:9.5mm;border-radius:50%;background:#C8A23A;color:#3b2f06;font-weight:800;font-size:4.8mm;display:grid;place-items:center}
.li .tx{font-size:5.2mm;font-weight:800;color:#0F4A3A;line-height:1.45;flex:1}
.li small{display:block;font-weight:600;font-size:3.6mm;color:#5C6B66}
.bl{display:flex;gap:3mm;background:#fff;border:.5mm solid #E4DFC9;border-radius:3.8mm;padding:4mm 4.6mm;font-size:5.3mm;line-height:1.6}
.bl::before{content:"";flex:none;width:3.2mm;height:3.2mm;border-radius:50%;background:var(--c);margin-top:2.3mm}
.bl b{color:#0F4A3A}
.h2{font-size:7.4mm;font-weight:800;color:#0F4A3A;line-height:1.4}
.pl{display:inline-block;background:#F6EFD6;color:#0F4A3A;font-weight:800;border-radius:2mm;padding:0 2mm;font-size:3.8mm;margin-inline-start:2mm}
.dense .li{padding:1.8mm 3mm;gap:3mm}.dense .li .n{width:8mm;height:8mm;font-size:4.2mm}.dense .li .tx{font-size:4.4mm;line-height:1.35}.dense .li small{font-size:3.3mm}.dense .body{gap:2.3mm}
.tight .desc{font-size:4.7mm}.tight .row span{font-size:4.5mm}.tight .row{padding:2.5mm 4mm}.tight .body{gap:3.2mm}.tight h1.t{font-size:7.4mm}.tight .row.hook span{font-size:5mm}.tight .chip{font-size:3.8mm}.tight .bl{font-size:4.6mm;padding:3mm 4mm}
.tighter .desc{font-size:4.3mm}.tighter .row span{font-size:4.1mm}.tighter .row.hook span{font-size:4.6mm}.tighter .row{padding:2mm 3.6mm}.tighter .body{gap:2.4mm}.tighter h1.t{font-size:6.8mm}.tighter .row b{font-size:3.5mm}.tighter .chip{font-size:3.5mm}
.meta{display:flex;flex-direction:column;gap:2.4mm}.two .meta{flex-direction:row;flex-wrap:wrap;align-items:center;gap:1.2mm 2.5mm}
.card{display:flex;flex-direction:column;gap:4.6mm}
.sep{height:.7mm;background:#C8A23A;opacity:.55;border-radius:9px;flex:none}
.two .body{padding-top:4.5mm;gap:3mm;justify-content:space-evenly}
.two .card{gap:2.3mm}.two .num{width:10.5mm;height:10.5mm;font-size:5mm;box-shadow:0 .8mm 0 #9E7E22}.two h1.t{font-size:6.1mm;line-height:1.3}.two .hd{gap:3mm}
.two .desc{font-size:3.9mm;line-height:1.5}.two .row{padding:1.2mm 3.2mm}.two .row b{font-size:3.2mm;margin:0}.two .row span{font-size:3.8mm;line-height:1.45}.two .row.hook span{font-size:4.1mm}.two h1.t{font-size:5.6mm}.two .num{width:9.5mm;height:9.5mm;font-size:4.6mm}
.two .chip{font-size:3.4mm;padding:.5mm 2.8mm}.two .imp{font-size:3.6mm}.two .imp i{width:4mm;height:4mm}.two .chips{gap:1.5mm}
.h2.s{font-size:6mm}.tighter .bl{font-size:4.1mm;padding:2mm 3.4mm}
.big1 .desc{font-size:6mm}.big1 .row span{font-size:5.8mm}.big1 .row.hook span{font-size:6.2mm}.big1 h1.t{font-size:9.4mm}.big1 .chip{font-size:4.7mm}.big1 .row b{font-size:4.5mm}.big1 .card{gap:5.6mm}.big1 .row{padding:4mm 5mm}
.big2 .desc{font-size:6.6mm}.big2 .row span{font-size:6.4mm}.big2 .row.hook span{font-size:6.8mm}.big2 h1.t{font-size:10mm}.big2 .chip{font-size:5mm}.big2 .row b{font-size:4.9mm}.big2 .card{gap:6.6mm}.big2 .row{padding:5mm 5.4mm}
.tbl{width:100%;border-collapse:collapse;font-size:3.9mm;margin:1mm 0}.tbl th{background:#0F4A3A;color:#fff;padding:1.2mm 1.5mm;font-weight:800}.tbl td{border:.4mm solid #E4DFC9;padding:1.2mm 1.5mm;text-align:center;color:#5C6B66}.tbl td:first-child{text-align:start;font-weight:800;color:#0F4A3A}
.note{font-size:3.7mm;color:#5C6B66;line-height:1.6}
"""

def dots(n, c):
    return '<div class="imp"><span>الأثر</span>' + ''.join('<i class="%s"></i>' % ('on' if i < n else '') for i in range(5)) + '</div>'

def page(key, inner, label, cnt='', cls=''):
    c = COL[key]; t = INK.get(key, '#fff'); bd = BD.get(key, '#C8A23A')
    return ('<section class="page %s" style="--c:%s;--t:%s;--bd:%s"><div class="bg1"></div><div class="bg2"></div>'
            '<div class="top"><span class="ic">%s</span><span class="lb">%s</span>%s<span class="lg"></span></div>'
            '<div class="body">%s</div><div class="ft"><span>مختبر أفكار أنجلومانيا</span></div></section>'
            % (cls, c, t, bd, ICO[key], e(label), ('<span class="cnt">%s</span>' % cnt) if cnt else '', inner))

def divider(key, title, lead, count):
    c = COL[key]; t = INK.get(key, '#fff')
    return ('<section class="page div" style="--c:%s;--t:%s"><div class="bg1" style="opacity:.14"></div><div class="bg2" style="opacity:.14"></div>'
            '<div class="big">%s</div><h1>%s</h1><p>%s</p>%s<div class="ft"><span>مختبر أفكار أنجلومانيا</span></div></section>'
            % (c, t, ICO[key], e(title), lead, ('<div class="cn">%s</div>' % count) if count else ''))

def card(x, i, key):
    chips = ['<span class="chip">الجهد: %s</span>' % EF.get(x['e'], '')]
    if x.get('cost'): chips.append('<span class="chip g">التكلفة: %s</span>' % e(x['cost']))
    if x.get('when'): chips.append('<span class="chip b">التوقيت: %s</span>' % e(x['when']))
    if x.get('late'): chips.append('<span class="chip r">مؤجَّلة</span>')
    if x.get('top') or x.get('star'): chips.append('<span class="chip s">★ ابدأ بها</span>')
    rows = ''
    for lab, tx in x['x']:
        cls = 'row hook' if lab == 'الجملة الجاهزة' else 'row'
        rows += '<div class="%s"><b>%s</b><span>%s</span></div>' % (cls, e(lab), e(tx))
    return ('<div class="card"><div class="hd"><div class="num">%d</div><h1 class="t">%s</h1></div>'
            '<p class="desc">%s</p><div class="meta">%s<div class="chips">%s</div></div>%s</div>'
            % (i, e(x['t']), e(x['d']), dots(x['i'], COL[key]), ''.join(chips), rows))

def bls(items): return ''.join('<div class="bl">%s</div>' % t for t in items)

OTHER = ['m6', 'b4', 'b5']

def sc(n, t, rows):
    r = ''.join('<div class="row"><b>%s</b><span>%s</span></div>' % (l, x) for l, x in rows)
    return '<div class="card"><div class="hd"><div class="num">%s</div><h1 class="t">%s</h1></div>%s</div>' % (n, t, r)

def static_pages(by, TOP):
    P = []
    P.append('<section class="page cover"><div class="mk"></div><div class="bar"></div><h1>مختبر أفكار<br>أنجلومانيا</h1>'
             '<p>أفكار تخدم الطالب والمعلم وولي الأمر<br>مناهج · دروس · أوراق عمل · اختبارات · شروحات</p>'
             '<div class="k"><span>6 أفكار للتنفيذ</span><span>10 للقسم التقني لاحقًا</span><span>3 للبدء</span></div>'
             '<div class="sg">ARAFAT ALRAJHI © 2026</div></section>')
    top4 = [
        ('نماذج اختبارات جاهزة للطباعة', 'لكل صف ووحدة ورقة اختبار نكتب أسئلتها نحن (لا من نصوص الكتب) بشعار أنجلومانيا، يطبعها المعلم أو ولي الأمر.', 'توفر على المعلمين ساعات، وتصلح لاحقًا ملفًا مدفوعًا. نبدأ بـ30 سؤالًا لوحدة واحدة.'),
        ('تذكير الأهل قبل الاختبار', 'قبل كل اختبار بـ7 أيام ثم 3 أيام ثم يوم، نرسل لأولياء الأمور في مجموعات واتساب رسالة قصيرة فيها موعد الاختبار ونشاط مراجعة من 5 دقائق يعمله الأب أو الأم مع ابنهم (مثلًا: اسألوه عن 5 كلمات من الوحدة).', 'الطالب غالبًا بلا جوال ولا مجموعة، فالمخاطَب هو ولي الأمر الذي يتابع مذاكرته. ونبقى حاضرين أمام الأهل في مواسم الاختبارات.'),
        ('لقاء الأهل: 20 دقيقة', 'محاضرة مجانية قصيرة بعنوان «كيف تذاكر مع ابنك الإنجليزي بدون ما تتقن اللغة».', 'تدخلنا مجموعات الأهالي بثقة، وأنسب وقتها قبل الاختبارات بأسبوعين.')]
    cs = [sc(j + 1, t, [('ما هي؟', d), ('لماذا نبدأ بها؟', w)]) for j, (t, d, w) in enumerate(top4)]
    P.append(page('start', cs[0] + '<div class="sep"></div>' + cs[1], 'أفضل 3 أفكار للبدء', '1–2 / 3', 'two'))
    P.append(page('start', cs[2], 'أفضل 3 أفكار للبدء', '3 / 3', 'single'))
    wk = lambda w, goal, items: '<div class="h2 s">%s</div><div class="note">%s</div>%s' % (w, goal, bls(items))
    P.append(page('start', wk('الأسبوع 1 — نجهّز الاختبار', 'الهدف: نموذج اختبار جاهز نقدمه للمعلمين.', ['نكتب 30 سؤالًا لوحدة واحدة ونصمّمها بشعار أنجلومانيا.'])
                  + wk('الأسبوع 2 — نرافق الأهل', 'الهدف: نكون حاضرين قبل الاختبار.', ['نرسل لأولياء الأمور تذكيرات (7 أيام ثم 3 ثم يوم) مع نشاط مراجعة من 5 دقائق.', 'في أي مشاركة: نأخذ موافقة ولي الأمر لا الطفل.']), 'خطة 30 يومًا'))
    P.append(page('start', wk('الأسبوع 3 — نجهّز لقاء الأهل', 'الهدف: لقاء مجاني قصير جاهز.', ['نحدد موضوع اللقاء وموعده قبل الاختبارات بأسبوعين.', 'نعلن عنه في مجموعات الأهالي.'])
                  + wk('الأسبوع 4 — القياس', 'الهدف: نعرف ما نجح.', ['نراجع الأرقام: كم طلب نموذج الاختبار؟ كم حضر اللقاء؟ ونكمل بما نجح.']), 'خطة 30 يومًا'))
    return P

def tail_pages():
    P = []
    tech = [('مولّد الاختبارات', 'المعلم يختار من بنك أسئلة ويطبع ورقة اختبار بشعار المنصة.'),
            ('تقرير الأحد لولي الأمر', 'المعلم يكتب 3 خانات فيخرج نص مرتب جاهز للإرسال للأهل.'),
            ('ردود واتساب السريعة بالكود', 'يكتب العميل رمز الكتاب (مثل KSA-04: السعودية، الصف الرابع) فيصله رد جاهز بالمواد والأسعار.'),
            ('كود صديقك', 'بطاقة مشاركة برمز لكل طالب، ومن يطلب بالرمز يربح الاثنان ورقة مجانية.'),
            ('ملصق QR في المكتبات', 'يمسح الأهل الرمز على رف الكتاب فيسمعون دروسه.')]
    tech2 = [('بيانات الطلب للناشرين', 'تقرير مجمّع بالكتب الأكثر طلبًا، بلا أسماء ولا أرقام هواتف.'),
             ('شعلة الـ3 دقائق', 'تحدٍّ يومي: 5 كلمات مع صوتها وعدّاد أيام متتالية.'),
             ('دوري المناهج الودّي', 'نقاط أسبوعية يجمعها الطلاب باسم منهجهم ولوحة ترتيب كل جمعة.'),
             ('التصحيح الصوتي بمسودة آلية', 'الطالب يرسل جملته صوتًا، والذكاء الاصطناعي يقترح تصحيحًا يراجعه المعلم قبل الإرسال.'),
             ('الرصيد والفواتير والكوبونات', 'تسجيل الرصيد المدفوع مسبقًا وإصدار الفاتورة. بعد فتح السجل التجاري.')]
    f2 = lambda L: ''.join('<div class="bl"><span><b>%s:</b> %s</span></div>' % (a, b) for a, b in L)
    P.append(page('cur', '<div class="h2 s">🔧 للقسم التقني مستقبلًا (1/2)</div><div class="note">أدوات وتطبيقات تنتظر قسم التحول الرقمي في المنصة.</div>' + f2(tech), 'أفكار مستقبلية', '', 'dense'))
    P.append(page('cur', '<div class="h2 s">🔧 للقسم التقني مستقبلًا (2/2)</div>' + f2(tech2), 'أفكار مستقبلية', '', 'dense'))
    P.append('<section class="page cover"><div class="mk"></div><div class="bar"></div><h1>شكرًا لكم</h1><p>نبني معًا مرجعًا عربيًا منظمًا<br>لتعليم الإنجليزية</p><p style="color:#C8A23A;font-weight:800">anglomaniaedu.com</p><div class="sg">ARAFAT ALRAJHI © 2026</div></section>')
    return P

META = {'dev': ('أفكار تطوير', 'تجربة الطالب والمعلم والأهل والمحتوى والتشغيل.'),
        'mkt': ('للمعلمين والأهل', 'أفكار انتشار وشراكات وتحويل زوار، مع جملة جاهزة لكل فكرة. ما يخص البيع مؤجَّل لما بعد السجل التجاري.'),
        'bold': ('أفكار للدروس', 'أفكار غير تقليدية: تميمة، طريقة تدريس باسمك، مسلسل صوتي، دوري مناهج.')}

def wrap(doc_pages):
    return '<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>مختبر أفكار أنجلومانيا</title><style>%s</style></head><body>%s</body></html>' % (CSS, ''.join(doc_pages))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto('file://' + SRC + '#start')
        data = await pg.evaluate("({D:D,TOP:TOP,TABS:TABS})")
        D = [x for x in data['D'] if x['id'] in OTHER]; TOP = data['TOP']
        by = {x['id']: x for x in data['D']}
        # مرحلة القياس: كل فكرة بنمط «اثنتان في صفحة»
        meas = []
        order = []
        for key in ('dev', 'mkt', 'bold'):
            for i, x in enumerate([x for x in D if x['k'] == key], 1):
                meas.append(page(key, card(x, i, key), META[key][0], '', 'two')); order.append((key, i, x))
        tmp = os.path.join(ROOT, 'ideas-partners', '_pdf.html')
        open(tmp, 'w', encoding='utf-8').write(wrap(meas))
        pg2 = await b.new_page()
        await pg2.goto('file://' + tmp)
        await pg2.evaluate("document.fonts.ready")
        await pg2.wait_for_timeout(400)
        m = await pg2.evaluate("""()=>{const out=[];document.querySelectorAll('.page').forEach(p=>{const b=p.querySelector('.body'),c=p.querySelector('.card');const cs=getComputedStyle(b);
            out.push([c.getBoundingClientRect().height, b.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom)]);});return out}""")
        mm = 96/25.4
        gap = 3*mm + 0.7*mm + 3*mm + 4  # فاصل بين البطاقتين + هامش أمان
        P = static_pages(by, TOP)
        idx = 0
        for key in ('dev', 'mkt', 'bold'):
            items = [o for o in order if o[0] == key]
            title, lead = META[key]
            n = len(items)
            if n == 0: continue
            hs = [(m[idx + j][0], j) for j in range(n)]
            av = m[idx][1]
            srt = sorted(hs); lo, hi = 0, len(srt) - 1; groups = []
            while lo <= hi:
                if lo < hi and srt[hi][0] + srt[lo][0] + gap <= av:
                    groups.append(sorted([srt[hi][1], srt[lo][1]])); lo += 1; hi -= 1
                else:
                    groups.append([srt[hi][1]]); hi -= 1
            groups.sort()
            num = 0
            for g in groups:
                cs = []; labs = []
                for j in g:
                    num += 1; labs.append(num); cs.append(card(items[j][2], num, key))
                if len(g) == 2:
                    P.append(page(key, cs[0] + '<div class="sep"></div>' + cs[1], title, '%d–%d / %d' % (labs[0], labs[1], n), 'two'))
                else:
                    P.append(page(key, cs[0], title, ('%d / %d' % (labs[0], n)) if n > 1 else '', 'single'))
            idx += n
        P += tail_pages()
        open(tmp, 'w', encoding='utf-8').write(wrap(P))
        await pg2.goto('file://' + tmp)
        await pg2.evaluate("document.fonts.ready")
        await pg2.wait_for_timeout(400)
        n = await pg2.evaluate("document.querySelectorAll('.page').length")
        await pg2.evaluate("document.querySelectorAll('.page.single').forEach(p=>{const b=p.querySelector('.body');for(const c of ['big2','big1']){p.classList.add(c);if(b.scrollHeight<=b.clientHeight+1)break;p.classList.remove(c)}})")
        await pg2.evaluate("document.querySelectorAll('.page').forEach(p=>{const b=p.querySelector('.body'); if(b && b.scrollHeight>b.clientHeight+1) p.classList.add('tight')})")
        await pg2.evaluate("document.querySelectorAll('.page.tight').forEach(p=>{const b=p.querySelector('.body'); if(b && b.scrollHeight>b.clientHeight+1) p.classList.add('tighter')})")
        await pg2.pdf(path=OUT, width='120mm', height='213mm', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        bad = await pg2.evaluate("[...document.querySelectorAll('.page')].map((p,i)=>{const b=p.querySelector('.body'); return b && b.scrollHeight>b.clientHeight+1 ? [i+1, p.querySelector('h1,.h2')?.textContent] : null}).filter(Boolean)")
        print('pages', n, 'overflow', bad)
        os.remove(tmp)
        await b.close()

asyncio.run(main())
