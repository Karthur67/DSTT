import numpy as np 
import matplotlib.pyplot as plt 
from PIL import Image 
# ==========================================
# PHẦN A: HÀM DÙNG CHUNG 
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
# PHẦN C: NHIỆM VỤ CỦA THÀNH VIÊN 3
# ==========================================
# %% Task 5: Sepia conversion
SepiaMatrix = np.array([[0.393, 0.769, 0.189],
                        [0.349, 0.686, 0.168],
                        [0.272, 0.534, 0.131]])
ImJPG_Sepia = apply_filter_loop(ImJPG, SepiaMatrix)
show(ImJPG_Sepia, "Task 5:Sepia Image")

# %% Task 13: Is the sepia transformation invertible?
detSepia = np.linalg.det(SepiaMatrix)
print(f"det(SepiaMatrix) = {detSepia:.2e}")

condSepia = np.linalg.cond(SepiaMatrix)
print("cond(SepiaMatrix) =", round(condSepia))

InvSepiaMatrix = np.linalg.inv(SepiaMatrix)
print("InvSepiaMatrix =\n", InvSepiaMatrix)

ImJPG_SepiaInv = apply_filter_loop(ImJPG_Sepia, InvSepiaMatrix)
ImJPG_SepiaInvOrig = apply_filter_loop(ImJPG, InvSepiaMatrix)

show(ImJPG_SepiaInv, "Inverse sepia applied to ImJPG_Sepia")
show(ImJPG_SepiaInvOrig, "Inverse sepia applied to ImJPG")

# Is the sepia transformation invertible?
# Mathematically, yes, since det(SepiaMatrix) is non-zero.
# However, the transformation is irreversible in practice.
# The restored image (ImJPG_SepiaInv) is multi-colored noise because SepiaMatrix 
# is ill-conditioned (cond = 16659) and collapses 3D RGB color space nearly onto 1D brown shades.
# The huge entries of InvSepiaMatrix magnify integer rounding errors by over 16000 times, destroying the image.

# Q6: What do you see? Why do you think this happened?
# A6: Formally, the sepia matrix is invertible (det = 1.21e-7 != 0), but the restored 
# image (ImJPG_SepiaInv) is random multi-colored noise rather than the original photo. 
# The rows of SepiaMatrix are almost linearly dependent, making it severely ill-conditioned 
# (cond = 16659) and collapsing 3D RGB color space almost onto 1D brown shades. 
# Because of this, InvSepiaMatrix has huge entries (~10^4), which magnify 
# rounding errors (up to 0.5) and clipping at 255 by over 16000 times into giant 
# errors, completely destroying the image. In practice, sepia is irreversible.
plt.show()