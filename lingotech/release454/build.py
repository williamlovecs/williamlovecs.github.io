"""Build v4.5.4 from the immutable v4.5.3 production source.

This is not a general-purpose rebuild. Reject any unexpected baseline hash or
missing insertion point rather than silently overwrite newer work.
"""
from pathlib import Path
import hashlib, json, re

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'_archive/lingotech-photo-booth/v4.5.3-20261101/index.html'
MANIFEST=ROOT/'lingotech/release.json'
old=BASE.read_bytes()
expected='aaf0544eb892b1fbf691280062fac9eef017772332dacd9071618cbad5e38554'
assert hashlib.sha256(old).hexdigest()==expected, 'Baseline changed: abort'
s=old.decode('utf-8')
before=s
assert s.count('name="app-version" content="4.5.3"')==1
assert s.count("const VERSION45='4.5.3';")==1
s=s.replace('name="app-version" content="4.5.3"','name="app-version" content="4.5.4"',1)
s=s.replace("const VERSION45='4.5.3';","const VERSION45='4.5.4';",1)

marker="  window.LingoTechQA453={version:'4.5.3',snapshot:()=>({mobile:mobile(),ios:ios(),sharing,previewOpen:activeModal==='exportModal',viewerOpen:activeModal==='photoViewer453',jpgReady:readyExport(),pngReady:!!exportCache?.blob,pngPending:!!exportCache?.pngPending,revision:state.revision,cacheRevision:exportCache?.revision,notice})};\n})();"
assert s.count(marker)==1, 'Latest export closure changed: abort'
patch=(Path(__file__).parent/'browser-fallback.js').read_text(encoding='utf-8')
s=s.replace(marker,marker.removesuffix('})();')+'\n'+patch+'\n})();',1)
assert s.count('LingoTechQA454')==1
assets=lambda source:re.findall(r'data:image/[^\s\"\\' + "'" + r']+',source)
assert assets(before)==assets(s), 'Embedded original photo or QR image changed'
assert s.count('rel="canonical"')==1

out=ROOT/'lingotech/index.html'
out.write_text(s,encoding='utf-8')
meta=json.loads(MANIFEST.read_text(encoding='utf-8'))
assert meta['version']=='4.5.3'
meta.update(version='4.5.4',baseline_commit='50265b6101506dd10e4b28fc302eaacbd26e4ca2',
            previous_release_archive=str(BASE.relative_to(ROOT)),
            sha256=hashlib.sha256(s.encode()).hexdigest())
meta['changes']+=['Android/WeChat no-native-share JPG download fallback (does not promise Photos save)',
                  'non-destructive new-release reminder and user-initiated clean-URL refresh']
MANIFEST.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'version':meta['version'],'sha256':meta['sha256'],'photo_assets_unchanged':True},indent=2))
