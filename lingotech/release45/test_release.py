"""v4.5 user-flow/QR/privacy regression. Native sharing is mocked, never sent.
Run with LT_ENGINES=chromium LT_CHROMIUM=/usr/bin/chromium locally,
or use the installed Playwright chromium + webkit in CI.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
import base64, json, os, traceback, re, hashlib
import cv2
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'test-output';OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a): pass
server=ThreadingHTTPServer(('127.0.0.1',8766),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
URL='http://127.0.0.1:8766/lingotech/'
img=Image.new('RGB',(1200,800),'#e2edfa');d=ImageDraw.Draw(img)
for rect,color in [((0,0,110,110),'red'),((1090,0,1200,110),'green'),((0,690,110,800),'blue'),((1090,690,1200,800),'yellow')]:d.rectangle(rect,fill=color)
d.text((330,350),'SYNTHETIC PRIVACY TEST PHOTO',fill='black');img.save(OUT/'synthetic.png')
INIT="""window.__calls=[];window.__shareMode='ok';window.__accept='image/jpeg';
Object.defineProperty(navigator,'canShare',{configurable:true,value:p=>p.files?p.files.every(f=>f.type===__accept):true});
Object.defineProperty(navigator,'share',{configurable:true,value:p=>{__calls.push({keys:Object.keys(p),types:(p.files||[]).map(f=>f.type)});if(__shareMode==='pending')return new Promise(r=>window.__resolveShare=r);if(__shareMode==='fail')return Promise.reject(new DOMException('failure','NotAllowedError'));if(__shareMode==='cancel')return Promise.reject(new DOMException('cancel','AbortError'));return Promise.resolve();}});"""
report={'version':'4.5','engines':{},'real_device_wechat':'NOT TESTED. Mocks do not confirm installed targets or actual posting.'}
def ready(page):
 page.wait_for_function('window.PhotoBoothQA && PhotoBoothQA.snapshot().ready',timeout=20000);page.wait_for_timeout(80)
def state(page):return page.evaluate('PhotoBoothQA.snapshot()')
def close_export(page):
 if page.locator('#exportModal').is_visible():page.locator('#closeExport').click()
def load(page):page.locator('#fileInput').set_input_files(str(OUT/'synthetic.png'));ready(page)
def decode(path):
 value=cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(path)))[0]
 assert value=='https://williamlovecs.github.io/lingotech/',('QR decode',str(path),value)
try:
 with sync_playwright() as pw:
  for engine in os.getenv('LT_ENGINES','chromium,webkit').split(','):
   options={'headless':True}
   if engine=='chromium' and os.getenv('LT_CHROMIUM'):options['executable_path']=os.environ['LT_CHROMIUM'];options['args']=['--no-sandbox']
   browser=getattr(pw,engine).launch(**options)
   context=browser.new_context(viewport={'width':1440,'height':1000},locale='en-US',accept_downloads=True,reduced_motion='reduce')
   context.add_init_script(INIT);page=context.new_page();errors=[];requests=[]
   page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append((r.method,r.url)))
   r={'checks':[]};report['engines'][engine]=r
   def ok(name):r['checks'].append(name)
   try:
    page.goto(URL+'?v=4.4&utm_source=chatgpt.com',wait_until='load');page.wait_for_function('window.LingoTechQA45');page.wait_for_timeout(500)
    assert page.url==URL
    assert state(page)['language']=='en' and page.locator('.version').inner_text()=='v4.5'
    assert page.locator('#headerJoin45').is_visible() and page.locator('#homeJoin45').is_visible()
    assert page.locator('#homeJoin45').get_attribute('href')=='https://ncncpg6l01bx.feishu.cn/share/base/shrcnZix9z8F9hvu5z0Oxnye0xc'
    ok('auto English; optional verified next-event CTA; clean URL')
    images=page.locator('#landingPhoto1,#landingPhoto2,.community-gallery img').evaluate_all('(es)=>es.map(e=>({src:e.src,loaded:e.complete&&e.naturalWidth>0}))')
    assert len(images)==5 and len({x['src'] for x in images})==5 and all(x['loaded'] for x in images);ok('five unique original photos load')
    page.locator('#languageBtn').click();assert state(page)['language']=='zh';page.reload();page.wait_for_function('window.LingoTechQA45');assert state(page)['language']=='zh';ok('manual language persists without photo storage')
    page.locator('#setupBtn').click();page.locator('#localCounts45').check();page.locator('#closeSetup').click()
    assert page.evaluate('LingoTechQA45.counts().enabled')
    load(page);page.locator('#personal summary').click();page.locator('#nickname').fill('PRIVATE-DO-NOT-STORE');ready(page)
    for scene in ('friends','play','build'):
     page.locator(f'[data-scene="{scene}"]').click();ready(page);assert state(page)['own'] and state(page)['nickname']=='PRIVATE-DO-NOT-STORE'
    ok('scene switches retain owned photo and nickname')
    geometry=page.evaluate("""()=>{let cases=0,errors=[];for(const scene of ['build','friends','play'])for(const template of ['build','crew','ideas','studio','night','friends','play'])for(const ratio of ['post','story','landscape'])for(const memoryStrip of [false,true])for(const showQr44 of [false,true]){const c=document.createElement('canvas');const r=LingoTechQA43.render(c,{scene,template,ratio,memoryStrip,showQr44,nickname:'这是用于检验边缘和二维码避让的四十字以内中文测试内容',role:'Creator'});for(const b of r.textBoxes)if(b.x<8||b.y<8||b.x+b.w>c.width-8||b.y+b.h>c.height-8)errors.push({scene,template,ratio,memoryStrip,showQr44,b});if(showQr44){const e=Math.round(Math.min(c.width,c.height)*.035),q={x:c.width-e-215,y:c.height-e-225,w:215,h:225};if(r.r.x<q.x+q.w&&r.r.x+r.r.w>q.x&&r.r.y<q.y+q.h&&r.r.y+r.r.h>q.y)errors.push({photoOverlapsQr:true,scene,template,ratio});for(const b of r.textBoxes)if(!b.text.startsWith('SCAN TO')&&!b.text.startsWith('扫码')&&b.x<q.x+q.w&&b.x+b.w>q.x&&b.y<q.y+q.h&&b.y+b.h>q.y)errors.push({textOverlapsQr:true,scene,template,ratio,b});}cases++;c.width=c.height=1;}return{cases,errors};}""")
    assert not geometry['errors'],geometry['errors'][:2];r['render_cases']=geometry['cases'];ok('all scenes/frames/ratios/strip/QR safe bounds and isolation')
    for width in (320,375,390,430,768,1024,1440):
     page.set_viewport_size({'width':width,'height':900});page.wait_for_timeout(100)
     for ratio in ('post','story','landscape'):
      page.locator(f'[data-ratio="{ratio}"]').click();ready(page)
      dims=page.evaluate("""()=>{const a=document.querySelector('#stage').getBoundingClientRect(),b=document.querySelector('#poster').getBoundingClientRect();return{overflow:document.documentElement.scrollWidth-innerWidth,inside:b.left>=a.left-1&&b.right<=a.right+1&&b.top>=a.top-1&&b.bottom<=a.bottom+1}}""")
      assert dims['overflow']<=1 and dims['inside'],(width,ratio,dims)
    ok('seven responsive widths and three ratios')
    page.set_viewport_size({'width':1440,'height':1000})
    for ratio in ('post','story','landscape'):
     page.locator(f'[data-ratio="{ratio}"]').click();ready(page)
     data=page.locator('#poster').evaluate('(c)=>c.toDataURL("image/png").split(",")[1]');path=OUT/f'{engine}-{ratio}.png';path.write_bytes(base64.b64decode(data));decode(path)
     small=Image.open(path);small=small.resize((720,round(small.height*720/small.width)));p=OUT/f'{engine}-{ratio}-720.jpg';small.save(p,quality=80);decode(p)
    ok('real QR decoded at native resolution and 720px JPEG for all ratios')
    page.locator('#previewBtn').click();page.wait_for_function('document.querySelector("#resultImage").naturalWidth>0')
    assert page.locator('#exportJoin45').is_visible()
    with page.expect_download() as download:page.locator('#modalDownload').click()
    path=OUT/f'{engine}-export.jpg';download.value.save_as(path);decode(path)
    with page.expect_download() as download:page.locator('#savePng').click()
    path=OUT/f'{engine}-export.png';download.value.save_as(path);decode(path)
    close_export(page);ok('export JPG/PNG contain genuine QR; signup remains optional')
    page.locator('#shareBtn').click();page.wait_for_timeout(150);assert page.evaluate('__calls.at(-1).keys')==['files'];assert page.evaluate('__calls.at(-1).types')==['image/jpeg'];close_export(page)
    page.evaluate("__accept='image/png'");page.locator('#shareBtn').click();page.wait_for_timeout(150);assert page.evaluate('__calls.at(-1).types')==['image/png'];close_export(page)
    page.evaluate("__shareMode='cancel'");page.locator('#shareBtn').click();page.wait_for_timeout(150);assert not page.locator('#exportModal').is_visible() and state(page)['ready']
    page.evaluate("__shareMode='fail'");page.locator('#shareBtn').click();page.wait_for_timeout(150);assert page.locator('#wechatGuide').is_visible();close_export(page)
    page.evaluate("__shareMode='pending'");page.locator('#shareBtn').click();page.locator('#clearBtn').click();page.evaluate('__resolveShare()');page.wait_for_timeout(250);assert not page.locator('#exportModal').is_visible() and state(page)['sourceState']=='empty';ok('native-share success/cancel/fail/PNG fallback and late callback privacy guard (mocked)')
    load(page);page.locator('#showQr44').uncheck();page.locator('#personal summary').click();page.locator('#nickname').fill('PRIVATE-DO-NOT-STORE');ready(page)
    page.locator('#previewBtn').click();page.locator('#nextVisitor45').click();page.wait_for_timeout(150)
    snap=page.evaluate('LingoTechQA45.snapshot()');assert not snap['hasExport'] and not snap['hasDataUrl'] and not snap['cameraActive'] and snap['qr'];assert state(page)['nickname']=='' and not page.locator('#resultImage').get_attribute('src');ok('next visitor clears photo/name/export buffers and resets QR')
    page.locator('#setupBtn').click();page.locator('#boothMode45').check();assert not page.locator('#setupModal').is_visible();assert page.locator('#kioskBanner45').is_visible()
    load(page);page.evaluate('LingoTechQA45.checkIdleAt(Date.now()+161000)');assert page.locator('#idleWarning45').is_visible();page.locator('#keepSession45').click();assert not page.locator('#idleWarning45').is_visible() and state(page)['own']
    page.evaluate('LingoTechQA45.checkIdleAt(Date.now()+181000)');assert state(page)['sourceState']=='empty' and page.evaluate('LingoTechQA45.snapshot().qr');ok('kiosk warning/continue/3-minute expiry')
    page.reload();page.wait_for_function('window.LingoTechQA45');assert page.evaluate('LingoTechQA45.snapshot().kiosk') and state(page)['language']=='en';ok('kiosk persists per tab; new visitor gets automatic language')
    page.goto('http://127.0.0.1:8766/lingotech-photo-booth/?v=old&utm_source=old&kiosk=1',wait_until='load');page.wait_for_function('window.LingoTechQA45');assert page.url==URL and page.evaluate('LingoTechQA45.snapshot().kiosk');ok('legacy URL redirects to canonical clean URL')
    storage=page.evaluate('JSON.stringify({...localStorage})');assert 'PRIVATE-DO-NOT-STORE' not in storage and 'data:image' not in storage and 'synthetic.png' not in storage
    stats=page.evaluate('LingoTechQA45.counts()');assert stats['scope']=='THIS_BROWSER_ONLY' and not stats['networkCollection'];assert all(k in ['page_open','photo_selected','sample_opened','photo_prepared','save_requested','share_requested','share_handed_to_system','share_cancelled','share_failed','share_fallback','join_clicked','partner_clicked','session_cleared','idle_cleared'] for day in stats['days'].values() for k in day)
    assert all(method=='GET' and url.startswith('http://127.0.0.1:8766/') for method,url in requests),requests;ok('no upload/telemetry requests; no personal data in local storage')
    assert page.evaluate('LingoTechShareDiagnostics().app')=='LingoTech Photo Booth 4.5';ok('diagnostics identify v4.5')
    page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(OUT/f'{engine}-home-mobile.png'),full_page=True)
    load(page);page.screenshot(path=str(OUT/f'{engine}-editor-mobile.png'),full_page=True)
    assert not errors,errors
    # Fresh context must not inherit shared booth mode or opt-in counters.
    other=browser.new_context(locale='zh-CN',viewport={'width':390,'height':844});p2=other.new_page();p2.goto(URL);p2.wait_for_function('window.LingoTechQA45');assert p2.evaluate('LingoTechQA45.snapshot().language')=='zh';assert not p2.evaluate('LingoTechQA45.snapshot().kiosk') and not p2.evaluate('LingoTechQA45.counts().enabled');other.close();ok('new visitor: Chinese detection, kiosk off, counters off')
    blocked=browser.new_context(locale='en-US');blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError')}});Object.defineProperty(window,'sessionStorage',{get(){throw new DOMException('blocked','SecurityError')}});")
    p3=blocked.new_page();errs=[];p3.on('pageerror',lambda e:errs.append(str(e)));p3.goto(URL);p3.wait_for_function('window.LingoTechQA45');assert p3.evaluate('LingoTechQA45.snapshot().language')=='en';p3.locator('#languageBtn').click();assert p3.evaluate('LingoTechQA45.snapshot().language')=='zh';assert not errs,errs;blocked.close();ok('blocked browser storage does not break editor or language switching')
    r.update(status='passed',page_errors=errors)
   except Exception as exc:
    r.update(status='failed',error=str(exc),traceback=traceback.format_exc(),page_errors=errors)
    page.screenshot(path=str(OUT/f'{engine}-FAIL.png'),full_page=True)
    raise
   finally:
    (OUT/'test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));browser.close()
 report['status']='passed';(OUT/'test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
finally:server.shutdown()
