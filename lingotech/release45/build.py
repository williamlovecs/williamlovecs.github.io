"""Deterministic upgrade from an immutable, byte-identical v4.4 archive."""
from pathlib import Path
import hashlib, json, re
ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / '_archive/lingotech-photo-booth/v4.4-20261030/index.html'
b = ARCHIVE.read_bytes()
blob = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert blob == '1382aacc30c32daab42354d0322e9a875f0f4c24', 'Unexpected baseline; do not overwrite newer work'
s = b.decode('utf-8')
marker = 'translate();scheduleRender(true);\n})();'
assert s.count(marker)==1
patch=(Path(__file__).parent/'qr-resilience.js').read_text()+'\n'+(Path(__file__).parent/'upgrade.js').read_text()+'\nwindow.LingoTechQA45.qrGeometry=qr44Geometry;\n'
s=s.replace(marker,patch+'\n'+marker)
s=s.replace('<!-- LingoTech release v4.4 shareable photos with scannable QR -->','<!-- LingoTech release v4.5 unified entry and shared-device privacy -->')
s=s.replace('<title>LingoTech Photo Booth</title>','<title>LingoTech Photo Booth</title>\n<link rel="canonical" href="https://williamlovecs.github.io/lingotech/">\n<meta name="app-version" content="4.5">')
pat=r'(window\.PHOTOBOOTH_CONFIG = )(\{[^<]*?\})(;)'
m=re.search(pat,s);assert m
cfg=json.loads(m.group(2));cfg['defaultLanguage']='auto'
s=s[:m.start(2)]+json.dumps(cfg,ensure_ascii=False,separators=(',',':'))+s[m.end(2):]
# Exact image data preservation, not a perceptual similarity claim.
assets=lambda x:re.findall(r'data:image/[^\s\"\']+',x)
assert assets(b.decode())==assets(s),'Unexpected photo/QR asset change'
(ROOT/'lingotech/index.html').write_text(s,encoding='utf-8')
legacy='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LingoTech Photo Booth — moved</title><link rel="canonical" href="https://williamlovecs.github.io/lingotech/"><meta name="robots" content="noindex,follow"><script>const dest=new URL('/lingotech/',location.origin);const source=new URL(location.href);for(const k of ['kiosk','lang']){const v=source.searchParams.get(k);if((k==='kiosk'&&['0','1'].includes(v))||(k==='lang'&&['zh','en'].includes(v)))dest.searchParams.set(k,v);}if(['#editor','#welcome'].includes(source.hash))dest.hash=source.hash;location.replace(dest.href);</script><noscript><meta http-equiv="refresh" content="0; url=/lingotech/"></noscript><style>body{font-family:system-ui,sans-serif;padding:48px;line-height:1.7;color:#101d42}a{color:#165dff}</style></head><body><h1>LingoTech Photo Booth</h1><p>入口已更新，正在前往新版。<br>Opening the current Photo Booth.</p><a href="/lingotech/">打开新版 / Open Photo Booth</a></body></html>'''
(ROOT/'lingotech-photo-booth').mkdir(exist_ok=True)
(ROOT/'lingotech-photo-booth/index.html').write_text(legacy,encoding='utf-8')
sha=lambda x:hashlib.sha256(x).hexdigest()
release={'version':'4.5','canonical':'https://williamlovecs.github.io/lingotech/','legacy':'https://williamlovecs.github.io/lingotech-photo-booth/','legacy_behavior':'client-side redirect with meta-refresh and link fallback','baseline_commit':'af1be693e9893a697e0be181ca93a3b6b1a54132','archive':'_archive/lingotech-photo-booth/v4.4-20261030/index.html','archive_git_blob':blob,'sha256':sha(s.encode()),'legacy_sha256':sha(legacy.encode()),'changes':['optional event CTA','full visitor reset including QR toggle','opt-in tab-only kiosk with 3-minute idle clear','automatic zh/en with remembered manual preference','opt-in anonymous local action totals; no collector','larger landscape QR for compressed sharing'], 'analytics':'local only; no site-wide reporting', 'physical_wechat_acceptance':'requires real-device testing'}
(ROOT/'lingotech/release.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(release,ensure_ascii=False,indent=2))
