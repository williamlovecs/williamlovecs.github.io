from pathlib import Path
from PIL import Image,ImageOps
import json,base64,hashlib,re,io
import gdown
import pillow_heif
pillow_heif.register_heif_opener()
R=Path(__file__).resolve().parent
base=Path('lingotech/index.html').read_text()
EXPECTED='89fe59dd1ed110cb0223748b11873587eb507271'
b=base.encode();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==EXPECTED,'Production baseline changed; refusing to overwrite.'
raw=Path('/tmp/lingotech-community-originals');raw.mkdir(exist_ok=True)
pub={};sources=[]
for key,identifier,name,sha,width,quality in [
 ('friends','1goG4YX6hm3a85aaz-oUAmoZ4Ssd9eAjG','IMG_0176.JPG','529097fe141081e06c3dc098a67db02f1aa30050a2204621c8033a405d48e14e',880,76),
 ('play','1E7JejIfEN-UPXAsAq0JIh9QOu8anoB-b','112.HEIC','88461883954bcc921944be7ade775c50f71c7b963cf7d5ae644916231a1e3c2e',720,76),
 ('highfive','1JBSFQEbfKAFc-e2Fgr-cLi2-eoUZruOP','IMG_1921.JPG','babe08a537d814e57e117dfb98dcf417020dbac189bc84935be13cf909cec476',600,74)]:
 p=raw/name
 gdown.download(id=identifier,output=str(p),quiet=False)
 assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==sha,'Unexpected source bytes: '+name
 im=ImageOps.exif_transpose(Image.open(p)).convert('RGB');original=im.size
 im.thumbnail((width,width),Image.Resampling.LANCZOS)
 buf=io.BytesIO();im.save(buf,'WEBP',quality=quality,method=6)
 data=buf.getvalue();pub[key]='data:image/webp;base64,'+base64.b64encode(data).decode()
 sources.append({'name':name,'sha256':sha,'original_px':original,'web_px':im.size,'web_bytes':len(data)})
s=base.replace('<!-- LingoTech release v3.2 -->','<!-- LingoTech release v4.0 Community Edition -->',1).replace('<span class="version">v3.2</span>','<span class="version">v4.0</span>',1)
s=s.replace("const FRAME_KEYS=['build','crew','ideas','studio','night'];","const FRAME_KEYS=['build','crew','ideas','studio','night','friends','play'];")
s=s.replace('5 STYLES','7 STYLES')
s=s.replace('const renderers={build:drawBuild,crew:drawCrew,ideas:drawIdeas,studio:drawStudio,night:drawNight};','const renderers={build:drawBuild,crew:drawCrew,ideas:drawIdeas,studio:drawStudio,night:drawNight,friends:drawFriends,play:drawPlay};')
s=s.replace("state.filename='sample-hicool';","state.sampleOrigin='HICOOL 2026';state.filename='sample-hicool';")
s=s.replace("state.own=true;state.demo=false;state.fit='contain';", "state.sampleOrigin='';state.own=true;state.demo=false;state.fit='contain';")
anchor='<small data-i18n="nightDesc">深蓝 · 入场券</small></span></button>'
assert s.count(anchor)==1
more=''
for key,title,desc in [('friends','Find Your People','朋友 · 快照与胶片'),('play','Culture & Play','文化 · 趣味入场券')]:
 more+=f'<button type="button" class="template" data-template="{key}" aria-pressed="false"><canvas id="thumb-{key}" width="216" height="270" aria-hidden="true"></canvas><span><b>{title}</b><small data-i18n="{key}Desc">{desc}</small></span></button>'
s=s.replace(anchor,anchor+more,1)
anchor='<p class="edit-promise"';idx=s.find(anchor);assert idx>0
controls='''<section id="communityControls" class="control-card community-controls" hidden><h3 data-i18n="communityOptions"></h3><label for="communityPaper" data-i18n="communityPaper"></label><select id="communityPaper"><option value="paper" data-i18n="paper"></option><option value="picnic" data-i18n="picnic"></option><option value="celebrate" data-i18n="celebrate"></option></select><label class="memory-check"><input type="checkbox" id="memoryStrip"><span data-i18n="memoryStrip"></span></label><small data-i18n="memoryHelp"></small></section>'''
s=s[:idx]+controls+s[idx:]
section='''<section class="community-story" aria-labelledby="storyTitle"><span class="eyebrow">AI × INTERNATIONAL × REAL COMMUNITY</span><h2 id="storyTitle" data-i18n="communityTitle"></h2><p data-i18n="communityIntro"></p><div class="community-gallery"><article><img id="community-ai" alt="HICOOL 2026 AI workshop" src="__AI_PHOTO__"><h3 data-i18n="aiMoment"></h3><p>Hands-on learning. Real projects.<br>实操、交流与创造。</p></article><article><img id="community-friends" alt="Past LingoCorner conversation event"><h3 data-i18n="peopleMoment"></h3><button id="tryPeople" class="text-btn" data-i18n="tryPeople"></button></article><article><img id="community-play" alt="Past LingoCorner cultural gathering"><h3 data-i18n="playMoment"></h3><button id="tryPlay" class="text-btn" data-i18n="tryPlay"></button></article></div></section>'''
a=re.search(r'window.PHOTOBOOTH_ASSETS\s*=\s*(\{.*?\});</script>',s,re.S);assert a
A=json.loads(a.group(1));section=section.replace('__AI_PHOTO__',A['workshop'])
s=s.replace('<section id="editor"',section+'<section id="editor"',1)
s=s.replace('<p class="disclaimer" data-i18n="wechatWhy"></p></section>', '<p class="disclaimer" data-i18n="wechatWhy"></p><button type="button" id="directRetry" class="btn outline" data-i18n="directRetry"></button></section>',1)
s=s.replace('<div class="modal-actions">','<p class="share-path-label" data-i18n="imageAction"></p><div class="modal-actions">',1)
s=s.replace('<div class="site-copy"><button id="copyWebsite"','<section class="site-path"><p class="share-path-label" data-i18n="siteAction"></p><button id="shareWebsite" class="btn outline" data-i18n="siteShare" type="button"></button><p id="siteShareNote" data-i18n="siteOnly"></p></section><div class="site-copy"><button id="copyWebsite"',1)
marker='translate();scheduleRender(true);\n})();';assert s.count(marker)==1
s=s.replace(marker,(R/'community.js').read_text()+'\n'+marker,1)
s=s.replace('</head>','<script id="communityAssets">window.LINGOTECH_COMMUNITY='+json.dumps(pub,separators=(',',':'))+';</script><style>'+(R/'community.css').read_text()+'</style></head>',1)
s=s.replace('<i>My build crew.</i>','<i>Meet your people.</i>',1).replace('<small>PEOPLE / IDEAS / FRIENDSHIP</small>','<small>LINGOCORNER · PAST EVENT</small>',1)
out=Path('community-candidate');out.mkdir(exist_ok=True)
(out/'index.html').write_text(s)
evidence={'version':'4.0','baseline_git_blob':EXPECTED,'html_sha256':hashlib.sha256(s.encode()).hexdigest(),'bytes':len(s.encode()),'sources':sources,'changes':['2 real-community-inspired frames','3 frame textures and labeled optional historical strip','7 frames total','Capability-first image-only share, including inside WeChat when supported','Separate website-link share','Original camera/forms retained'],'not_verified':['Physical WeChat/iPhone/Android targets','Actual Moments posting','Mainland venue connectivity']}
(out/'release.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
print(json.dumps(evidence,ensure_ascii=False,indent=2))
