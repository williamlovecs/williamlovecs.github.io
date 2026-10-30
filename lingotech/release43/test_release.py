"""Chromium + WebKit regression tests. Native sharing is mocked, never sent."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
import base64, json, traceback, shutil
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / 'test-output'
OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = ThreadingHTTPServer(('127.0.0.1', 8765), partial(Quiet, directory=str(ROOT)))
Thread(target=server.serve_forever, daemon=True).start()
URL = 'http://127.0.0.1:8765/lingotech/'
photo = Image.new('RGB', (1200, 800), '#e0e9f5')
draw = ImageDraw.Draw(photo)
for box, color in [((0,0,110,110),'#ff0000'),((1090,0,1200,110),'#00aa00'),((0,690,110,800),'#0000ff'),((1090,690,1200,800),'#ffbb00')]: draw.rectangle(box, fill=color)
draw.text((330,350), 'SYNTHETIC OWNED PHOTO - EDGE TEST', fill='#152449')
photo.save(OUT/'synthetic-owned.png')
INIT = """window.__shares=[];window.__shareMode='ok';window.__accept='image/jpeg';
Object.defineProperty(navigator,'canShare',{configurable:true,value:(p)=>p.files?p.files.every(f=>f.type===window.__accept):true});
Object.defineProperty(navigator,'share',{configurable:true,value:(p)=>{window.__shares.push({keys:Object.keys(p),types:(p.files||[]).map(f=>f.type),sizes:(p.files||[]).map(f=>f.size),url:p.url||null});if(window.__shareMode==='cancel')return Promise.reject(new DOMException('cancel','AbortError'));if(window.__shareMode==='fail')return Promise.reject(new DOMException('fail','NotAllowedError'));return Promise.resolve();}});
Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async(t)=>{window.__copied=t;}}});"""
report={'version':'4.3','engines':{},'physical_device_wechat':'not tested; system targets and delivery cannot be inferred from mocks'}
def ready(page):
    page.wait_for_function('window.PhotoBoothQA && PhotoBoothQA.snapshot().ready', timeout=20000)
    page.wait_for_timeout(70)
def state(page): return page.evaluate('LingoTechQA43.snapshot()')
def close_export(page):
    if page.locator('#exportModal').is_visible(): page.locator('#closeExport').click()
def layout(page):
    return page.evaluate("""()=>{const a=document.querySelector('#stage').getBoundingClientRect(),b=document.querySelector('#poster').getBoundingClientRect();return {a:{x:a.x,y:a.y,r:a.right,b:a.bottom},b:{x:b.x,y:b.y,r:b.right,b:b.bottom},overflow:document.documentElement.scrollWidth-innerWidth}}""")
def assert_layout(page):
    v=layout(page);a,b=v['a'],v['b']
    assert v['overflow']<=1, ('horizontal overflow',v)
    assert b['x']>=a['x']-1 and b['y']>=a['y']-1 and b['r']<=a['r']+1 and b['b']<=a['b']+1, ('canvas clipped',v)
def assert_metrics(s):
    W,H={'post':(1080,1350),'story':(1080,1920),'landscape':(1620,1080)}[s['ratio']]
    for b in s['metrics']:
        assert b['x']>=9 and b['y']>=9 and b['x']+b['w']<=W-9 and b['y']+b['h']<=H-9, ('text outside safe bounds',s['template'],s['ratio'],b)
try:
 with sync_playwright() as p:
  for engine in ('chromium','webkit'):
   browser=getattr(p,engine).launch(headless=True)
   context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1,accept_downloads=True,reduced_motion='reduce')
   context.add_init_script(INIT)
   page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   results={'viewports':[],'frame_ratio_cases':0,'scene_render_cases':0,'share_mock_checks':[]}
   report['engines'][engine]=results
   try:
    page.goto(URL+'?v=4.2&utm_source=chatgpt.com',wait_until='load')
    page.wait_for_function('window.LingoTechQA43');page.wait_for_timeout(700)
    assert '?' not in page.url, page.url
    images=page.locator('#landingPhoto1,#landingPhoto2,.community-gallery img').evaluate_all('(els)=>els.map(e=>({src:e.src,ok:e.complete&&e.naturalWidth>0}))')
    assert len(images)==5 and len({x['src'] for x in images})==5 and all(x['ok'] for x in images), 'hero duplicates or broken images'
    page.screenshot(path=str(OUT/f'{engine}-home-desktop.png'),full_page=True)
    page.locator('#tryPeople').click();ready(page)
    assert state(page)['scene']=='friends' and state(page)['template']=='friends'
    page.locator('[data-scene="play"]').click();ready(page)
    assert state(page)['scene']=='play' and state(page)['template']=='play'
    page.locator('#clearBtn').click()
    page.locator('#demoBtn').click();ready(page)
    assert state(page)['scene']=='build' and state(page)['template']=='build', 'stale scene after clear'
    for template in ('build','crew','ideas','studio','night','friends','play'):
     page.locator(f'[data-template="{template}"]').click()
     for ratio in ('post','story','landscape'):
      page.locator(f'[data-ratio="{ratio}"]').click();ready(page)
      s=state(page);assert s['template']==template and s['ratio']==ratio;assert_metrics(s);assert_layout(page)
      data=page.locator('#poster').evaluate('(c)=>c.toDataURL("image/png").split(",")[1]')
      (OUT/f'{engine}-{template}-{ratio}.png').write_bytes(base64.b64decode(data))
      results['frame_ratio_cases']+=1
    page.locator('#fileInput').set_input_files(str(OUT/'synthetic-owned.png'));ready(page)
    assert state(page)['own'] and not state(page)['demo']
    page.locator('#personal summary').click()
    note='William 与朋友一起创造值得留下的一刻'
    page.locator('#nickname').fill(note);ready(page)
    dims=state(page)['photo']
    for scene in ('friends','play','build'):
     page.locator(f'[data-scene="{scene}"]').click();ready(page)
     s=state(page);assert s['own'] and s['nickname']==note and s['photo']==dims and s['scene']==scene
    metrics=page.evaluate("""()=>{const q=LingoTechQA43;let count=0,errors=[];for(const scene of ['build','friends','play'])for(const template of ['build','crew','ideas','studio','night','friends','play'])for(const ratio of ['post','story','landscape'])for(const memoryStrip of [false,true]){const c=document.createElement('canvas'),r=q.render(c,{scene,template,ratio,memoryStrip,nickname:'这是一句用于边界测试的较长中文文字与名字',role:'Creator'});for(const b of r.textBoxes)if(b.x<9||b.y<9||b.x+b.w>c.width-9||b.y+b.h>c.height-9)errors.push({scene,template,ratio,memoryStrip,b});count++;c.width=1;c.height=1;}return{count,errors}}""")
    assert not metrics['errors'], metrics['errors'][:3];results['scene_render_cases']=metrics['count']
    page.locator('[data-scene="friends"]').click();ready(page)
    oldh=state(page)['frame']['h'];page.locator('#memoryStrip').check();ready(page)
    assert state(page)['memoryStrip'] and state(page)['frame']['h']<oldh
    assert_metrics(state(page));page.locator('#memoryStrip').uncheck();ready(page)
    page.locator('#fitCover').click();page.locator('#zoom').evaluate("e=>{e.value='1.5';e.dispatchEvent(new Event('input',{bubbles:true}));}");ready(page)
    assert state(page)['fit']=='cover';page.locator('#fitContain').click();ready(page)
    page.locator('#rotatePhoto').click();ready(page)
    assert state(page)['photo']['width']==dims['height'] and state(page)['photo']['height']==dims['width']
    page.locator('#languageBtn').click();ready(page);assert state(page)['language']=='en'
    page.locator('#languageBtn').click();ready(page)
    for width in (320,375,390,430,768,1024,1440):
     page.set_viewport_size({'width':width,'height':900});page.wait_for_timeout(130)
     for ratio in ('post','story','landscape'):
      page.locator(f'[data-ratio="{ratio}"]').click();ready(page);assert_layout(page)
     page.locator('#stage').screenshot(path=str(OUT/f'{engine}-stage-{width}.png'))
     results['viewports'].append(width)
    page.set_viewport_size({'width':1440,'height':1000})
    page.locator('#previewBtn').click();page.wait_for_function('document.querySelector("#resultImage").naturalWidth>0')
    assert page.locator('#resultImage').evaluate('(e)=>e.naturalWidth')==1620
    with page.expect_download() as download: page.locator('#savePng').click()
    download.value.save_as(OUT/f'{engine}-export.png')
    assert Image.open(OUT/f'{engine}-export.png').size==(1620,1080)
    with page.expect_download() as download: page.locator('#modalDownload').click()
    download.value.save_as(OUT/f'{engine}-export.jpg')
    assert Image.open(OUT/f'{engine}-export.jpg').size==(1620,1080)
    close_export(page)
    page.locator('#shareBtn').click();page.wait_for_timeout(200)
    call=page.evaluate('__shares.at(-1)');assert call['keys']==['files'] and call['types']==['image/jpeg'] and call['sizes'][0]>0
    results['share_mock_checks'].append('files-only JPEG');close_export(page)
    page.evaluate("__accept='image/png'");page.locator('#shareBtn').click();page.wait_for_timeout(200)
    assert page.evaluate('__shares.at(-1).types[0]')=='image/png';results['share_mock_checks'].append('PNG compatibility fallback');close_export(page)
    page.evaluate("__shareMode='cancel'");page.locator('#shareBtn').click();page.wait_for_timeout(200)
    assert not page.locator('#exportModal').is_visible();assert state(page)['ready'];results['share_mock_checks'].append('cancel preserves photo')
    page.evaluate("__shareMode='fail'");page.locator('#shareBtn').click();page.wait_for_timeout(200)
    assert page.locator('#wechatGuide').is_visible();results['share_mock_checks'].append('failure opens full-image fallback');close_export(page)
    page.evaluate("Object.defineProperty(navigator,'share',{value:undefined,configurable:true})")
    page.locator('#shareBtn').click();page.wait_for_timeout(150);assert page.locator('#wechatGuide').is_visible()
    results['share_mock_checks'].append('unsupported share fallback')
    page.locator('#copyWebsite').click();page.wait_for_timeout(100)
    assert page.evaluate('__copied')=='https://williamlovecs.github.io/lingotech/'
    close_export(page)
    page.locator('#brandHome').click();assert not page.locator('#welcome').is_hidden()
    page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(OUT/f'{engine}-home-mobile.png'),full_page=True)
    page.goto('http://127.0.0.1:8765/lingotech-photo-booth/',wait_until='load');page.wait_for_function('window.LingoTechQA43');assert state(page)['version']=='4.3'
    assert not errors,errors
    results.update(status='passed',page_errors=errors)
   except Exception as exc:
    results.update(status='failed',error=str(exc),traceback=traceback.format_exc(),page_errors=errors)
    page.screenshot(path=str(OUT/f'{engine}-FAIL.png'),full_page=True)
    raise
   finally:
    (OUT/'test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    browser.close()
 for rel in ('lingotech/index.html','lingotech/release.json'):
  shutil.copy2(ROOT/rel,OUT/Path(rel).name)
 report['status']='passed'
 (OUT/'test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False,indent=2))
finally:
 server.shutdown()
