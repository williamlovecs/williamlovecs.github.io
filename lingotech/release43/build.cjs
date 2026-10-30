'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {upgrade}=require('./upgrade.cjs');
const root=path.resolve(__dirname,'../..');
const baseline=fs.readFileSync(path.join(__dirname,'baseline-v42.html'),'utf8');
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
if(sha(baseline)!=='c4ab6ed46d72c97a4810d3e13f428dcff56cea993ae48199fff2235822ae34d3')throw new Error('Baseline hash mismatch');
const hero=fs.readFileSync(path.join(__dirname,'hero-build-8240.webp'));
const html=upgrade(baseline,'data:image/webp;base64,'+hero.toString('base64'));
for(const folder of['lingotech','lingotech-photo-booth']){fs.mkdirSync(path.join(root,folder),{recursive:true});fs.writeFileSync(path.join(root,folder,'index.html'),html);}
const release={version:'4.3',baseline_version:'4.2',html_sha256:sha(html),bytes:Buffer.byteLength(html),canonical:'https://williamlovecs.github.io/lingotech/',changes:['Separate creative scenes from frame layouts; preserve owned photos and personal text','Replace hero images with IMG_8240 and the existing LingoCorner high-five asset; five unique photos','Measured text boxes and dedicated safe areas across seven layouts and three ratios','Remove all star/sparkle decorations from preview and export','Responsive canvas containment; no fixed-height clipping','Keep native files-only JPG/PNG sharing and honest fallback','Remove UTM and version query parameters without changing the canonical URL'],limitations:['Browser share targets and actual WeChat delivery require physical-device confirmation']};
fs.writeFileSync(path.join(root,'lingotech','release.json'),JSON.stringify(release,null,2)+'\n');
console.log(JSON.stringify(release,null,2));
