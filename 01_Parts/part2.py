import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# ==========================================
# PHẦN A: HÀM DÙNG CHUNG CỦA NHÓM
# ==========================================
def to_uint8(x):
    x = np.sign(x) * np.floor(np.abs(x) + 0.5)
    return np.clip(x, 0, 255).astype(np.uint8)

def apply_filter(img, M):
    return to_uint8(img.astype(np.float64) @ M.T)

def show(img, title):
    plt.figure()
    plt.imshow(img, cmap="gray" if img.ndim == 2 else None, vmin=0, vmax=255)
    plt.title(title)
    plt.axis("off")

# ==========================================
# PHẦN B: ĐỌC ẢNH GỐC
# ==========================================
ImJPG = np.array(Image.open("daylilies.jpg").convert("RGB"))
m, n, l = ImJPG.shape

# ==========================================
# PHẦN C: NHIỆM VỤ CỦA THÀNH VIÊN 2
# ==========================================

# %% Task 4: Grayscale conversion
GrayMatrix = np.array([
    [1/3, 1/3, 1/3], 
    [1/3, 1/3, 1/3], 
    [1/3, 1/3, 1/3]
])
ImJPG_Gray = apply_filter(ImJPG, GrayMatrix)
show(ImJPG_Gray, "Task 4: Grayscale Image")

# Q1: Explain the purpose of uint8 and double commands in the code above.
# A1: uint8 stores image channel values as strictly 8-bit integers (0-255). We must use float/double during matrix multiplication to prevent integer overflow and preserve mathematical precision. After all calculations are completed, we convert the data back to uint8 using rounding and clipping functions because standard image display libraries require pixel intensities to be integers strictly within the 0 to 255 range.

# %% Task 11: User color-adjusting filter
UserMatrix = np.array([
    [0.7, 0.15, 0.15], 
    [0.15, 0.7, 0.15], 
    [0.15, 0.15, 0.7]
])
ImJPG_User = apply_filter(ImJPG, UserMatrix)
show(ImJPG_User, "Task 11: User Filter Image")

# Q4: Explain what the transformation above does to the image.
# A4: The UserMatrix applies a desaturation and blending effect. By distributing a portion of each channel's intensity to the other channels, it reduces the color contrast between the RGB channels. The overall brightness remains consistent, but colors are pulled closer to a uniform gray tone.

# Lệnh hiển thị ảnh (Dùng khi test độc lập file này)
plt.show()
