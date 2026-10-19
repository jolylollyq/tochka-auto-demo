from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import sys,json,os
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parent.parent
errors=[]
base=os.environ.get('SITE_URL','http://localhost:4321')
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1,reduced_motion='reduce')
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(base,wait_until='networkidle')
    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
    for img in page.locator('img[src]').all():
        if img.get_attribute('src'):
            img.scroll_into_view_if_needed()
            img.evaluate('(e)=>e.decode()')
            assert img.evaluate('(e)=>e.complete && e.naturalWidth>0')
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(root/'screenshots/01-desktop.png'))
    page.locator('#works').scroll_into_view_if_needed()
    page.screenshot(path=str(root/'screenshots/02-works.png'))
    page.get_by_role('button',name='Тормоза',exact=True).click()
    expect(page.locator('.work-card:visible')).to_have_count(1)
    page.locator('[data-case="0"]').click()
    expect(page.locator('#case-dialog')).to_be_visible()
    expect(page.locator('#dialog-title')).to_have_text('Торможение без вибрации')
    page.keyboard.press('Escape')
    expect(page.locator('#case-dialog')).not_to_be_visible()
    page.get_by_role('button',name='Все работы').click()
    expect(page.locator('.work-card:visible')).to_have_count(3)
    page.locator('.service summary').first.click()
    page.locator('[data-service="Диагностика"]').click()
    expect(page.locator('select[name="service"]')).to_have_value('Диагностика')
    page.locator('#booking').scroll_into_view_if_needed()
    page.screenshot(path=str(root/'screenshots/03-booking.png'))
    page.locator('button[type="submit"]').click()
    expect(page.locator('#form-result')).not_to_be_visible()
    page.locator('input[name="name"]').fill('Демо клиент')
    page.locator('input[name="phone"]').fill('+7 (000) 000-00-00')
    requests=[]
    page.on('request',lambda r:requests.append(r.url) if r.method=='POST' else None)
    page.locator('button[type="submit"]').click()
    expect(page.locator('#form-result')).to_be_visible()
    assert requests==[],requests
    expect(page.locator('input[name="name"]')).to_have_value('')
    page.locator('#form-reset').click()
    expect(page.locator('#form-result')).not_to_be_visible()
    for width in [390,320,768]:
        page.set_viewport_size({'width':width,'height':844})
        page.goto(base,wait_until='networkidle')
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'),f'Overflow at {width}'
        if width==390:
            page.screenshot(path=str(root/'screenshots/04-mobile.png'))
            page.screenshot(path=str(root/'screenshots/05-mobile-full.png'),full_page=True)
            page.get_by_role('button',name='Открыть меню').click()
            expect(page.locator('#navigation')).to_be_visible()
            page.locator('#navigation').get_by_text('Контакты',exact=True).click()
            expect(page.locator('#navigation')).not_to_be_visible()
    print(json.dumps({'result':'PASS','viewports':[1440,768,390,320],'checks':['images','no overflow','case filters','dialog and Escape','service selection','invalid form','valid demo form without network submission','mobile menu'],'pageErrors':errors},ensure_ascii=False,indent=2))
    assert errors==[],errors
    browser.close()
