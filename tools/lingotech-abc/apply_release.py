from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
EXPECTED='1d8af0393711853ce77e07578e4a7fece1c2fb7fdadae9f64bc26b503ed15b60'
OUTPUT='c6c29e63fc443e63631072b39b76cf736c275d7fd7512ae1ad0ff9442947645c'
def patch(s):
 if hashlib.sha256(s.encode()).hexdigest()!=EXPECTED:raise ValueError('Baseline changed; refusing overwrite')
 s=s.replace('<!-- LingoTech release v3.2 -->','<!-- LingoTech release v4.1 -->')
 s=s.replace('<span class="version">v4.0</span>','<span class="version">v4.1</span>')
 target='translate();scheduleRender(true);\n})();';assert s.count(target)==1
 s=s.replace(target,(HERE/'v41.js').read_text()+'\n'+target)
 diag='<details id="shareDiagnostics" class="share-diagnostics"><summary data-i18n="shareDiagnostics">分享检测（仅本机）</summary><p data-i18n="diagnosticNote"></p><pre id="shareDiagnosticText"></pre><button id="copyShareDiagnostics" type="button" class="text-btn" data-i18n="copyDiagnostics">复制检测结果</button></details>'
 target='<div class="join-section">';assert s.count(target)==1;s=s.replace(target,diag+target)
 css='''<style>.share-diagnostics{margin:14px 0;border:1px solid #dce4ef;border-radius:10px;padding:10px 12px;font-size:11px;color:#60718d}.share-diagnostics summary{cursor:pointer;font-weight:700;color:#165dff}.share-diagnostics p{line-height:1.65}.share-diagnostics pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:10px;line-height:1.55}.share-diagnostics button{font-size:11px}.community-options select{min-width:0}</style>'''
 s=s.replace('</head>',css+'</head>',1)
 old="state.source=im;state.userImage=im;state.sampleOrigin='';state.own=true;";assert old in s
 s=s.replace(old,"state.source=im;state.userImage=im;resetCommunityChoices();state.sampleOrigin='';state.own=true;",1)
 assert hashlib.sha256(s.encode()).hexdigest()==OUTPUT,'Output differs from tested bytes'
 return s
if __name__=='__main__':
 targets=[Path('lingotech/index.html'),Path('lingotech-photo-booth/index.html')]
 results=[patch(p.read_text()) for p in targets]
 assert results[0]==results[1]
 for p,s in zip(targets,results):p.write_text(s)
 p=Path('lingotech/release.json');manifest=json.loads(p.read_text());manifest['version']='4.1';manifest['html_sha256']=OUTPUT;manifest['bytes']=len(results[0].encode());manifest['baseline_sha256']=EXPECTED
 manifest['changes'] += ['Stronger visible community textures and model-specific historical-strip geometry','Image-only direct-first share retained, including WeChat capability path','Local-only share diagnostics: payload/capability/error, no photo or identity','New visitor resets optional decorative choices']
 manifest['latest_checks']={'functional':22,'render_cases':84,'theme_cases':12,'method':'Headless Chromium; Share interfaces mocked and mobile UA/viewports emulated. No physical device test.'}
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'version':'4.1','sha256':OUTPUT,'updated':[str(x) for x in targets]},indent=2))
