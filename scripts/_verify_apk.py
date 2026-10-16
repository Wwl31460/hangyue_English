# 校验打出来的 APK：前端资源版本、图标/启动图是否已替换成品牌样式
# 注意：AGP 会重命名并优化 res/ 下的图片，不能用原文件名查找，只能按尺寸识别。
import io
import pathlib
import zipfile

from PIL import Image

ROOT = pathlib.Path(r'C:\Users\wwl31460\WorkBuddy\2026-10-14-15-13-28')
APK = ROOT / 'android/app/build/outputs/apk/release/app-release.apk'
OUT = ROOT / 'shots'

# 图标相关尺寸（px）：legacy 图标 & 自适应图标前景
ICON_SIZES = {48, 72, 96, 144, 192, 108, 162, 216, 324, 432}

OUT.mkdir(exist_ok=True)

with zipfile.ZipFile(APK) as z:
    names = z.namelist()

    web = sorted(n for n in names if n.startswith('assets/public/'))
    print('=== 前端资源 ===')
    for n in web:
        print(' ', n)

    print()
    print('=== res/ 下的图片（按尺寸识别）===')
    hits = []
    for n in names:
        if not n.startswith('res/') or not n.endswith('.png'):
            continue
        data = z.read(n)
        try:
            im = Image.open(io.BytesIO(data))
            size = im.size
        except Exception as e:
            print('  解析失败', n, e)
            continue
        mark = ''
        if size[0] == size[1] and size[0] in ICON_SIZES:
            mark = '  <== 图标候选'
            hits.append((n, size, data))
        print(f'  {n:<32} {str(size):<12} {len(data):>8} B{mark}')

    # 把图标候选导出来，方便肉眼确认是不是品牌图标
    print()
    print('=== 导出图标候选到 shots/apk_icons ===')
    d = OUT / 'apk_icons'
    d.mkdir(parents=True, exist_ok=True)
    for n, size, data in hits[:8]:
        p = d / f'{size[0]}x{size[1]}_{pathlib.Path(n).name}'
        p.write_bytes(data)
        print(' ', p.name)
