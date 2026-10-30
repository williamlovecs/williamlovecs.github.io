"""Apply a versioned, source-preserving repair to the verified v3.1 production HTML.
Python standard library only. Fails closed if the baseline changed.
"""
from pathlib import Path
import json,re,hashlib,sys
R=Path(__file__).resolve().parent
EXPECTED='2e577330ed34b4d17bb41142c0552444e1cab382'
def patch(source):
    data=source.encode('utf-8')
    sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if '<!-- LingoTech release v3.2 -->' in source:return source
    if sha!=EXPECTED:raise RuntimeError('Production baseline changed; refusing overwrite: '+sha)
    s=source
    def replace(a,b):
        nonlocal s
        if s.count(a)!=1:raise RuntimeError('Expected unique anchor: '+a[:90]+' count='+str(s.count(a)))
        s=s.replace(a,b,1)
    f=json.loads((R/'forms.json').read_text(encoding='utf-8'))
    safe=lambda v:json.dumps(v,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    s=re.sub(r'<script id="publicConfig">[\s\S]*?</script>',lambda m:'<script id="publicConfig">window.PHOTOBOOTH_CONFIG = '+safe(f['config'])+';</script><script id="formInputs">window.LINGOTECH_FORMS = '+safe(f['forms'])+';</script>',s,count=1)
    replace('</head>','<meta name="referrer" content="no-referrer"><link rel="canonical" href="https://williamlovecs.github.io/lingotech/"><style>'+ (R/'enhancements.css').read_text()+'</style></head>')
    replace('<span class="version">v3.1</span>','<span class="version">v3.2</span>')
    s=s.replace('3 STYLES','5 STYLES')
    for name in ['updateUI','photoRect','clearPhoto']:
        replace('function '+name+'(', 'function '+name+'Base(')
    replace('async function loadFile(', 'async function loadFileBase(')
    # Clear the previous visitor identity only after the replacement file was decoded successfully.
    replace("state.own=true;state.demo=false;state.fit='contain';", "state.own=true;state.demo=false;state.fit='contain';state.nickname='';state.role='';$('nickname').value='';")
    # Append additional options without changing the existing three templates.
    anchor='<small data-i18n="ideasDesc">深蓝 · 杂志感</small></span></button>'
    more=''
    for key,title,label in [('studio','Studio Notes','奶油 · 手账感'),('night','Meet & Build','深蓝 · 入场券')]:
        more+=f'<button type="button" class="template" data-template="{key}" aria-pressed="false"><canvas id="thumb-{key}" width="216" height="270" aria-hidden="true"></canvas><span><b>{title}</b><small data-i18n="{key}Desc">{label}</small></span></button>'
    replace(anchor,anchor+more)
    replace('<button id="setupBtn" type="button" class="text-btn" data-i18n="setup">主办方设置</button>', '<div class="footer-actions"><button id="formsBtn" type="button" class="text-btn" data-i18n="forms">活动报名 / 商务合作</button><button id="setupBtn" type="button" class="text-btn" data-i18n="setup">主办方设置</button></div>')
    # Save-bar supplemental entry stays available even when native sharing is supported.
    anchor='<span data-i18n="share">分享</span></button></div></div>\n</aside>'
    replace(anchor,'<span data-i18n="share">分享</span></button></div><div class="social-options"><button id="wechatShare" class="text-btn" type="button" data-i18n="shareWechat" disabled>微信 / 朋友圈</button><button id="rotatePhoto" class="text-btn muted" type="button" data-i18n="rotate">旋转 90°</button></div></div>\n</aside>')
    guide='<section id="wechatGuide" class="wechat-guide" hidden><h3 data-i18n="wechatTitle">发给微信好友或朋友圈</h3><p data-i18n="wechatOne"></p><p data-i18n="wechatTwo"></p><p class="disclaimer" data-i18n="wechatWhy"></p></section>'
    replace('<p id="saveHint" class="help"></p>',guide+'<p id="saveHint" class="help"></p>')
    replace('<button id="modalShare" type="button" class="btn outline" data-i18n="share">分享</button>', '<button id="modalShare" type="button" class="btn outline" data-i18n="otherApps">分享至其他应用</button>')
    anchor='<div class="join-section">'
    extra='<p id="shareNote" class="share-note"></p><div class="site-copy"><button id="wechatInModal" class="text-btn" data-i18n="shareWechat" type="button">微信 / 朋友圈</button><button id="savePng" class="text-btn muted" data-i18n="pngOriginal" type="button">下载无损 PNG</button></div><div class="site-copy"><button id="copyWebsite" class="text-btn" data-i18n="copySite" type="button">复制 Photo Booth 网址</button></div><div id="siteLinkFallback" hidden><input id="siteLinkText" type="text" readonly aria-label="Photo Booth website address"></div>'
    replace(anchor,extra+anchor)
    replace('<p id="joinNote" class="help"></p>', '<a id="partnerLink" target="_blank" rel="noopener noreferrer" hidden data-i18n="business">商务合作</a><button id="formsInModal" class="text-btn" type="button" data-i18n="forms">活动报名 / 商务合作</button><p id="joinNote" class="help"></p>')
    replace('<label for="eventInput" data-i18n="eventLabel">', '<label for="partnerInput" data-i18n="partnerLabel">B 端商务合作链接（HTTPS）</label><input id="partnerInput" type="url" placeholder="https://…" autocomplete="off"><label class="check-label"><input id="formsVerified" type="checkbox"><span data-i18n="formsVerified">已人工核对两个表单的用途</span></label><label for="eventInput" data-i18n="eventLabel">')
    modal='<div id="formsModal" class="modal" hidden role="dialog" aria-modal="true" aria-labelledby="formsTitle"><section class="modal-card forms-card"><div class="modal-head"><h2 id="formsTitle" data-i18n="forms">活动报名 / 商务合作</h2><button id="closeForms" class="close-btn" type="button" aria-label="Close forms">×</button></div><p class="help" data-i18n="formsHelp"></p><p class="help" id="formMappingNote" data-i18n="formUnverified"></p><div id="formLinks" class="form-grid"></div></section></div>'
    replace('<div id="toast"',modal+'<div id="toast"')
    replace('translate();scheduleRender(true);\n})();', (R/'enhancements.js').read_text()+'\ntranslate();scheduleRender(true);\n})();')
    return s.replace('<!doctype html>','<!doctype html>\n<!-- LingoTech release v3.2 -->',1)
if __name__=='__main__':
    if len(sys.argv)==3:
        src,out=map(Path,sys.argv[1:]);out.write_text(patch(src.read_text()),encoding='utf-8');print(out)
    else:
        paths=[Path('lingotech/index.html'),Path('lingotech-photo-booth/index.html')]
        outputs=[patch(p.read_text()) for p in paths]
        for p,out in zip(paths,outputs):p.write_text(out,encoding='utf-8')
        assert outputs[0]==outputs[1]
        print('Updated both Photo Booth paths; all other site content unchanged.')
