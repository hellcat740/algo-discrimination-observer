# 生成扩展占位图标：圆角矩形底 + 柱状图 + 放大镜（纯形状绘制，不依赖字体）
# 输出到 public/icons/，构建时由 vite publicDir 拷贝到 dist/icons/
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "public" / "icons"
OUT.mkdir(parents=True, exist_ok=True)

BG = (79, 70, 229, 255)      # 靛蓝底
WHITE = (255, 255, 255, 255)
CYAN = (34, 211, 238, 255)

for size in (16, 48, 128):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 圆角矩形背景
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=BG)
    # 三根柱子（比价柱状图）
    bw = size * 0.14
    gap = size * 0.06
    x0 = size * 0.16
    base = size * 0.78
    for i, (h, c) in enumerate([(0.30, WHITE), (0.46, CYAN), (0.62, WHITE)]):
        x = x0 + i * (bw + gap)
        d.rectangle([x, base - size * h, x + bw, base], fill=c)
    # 放大镜（观测）
    cx, cy, r = size * 0.68, size * 0.30, size * 0.17
    w_ring = max(1, int(size * 0.05))
    w_handle = max(1, int(size * 0.06))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=w_ring)
    d.line([cx + r * 0.7, cy + r * 0.7, cx + r * 1.7, cy + r * 1.7], fill=WHITE, width=w_handle)
    img.save(OUT / f"icon{size}.png")
    print(f"已生成 {OUT / f'icon{size}.png'}")
