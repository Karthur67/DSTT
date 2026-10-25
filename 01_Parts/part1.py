# ======================= SHARED HEADER =======================
# Helper functions used by all tasks.
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def to_uint8(x):
    """Equivalent of MATLAB uint8(): round (halves away from zero) and clip to [0, 255].
    NOTE: numpy's .astype(np.uint8) does NOT clip - it wraps around
    (e.g. 260 -> 4, -5 -> 251), so we must clip explicitly."""
    x = np.sign(x) * np.floor(np.abs(x) + 0.5)
    return np.clip(x, 0, 255).astype(np.uint8)


def apply_filter_loop(img, M):
    """Multiply the color vector [R;G;B] of every pixel by the 3x3 matrix M,
    pixel by pixel with an explicit loop, as in the project text."""
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
# ===================== END OF SHARED HEADER =====================


# %% Task 1: Load and display the image
ImJPG = np.array(Image.open("daylilies.jpg").convert("RGB"))
show(ImJPG, "Original image")

# %% Task 2: Dimensions of the array
m, n, l = ImJPG.shape
print(f"m = {m}, n = {n}, l = {l}")
# m = number of rows (pixel height), n = number of columns (pixel width),
# l = 3 color channels (R, G, B). Each entry is an integer 0..255 (uint8),
# so one pixel can take 256^3 (about 16.7 million) different colors.

plt.show()
