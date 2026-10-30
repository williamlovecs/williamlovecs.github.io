"""Deterministic patch on the tested v4.5 source; original photos remain byte-identical."""
from pathlib import Path
import re,json,hashlib,base64,io
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'_archive/lingotech-photo-booth/v4.5-20261031/index.html'
b=source.read_bytes();assert hashlib.sha256(b).hexdigest()=='669c33c2c8586b2465e8121292ac07d1379115c043c8b91b8768533d957f80e5'
s=b.decode();before=s
s=re.sub(r'<link\b(?=[^>]*\brel=[\"\']canonical[\"\'])[^>]*>','',s,flags=re.I)
s=s.replace('name="app-version" content="4.5"','name="app-version" content="4.5.1"').replace("const VERSION45='4.5';","const VERSION45='4.5.1';")
meta='''<link rel="canonical" href="https://williamlovecs.github.io/lingotech/">
<meta property="og:type" content="website"><meta property="og:title" content="LingoTech Photo Booth">
<meta property="og:description" content="Your photo. Your people. Create a keepsake locally, with no AI face changes.">
<meta property="og:url" content="https://williamlovecs.github.io/lingotech/">
<meta property="og:image" content="https://williamlovecs.github.io/lingotech/og-v451.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="LingoTech Photo Booth - Your photo. Your people.">
<meta name="twitter:card" content="summary_large_image">
<style id="release451">.camera-viewport video{object-fit:contain}.camera-overlay{display:none}.toast{max-width:min(90vw,480px)}</style>
'''
s=s.replace('</head>',meta+'</head>',1)
patch="""
// v4.5.1 uses accurate form labels; community membership is not promised by a signup link.
WORDS.zh.community='活动报名'; WORDS.en.community='Event signup';
WORDS.zh.joinLabel='C 端活动报名链接（HTTPS）'; WORDS.en.joinLabel='Event signup link (HTTPS)';
WORDS.zh.cameraHint='预览显示完整取景；关闭窗口会停止摄像头。';
WORDS.en.cameraHint='Preview shows the full camera image. Closing stops the camera.';
window.LingoTechQA451={version:'4.5.1',canonical:CANONICAL};
"""
marker='translate();scheduleRender(true);\n})();';assert s.count(marker)==1
s=s.replace(marker,patch+'\n'+marker)
assets=lambda x:re.findall(r'data:image/[^\s\"\']+',x)
assert assets(before)==assets(s),'Photo or existing QR asset changed'
assert len(re.findall(r'<link\b(?=[^>]*\brel=[\"\']canonical[\"\'])[^>]*>',s))==1
(ROOT/'lingotech/index.html').write_text(s)
# Brand-only social preview uses the existing logo, not participant photos.
a=json.loads(re.search(r'window\.PHOTOBOOTH_ASSETS = (\{.*?\});',s).group(1))
logo=Image.open(io.BytesIO(base64.b64decode(a['logo'].split(',',1)[1]))).convert('RGBA');logo.thumbnail((105,105))
im=Image.new('RGB',(1200,630),'#f7f6f2');im.paste(logo,(68,50),logo);d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=lambda n:ImageFont.truetype(font,n)
d.text((185,59),'LingoTech',font=f(42),fill='#101d42');d.text((186,112),'PHOTO BOOTH',font=ImageFont.truetype(reg,20),fill='#53627d')
d.text((68,206),'YOUR PHOTO.',font=f(78),fill='#101d42');d.text((68,305),'YOUR PEOPLE.',font=f(78),fill='#165dff')
d.rectangle((72,424,735,437),fill='#ffe02e');d.text((72,484),'Create a keepsake. Photos stay on your device.',font=ImageFont.truetype(reg,28),fill='#53627d')
im.save(ROOT/'lingotech/og-v451.png')
manifest=json.loads((ROOT/'lingotech/release.json').read_text());manifest.update(version='4.5.1',baseline_commit='f71deda492bdc0c2a30e6b2d940d715233b354bd',previous_release_archive=str(source.relative_to(ROOT)),sha256=hashlib.sha256(s.encode()).hexdigest(),social_preview_sha256=hashlib.sha256((ROOT/'lingotech/og-v451.png').read_bytes()).hexdigest())
manifest['changes']+=['one canonical and social preview metadata','full-frame live camera preview matches capture','event form labels no longer imply automatic community membership']
(ROOT/'lingotech/release.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
