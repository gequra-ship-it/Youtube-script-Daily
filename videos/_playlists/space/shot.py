import os
from playwright.sync_api import sync_playwright
d=os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':1920,'height':1080}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    for n,name in [('A','bite-sized-knowledge-space'),('B','deep-dives-space')]:
        pg.goto(f'file://{d}/{n}.html'); pg.wait_for_timeout(600)
        print(n,pg.evaluate("document.fonts.check('700 100px Fredoka')"))
        pg.screenshot(path=f'{d}/{name}.png'); print(os.path.getsize(f'{d}/{name}.png'))
    print(errs)
