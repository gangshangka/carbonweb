import os
import numpy as np
from PIL import Image

# 自定义 RdYlGn 风格色带 (红 -> 黄 -> 绿)
# 每个点 [R, G, B] (0-255)
colormap = np.array([
    [215, 25, 28],   # 红
    [252, 141, 89],  # 橙
    [255, 255, 191], # 黄
    [166, 217, 106], # 浅绿
    [26, 150, 65]    # 深绿
], dtype=np.uint8)

# 创建查找表 (256 阶)
lut = np.zeros((256, 3), dtype=np.uint8)
for i in range(256):
    t = i / 255.0 * (len(colormap) - 1)
    idx0 = int(t)
    idx1 = min(idx0 + 1, len(colormap) - 1)
    frac = t - idx0
    lut[i] = (colormap[idx0] * (1 - frac) + colormap[idx1] * frac).astype(np.uint8)

# 处理所有灰度 PNG
for filename in os.listdir('.'):
    if filename.endswith('.png') and filename.startswith('nep') and not filename.startswith('color_'):
        gray = Image.open(filename).convert('L')
        data = np.array(gray)  # 0-255

        # 创建 RGBA 图像
        h, w = data.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)

        # 着色
        rgba[:, :, :3] = lut[data]

        # 透明度：将灰度值低于阈值的像素设为透明
        threshold = 5  # 值越小越透明，可根据背景调整
        alpha = np.where(data < threshold, 0, 255).astype(np.uint8)
        rgba[:, :, 3] = alpha

        img_out = Image.fromarray(rgba, mode='RGBA')
        out_name = 'color_' + filename
        img_out.save(out_name)
        print(f'✅ {filename} -> {out_name}')