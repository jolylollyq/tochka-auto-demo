from playwright.sync_api import sync_playwright, expect
from pathlib import Path
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parent.parent
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.goto('http://localhost:4321/admin/',wait_until='networkidle')
    page.get_by_role('button',name='Войти',exact=True).click()
    page.wait_for_timeout(1500)
    print(page.locator('body').inner_text())
    page.get_by_text('Тексты, услуги и работы',exact=True).click()
    page.wait_for_timeout(1500)
    headline=page.locator('input[id^="headline-field"]')
    original=headline.input_value()
    headline.fill(original+' Тест CMS')
    page.get_by_role('button',name='Опубликовать',exact=True).click()
    page.get_by_text('Опубликовать сейчас',exact=True).click()
    expect(page.get_by_text('ИЗМЕНЕНИЯ СОХРАНЕНЫ',exact=False)).to_be_visible(timeout=15000)
    assert json.loads((root/'src/content/site.json').read_text(encoding='utf-8'))['headline']==original+' Тест CMS'
    preview=browser.new_page()
    preview.goto('http://localhost:4321',wait_until='networkidle')
    expect(preview.locator('h1')).to_have_text(original+' Тест CMS')
    headline.fill(original)
    page.get_by_role('button',name='Опубликовать',exact=True).click()
    page.get_by_text('Опубликовать сейчас',exact=True).click()
    expect(page.get_by_text('ИЗМЕНЕНИЯ СОХРАНЕНЫ',exact=False)).to_be_visible(timeout=15000)
    assert json.loads((root/'src/content/site.json').read_text(encoding='utf-8'))['headline']==original
    print('CMS SAVE / FRONTEND UPDATE / RESTORE: PASSED')
    page.screenshot(path=str(root/'screenshots/cms-editor.png'))
    browser.close()
