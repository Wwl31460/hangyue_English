# 从 APK 里精确提取图标（按尺寸），合成到白底上便于查看
import io
import pathlib
import zipfile

from PIL import Image

ROOT = pathlib.Path(r'C:\Users\wwl31460\WorkBuddy\2026-10-14-15-13-28')
APK = ROOT / 'android/app/build/outputs/apk/release/app-release.apk'
OUT = ROOT / 'shots/apk_icons'
OUT.mkdir(parents=True, exist_ok=True)

# 192 = 传统图标 xxxhdpi；432 = 自适应图标前景 xxxhdpi；324 = 前景 xxhdpi
WANT = {192, 432, 324}

with zipfile.ZipFile(APK) as z:
    for n in z.namelist():
        if not n.startswith('res/') or not n.endswith('.png'):
            continue
        data = z.read(n)
        try:
            im = Image.open(io.BytesIO(data))
        except Exception:
            continue
        if im.size[0] == im.size[1] and im.size[0] in WANT:
            canvas = Image.new('RGB', im.size, (255, 255, 255))
            canvas.paste(im, (0, 0), im if im.mode in ('RGBA', 'LA') else None)
            name = f'{im.size[0]}px_{pathlib.Path(n).stem}.png'
            canvas.save(OUT / name)
            print(f'导出 {name}  mode={im.mode}  {len(data)} B')
