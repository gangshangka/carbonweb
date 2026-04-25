import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 使用 RdYlGn (红-黄-绿) 色彩映射
cmap = plt.get_cmap('RdYlGn')

for filename in os.listdir('.'):
    if filename.endswith('.png') and filename.startswith('nep') and not filename.startswith('color_'):
        # 读入灰度图（单通道）
        gray_img = Image.open(filename).convert('L')
        data = np.array(gray_img, dtype=np.float32) / 255.0  # 归一化到 0-1

        # 应用色彩映射，得到 RGBA 数组 (0-1)
        colored = cmap(data)  # shape (h, w, 4)

        # 创建透明通道：将数据背景（接近0）设为透明
        alpha = np.ones_like(data, dtype=np.float32)
        alpha[data < 0.02] = 0.0          # 阈值可调，值越小透明的越少
        colored[..., 3] = alpha

        # 转换为8位RGBa图像
        colored_uint8 = (colored * 255).astype(np.uint8)
        out = Image.fromarray(colored_uint8, mode='RGBA')
        out_name = 'color_' + filename
        out.save(out_name)
        print(f'✅ 生成 {out_name}')