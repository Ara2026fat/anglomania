import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg=await b.new_page()
        await pg.goto('file:///home/claude/anglomania/index.html'); await pg.wait_for_timeout(1500)
        d=await pg.evaluate('''()=>{const C=ANG.config;const out={systems:C.systems,grades:C.grades.map(g=>({id:g.id,num:g.num,system:g.system,stage:g.stage,ar:g.ar,en:g.en})),books:{}};
          C.grades.forEach(g=>{const c=(C.content[g.id]&&C.content[g.id].all&&C.content[g.id].all.curricula)||[];if(c.length)out.books[g.id]=c;});return out;}''')
        json.dump(d,open('/tmp/curricula-data.json','w'),ensure_ascii=False,indent=1)
        print([ (k,len(v)) for k,v in d['books'].items()][:60]); print(d['systems']); print(sorted({g['system'] for g in d['grades']}))
        await b.close()
asyncio.run(main())
