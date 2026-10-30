"""Independent deep regression. Baseline findings are recorded; patched failures block release.
No real forms or social posts are submitted. All imported photos are synthetic fixtures.
"""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright,expect
from PIL import Image,ImageDraw
import argparse,json,traceback,base64,io,hashlib
import cv2,numpy as np
P=argparse.ArgumentParser();P.add_argument('--baseline',action='store_true');args=P.parse_args()
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent/'test-output'/('baseline' if args.baseline else 'patched');OUT.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',8779),partial(Quiet,directory=str(ROOT)));Thread(target=server.serve_forever,daemon=True).start()
URL='http://127.0.0.1:8779/lingotech/';DEST='https://williamlovecs.github.io/lingotech/'
A=OUT/'synthetic-a.png';B=OUT/'synthetic-b.png';EXIF=OUT/'rotated-exif.jpg'
for path,size,color in [(A,(1200,800),'#d7eaff'),(B,(500,1000),'#f3d9b7')]:
 im=Image.new('RGB',size,color);d=ImageDraw.Draw(im);d.rectangle((0,0,90,90),fill='red');d.rectangle((size[0]-90,size[1]-90,*size),fill='green');d.text((100,100),'SYNTHETIC - NO PERSONAL DATA',fill='black');im.save(path)
im=Image.open(A);ex=Image.Exif();ex[274]=6;im.save(EXIF,exif=ex)
REPORT={'scope':'baseline' if args.baseline else 'candidate','engines':{},'physical_iPhone_WeChat':'not tested','externalFormSubmissions':0,'externalSocialPosts':0}
INIT="""window.__shares=[];window.__mode='ok';window.__type='image/jpeg';Object.defineProperty(navigator,'canShare',{configurable:true,value:p=>!p.files||p.files.every(f=>f.type===__type)});Object.defineProperty(navigator,'share',{configurable:true,value:p=>{__shares.push({keys:Object.keys(p),types:(p.files||[]).map(f=>f.type),active:navigator.userActivation?.isActive});if(__mode==='pending')return new Promise(r=>window.__settle=r);if(__mode==='cancel')return Promise.reject(new DOMException('cancel','AbortError'));if(__mode==='fail')return Promise.reject(new DOMException('fail','DataError'));return Promise.resolve();}});"""
def ready(p):p.wait_for_function('PhotoBoothQA.snapshot().ready',timeout=20000)
def snap(p):return p.evaluate('PhotoBoothQA.snapshot()')
def load(p,file=A):p.locator('#fileInput').set_input_files(str(file));ready(p)
def personal(p):
 if not p.locator('#personal').evaluate('(e)=>e.open'):p.locator('#personal summary').click()
def decode(data):
 raw=np.frombuffer(data,np.uint8);arr=cv2.imdecode(raw,cv2.IMREAD_COLOR)
 return cv2.QRCodeDetector().detectAndDecode(arr)[0]
def no_overflow(p):
 v=p.evaluate('({w:innerWidth,scroll:document.documentElement.scrollWidth})');assert v['scroll']<=v['w']+1,v
