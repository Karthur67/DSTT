import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ImJPG = np.array(Image.open("gigachad.img"))

def apply_filter(img, M):
    res = np.dot(img.astype(float), M.T)
    return np.clip(res, 0, 255).astype(np.uint8)

UserMatrix = np.array([
    [0.55, 0, 0],
    [0, 0.55, 0],
    [0, 0, 1.0]
])
ImJPG_User = apply_filter(ImJPG, UserMatrix)

# %% Task 8
NoGreen = np.array([
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 1]
])

ImJPG_NoGreen = apply_filter(ImJPG, NoGreen)

plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.imshow(ImJPG)
plt.title("ImJPG")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(ImJPG_NoGreen)
plt.title("ImJPG_NoGreen")
plt.axis("off")
plt.tight_layout()
plt.show()

# %% Task 12
det_UserMatrix = np.linalg.det(UserMatrix)
print("det(UserMatrix) =", round(det_UserMatrix, 4))

UserMatrix_inv = np.linalg.inv(UserMatrix)
ImJPG_User_inv = apply_filter(ImJPG_User, UserMatrix_inv)
ImJPG_inv = apply_filter(ImJPG, UserMatrix_inv)

diff = np.max(np.abs(ImJPG.astype(int) - ImJPG_User_inv.astype(int)))
print("Sai lech toi da:", diff)

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(ImJPG_User)
plt.title("ImJPG_User")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(ImJPG_User_inv)
plt.title("Recovered ImJPG_User")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(ImJPG_inv)
plt.title("Inverse on ImJPG")
plt.axis("off")
plt.tight_layout()
plt.show()
