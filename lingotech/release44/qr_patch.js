// v4.4: quiet-zone QR links to the clean Photo Booth URL. The QR contains no user data.
const QR44_DESTINATION='https://williamlovecs.github.io/lingotech/';
const QR44_MODULES=37;
const QR44_BITS=atob('AAAAAAAAAAAAAAAAAAAAAAAAAP4vM/gEEfkQQC6I1roBdNZF0AuhXq6AQUaJBAP6qq/gAAcOAACW940AAEbnckA2wyS8AClKE2ACbdzlgEqIDgABjDOv4BGE+xoAXklcEAHL1TpAK5KDZgB6EPcwC77Y+gAAQCRcA/mjqkAQW5EfALpb74AF1ADfgC6WBjoBBPq1IA/sFJkAAAAAAAAAAAAAAAAAAAAAAAAAAA==');
state.showQr44=true;
function qr44Geometry(W,H){
 const e=Math.round(Math.min(W,H)*.035),w=215,h=225;
 return{x:W-e-w,y:H-e-h,w,h,qrSize:185};
}
function qr44Bit(i){return (QR44_BITS.charCodeAt(i>>3)&(128>>(i&7)))!==0;}
function paintQr44(c,W,H){
 const g=qr44Geometry(W,H),dark=state.template==='ideas'||state.template==='night';
 c.save();c.fillStyle='#ffffff';c.strokeStyle=dark?'#7b8eae':'#dde4eb';c.lineWidth=2;
 rounded(c,g.x,g.y,g.w,g.h,9);c.fill();c.stroke();
 // Bilingual call to action remains part of the bitmap, not an HTML overlay.
 text43(c,language==='zh'?'扫码制作同款':'SCAN TO MAKE YOURS',
  {x:g.x+8,y:g.y+7,w:g.w-16,h:20},language==='zh'?15:13,INK,750,FONT,1,'center');
 const unit=g.qrSize/QR44_MODULES,xx=g.x+(g.w-g.qrSize)/2,yy=g.y+28;
 c.fillStyle='#ffffff';c.fillRect(xx,yy,g.qrSize,g.qrSize);
 c.fillStyle='#111b35';
 for(let r=0;r<QR44_MODULES;r++)for(let col=0;col<QR44_MODULES;col++){
  if(!qr44Bit(r*QR44_MODULES+col))continue;
  // QR modules occupy integral pixels (185 / 37 = 5); no anti-aliasing.
  c.fillRect(xx+col*unit,yy+r*unit,unit,unit);
 }
 c.restore();
}
const layoutBeforeQr44=layout43;
layout43=function(template,W,H,m=state){
 const g=layoutBeforeQr44(template,W,H,m);
 if(m.showQr44!==false){
  const q=qr44Geometry(W,H),maxRight=q.x-20;
  const photoEnd=g.photo.y+g.photo.h,limit=q.y-10;
  if(photoEnd>limit){const shift=photoEnd-limit;g.photo.h-=shift;g.title.y-=shift;g.caption.y-=shift;}
  for(const name of ['title','caption','footer']){
   g[name].w=Math.min(g[name].w,Math.max(160,maxRight-g[name].x));
  }
 }
 return g;
};
const memoryBeforeQr44=memory43;
memory43=function(c,W,H,m){
 if(m.showQr44===false)return memoryBeforeQr44(c,W,H,m);
 if(!m.memoryStrip)return;
 const e=Math.round(Math.min(W,H)*.035),y=H-e-142;
 box(c,e,y,W-2*e,142,'#fff',5);
 const iw=148,ih=98;
 ['friends','play'].forEach((key,i)=>{
  const im=communityPhotos[key];if(!im)return;
  const r={x:e+12+i*(iw+12),y:y+12,w:iw,h:ih};const p=placement(r,im,'contain');
  box(c,r.x,r.y,r.w,r.h,'#f3f3ef');c.drawImage(im,p.x,p.y,p.w,p.h);
 });
 const x=e+340,w=Math.max(120,qr44Geometry(W,H).x-x-17);
 text43(c,'PAST LINGOCORNER MOMENTS',{x,y:y+16,w,h:30},20,'#4e6079',750);
 text43(c,'往期社群活动 · 灵感照片',{x,y:y+52,w,h:32},22,'#4e6079',500);
 text43(c,'NOT THIS PHOTO / 非本次照片场景',{x,y:y+94,w,h:25},14,'#65758b',500);
};
const renderBeforeQr44=render43;
render43=function(c,W,H,m){
 const result=renderBeforeQr44(c,W,H,m);
 if(m.showQr44!==false)paintQr44(c,W,H);
 return result;
};
const qrPanel44=document.createElement('section');
qrPanel44.className='control-card qr-panel44';
qrPanel44.innerHTML='<label class="memory-check"><input type="checkbox" id="showQr44" checked><span data-i18n="qrToggle44"></span></label><small data-i18n="qrHelp44"></small>';
$('communityControls').insertAdjacentElement('afterend',qrPanel44);
$('showQr44').onchange=e=>{state.showQr44=e.target.checked;scheduleRender(true);};
const qrExportHint44=document.createElement('p');qrExportHint44.id='qrExportHint44';qrExportHint44.className='help';qrExportHint44.dataset.i18n='qrExportHint44';
$('resultImage').insertAdjacentElement('afterend',qrExportHint44);
const qrStyle44=document.createElement('style');
qrStyle44.textContent='.qr-panel44 .memory-check{display:flex;align-items:center;gap:9px;cursor:pointer;font-weight:650}.qr-panel44 small{display:block;margin-top:8px;color:#66738b;font-size:11px;line-height:1.55}#qrExportHint44{font-size:11px;color:#66738b;line-height:1.5;margin:7px 0 9px}';
document.head.append(qrStyle44);
Object.assign(WORDS.zh,{qrToggle44:'在照片上显示 LingoTech 二维码',qrHelp44:'默认开启，扫码可制作自己的照片；不收集或上传原图。可关闭后保存纯照片。',qrExportHint44:'照片右下角带有可扫码入口。微信里可长按照片尝试识别二维码。'});
Object.assign(WORDS.en,{qrToggle44:'Add a LingoTech QR code to my photo',qrHelp44:'On by default. Friends can scan to make their own; your photo stays on your device. Turn off for a clean keepsake.',qrExportHint44:'The QR on your photo opens Photo Booth. In WeChat, try long-pressing the shared picture to scan it.'});
const updateBeforeQr44=updateUI;
updateUI=function(){updateBeforeQr44();qrExportHint44.hidden=state.showQr44===false;};
window.LingoTechQA44={destination:QR44_DESTINATION,qr:()=>({...qr44Geometry(dims(state.ratio).W,dims(state.ratio).H),enabled:state.showQr44}),toggle:(v)=>{state.showQr44=!!v;$('showQr44').checked=!!v;scheduleRender(true);}};
