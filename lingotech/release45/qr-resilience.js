// Keep the original QR payload and four-module quiet zone.
// Landscape exports need 7px modules to survive 720px JPEG sharing.
qr44Geometry=function(W,H){
 const e=Math.round(Math.min(W,H)*.035),unit=W>H?7:5;
 const qrSize=QR44_MODULES*unit,w=qrSize+30,h=qrSize+40;
 return{x:W-e-w,y:H-e-h,w,h,qrSize};
};
