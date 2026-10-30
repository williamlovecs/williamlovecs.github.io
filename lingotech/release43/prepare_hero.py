"""Pin the publicly shared, user-approved Drive photo before optimizing it."""
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageOps
import io, hashlib
ROOT = Path(__file__).resolve().parent
EXPECTED = '5f135e10c529e9b133c5073b3bf763b3b0296a91bc81576f6b8eda163e209c1d'
URL = 'https://drive.google.com/uc?export=download&id=1A7MsEL3G1mqvZdsIc4_StXXjOdU208vr'
with urlopen(Request(URL, headers={'User-Agent': 'LingoTech-Release-Builder/4.3'}), timeout=45) as response:
    raw = response.read(12_000_000)
if hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise RuntimeError('Source image changed or download did not return the approved image; refusing to publish.')
image = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert('RGB')
image.thumbnail((640, 640))
image.save(ROOT / 'hero-build-8240.webp', 'WEBP', quality=65, method=6)
print('Approved IMG_8240 source hash verified; optimized hero:', image.size)
