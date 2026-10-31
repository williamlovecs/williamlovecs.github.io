from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
page=ROOT.parent/'index.html'
source=page.read_bytes()
expected='53fcdcbfd6ca0db54d4c427ca713826c6af7b2e539b1f70472576d480396392f'
assert hashlib.sha256(source).hexdigest()==expected,'Baseline changed: stop, do not overwrite newer work'
s=source.decode('utf-8')
marker='translate();scheduleRender(true);\n})();\n</script>'
assert s.count(marker)==1
s=s.replace(marker,(ROOT/'mobile-export.js').read_text()+'\n'+marker)
s=s.replace('<!-- LingoTech release v4.5.2 deep regression and reliability fixes -->','<!-- LingoTech v4.5.3 mobile album-first save and sharing -->').replace('name="app-version" content="4.5.2"','name="app-version" content="4.5.3"').replace("const VERSION45='4.5.2';","const VERSION45='4.5.3';")
page.write_text(s,encoding='utf-8')
release=ROOT.parent/'release.json'
meta=json.loads(release.read_text())
meta.update(version='4.5.3',baseline_commit='65777d736274af6bea9339839814fd6174d115b0',sha256=hashlib.sha256(page.read_bytes()).hexdigest(),physical_wechat_acceptance='not performed; requires physical iPhone/Android WeChat testing')
meta['changes']+=['mobile image-preview-first save instead of automatic file download','WeChat entry shows image and album instructions before optional native sharing','cancelled/failed/pending shares retain a visible image and immediate recovery','photo before registration and diagnostic sections','JPG ready independently of background PNG encoding','full-size native IMG viewer; no photo upload']
release.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(meta['sha256'])
