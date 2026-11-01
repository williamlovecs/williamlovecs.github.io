"""v4.5.4 browser-only regression for the Android in-app no-share screenshot.

No personal images, external form submissions, camera hardware or actual social posts.
Physical WeChat/Android album save remains unverified.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
import cv2, json, os

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).parent/'test-output'
OUT.mkdir(exist_ok=True)
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
MANIFEST=json.loads((ROOT/'release.json').read_text(encoding='utf-8'))
assert MANIFEST['version']=='4.5.4'
PHOTO=OUT/'synthetic.jpg'
im=Image.new('RGB',(850,1130),'#e5eaf3')
d=ImageDraw.Draw(im);d.rectangle((45,85,790,1040),outline='#3366ff',width=18)
d.text((170,400),'SYNTHETIC TEST IMAGE',fill='#000')
im.save(PHOTO)
CAN='https://williamlovecs.github.io/lingotech/'
WX='Mozilla/5.0 (Linux; Android 16; Pixel 9 Build/BC1234) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/139.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.65'
ANDROID=WX.split(' MicroMessenger')[0]
engine=os.environ.get('BROWSER','chromium')
rows=[]
with sync_playwright() as pw:
 browser=getattr(pw,engine).launch(headless=True)
 def make(ua=WX,locale='en-US',native=False,latest=None,mobile=True):
  ctx=browser.new_context(viewport={'width':393 if mobile else 1280,'height':852 if mobile else 900},
    is_mobile=mobile,has_touch=mobile,locale=locale,user_agent=ua if mobile else None,accept_downloads=True,reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  if native:
   page.evaluate("Object.defineProperty(navigator,'canShare',{configurable:true,value:()=>true});Object.defineProperty(navigator,'share',{configurable:true,value:d=>{window.__calls=(window.__calls||0)+1;return Promise.resolve();}});")
  else:
   page.evaluate("Object.defineProperty(navigator,'share',{configurable:true,value:undefined});")
  if latest:
   page.evaluate("window.fetch=async()=>({ok:true,json:async()=>({version:'4.5.5'})})")
  page.set_content(HTML,wait_until='load')
  page.wait_for_function('window.LingoTechQA454',timeout=20000)
  page.locator('#fileInput').set_input_files(str(PHOTO))
  page.wait_for_function('LingoTechQA453.snapshot().jpgReady',timeout=20000)
  return ctx,page,errors
 def run(name,fn):
  row={'case':name,'engine':engine}
  try:
   fn();row['passed']=True
  except Exception as exc:
   row.update(passed=False,error=str(exc))
  rows.append(row)
  print(('PASS' if row['passed'] else 'FAIL'),engine,name,flush=True)
  (OUT/f'{engine}-report.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
  if not row['passed']:raise AssertionError(name+': '+str(row['error']))
 def unsupported():
  ctx,page,errors=make()
  page.locator('#shareBtn').click()
  page.wait_for_function('document.querySelector("#resultImage").naturalWidth>0')
  assert page.locator('#modalShare').is_visible()
  assert page.locator('#modalShare').inner_text()=='Download JPG file'
  assert page.locator('#directRetry').is_hidden()
  assert page.locator('#resultImage').is_visible()
  children=page.locator('#exportModal .export-card').evaluate('e=>[...e.children].map(x=>x.id||x.className)')
  assert children.index('resultImage')<children.index('wechatGuide')
  assert children.index('resultImage')<children.index('exportMore453')
  page.screenshot(path=str(OUT/f'{engine}-android-wechat-fallback.png'),full_page=True)
  with page.expect_download(timeout=12000) as dl:page.locator('#modalShare').click()
  path=OUT/f'{engine}-android-fallback.jpg';dl.value.save_as(path)
  assert path.read_bytes().startswith(b'\xff\xd8')
  decoded=cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(path)))[0]
  assert decoded==CAN,decoded
  page.locator('#closeExport').click();page.locator('#clearBtn').click()
  assert not page.locator('#resultImage').get_attribute('src')
  assert page.evaluate('PhotoBoothQA.snapshot().sourceState')=='empty'
  assert not errors,errors
  ctx.close()
 run('unsupported share -> photo-first + real JPG + QR + privacy clear',unsupported)
 def chinese():
  ctx,page,errors=make(locale='zh-CN')
  page.locator('#shareBtn').click()
  assert page.locator('#modalShare').is_visible()
  assert page.locator('#modalShare').inner_text()=='下载 JPG 文件'
  assert '下载目录' in page.locator('#wechatGuide').inner_text()
  assert not errors,errors;ctx.close()
 run('Chinese copy and real fallback',chinese)
 def native():
  ctx,page,errors=make(ua=ANDROID,native=True)
  page.locator('#shareBtn').click()
  assert page.locator('#modalShare').is_visible()
  assert page.locator('#modalShare').inner_text()=='System save / share'
  assert not page.evaluate('LingoTechQA454.snapshot().shareFallbackVisible')
  count=page.evaluate('window.__calls||0')
  page.locator('#modalShare').click()
  page.wait_for_function(f'(window.__calls||0)=={count+1}')
  assert not errors,errors;ctx.close()
 run('supported native share unchanged',native)
 def desktop():
  ctx,page,errors=make(mobile=False)
  page.locator('#previewBtn').click()
  assert page.locator('#modalShare').is_hidden()
  with page.expect_download(timeout=12000) as dl:page.locator('#modalDownload').click()
  assert dl.value.suggested_filename.endswith('.jpg')
  assert not errors,errors;ctx.close()
 run('desktop existing download unchanged',desktop)
 def update_preserves_photo():
  ctx,page,errors=make(latest='4.5.5')
  page.wait_for_function('LingoTechQA454.snapshot().updateAvailable',timeout=6000)
  assert page.locator('#freshness454').is_visible()
  assert page.evaluate('PhotoBoothQA.snapshot().own')
  assert page.evaluate('LingoTechQA453.snapshot().jpgReady')
  assert not errors,errors;ctx.close()
 run('update hint does not reload unsaved photo',update_preserves_photo)
 browser.close()
print(json.dumps({'engine':engine,'passed':len(rows),'cases':rows},ensure_ascii=False,indent=2))
