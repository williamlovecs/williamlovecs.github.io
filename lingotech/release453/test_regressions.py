"""Focused v4.5.3 regressions: localized alternatives, resize health and compressed QR.
Uses a synthetic local photo. No physical device or native sharing is implied.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
import base64, cv2, io, json, numpy as np, os

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'test-output'
OUT.mkdir(exist_ok=True)
HTML = (ROOT.parent / 'index.html').read_text(encoding='utf-8')
ENGINE = os.getenv('BROWSER', 'chromium')
PHOTO = OUT / 'regression-synthetic.jpg'
im = Image.new('RGB', (1200, 800), '#d7eaff')
d = ImageDraw.Draw(im)
d.rectangle((0, 0, 100, 100), fill='red')
d.text((350, 380), 'SYNTHETIC REGRESSION PHOTO', fill='black')
im.save(PHOTO)
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'
results = []

with sync_playwright() as pw:
    browser = getattr(pw, ENGINE).launch(headless=True)
    def load():
        context = browser.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, locale='zh-CN', user_agent=UA, reduced_motion='reduce')
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.set_content(HTML, wait_until='load')
        page.locator('#fileInput').set_input_files(str(PHOTO))
        page.wait_for_function('window.LingoTechQA453?.snapshot().jpgReady', timeout=20000)
        return context, page, errors
    def case(name, fn):
        context, page, errors = load()
        row = {'test':name, 'engine':ENGINE}
        try:
            fn(page)
            assert not errors, errors
            row['passed'] = True
        except Exception as exc:
            row.update(passed=False, error=str(exc), pageErrors=errors)
            page.screenshot(path=str(OUT / f'{ENGINE}-{name}-FAILED.png'), full_page=True)
        finally:
            results.append(row)
            print(('PASS' if row['passed'] else 'FAIL'), ENGINE, name, flush=True)
            context.close()
            (OUT / f'{ENGINE}-regression-report.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
    try:
        def viewer_alt_zh(page):
            page.locator('#previewBtn').click()
            page.locator('#modalDownload').click()
            assert page.locator('#photoViewer453').is_visible()
            actual = page.locator('#viewerImage453').get_attribute('alt')
            assert actual == '长按这张成片保存到相册', actual
        case('viewer-alt-zh', viewer_alt_zh)

        def result_alt_after_language_switch(page):
            page.locator('#languageBtn').click()
            page.locator('#previewBtn').click()
            actual = page.locator('#resultImage').get_attribute('alt')
            assert actual == 'Touch and hold this framed photo to save', actual
        case('result-alt-after-language-switch', result_alt_after_language_switch)

        def resize_without_observer_error(page):
            for width, height in [(390,844),(844,390),(390,844)]:
                page.set_viewport_size({'width':width,'height':height})
                page.wait_for_timeout(500)
                assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
        case('resize-without-observer-error', resize_without_observer_error)

        def compressed_qr_decodes(page):
            data = page.evaluate("""()=>{const c=document.createElement('canvas');LingoTechQA43.render(c,{scene:'build',template:'night',ratio:'post',memoryStrip:true,showQr44:true,nickname:'中文与English edge test 123',role:'Creator'});return c.toDataURL('image/png').split(',')[1];}""")
            with Image.open(io.BytesIO(base64.b64decode(data))) as source:
                im = source.convert('RGB')
                im = im.resize((720, round(im.height * 720 / im.width)))
                stream = io.BytesIO()
                im.save(stream, format='JPEG', quality=80)
            (OUT / f'{ENGINE}-night-strip-720.jpg').write_bytes(stream.getvalue())
            pixels = cv2.imdecode(np.frombuffer(stream.getvalue(), np.uint8), cv2.IMREAD_COLOR)
            actual = cv2.QRCodeDetector().detectAndDecode(pixels)[0]
            assert actual == 'https://williamlovecs.github.io/lingotech/', actual
        case('night-strip-720-jpeg-qr', compressed_qr_decodes)
    finally:
        browser.close()

if any(not row['passed'] for row in results):
    raise SystemExit(1)
