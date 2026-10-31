# يولّد صفحات ثابتة لكل منهج (للفهرسة في Google) من بيانات index.html.
# التشغيل: python3 tools/dump_curricula.py && python3 tools/gen_curricula_pages.py
import json, os, html
D = json.load(open('/tmp/curricula-data.json'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://anglomaniaedu.com'
G = {g['id']: g for g in D['grades']}
SYS = {s['id']: s for s in D['systems']}
SLUG = {'sa': 'saudi', 'kw': 'kuwait', 'om': 'oman', 'eg': 'egypt', 'ae': 'uae', 'bh': 'bahrain'}
SERIES = {'sa': 'We Can وTop Goal وSuper Goal وMega Goal', 'eg': 'Connect Plus', 'kw': '', 'om': '', 'ae': '', 'bh': 'LOOK وIMPACT وREFLECT'}
e = html.escape

def grades_of(sid):
    return sorted([g for g in D['grades'] if g['system'] == sid and g['id'] in D['books']], key=lambda g: g['num'])

def sections(sid):
    out = []
    gs = grades_of(sid)
    done = False
    for g in gs:
        if sid == 'sa' and g['num'] in (11, 12):
            if done: continue
            done = True
            books = list(D['books']['g11'])
            out.append(('الصفان الثاني والثالث الثانوي — المسارات الأربعة (العام، الشرعي، إدارة الأعمال، علوم الحاسب والهندسة)', books))
            continue
        name = g['ar']['name']
        if sid == 'sa' and g['num'] == 10: name += ' (السنة المشتركة)'
        out.append((name, D['books'][g['id']]))
    out = [(n, [b for b in bs if 'بوابة عين' not in b['title']['ar']]) for n, bs in out]
    return out

def rng(sid):
    n = [g['num'] for g in grades_of(sid)]
    return (min(n), max(n)) if n else (0, 0)

CSS = """:root{--green:#0F4A3A;--gold:#C8A23A;--ivory:#FEFDF5;--ink:#17302A;--muted:#5c6b66;--line:#e4dfc9}
*{box-sizing:border-box}body{margin:0;background:var(--ivory);color:var(--ink);font-family:Cairo,system-ui,sans-serif;line-height:1.8}
.wrap{max-width:860px;margin:0 auto;padding:0 16px 40px}
header.top{background:var(--green);color:#fff;padding:18px 16px;border-bottom:4px solid var(--gold)}
header.top .in{max-width:860px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
header.top a{color:#fff;text-decoration:none;font-weight:700}
.crumbs{font-size:.9rem;color:var(--muted);margin:16px 0 0}.crumbs a{color:var(--green)}
h1{font-size:1.7rem;line-height:1.5;margin:10px 0 6px;color:var(--green)}
.lead{color:var(--muted);margin:0 0 18px}
h2{font-size:1.2rem;margin:26px 0 8px;padding-inline-start:10px;border-inline-start:4px solid var(--gold)}
ul.books{list-style:none;margin:0;padding:0;display:grid;gap:8px}
ul.books a{display:block;padding:12px 14px;border:2px solid var(--line);border-radius:14px;background:#fff;color:var(--ink);text-decoration:none}
ul.books a:hover,ul.books a:focus{border-color:var(--gold)}
ul.books b{display:block}ul.books small{color:var(--muted)}
.cta{display:inline-block;margin:22px 0 6px;padding:12px 20px;background:var(--green);color:#fff;border-radius:14px;text-decoration:none;font-weight:700}
nav.more{margin-top:28px;padding-top:16px;border-top:1px solid var(--line)}nav.more a{display:inline-block;margin:4px 0 4px 10px;color:var(--green)}
.note{font-size:.88rem;color:var(--muted);margin-top:24px}footer{margin-top:30px;color:var(--muted);font-size:.85rem}"""

def page(title, desc, h1, lead, body, path, crumbs, extra_ld=''):
    url = SITE + path
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(crumbs)]}
    cr = ' ‹ '.join('<a href="%s">%s</a>' % (e(p), e(n)) for n, p in crumbs[:-1]) + ' ‹ ' + e(crumbs[-1][0])
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="ar_SA">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta name="theme-color" content="#0F4A3A">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="in"><a href="/">أنجلومانيا · Anglomania</a><a href="/curricula/">كتب المناهج</a></div></header>
<main class="wrap">
<p class="crumbs">{cr}</p>
<h1>{e(h1)}</h1>
<p class="lead">{e(lead)}</p>
{body}
<footer><p>© 2026 أنجلومانيا — anglomaniaedu.com</p></footer>
</main>
</body>
</html>
"""

def more_nav(cur):
    links = ''.join('<a href="/curricula/%s/">%s</a>' % (SLUG[s], e(SYS[s]['ar']['name'])) for s in SLUG if s != cur)
    return '<nav class="more" aria-label="مناهج أخرى"><strong>مناهج أخرى:</strong><br>' + links + '</nav>'

NOTE = '<p class="note">حقوق الكتب محفوظة للجهات التعليمية الرسمية. هذه الصفحة تجمع الروابط لتسهيل الوصول إلى الكتب فقط. تتوفر الكتب على المنصة بنقرة واحدة لكل صف.</p>'

pages = {}
for sid, slug in SLUG.items():
    secs = sections(sid)
    lo, hi = rng(sid)
    name = SYS[sid]['ar']['name']
    total = sum(1 for _, bs in secs for b in bs if 'بوابة عين' not in b['title']['ar'])
    body = ''
    for gname, books in secs:
        items = ''.join('<li><a href="%s" rel="noopener" target="_blank"><b>%s</b><small>%s</small></a></li>' % (
            e(b['link']), e(b['title']['ar']), e((b.get('description') or {}).get('ar', ''))) for b in books)
        body += '<section><h2>%s</h2><ul class="books">%s</ul></section>' % (e(gname), items)
    if sid == 'sa':
        body += '<section><h2>المصدر الرسمي</h2><ul class="books"><li><a href="https://www.ien.edu.sa/Home/Dashbord" rel="noopener" target="_blank"><b>بوابة عين — كتب اللغة الإنجليزية</b><small>بوابة عين ← تحميل الكتب</small></a></li></ul></section>'
    body += '<a class="cta" href="/">افتح المنصة واختر صفك</a>' + more_nav(sid) + NOTE
    series = SERIES.get(sid)
    desc = 'كتب اللغة الإنجليزية في %s من الصف %d إلى الصف %d%s. روابط كتاب الطالب لكل صف من المصادر الرسمية، على منصة أنجلومانيا.' % (
        name, lo, hi, (': ' + series) if series else '')
    pages[slug] = (page('كتب اللغة الإنجليزية — %s (الصفوف %d–%d) | أنجلومانيا' % (name, lo, hi), desc,
                        'كتب اللغة الإنجليزية — %s' % name,
                        'كتاب الطالب لكل صف من الصف %d إلى الصف %d. اضغط على الكتاب ليفتح مباشرة.' % (lo, hi),
                        body, '/curricula/%s/' % slug,
                        [('أنجلومانيا', '/'), ('كتب المناهج', '/curricula/'), (name, '/curricula/%s/' % slug)]), total)

hub = '<ul class="books">' + ''.join('<li><a href="/curricula/%s/"><b>%s</b><small>%s</small></a></li>' % (
    s, e(SYS[i]['ar']['name']), 'الصفوف %d–%d · %d كتابًا' % (rng(i)[0], rng(i)[1], pages[s][1])) for i, s in SLUG.items()) + '</ul>' + NOTE
pages['_hub'] = (page('كتب المناهج الدراسية للغة الإنجليزية — السعودي والكويتي والعُماني والمصري والإماراتي | أنجلومانيا',
                      'كتب اللغة الإنجليزية للمناهج السعودية والكويتية والعُمانية والمصرية والإماراتية، لكل صف، بروابط مباشرة من المصادر الرسمية على منصة أنجلومانيا.',
                      'كتب مناهج اللغة الإنجليزية', 'اختر المنهج لترى كتب كل صف.', hub, '/curricula/',
                      [('أنجلومانيا', '/'), ('كتب المناهج', '/curricula/')]), 0)

for slug, (h, _) in pages.items():
    d = os.path.join(ROOT, 'curricula') if slug == '_hub' else os.path.join(ROOT, 'curricula', slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(h)

urls = ['/', '/curricula/'] + ['/curricula/%s/' % s for s in SLUG.values()]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    '  <url><loc>%s%s</loc><lastmod>2026-10-24</lastmod></url>\n' % (SITE, u) for u in urls) + '</urlset>\n'
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
print({k: v[1] for k, v in pages.items()})