failures=[]
try:
 with sync_playwright() as pw:
  for engine in ['chromium','webkit','firefox']:
   browser=getattr(pw,engine).launch(headless=True);rows=[];REPORT['engines'][engine]=rows
   def case(name,fn,locale='zh-CN',clock=False):
    ctx=browser.new_context(locale=locale,viewport={'width':390,'height':844},accept_downloads=True,reduced_motion='reduce');ctx.add_init_script(INIT);p=ctx.new_page();errors=[];traffic=[]
    p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:traffic.append((r.method,r.url)))
    row={'name':name}
    try:
     if clock:p.clock.install()
     p.goto(URL,wait_until='load');p.wait_for_function('window.LingoTechQA45');p.wait_for_function('document.querySelector("#landingPhoto1").complete && document.querySelector("#landingPhoto2").complete');
     detail=fn(p);assert not errors,errors
     assert all(m=='GET' and u.startswith('http://127.0.0.1:8779/') for m,u in traffic),traffic
     row.update(status='passed',details=detail,pageErrors=errors)
    except Exception as e:
     row.update(status='failed',error=str(e),traceback=traceback.format_exc(),pageErrors=errors);failures.append((engine,name,str(e)))
     try:p.screenshot(path=str(OUT/f'{engine}-{name}-FAIL.png'),full_page=True)
     except Exception:pass
    finally:
     rows.append(row);ctx.close();(OUT/'report.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2));print(engine,name,row['status'],flush=True)
   def clean_url(p):
    p.goto(URL+'index.html?utm_source=chatgpt.com&fbclid=example&v=old#editor');p.wait_for_function('window.LingoTechQA45');assert p.url==URL,p.url
    p.goto(URL+'?lang=en&kiosk=0&gclid=example');p.wait_for_function('window.LingoTechQA45');assert p.url==URL,p.url;assert not p.evaluate('LingoTechQA45.snapshot().kiosk');assert p.evaluate('LingoTechQA45.snapshot().language')=='en'
    p.goto(URL+'?kiosk=1');p.wait_for_function('window.LingoTechQA45');assert p.url==URL and p.evaluate('LingoTechQA45.snapshot().kiosk');assert p.evaluate('LingoTechQA45.snapshot().language')=='zh'  # New shared-device visitors use browser language, not a previous visitor preference.
   case('clean-url',clean_url)
   def empty_form(p):
    p.locator('#setupBtn').click();p.locator('#joinInput').fill('');p.locator('#partnerInput').fill('');p.locator('#formsVerified').check();p.locator('#applyConfig').click();p.locator('#formsBtn').click()
    links=p.locator('#formLinks a[href]').evaluate_all('(es)=>es.map(e=>e.href)');assert not links,links
    assert p.locator('#formLinks').inner_text().strip();assert not p.locator('#formLinks img').count()
   case('empty-form-no-false-link',empty_form)
   def stable_form(p):
    load(p);p.locator('#formsBtn').click();p.evaluate('window.__formBefore=document.querySelector("#formLinks a");__formBefore.focus()')
    p.locator('#nickname').evaluate("e=>{e.value='refresh';e.dispatchEvent(new Event('input',{bubbles:true}));}");ready(p)
    assert p.evaluate('__formBefore===document.querySelector("#formLinks a")'),'Form links were needlessly recreated'
    assert p.evaluate('document.activeElement===__formBefore'),'Focused form link lost focus'
   case('form-focus-stable',stable_form)
   def custom_form(p):
    p.locator('#setupBtn').click();p.locator('#joinInput').fill('https://example.com/event');p.locator('#applyConfig').click();p.locator('#formsBtn').click()
    card=p.locator('#formLinks article').first;assert card.locator('a').get_attribute('href')=='https://example.com/event';assert card.locator('img').count()==0
    assert '另一台' not in card.inner_text() and 'another phone' not in card.inner_text(),'Tells user to scan a QR that does not exist'
   case('custom-form-no-phantom-qr',custom_form)
   def texture(p):
    load(p);p.locator('[data-scene=friends]').click();ready(p)
    for frame in ['build','crew','ideas','studio','night']:
     p.locator(f'[data-template={frame}]').click();ready(p)
     if p.locator('#communityPaper').is_visible():
      p.locator('#communityPaper').select_option('paper');ready(p);before=p.locator('#poster').evaluate('c=>c.toDataURL()');p.locator('#communityPaper').select_option('picnic');ready(p);after=p.locator('#poster').evaluate('c=>c.toDataURL()');assert before!=after,frame+' has an inert texture selector'
    for frame in ['friends','play']:
     p.locator(f'[data-template={frame}]').click();ready(p);assert p.locator('#communityPaper').is_visible();p.locator('#communityPaper').select_option('paper');ready(p);before=p.locator('#poster').evaluate('c=>c.toDataURL()');p.locator('#communityPaper').select_option('picnic');ready(p);assert p.locator('#poster').evaluate('c=>c.toDataURL()')!=before
    p.locator('[data-scene=build]').click();ready(p);assert p.locator('#communityControls').is_hidden()
   case('texture-controls-have-effect',texture)
   def unicode(p):
    load(p);personal(p);p.locator('#nickname').focus();p.keyboard.insert_text('🐱'*40);ready(p)
    assert snap(p)['nickname']=='🐱'*40,('visible chars',len(snap(p)['nickname']))
    p.keyboard.insert_text('Z');assert snap(p)['nickname']=='🐱'*40
   case('forty-visible-characters',unicode)
   def save_after_edit(p):
    load(p);personal(p);p.locator('#nickname').fill('A final note');ready(p)
    p.locator('#previewBtn').click();expect(p.locator('#exportModal')).to_be_visible();expect(p.locator('#resultImage')).to_be_visible();assert snap(p)['nickname']=='A final note'
   case('blur-does-not-invalidate-save',save_after_edit)
   def retry_export(p):
    load(p);p.evaluate("()=>{window.__oldBlob=HTMLCanvasElement.prototype.toBlob;HTMLCanvasElement.prototype.toBlob=function(cb){setTimeout(()=>cb(null),0)};}")
    personal(p);p.locator('#nickname').fill('retry');p.wait_for_function('!PhotoBoothQA.snapshot().ready');p.wait_for_timeout(700)
    assert p.locator('#retryExport452').is_visible(),'No retry action after image encoder failure'
    p.evaluate('()=>{HTMLCanvasElement.prototype.toBlob=__oldBlob;}');p.locator('#retryExport452').click();ready(p);assert snap(p)['nickname']=='retry';assert not p.locator('#retryExport452').is_visible()
   case('export-failure-retry',retry_export)
   def hanging_share(p):
    load(p);p.evaluate("__mode='pending'");p.locator('#shareBtn').click();assert p.evaluate('__shares.length')==1
    p.clock.run_for(31000)
    assert p.locator('#recoverShare452').is_visible(),'Native share never settled; no recovery control'
    p.locator('#recoverShare452').click();expect(p.locator('#shareBtn')).to_be_enabled();assert snap(p)['own']
    p.locator('#clearBtn').click();p.evaluate('__settle()');p.wait_for_timeout(100);assert snap(p)['sourceState']=='empty';assert not p.locator('#exportModal').is_visible()
   case('hanging-share-recovery',hanging_share,clock=True)
   def native_share(p):
    load(p);p.locator('#shareBtn').click();p.wait_for_function('__shares.length===1');call=p.evaluate('__shares[0]');assert call['keys']==['files'] and call['types']==['image/jpeg'];assert call['active'] is not False
    if p.locator('#exportModal').is_visible():p.locator('#closeExport').click()
    p.evaluate("__type='image/png'");p.locator('#shareBtn').click();p.wait_for_function('__shares.length===2');assert p.evaluate('__shares[1].types')==['image/png']
    if p.locator('#exportModal').is_visible():p.locator('#closeExport').click()
    p.evaluate("__mode='cancel'");p.locator('#shareBtn').click();p.wait_for_function('!document.querySelector("#shareBtn").disabled');assert snap(p)['own'];assert not p.locator('#exportModal').is_visible()
    p.evaluate("__mode='fail'");p.locator('#shareBtn').click();expect(p.locator('#wechatGuide')).to_be_visible();p.locator('#closeExport').click()
    p.evaluate("__mode='pending'");p.locator('#shareBtn').click();p.locator('#clearBtn').click();p.evaluate('__settle()');p.wait_for_timeout(120);assert not p.locator('#exportModal').is_visible() and snap(p)['sourceState']=='empty'
    return 'native API mocked; file-only, active gesture, PNG fallback, cancel/failure and late resolution'
   case('native-share-state-machine',native_share)
   def delayed_import(p):
    load(p);personal(p);p.locator('#nickname').fill('PRIVATE_SENTINEL');ready(p)
    p.evaluate("()=>{const old=window.createImageBitmap.bind(window);window.__holdOne=true;window.createImageBitmap=async(...a)=>{const im=await old(...a);if(__holdOne){__holdOne=false;return await new Promise(r=>window.__releaseBitmap=()=>r(im));}return im;};}")
    p.locator('#fileInput').set_input_files(str(A));p.wait_for_function("typeof window.__releaseBitmap === 'function'");p.locator('#cancelLoad').click();ready(p);assert snap(p)['nickname']=='PRIVATE_SENTINEL'
    p.locator('#fileInput').set_input_files(str(B));ready(p);assert snap(p)['photo']=={'width':500,'height':1000};p.evaluate('__releaseBitmap()');p.wait_for_timeout(150);assert snap(p)['photo']=={'width':500,'height':1000};assert snap(p)['nickname']==''
    p.locator('#clearBtn').click();assert not p.evaluate('LingoTechQA45.snapshot().hasExport');assert not p.evaluate('LingoTechQA45.snapshot().hasDataUrl');assert 'PRIVATE_SENTINEL' not in p.evaluate('JSON.stringify({...localStorage})')
   case('cancelled-import-cannot-resurrect',delayed_import)
   def exif(p):
    load(p,EXIF);assert snap(p)['photo']=={'width':800,'height':1200},snap(p)['photo']
    p.locator('#rotatePhoto').click();ready(p);assert snap(p)['photo']=={'width':1200,'height':800}
    p.locator('#fileInput').set_input_files({'name':'bad.svg','mimeType':'image/svg+xml','buffer':b'<svg xmlns="http://www.w3.org/2000/svg"></svg>'});expect(p.locator('#fileError')).to_be_visible();ready(p);assert snap(p)['photo']=={'width':1200,'height':800}
   case('exif-rotation-and-invalid-file',exif)
   def privacy_idle(p):
    p.goto(URL+'?kiosk=1');p.wait_for_function('window.LingoTechQA45');load(p);personal(p);p.locator('#nickname').fill('PRIVATE_IDLE');ready(p)
    p.clock.fast_forward(161000);expect(p.locator('#idleWarning45')).to_be_visible();p.locator('#keepSession45').click();assert snap(p)['own']
    p.clock.fast_forward(181000);assert snap(p)['sourceState']=='empty' and snap(p)['nickname']==''
    assert p.evaluate('LingoTechQA45.snapshot().qr');assert not p.evaluate('LingoTechQA45.snapshot().hasExport');assert not p.locator('#resultImage').get_attribute('src')
   case('shared-device-idle-clear',privacy_idle,clock=True)
   def form_safety(p):
    p.locator('#setupBtn').click();p.locator('#joinInput').fill('javascript:alert(1)');p.locator('#applyConfig').click();expect(p.locator('#setupError')).to_be_visible();assert p.locator('#setupModal').is_visible()
    p.locator('#joinInput').fill('https://user:password@example.com/');p.locator('#applyConfig').click();expect(p.locator('#setupError')).to_be_visible();p.locator('#closeSetup').click()
   case('config-rejects-unsafe-links',form_safety)
   def responsive(p):
    samples=0
    for language in ['en','zh']:
     if snap(p)['language']!=language:p.locator('#languageBtn').click()
     for width in [320,375,390,430,768,1024,1440]:
      p.set_viewport_size({'width':width,'height':844});no_overflow(p);samples+=1
     load(p)
     for width in [320,375,390,430,768,1024,1440]:
      p.set_viewport_size({'width':width,'height':844})
      for ratio in ['post','story','landscape']:
       p.locator('[data-ratio='+ratio+']').click();ready(p);no_overflow(p);samples+=1
     p.set_viewport_size({'width':320,'height':568});p.locator('#previewBtn').click();no_overflow(p);p.locator('#closeExport').click();p.locator('#setupBtn').click();no_overflow(p);p.locator('#closeSetup').click();p.locator('#formsBtn').click();no_overflow(p);p.locator('#closeForms').click();p.locator('#clearBtn').click()
    p.set_viewport_size({'width':390,'height':844});p.screenshot(path=str(OUT/f'{engine}-home-mobile.png'),full_page=True);load(p);p.screenshot(path=str(OUT/f'{engine}-editor-mobile.png'),full_page=True)
    return {'responsive_states':samples}
   case('responsive-both-languages',responsive,locale='en-US')
   def qr_matrix(p):
    load(p);success=0
    for scene in ['build','friends','play']:
     for frame in ['build','crew','ideas','studio','night','friends','play']:
      for ratio in ['post','story','landscape']:
       for strip in [False,True]:
        data=p.evaluate("m=>{const c=document.createElement('canvas');const r=LingoTechQA43.render(c,m);const out={data:c.toDataURL('image/png').split(',')[1],bad:r.textBoxes.filter(b=>b.x<8||b.y<8||b.x+b.w>c.width-8||b.y+b.h>c.height-8)};c.width=c.height=1;return out;}",{'scene':scene,'template':frame,'ratio':ratio,'memoryStrip':strip,'showQr44':True,'nickname':'中文与English edge test 123','role':'Creator'})
        assert not data['bad'],(scene,frame,ratio,strip,data['bad'])
        raw=base64.b64decode(data['data']);assert decode(raw)==DEST,(scene,frame,ratio,strip,'PNG')
        im=Image.open(io.BytesIO(raw)).convert('RGB');im=im.resize((720,round(im.height*720/im.width)));stream=io.BytesIO();im.save(stream,format='JPEG',quality=80)
        assert decode(stream.getvalue())==DEST,(scene,frame,ratio,strip,'720 JPEG')
        success+=2
    return {'qr_decodes':success,'sizes':'original PNG and 720px JPEG at quality 80'}
   if not args.baseline:case('qr-every-scene-frame-ratio-strip',qr_matrix)
   browser.close()
 REPORT['failed_count']=len(failures);REPORT['status']='findings' if failures else 'passed';REPORT['failures']=failures
 (OUT/'report.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2));print(json.dumps({'status':REPORT['status'],'failures':failures},ensure_ascii=False,indent=2))
 if failures and not args.baseline:raise SystemExit(1)
finally:server.shutdown()
