/* LingoTech 4.3 — upgrade the immutable, audited v4.2 document.
   All processing stays on-device. No analytics or photo upload. */
(function(root){
'use strict';
const CSS = `
/* The preview must contain the entire canvas, not crop it to a fixed grid track. */
.stage{display:flex;align-items:center;justify-content:center;height:auto!important;min-height:0!important;overflow:visible;box-sizing:border-box;padding:18px}
.canvas-shell{flex:0 0 auto;min-width:0;width:var(--stage-w,100%);max-width:100%;overflow:visible}
.canvas-shell #poster{display:block;width:100%;height:auto!important;max-height:none;object-fit:contain}
.result-image{object-fit:contain!important;object-position:center}
.scene-picker{margin:0 0 15px;padding:13px;border:1px solid #dce5ef;background:#f7f9fc;border-radius:12px}
.scene-picker h3{font-size:13px;margin:0 0 9px}.scene-picker p{font-size:11px;line-height:1.65;color:#65738a;margin:9px 0 0}
.scene-options{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.scene-options button{min-width:0;min-height:44px;border:1px solid #d6deea;border-radius:8px;padding:8px 5px;background:white;color:#344465;font-size:11px;line-height:1.45}
.scene-options button[aria-pressed=true]{border-color:#165dff;background:#eaf0ff;color:#124dda;font-weight:750}
.template b{white-space:normal!important;line-height:1.35}.small-label{white-space:nowrap}
.welcome-art{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px;align-items:start;width:100%;height:auto;min-height:0;max-width:540px;margin:20px auto;transform:none}
.welcome-art .sample-card{position:relative!important;inset:auto!important;top:auto!important;left:auto!important;right:auto!important;bottom:auto!important;width:100%!important;height:auto;min-width:0;padding:10px;background:#fff;border-radius:8px;transform:none}
.welcome-art .sample-two{margin-top:40px}.welcome-art .sample-photo{height:auto;aspect-ratio:3/2;overflow:hidden}.welcome-art .sample-photo img{width:100%;height:100%;object-fit:contain}
.welcome-art .sample-caption{display:block;padding:10px 3px 5px;min-width:0}.welcome-art .sample-caption i{display:block;font-size:20px;line-height:1.25;white-space:normal}
.welcome-art .sample-caption small{display:block;margin-top:6px;font-size:8px;line-height:1.5;white-space:normal}
.welcome-art .sample-disclaimer{position:static;inset:auto;grid-column:1/-1;width:100%;max-width:none;line-height:1.7;text-align:center}
.art-spark,.art-orbit,.art-sticker{display:none!important}
@media(min-width:1100px){.welcome-art .sample-one{transform:rotate(-3deg)}.welcome-art .sample-two{transform:rotate(3deg)}}
@media(max-width:899px){.stage{padding:12px}.canvas-shell{width:var(--stage-w,100%)}.preview-panel{position:static}}
@media(max-width:650px){.welcome-art{gap:10px;margin:10px auto}.welcome-art .sample-two{margin-top:0}.welcome-art .sample-card{padding:7px}.welcome-art .sample-caption i{font-size:clamp(12px,3.4vw,17px)}.scene-options button{font-size:11px}.community-gallery img{object-fit:contain;background:#f2f2ed}.site-header .brand{min-width:0}.stage{border-radius:12px}}
`;
function patch(){
/* Executed inside the original application closure, after its declarations. */
state.scene='build';
const SCENES43={
 build:{frame:'build',accent:'#165dff',paper:'#f5f7ff',label:'BUILD WITH AI',title:'Build something together.',zh:'一起用 AI，把想法做出来。',en:'Make something real, together.'},
 friends:{frame:'friends',accent:'#326c59',paper:'#f2f6ee',label:'FIND YOUR PEOPLE',title:'Find your people.',zh:'不同背景，同样的好奇心。',en:'Different backgrounds. Shared curiosity.'},
 play:{frame:'play',accent:'#bd7818',paper:'#fff6e5',label:'CULTURE & PLAY',title:'Good times together.',zh:'多一点好奇，多一些朋友。',en:'A little curiosity. A lot of good company.'}
};
let textBoxes43=[];
function scene43(m){return SCENES43[m.scene]||SCENES43.build;}
function layout43(template,W,H,m=state){
 const land=W>H,edge=Math.round(Math.min(W,H)*.035),strip=m.memoryStrip?158:0;
 const footerH=land?192:230,bottom=edge+strip+(strip?20:0),photoY=land?100:118;
 const x=template==='ideas'?edge+72:edge+8;
 const photoBottom=H-bottom-footerH;
 return{edge,strip,land,photo:{x,y:photoY,w:W-x-edge-8,h:photoBottom-photoY},
 title:{x:edge+14,y:photoBottom+22,w:W-2*edge-28,h:land?64:78},
 caption:{x:edge+14,y:photoBottom+(land?98:120),w:W-2*edge-28,h:land?54:62},
 footer:{x:edge+14,y:H-bottom-21,w:W-2*edge-28,h:19}};
}
// Every text item has a measured box. Baseline and actual glyph bounds are respected.
function text43(c,value,rect,size,color,weight=600,family=FONT,maxLines=1,align='left'){
 c.save();c.fillStyle=color;c.textBaseline='alphabetic';c.textAlign='left';
 const str=String(value||'').replace(/\s+/g,' ').trim();let fs=size,lines=[];
 const wrap=()=>{let out=[],part='';for(const ch of Array.from(str)){if(part&&c.measureText(part+ch).width>rect.w){out.push(part.trim());part=ch;}else part+=ch;}if(part)out.push(part.trim());return out.length?out:[''];};
 for(;;){c.font=`${weight} ${fs}px ${family}`;lines=maxLines===1?[str]:wrap();const mm=c.measureText('国Ag');const lh=Math.max(fs*1.28,mm.actualBoundingBoxAscent+mm.actualBoundingBoxDescent+4);
  if((lines.length<=maxLines&&lines.every(s=>c.measureText(s).width<=rect.w)&&lh*lines.length<=rect.h)||fs<=10)break;fs-=.5;}
 if(lines.length>maxLines)lines=lines.slice(0,maxLines);
 const lh=Math.min(rect.h/Math.max(1,lines.length),fs*1.34);
 lines.forEach((s,i)=>{const mm=c.measureText(s),a=Math.max(0,mm.actualBoundingBoxAscent||fs*.85),d=Math.max(0,mm.actualBoundingBoxDescent||fs*.2);
  const x=align==='right'?rect.x+rect.w-mm.width:align==='center'?rect.x+(rect.w-mm.width)/2:rect.x;
  const y=rect.y+i*lh+Math.max(a,(lh-a-d)/2+a);c.fillText(s,x,y);
  const tr=c.getTransform(),left=x-(mm.actualBoundingBoxLeft||0),right=x+(mm.actualBoundingBoxRight||mm.width),top=y-a,bot=y+d;
  const pts=[[left,top],[right,top],[left,bot],[right,bot]].map(([xx,yy])=>({x:tr.a*xx+tr.c*yy+tr.e,y:tr.b*xx+tr.d*yy+tr.f}));
  const minX=Math.min(...pts.map(p=>p.x)),minY=Math.min(...pts.map(p=>p.y));
  textBoxes43.push({text:s,x:minX,y:minY,w:Math.max(...pts.map(p=>p.x))-minX,h:Math.max(...pts.map(p=>p.y))-minY,fontSize:fs,box:{...rect}});
 });c.restore();
}
function brand43(c,x,y,dark){
 const col=dark?'#fff':INK;
 c.save();if(logo.complete&&logo.naturalWidth){if(dark)c.filter='brightness(0) invert(1)';c.drawImage(logo,x,y+2,34*logo.naturalWidth/logo.naturalHeight,34);c.filter='none';}c.restore();
 text43(c,'LingoTech',{x:x+46,y,w:205,h:34},28,col,850);
 text43(c,'by LingoCorner',{x:x+47,y:y+35,w:190,h:20},12,dark?'#c2cde5':'#66738b',500);
}
function memory43(c,W,H,m){
 if(!m.memoryStrip)return;const e=Math.round(Math.min(W,H)*.035),y=H-e-142;
 box(c,e,y,W-2*e,142,'#fff',5);const iw=148,ih=98;
 ['friends','play'].forEach((k,i)=>{const im=communityPhotos[k];if(!im)return;const rr={x:e+12+i*(iw+12),y:y+12,w:iw,h:ih};const p=placement(rr,im,'contain');box(c,rr.x,rr.y,rr.w,rr.h,'#f3f3ef');c.drawImage(im,p.x,p.y,p.w,p.h);});
 const x=e+340,w=W-e-x-14;
 text43(c,'PAST LINGOCORNER MOMENTS',{x,y:y+16,w,h:30},20,'#4e6079',750);
 text43(c,'往期社群活动 · 灵感照片',{x,y:y+52,w,h:32},22,'#4e6079',500);
 text43(c,'NOT THIS PHOTO / 非本次照片场景',{x,y:y+94,w,h:25},14,'#65758b',500);
}
function render43(c,W,H,m){
 const k=m.template,sc=scene43(m),g=layout43(k,W,H,m),e=g.edge,r=g.photo;
 const dark=k==='ideas'||k==='night',paper=k==='crew'?'#f1e6c9':sc.paper;
 box(c,0,0,W,H,dark?'#152449':k==='build'?'#fff':paper);
 if(k==='crew'){box(c,22,18,W-44,H-36,'#fffefa',3);}
 if(k==='friends'||k==='play'){
  // Texture is confined to margins. No stars, emoji, or default confetti.
  if(m.communityPaper==='picnic'){c.save();c.globalAlpha=.1;for(let x=0;x<W;x+=64)box(c,x,0,20,H,sc.accent);for(let y=0;y<H;y+=64)box(c,0,y,W,20,sc.accent);c.restore();}
  if(m.communityPaper==='celebrate'){c.save();c.globalAlpha=.13;for(let j=0;j<48;j++)box(c,(j*173+16)%W,(j*277+18)%H,8,3,sc.accent);c.restore();}
  box(c,e-12,18,W-2*e+24,H-36,'#ffffffb8',k==='play'?12:3);
 }
 if(k==='build'){box(c,0,0,W,9,sc.accent);box(c,0,H-8,W,8,sc.accent);}
 if(k==='ideas')box(c,0,0,10,H,sc.accent);
 brand43(c,e+8,27,dark);
 text43(c,sampleLabel(m)||sc.label,{x:W*.46,y:34,w:W*.54-e-8,h:27},17,dark?'#d7e2f5':'#66738a',650,FONT,1,'right');
 if(k==='studio'){line(c,r.x,r.y-12,r.x+r.w,r.y-12,INK,2);}
 if(k==='friends'){box(c,W*.46,r.y-15,W*.13,8,'#e9cd68');}
 const p=drawPhoto(c,r,m);
 if(k==='night'){for(let x=r.x;x<r.x+r.w;x+=23)line(c,x,r.y+r.h+12,Math.min(x+9,r.x+r.w),r.y+r.h+12,'#8d9cb8',2);}
 if(k==='ideas'){
  c.save();c.translate(e, H-e);c.rotate(-Math.PI/2);
  text43(c,sc.label,{x:0,y:0,w:H-2*e,h:28},20,'#f7d65e',750);c.restore();
 }
 let title=sc.title;
 if(m.scene==='build'||!m.scene){title={build:'BUILD TOGETHER.',crew:'My build crew.',ideas:'MORE PEOPLE. MORE IDEAS.',studio:'Make a little magic.',night:'MEET. BUILD. REPEAT.',friends:'Build with your people.',play:'BUILD. PLAY. REPEAT.'}[k]||title;}
 const serif=['crew','studio','friends'].includes(k),color=dark?'#ffe02e':k==='crew'||k==='studio'?INK:sc.accent;
 if(k==='play'){box(c,g.title.x-8,g.title.y-6,g.title.w+16,g.title.h+12,'#ffe02e',4);}
 text43(c,title,g.title,g.land?50:58,k==='play'?INK:color,serif?700:850,serif?'Georgia,"Times New Roman",serif':FONT);
 if(k==='crew'||k==='friends')line(c,g.title.x,g.title.y+g.title.h+4,g.title.x+Math.min(260,g.title.w*.35),g.title.y+g.title.h+4,'#e8c752',5);
 text43(c,personalLine(m,language==='zh'?sc.zh:sc.en),g.caption,g.land?24:27,dark?'#ecf1ff':'#52647b',600,FONT,2);
 text43(c,sc.label+'  /  LINGOTECH',g.footer,13,dark?'#b1c2df':'#68778d',600);
 memory43(c,W,H,m);return{r,p};
}
photoRect=function(template,W,H,model=state){return layout43(template,W,H,model).photo;};
sparkle=function(){}; // Removed from all seven templates, preview AND export.
drawArt=function(target,m,metrics=false){
 const{W,H}=dims(m.ratio);if(target.width!==W)target.width=W;if(target.height!==H)target.height=H;
 const c=target.getContext('2d',{alpha:false});c.setTransform(1,0,0,1,0,0);c.imageSmoothingEnabled=true;c.imageSmoothingQuality='high';
 textBoxes43=[];const result=render43(c,W,H,m),boxes=textBoxes43.map(x=>({...x}));
 if(m===state){state.frame=result.r;state.placement=result.p;if(metrics)artMetrics=boxes;}
 result.textBoxes=boxes;return result;
};
fitStage=function(){
 const el=$('stage'),shell=$('canvasShell');if(!el||!shell)return;const{W,H}=dims(state.ratio),cs=getComputedStyle(el);
 const available=Math.max(80,(el.clientWidth||window.innerWidth-36)-(parseFloat(cs.paddingLeft)||0)-(parseFloat(cs.paddingRight)||0));
 const maxH=window.innerWidth<900?Math.min(520,Math.max(260,window.innerHeight*.53)):Math.min(680,Math.max(310,window.innerHeight*.64));
 shell.style.setProperty('--stage-w',Math.floor(Math.min(available,maxH*W/H))+'px');
};
const scenePicker43=document.createElement('section');scenePicker43.className='scene-picker';scenePicker43.innerHTML='<h3 data-i18n="sceneHeading43"></h3><div class="scene-options" role="group" aria-label="Creative scene"><button type="button" data-scene="build" data-i18n="sceneBuild43"></button><button type="button" data-scene="friends" data-i18n="sceneFriends43"></button><button type="button" data-scene="play" data-i18n="scenePlay43"></button></div><p id="sceneHint43" data-i18n="sceneHint43"></p>';
const templateCard43=document.querySelector('.templates').closest('.control-card');templateCard43.prepend(scenePicker43);
Object.assign(WORDS.zh,{sceneHeading43:'创作场景',sceneBuild43:'AI 共创',sceneFriends43:'认识朋友',scenePlay43:'文化与玩乐',sceneHint43:'场景决定文案与氛围，相框决定版式。切换不会替换你的照片。',chooseFrame:'选择相框版式',tryPeople:'用朋友场景制作',tryPlay:'用趣味场景制作',tryBuild43:'用 AI 共创场景制作',sampleSource:'左：HICOOL AI 共创；右：LingoCorner 往期互动。',communityOptions:'场景细节',sampleKept43:'场景已切换，你的照片与文字已保留。',sampleLoading:'示例照片正在准备，请稍后再试。'});
Object.assign(WORDS.en,{sceneHeading43:'Choose a scene',sceneBuild43:'Build with AI',sceneFriends43:'Find your people',scenePlay43:'Culture & play',sceneHint43:'Scenes set the message and mood; frames set the layout. Your photo stays yours.',chooseFrame:'Choose a frame layout',tryPeople:'Make a friendship keepsake',tryPlay:'Make a playful keepsake',tryBuild43:'Make an AI-build keepsake',sampleSource:'Left: HICOOL AI collaboration. Right: a past LingoCorner gathering.',communityOptions:'Scene details',sampleKept43:'Scene changed. Your photo and text are kept.'});
const buildCard43=document.querySelector('.community-gallery article');if(buildCard43&&!$('tryBuild43')){const b=document.createElement('button');b.id='tryBuild43';b.type='button';b.className='text-btn';b.dataset.i18n='tryBuild43';buildCard43.appendChild(b);}
function sample43(key){return key==='build'?samples.build:communityPhotos[key];}
function chooseScene43(key){
 if(!SCENES43[key])return;if(state.loading){toast(t('loading'));return;}
 // An owned image is NEVER replaced by a marketing/sample CTA.
 const own=state.own&&state.source,im=own?null:sample43(key);if(!own&&!im){toast(t('sampleLoading'));return;}
 shareSession++;sharing=false;
 Object.assign(state,{scene:key,template:SCENES43[key].frame,memoryStrip:false,communityPaper:'paper'});
 $('memoryStrip').checked=false;$('communityPaper').value='paper';
 if(!own){uploadToken++;Object.assign(state,{source:im,userImage:null,own:false,demo:true,fit:'contain',nickname:'',role:'',filename:'sample-'+key,sampleOrigin:key==='build'?'HICOOL 2026':'LingoCorner past events'});$('nickname').value='';}
 if(state.auto)state.ratio=chooseAuto(state.source);resetGeometry();backdrops.clear();showEditor();scheduleRender(true);toast(t(own?'sampleKept43':'sampleUsed'));
}
useDemo=function(){chooseScene43(state.scene||'build');};
useCommunitySample=function(key){chooseScene43(key);};
const oldClear43=clearPhoto;
clearPhoto=function(){Object.assign(state,{scene:'build',template:'build',memoryStrip:false,communityPaper:'paper',sampleOrigin:'HICOOL 2026'});$('memoryStrip').checked=false;$('communityPaper').value='paper';oldClear43();};
const oldUpdate43=updateUI;
updateUI=function(){oldUpdate43();document.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scene===state.scene)));if($('communityControls'))$('communityControls').hidden=state.scene==='build';};
$('tryBuild43').onclick=()=>chooseScene43('build');$('tryPeople').onclick=()=>chooseScene43('friends');$('tryPlay').onclick=()=>chooseScene43('play');
document.querySelectorAll('[data-scene]').forEach(b=>b.onclick=()=>chooseScene43(b.dataset.scene));
$('demoBtn').onclick=()=>useDemo();$('clearBtn').onclick=()=>clearPhoto();$('brandHome').onclick=e=>{e.preventDefault();clearPhoto();};
// Styles change layout only. The selected scene, source photo, and personal text persist.
document.querySelectorAll('[data-template]').forEach(b=>b.onclick=()=>{state.template=b.dataset.template;if(state.auto)state.ratio=chooseAuto(state.source);resetGeometry();scheduleRender(true);});
$('landingPhoto1').src=window.PHOTOBOOTH_HERO43||A.people;$('landingPhoto1').alt='HICOOL: two participants collaborating at a laptop';
$('landingPhoto2').src=COMMUNITY.highfive;$('landingPhoto2').alt='Past LingoCorner event: participants exchanging a high five';
const heroLabels43=document.querySelectorAll('.sample-caption small');if(heroLabels43[0])heroLabels43[0].textContent='HICOOL / AI COLLABORATION';if(heroLabels43[1])heroLabels43[1].textContent='LINGOCORNER / PAST EVENT';
document.querySelectorAll('.version').forEach(e=>e.textContent='v4.3');
try{const u=new URL(location.href);for(const k of [...u.searchParams.keys()])if(/^utm_/i.test(k)||k==='v')u.searchParams.delete(k);history.replaceState(null,'',u.pathname+u.search+u.hash);}catch(_){}
const oldDiag43=diagnostics;diagnostics=function(){return{...oldDiag43(),app:'LingoTech Photo Booth 4.3'};};window.LingoTechShareDiagnostics=diagnostics;
window.LingoTechQA43={snapshot:()=>({...window.PhotoBoothQA.snapshot(),scene:state.scene,memoryStrip:state.memoryStrip,version:'4.3'}),layout:layout43,render:(target,model)=>drawArt(target,{...state,...model}),chooseScene:chooseScene43};
if(typeof ResizeObserver==='function'){let width43=0;new ResizeObserver(entries=>{const w=entries[0]?.contentRect.width||0;if(Math.abs(w-width43)>.5){width43=w;fitStage();}}).observe($('stage'));}
if(document.fonts?.ready)document.fonts.ready.then(()=>scheduleRender(true));
}
function upgrade(html,heroData){
 if(!html.includes('LingoTech release v4.2')||!html.includes('translate();scheduleRender(true);\n})();'))throw new Error('Unexpected baseline. Refusing to alter an unknown release.');
 const body=patch.toString().slice(patch.toString().indexOf('{')+1,-1);
 html=html.replace('<!-- LingoTech release v4.2 Mobile & Share UX -->','<!-- LingoTech release v4.3 Scenes, safe-area frames & unique community photos -->');
 html=html.replace('</head>','<link rel="canonical" href="https://williamlovecs.github.io/lingotech/"><style id="release43">'+CSS+'</style></head>');
 if(heroData)html=html.replace('<script id="publicConfig">','<script>window.PHOTOBOOTH_HERO43='+JSON.stringify(heroData)+';</script><script id="publicConfig">');
 html=html.replace('translate();scheduleRender(true);\n})();',body+'\ntranslate();scheduleRender(true);\n})();');
 return html;
}
root.LingoTechUpgrade43=upgrade;
if(typeof module!=='undefined')module.exports={upgrade,patch,CSS};
})(typeof window!=='undefined'?window:globalThis);
