"""
Project 3 - part5.py (TV5): Task 7 (permute + hue rotation) and Task 14 (Gamma)
Run: python part5.py   (daylilies.jpg must be in the same folder)
"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# ---------- Phan dau file chung (TV2) ----------
def to_uint8(x):
    """Equivalent of MATLAB uint8(): round (halves away from zero) and clip to [0, 255].
    NOTE: numpy's .astype(np.uint8) does NOT clip - it wraps around
    (e.g. 260 -> 4, -5 -> 251), so we must clip explicitly."""
    x = np.sign(x) * np.floor(np.abs(x) + 0.5)   # round half away from zero, like MATLAB
    return np.clip(x, 0, 255).astype(np.uint8)


def apply_filter_loop(img, M):
    """Multiply the color vector [R;G;B] of every pixel by the 3x3 matrix M,
    written with the explicit double loop from the project text."""
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


ImJPG = np.array(Image.open("daylilies.jpg").convert("RGB"))
m, n, l = ImJPG.shape
# ---------- het phan dau file chung ----------


# %% Task 7: Permute the colors and hue rotation
PermuteMatrix = np.array([[0, 0, 1],
                          [0, 1, 0],
                          [1, 0, 0]])
ImJPG_Permute = apply_filter_loop(ImJPG, PermuteMatrix)
show(ImJPG_Permute, "Colors permuted (R <-> B)")

# HueRotate(theta) = A + cos(theta)*B + sin(theta)*C
HueA = np.array([[0.213, 0.715, 0.072],
                 [0.213, 0.715, 0.072],
                 [0.213, 0.715, 0.072]])
HueB = np.array([[0.787, -0.715, -0.072],
                 [-0.213, 0.285, -0.072],
                 [-0.213, -0.715, 0.928]])
HueC = np.array([[-0.213, -0.715, 0.928],
                 [0.143, 0.140, -0.283],
                 [-0.787, 0.715, 0.072]])


def hue_rotate_matrix(theta):
    return HueA + np.cos(theta) * HueB + np.sin(theta) * HueC


theta = np.pi / 2
HueRotateMatrix = hue_rotate_matrix(theta)
ImJPG_HueRotate = apply_filter_loop(ImJPG, HueRotateMatrix)
show(ImJPG_HueRotate, "Hue rotation, theta = pi/2")

# Other angles (experiment)
hue_results = {}
for deg in (30, 90, 180, 270):
    hue_results[deg] = apply_filter_loop(ImJPG, hue_rotate_matrix(np.deg2rad(deg)))
    show(hue_results[deg], f"Hue rotation, theta = {deg} deg")

# Short explanation of hue rotation (English)
# E7: The hue rotation matrix is A + cos(theta)*B + sin(theta)*C.
#     A projects each color onto its brightness (every row holds the luminance
#     weights 0.213, 0.715, 0.072). B and C span the two directions of the
#     "color plane" orthogonal to the gray axis [1,1,1]; cos/sin of theta turn
#     the color in that plane, like rotating a point on a color wheel.
#     For theta = 0 the matrix is the identity, so the image is unchanged.
#     Gray pixels [t,t,t] stay fixed (B and C map [1,1,1] to 0) and the
#     brightness is (almost) preserved, so only the hue changes: reds drift
#     to yellow/green/blue as theta grows, and after theta = 2*pi the colors
#     come back to the start. PermuteMatrix is different: it only swaps the
#     R and B channels (an orthogonal matrix that reflects, not a smooth rotation).


# %% Task 14: Non-linear (Gamma) color transformations
# Compute in float and clip: uint8 arithmetic in numpy wraps (250 + 30 = 24).
ImJPG_Gamma1 = to_uint8(to_uint8(ImJPG.astype(np.float64) ** 0.9).astype(np.float64) + 30)
ImJPG_Gamma2 = to_uint8(to_uint8(ImJPG.astype(np.float64) ** 1.1).astype(np.float64) - 50)
show(ImJPG_Gamma1, "Gamma 0.9, +30")
show(ImJPG_Gamma2, "Gamma 1.1, -50")
# Gamma1: x^0.9 compresses the range (255 -> 147) and +30 lifts the black level, so all
#   output values lie in [30, 177]: shadows are lighter and highlights are lowered,
#   giving a flatter, low-contrast image (mean brightness about the same).
# Gamma2: x^1.1 stretches the range (anything above ~154 exceeds 255 and is clipped);
#   after -50 those pixels all become 205, and dark pixels are pushed down to 0, so the
#   image has higher contrast and is slightly darker on average.
# These maps are not of the form M @ [R;G;B], so they are not linear.


plt.show()   # TV1 xoa dong nay khi ghep (chi giu plt.show() cuoi file ghep)
