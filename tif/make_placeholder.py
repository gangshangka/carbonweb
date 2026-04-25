from PIL import Image
import numpy as np

# 任选一张彩色PNG作为形状模板
template = Image.open('color_nep202207.png').convert('RGBA')
data = np.array(template)

# 填充颜色：淡黄绿色（代表陆地基础色调）
fill_color = (212, 230, 196)  # R,G,B
alpha = data[..., 3]
mask = alpha > 0

data[mask, 0] = fill_color[0]
data[mask, 1] = fill_color[1]
data[mask, 2] = fill_color[2]

placeholder = Image.fromarray(data, mode='RGBA')
placeholder.save('placeholder.png')
print('占位底图已生成：placeholder.png')