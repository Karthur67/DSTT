import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
ImJPG = np.array(Image.open("daylilies.jpg").convert("RGB"))
def apply_filter(img, M):
    res = np.dot(img.astype(float), M.T)
    res = np.sign(res) * np.floor(np.abs(res) + 0.5)
    return np.clip(res, 0, 255).astype(np.uint8)
UserMatrix = np.array([
    [0.7, 0.15, 0.15],
    [0.15, 0.7, 0.15],
    [0.15, 0.15, 0.7]
])
ImJPG_User = apply_filter(ImJPG, UserMatrix)
# %% Task 8
DeleteGreenMatrix = np.array([
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 1]
])
ImJPG_DeleteGreen = apply_filter(ImJPG, DeleteGreenMatrix)
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.imshow(ImJPG)
plt.title("ImJPG")
plt.axis("off")
plt.subplot(1, 2, 2)
plt.imshow(ImJPG_DeleteGreen)
plt.title("ImJPG_DeleteGreen")
plt.axis("off")
plt.tight_layout()
# %% Task 12
det_UserMatrix = np.linalg.det(UserMatrix)
print("det(UserMatrix) =", round(det_UserMatrix, 4))
InvUserMatrix = np.linalg.inv(UserMatrix)
ImJPG_UserInv = apply_filter(ImJPG_User, InvUserMatrix)
ImJPG_Inv = apply_filter(ImJPG, InvUserMatrix)
diff = np.max(np.abs(ImJPG.astype(int) - ImJPG_UserInv.astype(int)))
print("Sai lech toi da:", diff)
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(ImJPG_User)
plt.title("ImJPG_User")
plt.axis("off")
plt.subplot(1, 3, 2)
plt.imshow(ImJPG_UserInv)
plt.title("Recovered ImJPG_User")
plt.axis("off")
plt.subplot(1, 3, 3)
plt.imshow(ImJPG_Inv)
plt.title("Inverse on ImJPG")
plt.axis("off")
plt.tight_layout()
plt.show()