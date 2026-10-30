"""Visual and machine-readable QR regression for LingoTech v4.4."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import base64, io, json
import cv2, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'test-output'
OUT.mkdir(exist_ok=True)
CANONICAL='https://williamlovecs.github.io/lingotech/'
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',8774),partial(Handler,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
report={'version':'4.4','engines':{},'url':CANONICAL}
def scan(im):
 rgb=np.asarray(im.convert('RGB'))
 val,_,_=cv2.QRCodeDetector().detectAndDecode(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR))
 return val
def picture(page):
 payload=page.locator('#poster').evaluate('(e)=>e.toDataURL("image/png").split(",")[1]')
 return Image.open(io.BytesIO(base64.b64decode(payload))).convert('RGB')
try:
 with sync_playwright() as playwright:
  for name in ['chromium','webkit']:
   browser=getattr(playwright,name).launch(headless=True)
   page=browser.new_page(viewport={'width':1300,'height':940},device_scale_factor=1,accept_downloads=True)
   errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
   result={'decoded_ratios':[],'render_checks':0,'qr_toggle':None,'page_errors':errors}
   report['engines'][name]=result
   try:
    page.goto('http://127.0.0.1:8774/lingotech/?utm_source=chatgpt.com&v=4.4',wait_until='load')
    page.wait_for_function('window.LingoTechQA44 && window.LingoTechQA43')
    assert '?' not in page.url
    assert page.evaluate('LingoTechQA44.destination')==CANONICAL
    page.locator('#demoBtn').click();page.wait_for_function('PhotoBoothQA.snapshot().ready')
    assert page.locator('#showQr44').is_checked()
    result['render_checks']=page.evaluate("""()=>{const names=['build','crew','ideas','studio','night','friends','play'];let count=0;for(const template of names)for(const ratio of ['post','story','landscape'])for(const memoryStrip of [false,true]){const W=ratio==='landscape'?1620:1080,H=ratio==='landscape'?1080:ratio==='story'?1920:1350;let c=document.createElement('canvas');let output=LingoTechQA43.render(c,{template,ratio,memoryStrip,showQr44:true,nickname:'一起来创造值得分享的回忆',role:'Creator'});const e=Math.round(Math.min(W,H)*.035),x=W-e-215,y=H-e-225;const overlaps=output.textBoxes.filter(b=>b.text!=='扫码制作同款'&&b.text!=='SCAN TO MAKE YOURS'&&b.x<x+215&&b.x+b.w>x&&b.y<y+225&&b.y+b.h>y);if(overlaps.length)throw Error('QR/text overlap '+template+' '+ratio+' '+JSON.stringify(overlaps));if(output.r.y+output.r.h>y)throw Error('QR/photo overlap '+template+' '+ratio);count++;c.width=c.height=1;}return count;}""")
    for ratio in ['landscape','post','story']:
     page.locator(f'[data-ratio="{ratio}"]').click();page.wait_for_function('PhotoBoothQA.snapshot().ready')
     im=picture(page);assert scan(im)==CANONICAL,(name,ratio,'full image not scannable')
     thumb=im.copy();thumb.thumbnail((720,100000));assert scan(thumb)==CANONICAL,(name,ratio,'720px social image not scannable')
     im.save(OUT/f'{name}-qr-{ratio}.png')
     if ratio=='landscape':
      im.save(OUT/f'{name}-qr-export.jpg',quality=85,subsampling=2)
      assert scan(Image.open(OUT/f'{name}-qr-export.jpg'))==CANONICAL
     result['decoded_ratios'].append(ratio)
    page.locator('#showQr44').uncheck();page.wait_for_function('PhotoBoothQA.snapshot().ready')
    without=picture(page);assert scan(without)=='', 'QR still on after user disabled it'
    page.locator('#showQr44').check();page.wait_for_function('PhotoBoothQA.snapshot().ready')
    assert scan(picture(page))==CANONICAL
    result['qr_toggle']='passed'
    page.locator('#previewBtn').click();page.wait_for_function('document.querySelector("#resultImage").naturalWidth>0')
    assert page.locator('#qrExportHint44').is_visible()
    with page.expect_download() as download:page.locator('#modalDownload').click()
    download.value.save_as(OUT/f'{name}-shared.jpg')
    assert scan(Image.open(OUT/f'{name}-shared.jpg'))==CANONICAL
    assert not errors,errors
    result['status']='passed'
   except Exception as exc:
    result.update(status='failed',error=str(exc))
    page.screenshot(path=str(OUT/f'{name}-qr-FAIL.png'),full_page=True)
    raise
   finally:
    browser.close()
 report['status']='passed'
 (OUT/'qr-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False,indent=2))
finally:
 server.shutdown()
