"""Additional camera and release-contract tests; never submit forms or native shares."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent/'test-output';OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',8768),partial(Quiet,directory=str(ROOT)));Thread(target=server.serve_forever,daemon=True).start()
URL='http://127.0.0.1:8768/lingotech/';report={'version':'4.5.1','engines':{},'real_device_wechat':'not tested','feishu_submissions':0}
try:
 with sync_playwright() as p:
  for engine in ['chromium','webkit']:
   browser=getattr(p,engine).launch(headless=True)
   context=browser.new_context(locale='zh-CN',viewport={'width':390,'height':844},accept_downloads=True)
   page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   row={'checks':[]};report['engines'][engine]=row
   try:
    page.goto(URL);page.wait_for_function('window.LingoTechQA451');assert page.locator('link[rel=canonical]').count()==1
    assert page.locator('meta[property="og:image"]').get_attribute('content').endswith('/og-v451.png');assert (ROOT/'lingotech/og-v451.png').stat().st_size>1000
    row['checks'].append('one canonical, correct social preview metadata')
    page.evaluate("navigator.mediaDevices.getUserMedia=async()=>{throw new DOMException('denied','NotAllowedError')}")
    page.locator('#cameraBtn').click();page.wait_for_function("document.querySelector('#cameraWait').innerText.includes('权限')")
    assert page.locator('#fallbackCamera').is_visible() and not page.evaluate('LingoTechQA45.snapshot().cameraActive')
    assert page.locator('#liveCamera').evaluate('e=>getComputedStyle(e).objectFit')=='contain'
    page.locator('#closeCamera').click();row['checks'].append('denied camera handled; full-frame preview CSS; fallback visible')
    page.evaluate("window.__stopped=0;navigator.mediaDevices.getUserMedia=()=>new Promise(r=>window.__grant=r)")
    page.locator('#cameraBtn').click();page.locator('#closeCamera').click();page.evaluate("__grant({getTracks:()=>[{stop:()=>__stopped++}]})")
    page.wait_for_function('__stopped===1');assert page.locator('#cameraModal').is_hidden() and not page.evaluate('LingoTechQA45.snapshot().cameraActive')
    row['checks'].append('late camera authorization after close stops tracks')
    page.locator('#fileInput').set_input_files({'name':'not-a-photo.png','mimeType':'image/png','buffer':b'not an image'})
    page.wait_for_timeout(300);assert page.locator('#fileError').is_visible();assert not page.evaluate('PhotoBoothQA.snapshot().ready')
    row['checks'].append('invalid photo file rejected')
    page.locator('#demoBtn').click();page.wait_for_function('PhotoBoothQA.snapshot().ready')
    assert page.locator('#communityControls').is_hidden()
    page.locator('[data-scene=friends]').click();page.wait_for_function('PhotoBoothQA.snapshot().ready');assert page.locator('#communityControls').is_visible()
    page.locator('#memoryStrip').check();page.wait_for_function('PhotoBoothQA.snapshot().ready')
    page.locator('[data-scene=build]').click();page.wait_for_function('PhotoBoothQA.snapshot().ready');assert page.locator('#communityControls').is_hidden() and not page.locator('#memoryStrip').is_checked()
    row['checks'].append('AI scene intentionally hides decorations; switching resets optional historical strip')
    page.locator('#personal summary').click();page.locator('#nickname').fill('PRIVATE_SENTINEL_451');page.wait_for_function('PhotoBoothQA.snapshot().ready')
    page.locator('#setupBtn').click()
    with page.expect_download() as dl:page.locator('#downloadConfigured').click()
    dest=OUT/f'{engine}-configured.html';dl.value.save_as(dest);saved=dest.read_text()
    assert 'PRIVATE_SENTINEL_451' not in saved and 'data:image' in saved and 'app-version" content="4.5.1' in saved
    row['checks'].append('configured HTML excludes visitor nickname and retains current version')
    assert not errors,errors;row['status']='passed'
   except Exception as e:
    row.update(status='failed',error=str(e),page_errors=errors);page.screenshot(path=str(OUT/f'{engine}-FAIL.png'),full_page=True);raise
   finally:
    (OUT/'extra-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));browser.close()
  browser=p.chromium.launch(headless=True,args=['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
  context=browser.new_context(locale='en-US',permissions=['camera']);page=context.new_page();page.goto(URL);page.wait_for_function('window.LingoTechQA451')
  page.locator('#cameraBtn').click();page.wait_for_function('!document.querySelector("#snapPhoto").disabled',timeout=20000)
  dims=page.locator('#liveCamera').evaluate('(e)=>({w:e.videoWidth,h:e.videoHeight,fit:getComputedStyle(e).objectFit})');assert dims['fit']=='contain'
  page.locator('#snapPhoto').click();page.wait_for_function('PhotoBoothQA.snapshot().ready')
  snap=page.evaluate('PhotoBoothQA.snapshot()');assert snap['own'] and snap['photo']['width']==dims['w'] and snap['photo']['height']==dims['h']
  assert not page.evaluate('LingoTechQA45.snapshot().cameraActive')
  report['fake_camera']={'status':'passed','raw_dimensions':dims,'captured_dimensions':snap['photo'],'scope':'Chromium synthetic camera only'}
  browser.close()
 report['status']='passed';print(json.dumps(report,ensure_ascii=False,indent=2))
finally:
 (OUT/'extra-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));server.shutdown()
