from playwright.sync_api import sync_playwright
from pathlib import Path
root=Path(__file__).resolve().parent.parent
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    page.goto('http://localhost:4321',wait_until='networkidle')
    page.screenshot(path=str(root/'screenshots/desktop-first.png'))
    print('TITLE',page.title())
    print('OVERFLOW',page.evaluate('document.documentElement.scrollWidth > innerWidth'))
    page.on('console',lambda msg: print('CONSOLE',msg.type,msg.text))
    page.on('pageerror',lambda error: print('ERROR',str(error)))
    page.goto('http://localhost:4321/admin/',wait_until='networkidle')
    page.wait_for_timeout(5000)
    print('CMS',page.locator('body').inner_text())
    page.screenshot(path=str(root/'screenshots/cms-inspect.png'))
    browser.close()
