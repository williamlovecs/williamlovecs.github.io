"""v4.5.2: deterministic, asset-preserving reliability patch on exact v4.5.1."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'_archive/lingotech-photo-booth/v4.5.1-20261031/index.html'
b=BASE.read_bytes()
assert hashlib.sha256(b).hexdigest()=='3f44a0d1c5653ddf6fc35795fca709f5d5424ae33b75be5acbc4a5a4d24033b5'
s=b.decode();before=s
s=s.replace('name="app-version" content="4.5.1"','name="app-version" content="4.5.2"').replace("const VERSION45='4.5.1';","const VERSION45='4.5.2';")
s=s.replace('<!-- LingoTech release v4.5 unified entry and shared-device privacy -->','<!-- LingoTech release v4.5.2 deep regression and reliability fixes -->')
# QR thumbnails must use the template being drawn, not another selected template.
s=s.replace('function paintQr44(c,W,H){','function paintQr44(c,W,H,m=state){').replace("dark=state.template==='ideas'||state.template==='night';","dark=m.template==='ideas'||m.template==='night';").replace('if(m.showQr44!==false)paintQr44(c,W,H);','if(m.showQr44!==false)paintQr44(c,W,H,m);')
s=s.replace('for(const ch of Array.from(str))','for(const ch of graphemes452(str))')
patch=r'''
/* v4.5.2: no new photo assets, uploads, trackers, remote fonts or dependencies. */
function graphemes452(value){const s=String(value||'');return typeof Intl.Segmenter==='function'?[...new Intl.Segmenter(undefined,{granularity:'grapheme'}).segment(s)].map(x=>x.segment):Array.from(s);}
// Consume existing supported settings first (v4.5), then leave a single clean URL.
try{const u=new URL(location.href);if(u.protocol==='https:'||u.protocol==='http:'){if(/^\/lingotech(?:\/index\.html)?\/?$/.test(u.pathname))u.pathname='/lingotech/';u.search='';u.hash='';history.replaceState(null,'',u.pathname);}}catch(_){}
Object.assign(WORDS.zh,{
 textureFixed452:'这个版式使用固定底纹。选择「认识朋友」或「文化与玩乐」相框，可调整底纹。',
 missingForm452:'这个入口尚未配置，请直接联系现场工作人员。',
 openForm:'打开表单 ↗',
 shareRecover452:'分享面板已关闭？返回编辑',
 shareUnknown452:'系统没有返回分享结果。照片已保留；请在目标应用确认是否发送成功。',
 retryExport452:'重新生成照片',
 shareCancelled:'已取消分享，或设备没有可用分享目标。照片已保留。',
 eventLabel:'照片上的活动名称（选填，最多 32 字）'
});
Object.assign(WORDS.en,{
 textureFixed452:'This layout has a fixed paper style. Choose the Friends or Culture & Play frame to change its texture.',
 missingForm452:'This entry is not configured. Please speak to the event team.',
 openForm:'Open form ↗',
 shareRecover452:'Share sheet closed? Return to editing',
 shareUnknown452:'The system did not return a share result. Your photo is kept; check delivery in the target app.',
 retryExport452:'Retry preparing photo',
 shareCancelled:'Sharing was cancelled, or no share target was available. Your photo is kept.',
 eventLabel:'Event label on photos (optional, up to 32 characters)'
});
// Avoid rebuilding focused form links and decoding their QR assets on every render.
let formSignature452='';
function checkedLink452(value){try{return validURL(value);}catch(_){return '';}}
updateJoin=function(){
 const verified=!!config.formsVerified,join=verified?checkedLink452(config.joinUrl):'',partner=verified?checkedLink452(config.partnerUrl):'';
 for(const [id,url]of[['joinLink',join],['partnerLink',partner],['headerJoin45',join],['homeJoin45',join],['editorJoin45',join],['exportJoin45',join]]){
  const a=$(id);if(!a)continue;a.hidden=!url;a.target='_blank';a.rel='noopener noreferrer';if(url)a.href=url;else a.removeAttribute('href');
 }
 $('joinNote').textContent=t(join?'joinOptional':verified?'joinMissing':'formUnverified');
 if($('nextEvent45'))$('nextEvent45').hidden=!join;if($('eventExport45'))$('eventExport45').hidden=!join;
 const items=formItems(),signature=JSON.stringify([language,verified,items.map(f=>[f.url,f.label])]);
 if(signature===formSignature452)return;formSignature452=signature;
 const host=$('formLinks');if(!host)return;host.replaceChildren();
 for(const f of items){
  const card=document.createElement('article');card.className='form-card';
  const h=document.createElement('h3');h.textContent=f.label;card.append(h);
  const url=checkedLink452(f.url);
  if(!url){const missing=document.createElement('p');missing.textContent=t('missingForm452');card.append(missing);host.append(card);continue;}
  const a=document.createElement('a');a.href=url;a.target='_blank';a.rel='noopener noreferrer';a.className='btn primary';a.textContent=t('openForm');card.append(a);
  const known=INPUT_FORMS.find(x=>checkedLink452(x.url)===url);
  if(known?.qr){const im=document.createElement('img');im.src=known.qr;im.alt=f.label;im.width=180;im.height=180;im.className='form-qr';card.append(im);const hint=document.createElement('p');hint.textContent=t('formQr');card.append(hint);}
  host.append(card);
 }
 $('formMappingNote').hidden=verified;
};
// Paper controls are only offered when the selected layout actually draws them.
const textureNote452=document.createElement('p');textureNote452.id='textureNote452';textureNote452.className='help';textureNote452.dataset.i18n='textureFixed452';
$('communityPaper').insertAdjacentElement('afterend',textureNote452);
function syncTexture452(){const supported=state.scene!=='build'&&['friends','play'].includes(state.template);$('communityPaper').hidden=!supported;$('communityPaper').disabled=!supported;document.querySelector('label[for="communityPaper"]').hidden=!supported;textureNote452.hidden=supported;}
// Native maxlength counts UTF-16 code units, not the 40 visible characters promised.
let composing452=false;
$('nickname').removeAttribute('maxlength');$('nickname').setAttribute('aria-describedby','nicknameLimit452');
const nickCount452=document.createElement('small');nickCount452.id='nicknameLimit452';nickCount452.className='help';$('nickname').insertAdjacentElement('afterend',nickCount452);
function syncNickname452(e){if(composing452||e?.isComposing)return;const input=$('nickname'),next=limitText(input.value,40);if(input.value!==next)input.value=next;state.nickname=next;nickCount452.textContent=graphemes452(next).length+' / 40';scheduleRender(true);}
$('nickname').oninput=syncNickname452;$('nickname').onblur=syncNickname452;
$('nickname').addEventListener('compositionstart',()=>{composing452=true;});
$('nickname').addEventListener('compositionend',()=>{composing452=false;syncNickname452();});
$('eventInput').maxLength=32;
// Export errors can be retried without replacing a photo or losing its edits.
let exportFailed452=false;
const retry452=document.createElement('button');retry452.type='button';retry452.id='retryExport452';retry452.className='text-btn';retry452.dataset.i18n='retryExport452';retry452.hidden=true;
$('saveBar').append(retry452);retry452.onclick=()=>{exportFailed452=false;setError('');scheduleRender(true);};
const dropBefore452=dropExport;
dropExport=function(){exportFailed452=false;retry452.hidden=true;dropBefore452();};
const prepareBefore452=prepareExport;
prepareExport=async function(){const rev=state.revision;await prepareBefore452();if(rev===state.revision&&canExport()&&!exportPending&&!readyExport()){exportFailed452=true;retry452.hidden=false;}};
// Some WebViews never settle navigator.share(). Provide explicit, non-destructive recovery.
let shareTimer452=null,shareExpired452=false;
const recoveryButtons452=[];
for(const [id,parent]of[['recoverShare452',$('saveBar')],['recoverShareModal452',$('shareNote').parentElement]]){
 const el=document.createElement('button');el.type='button';el.id=id;el.className='text-btn share-recovery452';el.dataset.i18n='shareRecover452';el.hidden=true;
 el.onclick=()=>{if(!sharing)return;shareSession++;sharing=false;shareExpired452=false;clearTimeout(shareTimer452);lastShareEvent={action:lastShareEvent.action,outcome:'result_unknown_user_recovered',error:null};updateUI();refreshDiagnostics();toast(t('shareUnknown452'));};
 parent.append(el);recoveryButtons452.push(el);
}
function armShare452(){clearTimeout(shareTimer452);shareExpired452=false;const id=shareSession;if(!sharing)return;shareTimer452=setTimeout(()=>{if(sharing&&shareSession===id){shareExpired452=true;updateUI();}},30000);}
const sharePhotoBefore452=sharePhoto;
sharePhoto=function(channel='photo'){if(sharing)return;sharePhotoBefore452(channel);armShare452();};
const shareWebsiteBefore452=shareWebsite;
shareWebsite=function(){if(sharing)return;shareWebsiteBefore452();armShare452();};
$('shareWebsite').onclick=()=>shareWebsite();
const updateBefore452=updateUI;
updateUI=function(){
 updateBefore452();syncTexture452();nickCount452.textContent=graphemes452(state.nickname).length+' / 40';
 if(!sharing){clearTimeout(shareTimer452);shareExpired452=false;}
 for(const el of recoveryButtons452)el.hidden=!(sharing&&shareExpired452);
 retry452.hidden=!exportFailed452;
 for(const id of['modalDownload','savePng'])$(id).disabled=!readyExport();
 const closeNames=language==='zh'?['关闭','关闭相机','关闭报名与合作入口']:['Close','Close camera','Close events and partnerships'];
 for(const id of['closeExport','closeSetup'])$(id).setAttribute('aria-label',closeNames[0]);$('closeCamera').setAttribute('aria-label',closeNames[1]);$('closeForms').setAttribute('aria-label',closeNames[2]);
};
const clearBefore452=clearPhoto;
clearPhoto=function(reason='manual'){composing452=false;clearTimeout(shareTimer452);shareExpired452=false;exportFailed452=false;clearBefore452(reason);};
// Keep focused controls visible above a changing mobile action bar and software keyboard.
const style452=document.createElement('style');style452.id='release452';style452.textContent=`
.share-recovery452{white-space:normal;text-align:left;line-height:1.5;min-height:40px}#nicknameLimit452{display:block;margin-top:5px}#textureNote452{margin-bottom:12px}.scene-options button,.fit-choice,.tags button{min-height:40px}
@media(max-width:899px){body.is-editing{padding-bottom:calc(var(--action-height452,130px) + 18px)!important}.is-editing .toast{bottom:calc(var(--action-height452,130px) + 12px)}.save-bar{max-height:45svh;overflow:auto}.is-editing input,.is-editing select{scroll-margin-bottom:calc(var(--action-height452,130px) + 28px)}}
@media(max-width:360px){#headerJoin45{display:none}.editor-bar{flex-wrap:wrap}.editor-links{width:100%;justify-content:flex-start}}
@media(max-width:650px){.modal-head{flex-wrap:wrap;gap:8px}.modal-head h2{overflow-wrap:anywhere}.modal-card{max-width:100%;overscroll-behavior:contain}.btn{max-width:100%}.event-export45 small{min-width:0}}
`;
document.head.append(style452);
if(typeof ResizeObserver==='function')new ResizeObserver(entries=>{const height=entries[0]?.target.getBoundingClientRect().height||0;document.documentElement.style.setProperty('--action-height452',Math.ceil(height)+'px');}).observe($('saveBar'));
for(const ev of ['pointermove','touchmove'])document.addEventListener(ev,e=>{if(e.isTrusted&&(pointers.size||e.type==='touchmove'))touch45();},{passive:true});
window.LingoTechQA452={version:'4.5.2',snapshot:()=>({sharing,shareRecovery:shareExpired452,exportFailed:exportFailed452,textureEditable:!$('communityPaper').hidden,formSignature:!!formSignature452})};
updateJoin();updateUI();
'''
marker='translate();scheduleRender(true);\n})();';assert s.count(marker)==1
s=s.replace(marker,patch+'\n'+marker)
assets=lambda x:re.findall(r'data:image/[^\s\"\']+',x)
assert assets(before)==assets(s),'Original photo or QR bytes changed'
assert s.count('rel="canonical"')==1
(ROOT/'lingotech/index.html').write_text(s)
m=json.loads((ROOT/'lingotech/release.json').read_text())
m.update(version='4.5.2',baseline_commit='6c59267b06c49982052ee50c128aeb57e126c0fb',previous_release_archive=str(BASE.relative_to(ROOT)),sha256=hashlib.sha256(s.encode()).hexdigest())
m['changes']+=['no inert texture selector for fixed-style frames','empty forms no longer link back to this page','stable form DOM during rerenders','40 visible-character limit with IME support','recover unreturned native shares','retry failed image export','clean index.html and all query parameters','responsive action bar spacing']
(ROOT/'lingotech/release.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(m,ensure_ascii=False,indent=2))
