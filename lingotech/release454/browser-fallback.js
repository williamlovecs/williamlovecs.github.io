/* v4.5.4: Android in-app browser fallback and non-destructive update hint.
   Preserve scene rendering, image assets, QR payload and supported native share. */
(function(){
  Object.assign(WORDS.zh, {
    noMenu453:'如果长按照片没有“保存图片”选项，可点“下载 JPG 文件”，从下载目录查找。若微信拦截下载，请用右上角菜单在系统浏览器打开。',
    downloadFallback454:'下载 JPG 文件',
    updateReady454:'Photo Booth 有更新。请先保存当前照片，再刷新网页。',
    updateNow454:'刷新到新版'
  });
  Object.assign(WORDS.en, {
    noMenu453:'If long-press Save Image is unavailable, tap Download JPG file and check Downloads. If your app blocks downloads, use its menu to open in your system browser.',
    downloadFallback454:'Download JPG file',
    updateReady454:'A newer Photo Booth is available. Save this photo before refreshing.',
    updateNow454:'Refresh to update'
  });
  // The existing secondary action becomes a real JPG download when file sharing is unavailable.
  const shareAction454=$('modalShare');
  const previousUpdate454=updateUI;
  updateUI=function(){
    previousUpdate454();
    const ready=readyExport(),nativeReady=ready&&!!shareCandidate();
    const fileFallback=ready&&!nativeReady&&(mobile()||isWechat());
    shareAction454.hidden=!(nativeReady||fileFallback);
    shareAction454.disabled=!ready||sharing;
    shareAction454.textContent=nativeReady?t('native453'):t('downloadFallback454');
  };
  shareAction454.onclick=()=>{
    if(!readyExport()||sharing)return;
    if(shareCandidate())sharePhoto('native');
    else downloadJpg(); // file requested; NOT a claim of successful Photos-library save
  };
  // Never force reload while editing: a reload would destroy the visitor's photo.
  // GitHub Pages does not support application-defined cache-control response headers.
  const freshness454=document.createElement('div');
  freshness454.id='freshness454';freshness454.hidden=true;
  freshness454.setAttribute('role','status');
  const freshnessText454=document.createElement('span');
  const freshnessButton454=document.createElement('button');
  freshnessButton454.type='button';freshnessButton454.className='text-btn';
  freshness454.append(freshnessText454,freshnessButton454);
  const style454=document.createElement('style');style454.id='release454';
  style454.textContent='#freshness454[hidden]{display:none!important}#freshness454{position:fixed;z-index:1400;bottom:calc(12px + env(safe-area-inset-bottom));left:50%;transform:translateX(-50%);width:min(92vw,520px);display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:12px;background:#fff6d5;border:1px solid #e9d38f;box-shadow:0 5px 22px #0002;color:#101d42;font:12px/1.45 system-ui,sans-serif}#freshness454 span{flex:1}#freshness454 button{min-height:40px;white-space:normal;font-weight:750}';
  document.head.append(style454);document.body.append(freshness454);
  let targetVersion454='',lastVersionCheck454=0;
  function redrawUpdate454(){
    freshnessText454.textContent=t('updateReady454');
    freshnessButton454.textContent=t('updateNow454');
  }
  function newer454(remote){
    const parsed=s=>/^\d+\.\d+\.\d+$/.test(s)?s.split('.').map(Number):[];
    const a=parsed(remote),b=parsed('4.5.4');
    if(a.length!==3||b.length!==3)return false;
    for(let i=0;i<3;i++){if(a[i]>b[i])return true;if(a[i]<b[i])return false;}return false;
  }
  async function checkVersion454(){
    if(typeof fetch!=='function'||Date.now()-lastVersionCheck454<120000)return;
    lastVersionCheck454=Date.now();
    try{
      const response=await fetch('/lingotech/release.json?check='+Date.now(),{cache:'no-store',credentials:'omit'});
      if(!response.ok)return;
      const info=await response.json();
      if(!newer454(info?.version))return;
      targetVersion454=info.version;redrawUpdate454();freshness454.hidden=false;
    }catch(_){/* Offline and restricted WebViews should remain fully usable. */}
  }
  freshnessButton454.onclick=()=>{
    // One fresh HTML request; normal startup restores the exact clean URL.
    location.replace('/lingotech/?v='+encodeURIComponent(targetVersion454)+'-'+Date.now());
  };
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)checkVersion454();});
  setTimeout(checkVersion454,1100);
  const previousDiagnostics454=diagnostics;
  diagnostics=function(){return{...previousDiagnostics454(),app:'LingoTech Photo Booth 4.5.4',nativeShareFallback:'JPG download; photo library not verified'};};
  window.LingoTechShareDiagnostics=diagnostics;
  window.LingoTechQA454={version:'4.5.4',snapshot:()=>({shareFallbackVisible:!shareAction454.hidden&&!shareCandidate(),shareButtonLabel:shareAction454.textContent,updateAvailable:!freshness454.hidden,targetVersion:targetVersion454})};
  updateUI();
})();