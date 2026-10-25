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

def apply_filter_loop(img, M):
    m, n, l = img.shape
    out = np.zeros((m, n, l), dtype=np.uint8)
    for i in range(m):
        for j in range(n):
            PixelColor = img[i, j, :].astype(np.float64).reshape(3, 1)
            out[i, j, :] = to_uint8(M @ PixelColor).ravel()
    return out

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
# PHẦN C: NHIỆM VỤ CỦA THÀNH VIÊN 4 (Task 3, Task 6)
# ==========================================

# %% Task 3: Extract the individual color channels
# Python indexes from 0, so MATLAB ImJPG(:,:,1) becomes ImJPG[:, :, 0].
redChannel = ImJPG[:, :, 0]
greenChannel = ImJPG[:, :, 1]
blueChannel = ImJPG[:, :, 2]
show(redChannel, "Task 3: Red channel")
show(greenChannel, "Task 3: Green channel")
show(blueChannel, "Task 3: Blue channel")

# %% Task 6: Red filter
RedMatrix = np.array([
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
])
ImJPG_Red = apply_filter_loop(ImJPG, RedMatrix)
show(ImJPG_Red, "Task 6: Red Only Image")

# Q2: What does the transformation above do?
# A2: It maps every pixel [R; G; B] to [R; 0; 0]: the red component is kept
#     unchanged while green and blue are set to zero, so the image is shown
#     only in shades of red. Geometrically, RedMatrix projects each color
#     vector onto the red axis of RGB space. It has rank 1 (det = 0), so the
#     information stored in the green and blue channels is lost and cannot be
#     recovered from ImJPG_Red.

plt.show()
