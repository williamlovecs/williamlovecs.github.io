/* v4.1: audit-safe community rendering and local sharing diagnostics.
   No photo upload, no forced WeChat route, no user tracking. */
let lastShareEvent={action:'none',outcome:'not_tested',error:null};
function photoRect(template,W,H,model=state){
 if(template==='friends'||template==='play'){
  const land=W>H,strip=model.memoryStrip?158:0;
  return{x:46,y:land?92:123,w:W-92,h:H-(land?275:310)-strip};
 }
 if(template==='studio'||template==='night'){const land=W>H;return{x:42,y:land?84:108,w:W-84,h:H-(land?204:267)};}
 return photoRectBase(template,W,H);
}
function basePatternColor(m){return m.communityPaper==='picnic'?'#f0f6e9':m.communityPaper==='celebrate'?'#fff5e3':'#fffcf5';}
function drawFriends(c,W,H,m){
 themePattern(c,W,H,m);const r=photoRect('friends',W,H,m);
 // White edge, translucent paper: texture remains visible outside the user's photo.
 c.save();c.shadowBlur=12;c.shadowOffsetY=5;c.shadowColor='#18274718';box(c,23,17,W-46,H-34,'#fffefb',3);c.restore();
 c.save();c.beginPath();c.rect(30,23,W-60,H-46);c.clip();c.globalAlpha=.52;themePattern(c,W,H,m);c.restore();
 brand(c,47,26,false,.83);txt(c,sampleLabel(m)||'HELLO / 你好 / HOLA',W-47,40,17,'#6c7892',650,'right',W-420);
 const p=drawPhoto(c,r,m);c.save();c.translate(W*.49,r.y-18);c.rotate(-.045);box(c,-90,-5,180,17,'#ffe02ea0');c.restore();
 const y=r.y+r.h;brush(c,53,y+70,345);txt(c,'Find your people.',52,y+23,W>H?53:61,BLUE,750,'left',W-155,'Georgia,serif');sparkle(c,W-90,y+61,18,BLUE);
 borderCaption(c,W,y+109,m,'不同背景，同样的好奇心。');txt(c,'INSPIRED BY LINGOCORNER / 社群灵感',54,y+148,13,'#6e798e',550);drawMemoryStrip(c,W,H,m);return{r,p};
}
function drawPlay(c,W,H,m){
 const paper={...m,communityPaper:m.communityPaper==='paper'?'celebrate':m.communityPaper};themePattern(c,W,H,paper);
 const r=photoRect('play',W,H,m);box(c,24,18,W-48,H-36,basePatternColor(paper),12);
 c.save();c.beginPath();c.rect(30,24,W-60,H-48);c.clip();c.globalAlpha=.68;themePattern(c,W,H,paper);c.restore();
 brand(c,47,25,false,.83);txt(c,sampleLabel(m)||'CULTURE + PLAY / GOOD TIMES',W-48,40,17,'#69738a',650,'right',W-430);
 const p=drawPhoto(c,r,m);for(let x=48;x<W-48;x+=23)line(c,x,r.y+r.h+12,x+9,r.y+r.h+12,'#c6b991',2);
 const y=r.y+r.h;box(c,45,y+29,W-90,63,YELLOW,4);txt(c,'GOOD TIMES TOGETHER.',59,y+40,W>H?41:46,INK,850,'left',W-205);bananaMotif(c,W-131,y+24,1.03);
 borderCaption(c,W,y+112,m,'多一点好奇，多一些朋友。');txt(c,'LINGOCORNER INSPIRED / 文化与玩乐',54,y+151,13,'#6e798e',550);drawMemoryStrip(c,W,H,m);return{r,p};
}
Object.assign(WORDS.zh,{share:'直接分享照片',otherApps:'直接分享照片',shareDiagnostics:'分享检测（仅本机）',copyDiagnostics:'复制检测结果',diagnosticsCopied:'已复制兼容信息，不含照片或昵称。',diagnosticNote:'此检测不能读取已安装的应用，也不能确认微信是否发送成功。没有数据上传。',shareReadyNote:'先调用设备分享面板；只有不支持或失败时才显示备用路径。'});
Object.assign(WORDS.en,{share:'Share photo',otherApps:'Share photo',shareDiagnostics:'Share diagnostics · local only',copyDiagnostics:'Copy diagnostics',diagnosticsCopied:'Compatibility details copied; no photo or nickname included.',diagnosticNote:'This cannot inspect installed apps or confirm WeChat delivery. Nothing is uploaded.',shareReadyNote:'Native sharing first. A fallback appears only when unsupported or unsuccessful.'});
function diagnostics(){
 let jpeg=false,png=false;try{jpeg=!!(exportCache?.file&&navigator.canShare?.({files:[exportCache.file]}));png=!!(exportCache?.pngFile&&navigator.canShare?.({files:[exportCache.pngFile]}));}catch(_){}
 return{app:'LingoTech Photo Booth 4.1',secureContext:window.isSecureContext,inWeChat:isWechat(),systemShare:typeof navigator.share==='function',fileCapabilityCheck:typeof navigator.canShare==='function',jpgAccepted:jpeg,pngAccepted:png,photoPrepared:readyExport(),sharePayload:'files only — no text or URL',lastAttempt:{...lastShareEvent},targetApps:'not observable by this page',delivery:'not observable by this page'};
}
function refreshDiagnostics(){const el=$('shareDiagnosticText');if(el)el.textContent=JSON.stringify(diagnostics(),null,2);}
function sharePhoto(channel='photo'){
 if(!readyExport()||sharing)return;
 const f=shareCandidate();
 if(!f){lastShareEvent={action:'photo',outcome:'unsupported',error:null};openExport('wechat');refreshDiagnostics();toast(t('shareFallback'));return;}
 const session=++shareSession,revision=state.revision;sharing=true;lastShareEvent={action:'photo',outcome:'requested',error:null};updateUI();
 const finish=()=>{if(session===shareSession){sharing=false;updateUI();refreshDiagnostics();}};
 const failed=e=>{if(session!==shareSession||revision!==state.revision){finish();return;}lastShareEvent={action:'photo',outcome:e?.name==='AbortError'?'cancelled_or_no_target':'failed',error:e?.name||'Error'};finish();if(e?.name==='AbortError'){toast(t('shareCancelled'));return;}openExport('wechat');refreshDiagnostics();toast(t('shareFailed'));};
 try{const result=navigator.share({files:[f]});Promise.resolve(result).then(()=>{if(session!==shareSession||revision!==state.revision){finish();return;}lastShareEvent={action:'photo',outcome:'handed_to_system_not_delivery_confirmation',error:null};finish();if(!readyExport())return;openExport('default');refreshDiagnostics();toast(t('shareDone'));}).catch(failed);}catch(e){failed(e);}
}
function shareWebsite(){
 if(sharing)return;const payload={title:'LingoTech Photo Booth',url:CANONICAL};let supported=false;
 try{supported=typeof navigator.share==='function'&&(!navigator.canShare||navigator.canShare(payload));}catch(_){}
 if(!supported){lastShareEvent={action:'website',outcome:'copy_link_fallback',error:null};copyWebsite();if(isWechat())$('siteShareNote').textContent=t('siteInWechat');refreshDiagnostics();return;}
 const id=++shareSession;sharing=true;lastShareEvent={action:'website',outcome:'requested',error:null};updateUI();
 const settle=(outcome,error)=>{if(id!==shareSession)return false;sharing=false;lastShareEvent={action:'website',outcome,error:error||null};updateUI();refreshDiagnostics();return true;};
 try{Promise.resolve(navigator.share(payload)).then(()=>{if(settle('handed_to_system_not_delivery_confirmation'))toast(t('siteOnly'));}).catch(e=>{if(!settle(e?.name==='AbortError'?'cancelled_or_no_target':'failed',e?.name))return;if(e?.name!=='AbortError')copyWebsite();});}catch(e){if(settle('failed',e?.name))copyWebsite();}
}
function resetCommunityChoices(){state.memoryStrip=false;state.communityPaper='paper';$('memoryStrip').checked=false;$('communityPaper').value='paper';lastShareEvent={action:'none',outcome:'not_tested',error:null};}
$('clearBtn').addEventListener('click',resetCommunityChoices);
$('shareDiagnostics').ontoggle=refreshDiagnostics;
$('copyShareDiagnostics').onclick=async()=>{const text=JSON.stringify(diagnostics(),null,2);try{await navigator.clipboard.writeText(text);toast(t('diagnosticsCopied'));}catch(_){const r=document.createRange();r.selectNodeContents($('shareDiagnosticText'));getSelection().removeAllRanges();getSelection().addRange(r);toast(language==='zh'?'请复制已选中的检测信息。':'Copy the selected diagnostics.');}};
// Listeners are rebound explicitly: no stale function references from an earlier release.
$('shareBtn').onclick=()=>sharePhoto('photo');$('modalShare').onclick=()=>sharePhoto('photo');$('wechatShare').onclick=()=>sharePhoto('wechat');$('wechatInModal').onclick=()=>sharePhoto('wechat');$('directRetry').onclick=()=>sharePhoto('wechat');$('shareWebsite').onclick=shareWebsite;
window.LingoTechShareDiagnostics=diagnostics;
