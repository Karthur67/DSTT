"""
Project 3 - part5.py (TV5): Task 7 (permute + hue rotation) and Task 14 (Gamma)
Run: python part5.py   (daylilies.jpg must be in the same folder)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# ---------- Phan dau file chung (TV2) ----------
def to_uint8(x):
    """Equivalent of MATLAB uint8(): round half away from zero, clip to [0, 255]."""
    x = np.sign(x) * np.floor(np.abs(x) + 0.5)
    return np.clip(x, 0, 255).astype(np.uint8)


def apply_filter(img, M):
    """Multiply [R;G;B] of every pixel by the 3x3 matrix M."""
    return to_uint8(img.astype(np.float64) @ M.T)


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
ImJPG_Permute = apply_filter(ImJPG, PermuteMatrix)
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
ImJPG_HueRotate = apply_filter(ImJPG, HueRotateMatrix)
show(ImJPG_HueRotate, "Hue rotation, theta = pi/2")

# Other angles (experiment)
hue_results = {}
for deg in (30, 90, 180, 270):
    hue_results[deg] = apply_filter(ImJPG, hue_rotate_matrix(np.deg2rad(deg)))
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
# Gamma1: x^0.9 on the 0..255 scale compresses the range (255 -> 147), and +30 only
#   partly compensates, so the image is slightly darker, flatter and low-contrast.
# Gamma2: x^1.1 stretches the range (anything above ~190 exceeds 255 and is clipped),
#   and -50 darkens the shadows, so the image is brighter in the highlights with
#   higher contrast and more saturated colors.
# These maps are not of the form M @ [R;G;B], so they are not linear.


# ---------- Chi de luu anh nop (TV1 bo phan nay khi ghep) ----------
os.makedirs("02_Anh", exist_ok=True)
fig, ax = plt.subplots(2, 3, figsize=(15, 8))
panels = [(ImJPG, "Original"), (ImJPG_Permute, "Permute (R<->B)"),
          (ImJPG_HueRotate, "HueRotate 90 deg"), (hue_results[30], "HueRotate 30 deg"),
          (hue_results[180], "HueRotate 180 deg"), (hue_results[270], "HueRotate 270 deg")]
for a, (im, t) in zip(ax.ravel(), panels):
    a.imshow(im); a.set_title(t); a.axis("off")
fig.tight_layout(); fig.savefig("02_Anh/TV5_Task7.png", dpi=150)

fig, ax = plt.subplots(1, 3, figsize=(15, 5))
for a, (im, t) in zip(ax, [(ImJPG, "Original"), (ImJPG_Gamma1, "Gamma1: x^0.9 + 30"),
                           (ImJPG_Gamma2, "Gamma2: x^1.1 - 50")]):
    a.imshow(im); a.set_title(t); a.axis("off")
fig.tight_layout(); fig.savefig("02_Anh/TV5_Task14.png", dpi=150)

plt.show()   # TV1 xoa dong nay khi ghep (chi giu plt.show() cuoi file ghep)