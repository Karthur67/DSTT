# =====================================================================
#  FILE MẪU - mỗi người chép file này thành partX.py của mình
#  (TV1 -> part1.py, TV2 -> part2.py, ..., TV7 -> part7.py)
#  KHÔNG sửa PHẦN A. Chỉ viết vào PHẦN B và PHẦN C.
# =====================================================================

# ---------------- PHẦN A: phần đầu file chung (giữ nguyên) ----------------
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def to_uint8(x):
    """Equivalent of MATLAB uint8(): round (halves away from zero) and clip to [0, 255]."""
    x = np.sign(x) * np.floor(np.abs(x) + 0.5)
    return np.clip(x, 0, 255).astype(np.uint8)


def apply_filter(img, M):
    """Multiply the color vector [R;G;B] of every pixel by the 3x3 matrix M."""
    return to_uint8(img.astype(np.float64) @ M.T)


def apply_filter_loop(img, M):
    """Same as apply_filter, with the explicit loop from the project text."""
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

# ---------------- PHẦN B: chuẩn bị riêng (nếu cần) ----------------
# Biến lấy từ task của NGƯỜI KHÁC thì chép code của họ vào ĐÂY,
# phía trên dòng "# %% Task" đầu tiên. Khi ghép, phần này tự bị bỏ đi,
# nên không bị trùng code.
#   Ví dụ TV7 (Task 12 cần ImJPG_User của Task 11):
#   UserMatrix = np.array([[0.7, 0.15, 0.15],
#                          [0.15, 0.7, 0.15],
#                          [0.15, 0.15, 0.7]])
#   ImJPG_User = apply_filter(ImJPG, UserMatrix)


# ---------------- PHẦN C: các task của bạn ----------------
# Mỗi task bắt đầu bằng đúng một dòng "# %% Task <số>: <tên>"
# Dùng ĐÚNG tên biến trong đề. Câu trả lời tiếng Anh: # Q..: / # A..:

# %% Task 99: Ten bo loc  (đổi 99 thành số task của bạn)
FilterMatrix = np.array([[1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])
ImJPG_Out = apply_filter(ImJPG, FilterMatrix)
show(ImJPG_Out, "Ten bo loc")

# Q?: (chép câu hỏi trong đề)
# A?: (câu trả lời tiếng Anh, tự viết)


plt.show()   # để chạy riêng; khi ghép sẽ tự bỏ
