"""Browser regression tests. Native share is mocked; this is NOT physical WeChat acceptance."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json,os,base64,io
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'test-output';OUT.mkdir(exist_ok=True)
HTML=(ROOT.parent/'index.html').read_text()
im=Image.new('RGB',(1200,800),'#bfd5ed');d=ImageDraw.Draw(im);d.rectangle((0,0,230,200),fill='#ec9b46');d.rectangle((970,600,1199,799),fill='#6472b5');d.text((420,380),'LINGOTECH TEST PHOTO',fill='black');im.save(OUT/'test-photo.jpg')
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'
engine=os.getenv('BROWSER','chromium');results=[]
def record(name,**kwargs):
 results.append(dict(test=name,passed=True,engine=engine,**kwargs));print('PASS',name,flush=True)
with sync_playwright() as p:
 browser=getattr(p,engine).launch(**({'executable_path':os.environ['CHROMIUM_PATH']} if os.getenv('CHROMIUM_PATH') else {}),args=['--no-sandbox'] if engine=='chromium' else [])
 def load(behavior='none',wx=False,width=390,height=844,locale='zh-CN',mobile=True,delay_png=False):
  context=browser.new_context(viewport={'width':width,'height':height},is_mobile=mobile,has_touch=mobile,locale=locale,user_agent=(UA if mobile else 'Mozilla/5.0 Desktop Chromium')+(' MicroMessenger/8.0.65' if wx else ''),accept_downloads=True)
  page=context.new_page();errors=[];downloads=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('download',lambda d:downloads.append(d.suggested_filename))
  script="window._shares=[];Object.defineProperty(navigator,'canShare',{value:d=>!!d.files,configurable:true});"
  if behavior=='none':script+="Object.defineProperty(navigator,'share',{value:undefined,configurable:true});"
  else:
   ending={'resolve':'return Promise.resolve();','cancel':"return Promise.reject(new DOMException('Cancelled','AbortError'));",'fail':"return Promise.reject(new DOMException('Blocked','NotAllowedError'));",'hang':'return new Promise(()=>{});'}[behavior]
   script+="Object.defineProperty(navigator,'share',{value:d=>{window._shares.push({keys:Object.keys(d),type:d.files?.[0]?.type,size:d.files?.[0]?.size,activation:navigator.userActivation?.isActive});"+ending+"},configurable:true});"
  page.evaluate(script)
  if delay_png:page.evaluate("const orig=HTMLCanvasElement.prototype.toBlob;HTMLCanvasElement.prototype.toBlob=function(cb,type,q){if(type==='image/png')return orig.call(this,b=>setTimeout(()=>cb(b),2500),type,q);return orig.call(this,cb,type,q);};void 0;")
  page.set_content(HTML,wait_until='load');page.locator('#fileInput').set_input_files(str(OUT/'test-photo.jpg'));page.wait_for_function('window.LingoTechQA453?.snapshot().jpgReady',timeout=15000)
  return context,page,errors,downloads
 try:
  c,page,errors,downloads=load('resolve');page.locator('#downloadBtn').click();page.wait_for_timeout(150)
  assert not downloads and page.locator('#exportModal').is_visible()
  r=page.locator('#resultImage').bounding_box();assert r and r['y']<300 and r['y']+r['height']<760,r
  assert page.locator('#exportMore453').get_attribute('open') is None
  page.screenshot(path=str(OUT/(engine+'-mobile-save.png')))
  page.locator('#modalDownload').click();assert page.locator('#photoViewer453').is_visible();assert page.locator('#viewerImage453').get_attribute('src').startswith('data:image/jpeg;base64,')
  page.locator('#viewerBack453').click();assert page.locator('#exportModal').is_visible();page.locator('#closeExport').click();page.locator('#clearBtn').click()
  assert not page.locator('#viewerImage453').get_attribute('src') and not page.locator('#resultImage').get_attribute('src');assert not errors,errors
  record('mobile save: no automatic download, visible image, full image, privacy clear',imageTop=r['y']);c.close()
  for behavior in ['cancel','fail','resolve','hang','none']:
   c,page,errors,downloads=load(behavior);page.locator('#shareBtn').click();page.wait_for_timeout(150)
   assert page.locator('#exportModal').is_visible();assert page.locator('#resultImage').get_attribute('src').startswith('data:image/jpeg;base64,')
   snap=page.evaluate('LingoTechQA453.snapshot()');calls=page.evaluate('window._shares')
   if behavior=='hang':
    assert page.locator('#recover453').is_visible();page.locator('#recover453').click();assert not page.evaluate('LingoTechQA453.snapshot().sharing')
   else:assert not snap['sharing']
   if calls:assert calls[0]['keys']==['files'] and calls[0]['type']=='image/jpeg' and calls[0]['activation'],calls
   assert not errors,errors;record('native share '+behavior,snapshot=snap,calls=calls);c.close()
  c,page,errors,downloads=load('resolve',wx=True);page.locator('#wechatShare').click();assert not page.evaluate('window._shares');assert page.locator('#exportModal').is_visible() and page.locator('#wechatGuide').is_visible();assert not downloads
  r=page.locator('#resultImage').bounding_box();assert r['y']<300 and r['y']+r['height']<760,r
  page.screenshot(path=str(OUT/(engine+'-wechat-guide.png')));page.locator('#modalShare').click();assert page.evaluate('window._shares.length')==1;assert not errors,errors
  record('WeChat guide before optional explicit native share',imageTop=r['y']);c.close()
  c,page,errors,downloads=load('none',wx=True);page.locator('#downloadBtn').click();assert page.locator('#resultImage').is_visible() and page.locator('#modalShare').is_hidden();assert not downloads and not errors;record('WeChat without share API');c.close()
  c,page,errors,downloads=load('resolve',delay_png=True);snap=page.evaluate('LingoTechQA453.snapshot()');assert snap['jpgReady'] and snap['pngPending'] and not snap['pngReady'],snap
  page.locator('#shareBtn').click();assert page.evaluate('window._shares.length')==1;page.wait_for_function('LingoTechQA453.snapshot().pngReady');assert not errors,errors;record('slow PNG does not block JPG');c.close()
  c,page,errors,downloads=load('none',mobile=False,width=1280,height=900);page.locator('#downloadBtn').click();page.wait_for_timeout(300);assert downloads and downloads[0].endswith('.jpg');assert not errors,errors;record('desktop download');c.close()
  for width,height,locale in [(320,568,'zh-CN'),(375,667,'en-US'),(390,844,'zh-CN'),(430,932,'en-US'),(844,390,'zh-CN'),(768,1024,'en-US')]:
   c,page,errors,downloads=load('none',wx=True,width=width,height=height,locale=locale);page.locator('#downloadBtn').click();assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   btn=page.locator('#modalDownload').bounding_box();assert btn and btn['width']<=width and btn['height']>=44;assert not errors,errors;record('viewport '+str((width,height,locale)));c.close()
  c,page,errors,downloads=load('none');n=0
  for scene in ['build','friends','play']:
   page.locator('[data-scene="'+scene+'"]').click()
   for frame in ['build','crew','ideas','studio','night','friends','play']:
    page.locator('[data-template="'+frame+'"]').click()
    for ratio in ['post','landscape','story']:
     page.locator('[data-ratio="'+ratio+'"]').click();page.wait_for_function('LingoTechQA453.snapshot().jpgReady && LingoTechQA453.snapshot().pngReady')
     snap=page.evaluate('LingoTechQA453.snapshot()');assert snap['revision']==snap['cacheRevision']
     page.locator('#previewBtn').click();data=page.locator('#resultImage').get_attribute('src');im=Image.open(io.BytesIO(base64.b64decode(data.split(',',1)[1])))
     assert im.size=={'post':(1080,1350),'landscape':(1620,1080),'story':(1080,1920)}[ratio];page.locator('#closeExport').click();n+=1
  assert not errors,errors;record('all scene-frame-ratio exports',combinations=n);c.close()
 except Exception as exc:
  results.append(dict(test='failure',passed=False,error=str(exc),engine=engine))
  if 'page' in locals() and not page.is_closed():page.screenshot(path=str(OUT/(engine+'-FAILED.png')))
  raise
 finally:
  browser.close();(OUT/(engine+'-report.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2))
