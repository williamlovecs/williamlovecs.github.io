/* v4.5.3 — album-first mobile export; all images remain on this device. */
(function installMobileExport453(){
  const mobile=()=>/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)||
    (navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  const ios=()=>/iPhone|iPad|iPod/i.test(navigator.userAgent)||
    (navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  let notice='',viewerMode='default';
  const words={
    zh:{save453:'保存图片',share453:'分享照片',wechat453:'发微信 / 朋友圈',title453:'照片已生成',
      hold453:'长按下方图片 → 选择“保存图片”或“添加到照片”。',
      desktop453:'下载 JPG 图片，或使用系统分享。',
      wechatTip453:'保存后，在微信聊天或朋友圈中从相册选这张图。',
      noMenu453:'长按没有保存菜单？可试“查看大图”或系统分享。仍不可用时，请用 Safari / 系统浏览器重新打开。',
      native453:'系统保存 / 分享',view453:'查看大图，长按保存',download453:'下载 JPG 文件',
      more453:'更多：PNG、网站链接与检测',back453:'返回保存页',viewer453:'长按图片保存',
      preparing453:'正在生成照片…',ready453:'图片已就绪 · 照片只在本机处理',
      unsupported453:'当前浏览器不支持图片系统分享。请长按图片保存，再从微信相册发送。',
      cancelled453:'分享已取消，或系统没有可用目标。照片仍在这里，可以长按保存。',
      failed453:'系统分享未完成。请长按图片保存，再从微信相册发送。',
      sent453:'已交给系统分享；是否发出，请在微信或目标应用确认。',
      pending453:'系统分享处理中。图片仍保留在本页。',
      recover453:'系统面板已关闭？返回图片保存',
      unknown453:'已返回保存页。系统未报告结果，请在目标应用确认；仍可长按图片保存。',
      file453:'已请求下载文件，不代表已存入相册。',
      preparingPng453:'无损 PNG 仍在生成，JPG 已可保存。',
      pngFailed453:'无损 PNG 暂不可用；JPG 仍可保存。换一个画幅可重新生成。'},
    en:{save453:'Save photo',share453:'Share photo',wechat453:'WeChat / Moments',title453:'Your photo is ready',
      hold453:'Touch and hold the image → Save Image or Add to Photos.',
      desktop453:'Download the JPG image, or use system sharing.',
      wechatTip453:'Then choose this photo from your album in a WeChat chat or Moments.',
      noMenu453:'No save option? Try Full-size image or system sharing. If neither works, reopen in Safari / your system browser.',
      native453:'System save / share',view453:'Full-size image · hold to save',download453:'Download JPG file',
      more453:'More: PNG, website link & diagnostics',back453:'Back to save options',viewer453:'Touch and hold to save',
      preparing453:'Preparing your photo…',ready453:'Photo ready · stays on this device',
      unsupported453:'System image sharing is unavailable. Hold the image to save it, then choose it from your WeChat album.',
      cancelled453:'Sharing was cancelled, or no target was available. Your photo is here; hold it to save.',
      failed453:'System sharing did not finish. Hold the image to save it, then choose it from your WeChat album.',
      sent453:'Handed to system sharing. Check WeChat or the target app to confirm delivery.',
      pending453:'System sharing is in progress. Your photo is kept on this page.',
      recover453:'Share sheet closed? Return to saving',
      unknown453:'Back to saving. The system did not report a result; check the target app. You can still hold the image to save.',
      file453:'File download requested. This does not confirm saving to Photos.',
      preparingPng453:'Lossless PNG is still preparing. JPG is ready to save.',
      pngFailed453:'Lossless PNG is unavailable; JPG can still be saved. Change the layout to regenerate.'}
  };
  Object.assign(WORDS.zh,words.zh,{save:words.zh.save453,share:words.zh.share453,shareWechat:words.zh.wechat453,preparing:words.zh.preparing453,exportReady:words.zh.ready453,exportFailed:'图片生成失败，请点“重新生成照片”。'});
  Object.assign(WORDS.en,words.en,{save:words.en.save453,share:words.en.share453,shareWechat:words.en.wechat453,preparing:words.en.preparing453,exportReady:words.en.ready453,exportFailed:'Could not prepare your photo. Select Retry preparing photo.'});
  const card=document.querySelector('#exportModal .export-card');
  const head=card.querySelector('.modal-head'),actions=card.querySelector('.modal-actions');
  const hint=document.createElement('p');hint.id='albumHint453';hint.className='album-hint453';
  const meta=document.createElement('p');meta.id='imageMeta453';meta.className='image-meta453';
  const recover=document.createElement('button');recover.type='button';recover.id='recover453';recover.className='btn outline';recover.hidden=true;recover.dataset.i18n='recover453';
  const more=document.createElement('details');more.id='exportMore453';more.className='export-more453';
  const summary=document.createElement('summary');summary.dataset.i18n='more453';more.append(summary);
  // Keep registrations, website sharing and diagnostics, but never put them before the photo.
  const keep=new Set([head,$('resultImage'),$('demoNotice'),actions,$('shareNote'),$('wechatGuide')]);
  for(const child of Array.from(card.children))if(!keep.has(child))more.append(child);
  if($('nextVisitor45'))more.append($('nextVisitor45'));
  const download=document.createElement('button');download.type='button';download.id='downloadJpg453';download.className='text-btn';download.dataset.i18n='download453';more.insertBefore(download,more.children[1]||null);
  card.replaceChildren(head,hint,$('resultImage'),meta,$('demoNotice'),actions,$('shareNote'),recover,$('wechatGuide'),more);
  $('exportTitle').dataset.i18n='title453';
  $('shareNote').setAttribute('role','status');$('shareNote').setAttribute('aria-live','polite');
  $('resultImage').alt=language==='zh'?'长按这张成片保存到相册':'Touch and hold this framed photo to save';
  // The standalone in-page viewer is a real IMG, not canvas or a CSS background.
  const viewer=document.createElement('div');viewer.id='photoViewer453';viewer.className='modal';viewer.hidden=true;
  viewer.setAttribute('role','dialog');viewer.setAttribute('aria-modal','true');viewer.setAttribute('aria-labelledby','viewerTitle453');
  viewer.innerHTML='<div class="modal-card photo-viewer453"><div class="modal-head"><h2 id="viewerTitle453" data-i18n="viewer453"></h2><button id="viewerBack453" type="button" class="btn outline" data-i18n="back453"></button></div><img id="viewerImage453" alt="Full-size framed photo"><p class="help" data-i18n="noMenu453"></p></div>';
  document.body.append(viewer);
  const style=document.createElement('style');style.textContent=`
    #exportModal .export-card{max-width:520px}
    #exportModal .modal-head{flex-wrap:nowrap;align-items:flex-start}
    #exportModal .modal-head h2{margin:4px 0 0;font-size:23px;line-height:1.3}
    #exportModal .modal-head .eyebrow{font-size:9px}
    #exportModal .album-hint453{font-size:14px;font-weight:650;line-height:1.55;padding:10px 12px;background:#eff4ff;border-radius:10px;margin:12px 0 8px}
    #exportModal .result-image{max-height:43svh;max-width:100%;width:auto;display:block;margin:8px auto;object-fit:contain;-webkit-touch-callout:default;-webkit-user-select:auto;user-select:auto;touch-action:auto}
    #imageMeta453{font-size:10px;color:var(--muted);text-align:center;line-height:1.5;margin:5px 0 12px}
    #exportModal .modal-actions{grid-template-columns:1fr;gap:8px}
    #exportModal .modal-actions .btn{min-height:46px;font-size:14px;white-space:normal}
    #exportModal .share-note{font-size:12px;line-height:1.55;margin:10px 0}
    #exportModal .wechat-guide{margin:10px 0;padding:10px 12px}
    #exportModal .wechat-guide h3,#exportModal #directRetry,#exportModal #saveHint,#wechatInModal,#recoverShare452,#recoverShareModal452{display:none!important}
    #exportModal .wechat-guide p{margin:0 0 4px;font-size:12px;line-height:1.55}
    #exportMore453{margin:14px 0 0;border-top:1px solid var(--line);padding-top:12px}
    #exportMore453>summary{min-height:36px;font-size:12px;font-weight:650;color:var(--muted);cursor:pointer}
    #exportMore453 .share-path-label{margin-top:14px}
    #recover453{width:100%;min-height:44px;white-space:normal;font-size:12px}
    #photoViewer453{padding:10px}
    #photoViewer453 .photo-viewer453{max-width:1000px;padding:14px;max-height:96svh}
    #photoViewer453 .modal-head{align-items:center;flex-wrap:wrap;margin-bottom:12px}
    #viewerTitle453{font-size:17px;margin:0}
    #viewerImage453{display:block;width:100%;height:auto;max-width:100%;-webkit-touch-callout:default;-webkit-user-select:auto;user-select:auto;touch-action:auto}
    @media(max-width:650px){#exportModal{padding:8px}#exportModal .export-card{max-height:95svh;padding:14px}#exportModal .album-hint453{font-size:13px}#exportModal .result-image{max-height:39svh}#exportModal .modal-actions .btn{min-height:44px}#exportModal .wechat-guide .disclaimer{font-size:10px}}
    @media(max-height:600px){#exportModal .result-image{max-height:34svh}}
  `;document.head.append(style);

  const oldClose=closeModal;
  closeModal=function(){const wasViewer=activeModal==='photoViewer453';oldClose();if(wasViewer)$('viewerImage453').removeAttribute('src');};
  $('closeExport').onclick=()=>closeModal();$('closeSetup').onclick=()=>closeModal();
  const oldOpen=openExport;
  showExportGuide=function(mode='default'){
    exportView=typeof mode==='string'?mode:'default';
    const wx=isWechat()||exportView==='wechat';
    $('wechatGuide').hidden=!wx;
    const ps=$('wechatGuide').querySelectorAll('p');
    if(ps[0]){ps[0].removeAttribute('data-i18n');ps[0].textContent=t('wechatTip453');}
    if(ps[1]){ps[1].removeAttribute('data-i18n');ps[1].textContent=t('noMenu453');}
    if(ps[2])ps[2].hidden=true;
    $('saveHint').hidden=true;$('wechatInModal').hidden=true;
    hint.textContent=t(mobile()||wx?'hold453':'desktop453');
  };
  openExport=function(mode='default'){
    if(!readyExport()){toast(t('unready'));return;}
    clearTimeout(toastTimer);$('toast').classList.remove('show');
    const same=activeModal==='exportModal';
    if(!same)oldOpen(mode);else showExportGuide(mode);
    $('resultImage').src=exportCache.data;photoDataUrl=exportCache.data;
    if(!same){more.open=false;card.scrollTop=0;}
    updateUI();
  };
  function viewImage(){
    if(!readyExport())return;
    viewerMode=exportView;
    const data=exportCache.data;
    openModal('photoViewer453');
    $('viewerImage453').src=data;
    viewer.querySelector('.modal-card').scrollTop=0;
  }
  $('viewerBack453').onclick=()=>openExport(viewerMode);
  viewer.onclick=e=>{if(e.target===viewer)openExport(viewerMode);};
  function downloadJpg(){
    if(!readyExport())return;
    saveBlob(exportCache.jpgBlob,exportCache.jpgName);notice='file453';updateUI();
  }
  saveJpg=function(){if(mobile()||isWechat()){viewImage();return;}downloadJpg();};
  downloadPhoto=function(){
    if(!readyExport()){toast(t('unready'));return;}
    notice='';openExport(isWechat()?'wechat':'default');
    // Downloading a file is NOT equivalent to adding it to the phone's photo album.
    if(!mobile()&&!isWechat())downloadJpg();
  };
  download.onclick=downloadJpg;
  $('downloadBtn').onclick=()=>downloadPhoto();
  $('modalDownload').onclick=()=>saveJpg();
  $('previewBtn').onclick=()=>openExport('default');
  $('savePng').onclick=()=>{if(readyExport()&&exportCache.blob){saveBlob(exportCache.blob,exportCache.filename);notice='file453';updateUI();}};

  sharePhoto=function(channel='photo'){
    if(!readyExport()||sharing)return;
    notice='';
    // A WeChat-labelled button opens the useful photo first, not a generic share sheet.
    if(channel==='wechat'||(isWechat()&&channel!=='native')){openExport('wechat');return;}
    const f=shareCandidate();
    openExport(isWechat()?'wechat':'default');
    if(!f){lastShareEvent={action:'photo',outcome:'unsupported',error:null};notice='unsupported453';updateUI();refreshDiagnostics();return;}
    const session=++shareSession,revision=state.revision;
    sharing=true;notice='pending453';lastShareEvent={action:'photo',outcome:'requested',error:null};updateUI();
    const settle=(outcome,error,key)=>{
      if(session!==shareSession)return;
      sharing=false;
      if(revision!==state.revision){updateUI();return;}
      lastShareEvent={action:'photo',outcome,error:error||null};notice=key;
      updateUI();refreshDiagnostics();
    };
    // Prepared File; no await, fetch, timer, or image encoding before this user-gesture call.
    try{
      const result=navigator.share({files:[f]});
      Promise.resolve(result).then(()=>settle('handed_to_system_not_delivery_confirmation',null,'sent453'))
        .catch(e=>settle(e?.name==='AbortError'?'cancelled_or_no_target':'failed',e?.name||'Error',e?.name==='AbortError'?'cancelled453':'failed453'));
    }catch(e){settle(e?.name==='AbortError'?'cancelled_or_no_target':'failed',e?.name||'Error',e?.name==='AbortError'?'cancelled453':'failed453');}
  };
  recover.onclick=()=>{
    if(!sharing)return;
    shareSession++;sharing=false;clearTimeout(shareTimer452);shareExpired452=false;
    lastShareEvent={action:lastShareEvent.action,outcome:'result_unknown_user_recovered',error:null};
    notice='unknown453';updateUI();refreshDiagnostics();
  };
  $('shareBtn').onclick=()=>sharePhoto('photo');
  $('wechatShare').onclick=()=>sharePhoto('wechat');
  $('modalShare').onclick=()=>sharePhoto('native');
  $('wechatInModal').onclick=()=>sharePhoto('wechat');
  $('directRetry').onclick=()=>sharePhoto('native');

  // JPG is the critical path. A slower/larger lossless PNG must not block mobile save/share.
  prepareExport=async function(){
    if(!canExport())return;
    const token=++exportToken,revision=state.revision;
    exportPending=true;exportFailed452=false;updateUI();
    const copy=document.createElement('canvas');copy.width=canvas.width;copy.height=canvas.height;
    try{
      copy.getContext('2d').drawImage(canvas,0,0);
      const jpg=await canvasBlob(copy,'image/jpeg',.94),data=await blobAsData(jpg);
      if(token!==exportToken||revision!==state.revision)return;
      const base=`${state.filename}-${state.template}-${state.ratio}`;
      if(exportCache?.url)URL.revokeObjectURL(exportCache.url);
      const cache={jpgBlob:jpg,file:new File([jpg],base+'.jpg',{type:'image/jpeg'}),jpgName:base+'.jpg',data,revision,
        blob:null,pngFile:null,filename:base+'.png',url:null,pngPending:true,pngError:false};
      exportCache=cache;exportPending=false;exportFailed452=false;
      if(state.own&&!prepared45){prepared45=true;count45('photo_prepared');}
      updateUI();
      try{
        const png=await canvasBlob(copy,'image/png');
        if(token!==exportToken||revision!==state.revision||exportCache!==cache)return;
        cache.blob=png;cache.pngFile=new File([png],base+'.png',{type:'image/png'});cache.url=URL.createObjectURL(png);
      }catch(_){if(exportCache===cache)cache.pngError=true;}
      finally{if(exportCache===cache){cache.pngPending=false;updateUI();}}
    }catch(_){
      if(token===exportToken&&revision===state.revision){exportPending=false;exportFailed452=true;setError(t('exportFailed'));updateUI();}
    }finally{copy.width=1;copy.height=1;}
  };
  const oldDrop=dropExport;
  dropExport=function(){
    notice='';if(sharing){shareSession++;sharing=false;}
    oldDrop();
    // Do not leave a previous guest's or previous edit's image in either preview.
    $('viewerImage453').removeAttribute('src');
    if(activeModal==='exportModal')$('resultImage').removeAttribute('src');
  };
  const oldUpdate=updateUI;
  updateUI=function(){
    oldUpdate();
    const ready=readyExport(),f=ready?shareCandidate():null;
    $('modalDownload').removeAttribute('data-i18n');$('modalDownload').textContent=t(mobile()||isWechat()?'view453':'download453');
    $('modalDownload').disabled=!ready;
    $('modalShare').removeAttribute('data-i18n');$('modalShare').textContent=t('native453');$('modalShare').hidden=!f;$('modalShare').disabled=!ready||sharing;
    $('savePng').disabled=!ready||!exportCache?.blob;download.disabled=!ready;
    $('savePng').title=exportCache?.pngPending?t('preparingPng453'):exportCache?.pngError?t('pngFailed453'):'';
    $('shareNote').hidden=!notice;$('shareNote').textContent=notice?t(notice):'';
    recover.hidden=!sharing;
    // Recovery is visible as soon as the user returns; no arbitrary 30-second lock.
    if(activeModal==='exportModal'){
      showExportGuide(exportView);
      if(ready){
        if($('resultImage').getAttribute('src')!==exportCache.data)$('resultImage').src=exportCache.data;
        const d=dims(state.ratio);meta.textContent=`${d.W} × ${d.H} · JPG · ${Math.max(1,Math.round(exportCache.jpgBlob.size/1024))} KB`;
      }else meta.textContent=t('preparing453');
    }
  };
  const oldClear=clearPhoto;
  clearPhoto=function(reason='manual'){notice='';$('viewerImage453').removeAttribute('src');more.open=false;oldClear(reason);};
  const oldDiagnostics=diagnostics;
  diagnostics=function(){return{...oldDiagnostics(),app:'LingoTech Photo Booth 4.5.3',mobileSaveMode:mobile()?'image-preview-first':'download',photoUpload:false,nativeAlbumSaveConfirmed:false};};
  window.LingoTechShareDiagnostics=diagnostics;
  window.LingoTechQA453={version:'4.5.3',snapshot:()=>({mobile:mobile(),ios:ios(),sharing,previewOpen:activeModal==='exportModal',viewerOpen:activeModal==='photoViewer453',jpgReady:readyExport(),pngReady:!!exportCache?.blob,pngPending:!!exportCache?.pngPending,revision:state.revision,cacheRevision:exportCache?.revision,notice})};
})();
