'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const read=f=>fs.readFileSync(path.join(root,f),'utf8');
const before=read('lingotech/index.html');
if(sha(before)!=='38f4517e1aa2ed75a1324844c1de4f903773eb08dbe3c4e51f2ef8b83bfd59d0')throw Error('Expected clean v4.3 baseline; run release43/build.cjs first.');
const patch=read('lingotech/release44/qr_patch.js').trimEnd()+'\n';
const marker='translate();scheduleRender(true);\n})();\n</script>\n</body></html>';
if(!before.includes(marker)||before.includes('// v4.4: quiet-zone QR'))throw Error('Invalid baseline or already patched');
let after=before.replace(marker,patch+'\n'+marker)
 .replace('<!-- LingoTech release v4.3 Scenes, safe-area frames & unique community photos -->','<!-- LingoTech release v4.4 shareable photos with scannable QR -->')
 .replace("document.querySelectorAll('.version').forEach(e=>e.textContent='v4.3');","document.querySelectorAll('.version').forEach(e=>e.textContent='v4.4');");
const actual=sha(after),expected='fca15ade3bae056e30a3ae12006befc989f2d91a3d7848de62f1d766edc842dc';
if(actual!==expected)throw Error('Generated output mismatch: '+actual+' != '+expected);
for(const rel of ['lingotech/index.html','lingotech-photo-booth/index.html'])fs.writeFileSync(path.join(root,rel),after);
const release={version:'4.4',baseline_version:'4.3',html_sha256:actual,bytes:Buffer.byteLength(after),canonical:'https://williamlovecs.github.io/lingotech/',qr_destination:'https://williamlovecs.github.io/lingotech/',changes:['Scannable branded QR integrated into every frame and ratio, with no photo/face overlap','Separate reserved text and QR zones, including the historical photo memory strip','Default-on opt-out checkbox; QR appears in both preview and saved/shared JPG/PNG','Bilingual scan-to-create CTA; clean canonical URL without user-specific tracking','Preserve scene and frame editor, public URL, sharing fallbacks, and privacy'],limitations:['Physical iPhone/WeChat delivery and long-press recognition still require device verification']};
fs.writeFileSync(path.join(root,'lingotech/release.json'),JSON.stringify(release,null,2)+'\n');
console.log(JSON.stringify(release,null,2));
