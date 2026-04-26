"""
从 TIF 重新生成带透明通道的 PNG 热力图。
- NODATA (NaN) 区域设为全透明
- 使用固定色域 -1000..400 保证各月份色彩一致
- 色带：红(低NEP) → 黄(中) → 绿(高NEP)
"""
from PIL import Image
import numpy as np
import os

VMIN, VMAX = -1000.0, 400.0

def rdylgn_colormap(t):
    """t: 0=红(low) -> 0.5=黄(mid) -> 1=绿(high)"""
    t = np.clip(t, 0, 1)
    r = np.where(t < 0.5, (215 + t/0.5*40), (255 - (t-0.5)/0.5*241))
    g = np.where(t < 0.5, (25 + t/0.5*230),  (255 - (t-0.5)/0.5*105))
    b = np.where(t < 0.5, (28 + t/0.5*163),  (191 - (t-0.5)/0.5*125))
    return np.clip(np.stack([r, g, b], axis=-1), 0, 255).astype(np.uint8)

for fname in sorted(os.listdir('.')):
    if not fname.startswith('nep') or not fname.endswith('.tif'):
        continue
    out_name = 'color_' + fname.replace('.tif', '.png')

    try:
        src = Image.open(fname)
        arr = np.array(src, dtype=np.float32)

        # 50% resize
        h, w = arr.shape
        arr_resized = np.array(Image.fromarray(arr).resize((w//2, h//2), Image.BILINEAR))

        nan_mask = np.isnan(arr_resized)
        # 用 0 填充 NaN 避免 colormap 计算报 warning
        arr_filled = np.where(nan_mask, 0, arr_resized)

        normalized = (arr_filled - VMIN) / (VMAX - VMIN)
        rgb = rdylgn_colormap(normalized)

        alpha = np.where(nan_mask, 0, 255).astype(np.uint8)
        rgba = np.dstack([rgb, alpha]).astype(np.uint8)

        out = Image.fromarray(rgba, 'RGBA')
        out.save(out_name, optimize=True)
        print(f'OK {out_name}  transparent={(alpha==0).sum()}/{alpha.size}')
    except Exception as e:
        print(f'FAIL {fname}: {e}')
