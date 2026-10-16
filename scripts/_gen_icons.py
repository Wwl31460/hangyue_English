# 生成品牌启动图标：深蓝底 + 白色打开的书（呼应 App 的「航悦英语」品牌）
# 产出 Android 各 dpi 的 ic_launcher / ic_launcher_round / ic_launcher_foreground
from PIL import Image, ImageDraw
import os

RES = r'C:\Users\wwl31460\WorkBuddy\2026-10-14-15-13-28\android\app\src\main\res'

BRAND_LIGHT = (31, 111, 174)   # #1f6fae 渐变起点
BRAND_DARK = (11, 44, 70)      # #0b2c46 渐变终点
WHITE = (255, 255, 255, 255)

# Android 各密度对应的倍率
DPIS = [('mdpi', 1), ('hdpi', 1.5), ('xhdpi', 2), ('xxhdpi', 3), ('xxxhdpi', 4)]


def gradient_rgba(size, c1, c2):
    """斜向线性渐变"""
    img = Image.new('RGBA', (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / max(1, (2 * size - 2))
            px[x, y] = (
                int(c1[0] + (c2[0] - c1[0]) * t),
                int(c1[1] + (c2[1] - c1[1]) * t),
                int(c1[2] + (c2[2] - c1[2]) * t),
                255,
            )
    return img


def draw_book(img, cx, cy, w, h, color=WHITE):
    """在画布 (cx,cy) 处居中画一本打开的书，w/h 为整本书宽高"""
    d = ImageDraw.Draw(img)
    gap = w * 0.06          # 中缝宽度
    radius = max(2, int(w * 0.08))
    # 左右两页
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx - gap, cy + h / 2], radius=radius, fill=color)
    d.rounded_rectangle([cx + gap, cy - h / 2, cx + w / 2, cy + h / 2], radius=radius, fill=color)
    # 书页上的「文字」细线（半透明深蓝，压在白页上）
    line = (11, 44, 70, 105)
    lw = max(2, int(w * 0.022))
    for i in range(3):
        yy = cy - h * 0.20 + i * h * 0.20
        d.line([cx - w * 0.40, yy, cx - w * 0.13, yy], fill=line, width=lw)
        d.line([cx + w * 0.13, yy, cx + w * 0.40, yy], fill=line, width=lw)


def make_foreground(px):
    """自适应图标前景：108dp 画布，图形落在中心 72dp 安全区内"""
    img = Image.new('RGBA', (px, px), (0, 0, 0, 0))
    # 书本占安全区的约 78%
    book_w = px * 0.62
    book_h = book_w * 0.72
    draw_book(img, px / 2, px / 2, book_w, book_h)
    return img


def make_legacy(px, round_icon=False):
    """传统图标：整图背景 + 书本"""
    img = gradient_rgba(px, BRAND_LIGHT, BRAND_DARK)
    mask = Image.new('L', (px, px), 0)
    md = ImageDraw.Draw(mask)
    if round_icon:
        md.ellipse([0, 0, px - 1, px - 1], fill=255)
    else:
        r = int(px * 0.22)
        md.rounded_rectangle([0, 0, px - 1, px - 1], radius=r, fill=255)
    out = Image.new('RGBA', (px, px), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    draw_book(out, px / 2, px / 2, px * 0.52, px * 0.52 * 0.72)
    return out


def save(img, folder, name):
    d = os.path.join(RES, folder)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, name)
    img.save(path, 'PNG')
    return path


def main():
    n = 0
    for dpi, scale in DPIS:
        # 自适应图标前景：108dp
        fg_px = int(round(108 * scale))
        save(make_foreground(fg_px), f'mipmap-{dpi}', 'ic_launcher_foreground.png')
        # 传统图标：48dp
        legacy_px = int(round(48 * scale))
        save(make_legacy(legacy_px), f'mipmap-{dpi}', 'ic_launcher.png')
        save(make_legacy(legacy_px, round_icon=True), f'mipmap-{dpi}', 'ic_launcher_round.png')
        n += 3
        print(f'{dpi}: foreground={fg_px}px legacy={legacy_px}px')
    print(f'DONE 共生成 {n} 个图标文件')


if __name__ == '__main__':
    main()
