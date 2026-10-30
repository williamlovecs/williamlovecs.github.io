/* v4.5: canonical entry, optional event CTA, opt-in local counters, shared-device privacy.
   This code runs inside the existing editor closure. No image assets are replaced.
   No analytics requests, photos, nicknames, file names, or identifiers are sent/stored. */
const VERSION45='4.5';
const LANG45='lingotech.language.v1', COUNTS45='lingotech.counts.v1', ENABLE45='lingotech.counts.enabled.v1', KIOSK45='lingotech.kiosk.v1';
const store45={get:(k,session=false)=>{try{return(session?sessionStorage:localStorage).getItem(k);}catch(_){return null;}},set:(k,v,session=false)=>{try{(session?sessionStorage:localStorage).setItem(k,v);return true;}catch(_){return false;}},remove:(k)=>{try{localStorage.removeItem(k);}catch(_){}}};
let kiosk45=store45.get(KIOSK45,true)==='1',countEnabled45=store45.get(ENABLE45)==='1',lastActive45=Date.now(),lastShareKey45='',prepared45=false;
let resumeAt45=null;
try{const u=new URL(location.href);if(u.searchParams.get('kiosk')==='1')kiosk45=true;if(u.searchParams.get('kiosk')==='0')kiosk45=false;const l=u.searchParams.get('lang');if(l==='zh'||l==='en')store45.set(LANG45,l);for(const k of [...u.searchParams.keys()])if(/^utm_/i.test(k)||['v','kiosk','lang'].includes(k))u.searchParams.delete(k);history.replaceState(null,'',u.pathname+u.search+u.hash);}catch(_){}
store45.set(KIOSK45,kiosk45?'1':'0',true);
config.defaultLanguage=['zh','en','auto'].includes(initialConfig.defaultLanguage)?initialConfig.defaultLanguage:'auto';
function automaticLanguage45(){if(config.defaultLanguage==='zh'||config.defaultLanguage==='en')return config.defaultLanguage;return /^zh\b/i.test((navigator.languages||[])[0]||navigator.language||'en')?'zh':'en';}
function initialLanguage45(){const saved=kiosk45?null:store45.get(LANG45);return saved==='zh'||saved==='en'?saved:automaticLanguage45();}
language=initialLanguage45();
const EVENTS45=['page_open','photo_selected','sample_opened','photo_prepared','save_requested','share_requested','share_handed_to_system','share_cancelled','share_failed','share_fallback','join_clicked','partner_clicked','session_cleared','idle_cleared'];
let counts45={};
try{const parsed=JSON.parse(store45.get(COUNTS45)||'{}'),cutoff=new Date(Date.now()-30*86400000).toISOString().slice(0,10);for(const day of Object.keys(parsed)){if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||day<cutoff)continue;counts45[day]={};for(const key of EVENTS45){const n=parsed[day]?.[key];if(Number.isSafeInteger(n)&&n>0&&n<=1e9)counts45[day][key]=n;}}}catch(_){}
let countsPersisted45=true;
function count45(key){if(!countEnabled45||!EVENTS45.includes(key))return;const day=new Date().toISOString().slice(0,10);counts45[day]??={};counts45[day][key]=(counts45[day][key]||0)+1;const days=Object.keys(counts45).sort();while(days.length>30)delete counts45[days.shift()];countsPersisted45=store45.set(COUNTS45,JSON.stringify(counts45));}
function countReport45(){return{version:VERSION45,scope:'THIS_BROWSER_ONLY',enabled:countEnabled45,persistent:countsPersisted45,dayBoundary:'UTC',unit:'actions, not unique people or completed registrations',networkCollection:false,personalData:false,days:JSON.parse(JSON.stringify(counts45))};}
Object.assign(WORDS.zh,{next45:'加入下一场活动 ↗',nextTitle45:'照片留下了，下一次线下见。',nextHelp45:'工作坊 · 创作者交流 · 项目分享。报名自愿，不影响拍照、保存或分享。',headerNext45:'下一场活动 ↗',autoLanguage45:'自动（跟随浏览器）',kiosk45:'公用展台模式',kioskHelp45:'开启时清除当前照片；闲置 3 分钟自动清除，最后 20 秒提示。仅影响本标签页，不影响其他访客。',kioskActive45:'展台模式：3 分钟无操作自动清除照片',idle45:'即将清除这位访客的照片',stay45:'继续制作',nextVisitor45:'完成 / 下一位',counter45:'启用本机匿名操作计数',counterHelp45:'默认关闭，仅此浏览器保存最近 30 天的汇总次数，不上传照片、昵称或数据。不是全站统计；报名点击不代表报名成功。',counterExport45:'导出本机统计 JSON',counterClear45:'清空本机统计',counterTitle45:'本机统计（不是全站数据）',counterMemory45:'浏览器禁止存储，计数只保留到本页关闭。',privacyReset45:'照片、昵称、导出缓存和相机已清除。',formsHelp:'报名完全自愿。以下飞书入口会在新窗口打开；只有主动提交的表单信息会发给团队。',setupHelp:'活动链接需先核对；展台开关与本机计数只影响本标签页 / 浏览器，不改变其他访客设置。',qrExportHint44:'已附带“制作同款”二维码，指向 Photo Booth。微信长按识别是否可用，请以实际客户端为准。'});
Object.assign(WORDS.en,{next45:'Join our next event ↗',nextTitle45:'Keep the photo. Meet us next time.',nextHelp45:'Workshops · Creator meetups · Project showcases. Signup is optional; saving and sharing stay available.',headerNext45:'Next event ↗',autoLanguage45:'Automatic (browser language)',kiosk45:'Shared booth mode',kioskHelp45:'Enabling clears the current photo. Clears after 3 idle minutes with a 20-second warning. Applies only to this tab.',kioskActive45:'Booth mode: photos clear after 3 idle minutes',idle45:'This visitor’s photo will be cleared soon',stay45:'Keep creating',nextVisitor45:'Done / Next visitor',counter45:'Enable local anonymous action counts',counterHelp45:'Off by default. Stores 30 days of totals in this browser only. No photos, names or data uploads. Not site-wide analytics; signup clicks are not completed registrations.',counterExport45:'Export local counts (JSON)',counterClear45:'Clear local counts',counterTitle45:'Local counts (not site-wide)',counterMemory45:'Storage is blocked. Counts last only until this page closes.',privacyReset45:'Photo, name, export cache and camera cleared.',formsHelp:'Signup is optional. Feishu opens in a new window; only information you submit there is sent to the team.',setupHelp:'Verify event links first. Booth mode and local counts affect this tab / browser only, not other visitors.',qrExportHint44:'The embedded QR opens Photo Booth. Long-press recognition in WeChat depends on the actual client.'});
const style45=document.createElement('style');style45.textContent=`.header-join45{font-size:12px;font-weight:750;color:var(--blue);white-space:nowrap}.next-event45{order:6;border:1px solid #d4dfef;background:#eff4ff;border-radius:13px;padding:14px 16px;margin:18px 0;max-width:478px}.next-event45 h2{font-size:16px;line-height:1.5;margin:0 0 7px}.next-event45 p{font-size:12px;line-height:1.6;margin:0 0 10px;color:var(--muted)}.next-event45 .btn{font-size:13px;min-height:42px}.event-export45{display:flex;align-items:center;flex-wrap:wrap;gap:10px;margin:8px 0 16px;padding:12px;background:#eff4ff;border-radius:10px}.event-export45 small{flex:1;min-width:140px;font-size:11px;line-height:1.6;color:var(--muted)}.kiosk-banner45{background:#fff4cc;border-bottom:1px solid #e3cf7f;text-align:center;font-size:12px;line-height:1.7;padding:8px 16px}.booth-settings45{border-top:1px solid #d9dfeb;margin-top:18px;padding-top:12px}.booth-settings45 .check-label{display:flex;align-items:center;gap:9px}.booth-settings45 input[type=checkbox]{width:18px;height:18px;padding:0;flex-shrink:0}.booth-settings45 button{margin:8px 10px 0 0;white-space:normal}.booth-settings45 pre{white-space:pre-wrap;overflow-wrap:anywhere;max-height:210px;overflow:auto;font-size:11px}.kiosk-warning45{position:fixed;z-index:1200;bottom:18px;left:50%;transform:translateX(-50%);background:#101d42;color:white;padding:18px;border-radius:14px;width:min(94vw,470px);box-shadow:0 8px 30px #0004}.kiosk-warning45 p{margin:0 0 12px;line-height:1.6}.kiosk-warning45 .btn{white-space:normal;min-height:44px}.kiosk-warning45 .actions45{display:flex;gap:10px}.kiosk-cover45{position:fixed;inset:0;z-index:2000;background:#f7f6f2;display:grid;place-items:center;color:#101d42;font-size:24px}.editor-links{flex-wrap:wrap;justify-content:flex-end}.next-visitor45{min-height:36px;font-size:12px;margin-left:auto}.event-export45 a{white-space:normal}@media(max-width:600px){.header-right{gap:8px}.header-join45{font-size:11px}.site-header{gap:8px}.header-right .local-note{display:none}.editor-bar{align-items:flex-start;gap:10px}.editor-links{gap:8px}.next-event45{margin:13px 0 0}.event-export45 .btn{width:100%}.event-export45 small{width:100%}.next-visitor45{margin-left:0}}`;
document.head.append(style45);
function makeLink45(id,key,cls){const a=document.createElement('a');a.id=id;a.dataset.i18n=key;a.className=cls;a.target='_blank';a.rel='noopener noreferrer';a.hidden=true;return a;}
const header45=makeLink45('headerJoin45','headerNext45','header-join45');document.querySelector('.header-right').prepend(header45);
const next45=document.createElement('section');next45.className='next-event45';next45.id='nextEvent45';next45.innerHTML='<h2 data-i18n="nextTitle45"></h2><p data-i18n="nextHelp45"></p>';next45.append(makeLink45('homeJoin45','next45','btn outline'));document.querySelector('.upload-card').insertAdjacentElement('afterend',next45);
const editor45=makeLink45('editorJoin45','headerNext45','text-btn');document.querySelector('.editor-links').prepend(editor45);
const export45=document.createElement('section');export45.className='event-export45';export45.id='eventExport45';export45.append(makeLink45('exportJoin45','next45','btn outline'));const help45=document.createElement('small');help45.dataset.i18n='nextHelp45';export45.append(help45);document.querySelector('#exportModal .modal-head').insertAdjacentElement('afterend',export45);
const nextVisitor45=document.createElement('button');nextVisitor45.type='button';nextVisitor45.id='nextVisitor45';nextVisitor45.className='text-btn next-visitor45';nextVisitor45.dataset.i18n='nextVisitor45';document.querySelector('#exportModal .modal-head').insertBefore(nextVisitor45,$('closeExport'));
const auto45=document.createElement('option');auto45.value='auto';auto45.dataset.i18n='autoLanguage45';$('defaultLanguage').prepend(auto45);
const settings45=document.createElement('section');settings45.className='booth-settings45';settings45.innerHTML='<label class="check-label"><input type="checkbox" id="boothMode45"><span data-i18n="kiosk45"></span></label><p class="help" data-i18n="kioskHelp45"></p><label class="check-label"><input type="checkbox" id="localCounts45"><span data-i18n="counter45"></span></label><p class="help" data-i18n="counterHelp45"></p><p id="counterStorage45" class="help" data-i18n="counterMemory45" hidden></p><details id="countsDetails45"><summary data-i18n="counterTitle45"></summary><pre id="countsView45"></pre></details><button type="button" id="exportCounts45" class="text-btn" data-i18n="counterExport45"></button><button type="button" id="clearCounts45" class="text-btn muted" data-i18n="counterClear45"></button>';$('applyConfig').insertAdjacentElement('beforebegin',settings45);
const banner45=document.createElement('div');banner45.className='kiosk-banner45';banner45.id='kioskBanner45';banner45.dataset.i18n='kioskActive45';$('page').prepend(banner45);
const warn45=document.createElement('section');warn45.className='kiosk-warning45';warn45.id='idleWarning45';warn45.hidden=true;warn45.setAttribute('role','alertdialog');warn45.setAttribute('aria-labelledby','idleLabel45');warn45.innerHTML='<p><b id="idleLabel45" data-i18n="idle45"></b> · <span id="idleSeconds45"></span>s</p><div class="actions45"><button type="button" id="keepSession45" class="btn yellow" data-i18n="stay45"></button><button type="button" id="clearSession45" class="btn outline" data-i18n="nextVisitor45"></button></div>';document.body.append(warn45);
const curtain45=document.createElement('div');curtain45.className='kiosk-cover45';curtain45.hidden=true;curtain45.textContent='LingoTech';document.body.append(curtain45);
let warningFocus45=null;
function hideWarning45(){const focused=warn45.contains(document.activeElement);warn45.hidden=true;if(focused&&warningFocus45?.isConnected)warningFocus45.focus();warningFocus45=null;}
function touch45(){lastActive45=Date.now();hideWarning45();}
function refreshCounts45(){$('countsView45').textContent=JSON.stringify(countReport45(),null,2);$('counterStorage45').hidden=countsPersisted45;}
const joinBefore45=updateJoin;
updateJoin=function(){joinBefore45();let link='';try{if(config.formsVerified)link=validURL(config.joinUrl);}catch(_){}for(const id of ['headerJoin45','homeJoin45','editorJoin45','exportJoin45']){const a=$(id);a.hidden=!link;if(link)a.href=link;else a.removeAttribute('href');}next45.hidden=export45.hidden=!link;};
const langBefore45=setLanguage;
setLanguage=function(next,remember=false){const resolved=next==='auto'?automaticLanguage45():next;langBefore45(resolved);if(remember&&!kiosk45)store45.set(LANG45,language);updateJoin();refreshCounts45();};
$('languageBtn').onclick=()=>setLanguage(language==='zh'?'en':'zh',true);
const configBefore45=readConfig;
readConfig=function(){const result=configBefore45();result.defaultLanguage=['zh','en','auto'].includes($('defaultLanguage').value)?$('defaultLanguage').value:'auto';return result;};
const setupBefore45=$('setupBtn').onclick;
$('setupBtn').onclick=()=>{setupBefore45();$('defaultLanguage').value=config.defaultLanguage;$('boothMode45').checked=kiosk45;$('localCounts45').checked=countEnabled45;refreshCounts45();};
const clearBefore45=clearPhoto;
clearPhoto=function(reason='manual'){
 stopCamera();pointers.clear();gesture=null;photoDataUrl='';prepared45=false;lastShareKey45='';lastShareEvent={action:'none',outcome:'not_tested',error:null};
 Object.assign(state,{showQr44:true,background:'blur'});$('showQr44').checked=true;$('background').value='blur';
 clearBefore45();exportPending=false;$('resultImage').removeAttribute('src');$('siteLinkFallback').hidden=true;$('siteLinkText').value='';$('shareDiagnosticText').textContent='';$('shareDiagnostics').open=false;$('fileError').hidden=true;
 for(const c of [canvas,...document.querySelectorAll('.template canvas')]){c.getContext('2d').clearRect(0,0,c.width,c.height);}
 hideWarning45();lastActive45=Date.now();if(kiosk45)setLanguage(automaticLanguage45());
 count45(reason==='idle'?'idle_cleared':'session_cleared');updateUI();toast(t('privacyReset45'));
};
$('clearBtn').onclick=()=>clearPhoto();$('brandHome').onclick=e=>{e.preventDefault();clearPhoto();};$('nextVisitor45').onclick=()=>clearPhoto();$('clearSession45').onclick=()=>clearPhoto();$('keepSession45').onclick=touch45;
const loadBefore45=loadFile;
loadFile=async function(file){if(!file)return;touch45();const before=state.source,pending=loadBefore45(file),ticket=uploadToken;await pending;if(ticket===uploadToken&&state.own&&state.source!==before&&!state.loading){prepared45=false;count45('photo_selected');}};
const chooseBefore45=chooseScene43;
chooseScene43=function(key){const own=state.own;chooseBefore45(key);if(!own&&state.demo){prepared45=false;count45('sample_opened');}touch45();};
const prepareBefore45=prepareExport;
prepareExport=async function(){await prepareBefore45();if(readyExport()&&state.own&&!prepared45){prepared45=true;count45('photo_prepared');}};
const updateBefore45=updateUI;
updateUI=function(){updateBefore45();banner45.hidden=!kiosk45;$('boothMode45').checked=kiosk45;const event=lastShareEvent,key=shareSession+'|'+event.action+'|'+event.outcome;if(key!==lastShareKey45){lastShareKey45=key;if(event.action==='photo'){const map={requested:'share_requested',handed_to_system_not_delivery_confirmation:'share_handed_to_system',cancelled_or_no_target:'share_cancelled',failed:'share_failed',unsupported:'share_fallback'};if(map[event.outcome])count45(map[event.outcome]);}}};
function sensitive45(){return !!(state.source||state.loading||cameraStream||activeModal==='cameraModal');}
function checkIdle45(now=Date.now()){
 if(!kiosk45||!sensitive45()){hideWarning45();return;}
 const remaining=180000-(now-lastActive45);
 if(remaining<=0){clearPhoto('idle');return;}
 if(remaining<=20000){$('idleSeconds45').textContent=String(Math.ceil(remaining/1000));if(warn45.hidden){warningFocus45=document.activeElement;warn45.hidden=false;$('keepSession45').focus();}}else hideWarning45();
}
$('boothMode45').onchange=e=>{kiosk45=e.target.checked;store45.set(KIOSK45,kiosk45?'1':'0',true);clearPhoto();banner45.hidden=!kiosk45;};
$('localCounts45').onchange=e=>{countEnabled45=e.target.checked;store45.set(ENABLE45,countEnabled45?'1':'0');if(countEnabled45)count45('page_open');refreshCounts45();};
$('countsDetails45').ontoggle=refreshCounts45;
$('exportCounts45').onclick=()=>{refreshCounts45();saveBlob(new Blob([JSON.stringify(countReport45(),null,2)],{type:'application/json'}),'LingoTech-local-counts-'+new Date().toISOString().slice(0,10)+'.json');};
$('clearCounts45').onclick=()=>{counts45={};store45.remove(COUNTS45);refreshCounts45();};
for(const event of ['pointerdown','keydown','input','wheel'])document.addEventListener(event,e=>{if(e.isTrusted&&!warn45.contains(e.target))touch45();},{passive:true,capture:true});
document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(a){if(a.href===config.joinUrl)count45('join_clicked');else if(a.href===config.partnerUrl)count45('partner_clicked');}const b=e.target.closest('button');if(b&&['downloadBtn','modalDownload','savePng'].includes(b.id)&&readyExport())count45('save_requested');});
// Clear expired state BEFORE revealing a resumed shared tab, including suspended timers.
document.addEventListener('visibilitychange',()=>{if(document.hidden){resumeAt45=Date.now();if(kiosk45)curtain45.hidden=false;}else{if(kiosk45)checkIdle45();curtain45.hidden=true;resumeAt45=null;}});
window.addEventListener('pagehide',()=>{if(kiosk45)clearPhoto('leave');});
window.addEventListener('pageshow',e=>{if(kiosk45&&e.persisted)clearPhoto('restore');curtain45.hidden=true;});
setInterval(()=>checkIdle45(),1000);
// The original modal focus trap must not fight with the shared-mode timeout dialog.
document.addEventListener('keydown',e=>{if(warn45.hidden)return;if(e.key==='Tab'){e.preventDefault();e.stopImmediatePropagation();(document.activeElement===$('keepSession45')?$('clearSession45'):$('keepSession45')).focus();}else if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();touch45();}},true);
const diagBefore45=diagnostics;
diagnostics=function(){return{...diagBefore45(),app:'LingoTech Photo Booth '+VERSION45,canonical:CANONICAL,kioskMode:kiosk45,localCountsEnabled:countEnabled45,analyticsScope:'local browser only',networkCollection:false};};
window.LingoTechShareDiagnostics=diagnostics;
window.LingoTechQA45={version:VERSION45,snapshot:()=>({version:VERSION45,kiosk:kiosk45,idleMilliseconds:Date.now()-lastActive45,hasExport:!!exportCache,hasDataUrl:!!photoDataUrl,cameraActive:!!cameraStream,countsEnabled:countEnabled45,language,qr:state.showQr44}),counts:countReport45,checkIdleAt:checkIdle45};
document.querySelectorAll('.version').forEach(e=>e.textContent='v'+VERSION45);
$('boothMode45').checked=kiosk45;$('localCounts45').checked=countEnabled45;banner45.hidden=!kiosk45;
count45('page_open');updateJoin();refreshCounts45();
