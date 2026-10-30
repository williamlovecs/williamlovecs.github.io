'use strict';
// Regression-driven corrections applied at build time, not a runtime loader.
module.exports=function refine(html){
 function once(from,to){if(html.split(from).length!==2)throw new Error('Unexpected source while applying tested correction: '+from.slice(0,70));html=html.replace(from,to);}
 // Magazine side-label ends at the photo boundary, never beside footer copy.
 once('c.translate(e, H-e);c.rotate(-Math.PI/2);','c.translate(e, r.y+r.h);c.rotate(-Math.PI/2);');
 once("text43(c,sc.label,{x:0,y:0,w:H-2*e,h:28}","text43(c,sc.label,{x:0,y:0,w:r.h,h:28}");
 const addition=`
// The old input silently truncated to 18 characters. The explicit 40-character
// limit now agrees with the input and two-line, measured caption area.
$('nickname').maxLength=40;
$('nickname').oninput=e=>{state.nickname=limitText(e.target.value,40);scheduleRender(true);};
WORDS.zh.nickname='你的名字或一句短句（最多 40 字）';
WORDS.en.nickname='Your name or short line (up to 40 characters)';
const setLanguage43=setLanguage;
setLanguage=function(next){setLanguage43(next);scheduleRender(true);};
`;
 once('translate();scheduleRender(true);\n})();',addition+'\ntranslate();scheduleRender(true);\n})();');
 return html;
};
