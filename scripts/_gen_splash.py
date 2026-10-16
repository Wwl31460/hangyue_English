# 替换启动画面：把 Capacitor 默认 logo 换成本 App 的品牌启动图
# （深蓝渐变底 + 白色打开的书，与桌面版/图表风格一致）
from PIL import Image, ImageDraw
import glob
import os

RES = r'C:\Users\wwl31460\WorkBuddy\2026-10-14-15-13-28\android\app\src\main\res'

BRAND_LIGHT = (31, 111, 174)
BRAND_DARK = (11, 44, 70)
WHITE = (255, 255, 255, 255)


def gradient(size, c1, c2):
    w, h = size
    img = Image.new('RGB', size)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        row = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = row
    return img


def draw_book(img, cx, cy, w, h):
    d = ImageDraw.Draw(img)
    gap = w * 0.06
    radius = max(2, int(w * 0.08))
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx - gap, cy + h / 2], radius=radius, fill=WHITE)
    d.rounded_rectangle([cx + gap, cy - h / 2, cx + w / 2, cy + h / 2], radius=radius, fill=WHITE)
    line = (11, 44, 70, 105)
    lw = max(2, int(w * 0.022))
    for i in range(3):
        yy = cy - h * 0.20 + i * h * 0.20
        d.line([cx - w * 0.40, yy, cx - w * 0.13, yy], fill=line, width=lw)
        d.line([cx + w * 0.13, yy, cx + w * 0.40, yy], fill=line, width=lw)


def main():
    targets = sorted(glob.glob(os.path.join(RES, '**', 'splash.png'), recursive=True))
    if not targets:
        print('未找到 splash.png')
        return
    for path in targets:
        old = Image.open(path)
        w, h = old.size
        img = gradient((w, h), BRAND_LIGHT, BRAND_DARK).convert('RGBA')
        short = min(w, h)
        draw_book(img, w / 2, h / 2, short * 0.30, short * 0.30 * 0.72)
        img.save(path, 'PNG')
        rel = os.path.relpath(path, RES)
        print(f'{rel:<42} {w}x{h} 已替换')
    print('DONE 启动图已全部换为品牌样式')


if __name__ == '__main__':
    main()
