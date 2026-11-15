# ============================================================
# PART A — SHARED HEADER (KEEP UNCHANGED WHEN MERGING)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def to_uint8(x):
    x = np.sign(x) * np.floor(np.abs(x) + 0.5)
    return np.clip(x, 0, 255).astype(np.uint8)


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
    plt.imshow(img, cmap="gray" if img.ndim == 2 else None)
    plt.title(title)
    plt.axis("off")


ImJPG = np.array(Image.open("daylilies.jpg").convert("RGB"))
m, n, l = ImJPG.shape


# ============================================================
# PART B — TASK-SPECIFIC PREPARATION
# No extra preparation is required for TV6.
# This section is discarded by the group's merge script.
# ============================================================


# ============================================================
# PART C — TV6 TASKS
# ============================================================

# %% Task 9: Invert the colors
ImJPG_Invert = 255 - ImJPG
show(ImJPG_Invert, "ImJPG_Invert")


# %% Task 10: Apply the saturation matrix
SaturateMatrix = np.array([
    [1.2, 0, 0],
    [0, 0.75, 0],
    [0, 0, 2]
])

ImJPG_Saturate = apply_filter_loop(ImJPG, SaturateMatrix)
show(ImJPG_Saturate, "ImJPG_Saturate")

# Q3: Explain what the transformation above does to the image?
# A3: The matrix scales the RGB channels independently: red is multiplied
#     by 1.2, green by 0.75, and blue by 2. Red becomes 20% stronger,
#     green is reduced to 75% of its original value, and blue is doubled.
#     In green foliage, the reduced green contribution makes the leaves
#     look less green and generally darker. In regions containing both
#     red and blue, the stronger red and blue contributions can produce
#     a more magenta or pink appearance. Since an 8-bit channel is limited
#     to 255, every original blue value greater than 127.5 is clipped to
#     255 after being doubled. Red values greater than 212.5 are also
#     clipped after multiplication by 1.2. This clipping can remove
#     detail in bright areas.

plt.show()
