import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# PART A: GENERAL CODE

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
    plt.imshow(img, cmap="gray" if img.ndim == 2 else None, vmin=0, vmax=255)
    plt.title(title)
    plt.axis("off")

# PART B: ORIGINAL IMAGE

ImJPG = np.array(Image.open("daylilies.jpg").convert("RGB"))
m, n, l = ImJPG.shape

# ---------------- Setup (Part B in the template) ----------------
# Task 12 needs ImJPG_User from Task 11 (TV2's part), so I copied it here
# to be able to run this file on its own. It's above "# %% Task 8",
# so the merge script drops it and nothing gets duplicated.
UserMatrix = np.array([
    [0.7, 0.15, 0.15],
    [0.15, 0.7, 0.15],
    [0.15, 0.15, 0.7]
])
ImJPG_User = apply_filter_loop(ImJPG, UserMatrix)

# PART C: MEMBER_7's TASKS (Task 8, Task 12)

# %% Task 8: Delete green
# keep R and B, set G = 0 (second row is all zeros)
DeleteGreenMatrix = np.array([
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 1]
])
ImJPG_DeleteGreen = apply_filter_loop(ImJPG, DeleteGreenMatrix)
show(ImJPG_DeleteGreen, "Task 8: Green Deleted")

# quick check: green channel should be 0 everywhere
print("Max green value after deleting:", ImJPG_DeleteGreen[:, :, 1].max())

# %% Task 12: Inverse of UserMatrix
det_User = np.linalg.det(UserMatrix)
print("det(UserMatrix) =", round(det_User, 4))   # 0.3025, not 0

InvUserMatrix = np.linalg.inv(UserMatrix)
print("inv(UserMatrix) =")
print(np.round(InvUserMatrix, 4))

ImJPG_UserInv = apply_filter_loop(ImJPG_User, InvUserMatrix)
ImJPG_Inv = apply_filter_loop(ImJPG, InvUserMatrix)
show(ImJPG_UserInv, "Task 12: Inverse filter on ImJPG_User")
show(ImJPG_Inv, "Task 12: Inverse filter on ImJPG")

# compare the recovered image with the original
err = np.abs(ImJPG.astype(int) - ImJPG_UserInv.astype(int)).max()
print("Max difference between ImJPG_UserInv and ImJPG:", err)

# Is the transformation invertible? Can you get the original image back?
# Yes. det(UserMatrix) = 0.3025 is not 0, so the matrix has an inverse and
# we can get the original colors back. The recovered image is off by at most
# 1 (out of 255) because ImJPG_User was rounded to integers after filtering.
# This is too small to see, so basically no information is lost.

# Q5: What does the inverse transformation do with the colors?
# A5: UserMatrix mixes a bit of the other two channels into each channel, so
#     colors get closer to gray (washed out). The inverse does the opposite:
#     it takes away part of the other channels from each one, which pushes the
#     colors away from gray. On ImJPG_User this cancels the filter and we get
#     the original image back. On the original ImJPG the colors become much
#     stronger - the flowers are deeper red and the leaves are brighter green.
#     Some pixels go over 255 or below 0 and get cut off, so this result
#     can't be undone exactly.

plt.show()   # only for running this file alone, removed when merging
