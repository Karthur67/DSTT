"""Các hàm dùng chung để xử lý ảnh RGB trong Project 3."""
import numpy as np
import matplotlib.pyplot as plt


def to_uint8(values):
    """Làm tròn pixel và giữ giá trị trong khoảng 0 đến 255."""
    values = np.array(values, dtype=float)
    values = np.floor(values + 0.5)
    values = np.clip(values, 0, 255)
    return values.astype(np.uint8)


def apply_filter(img, M):
    """Áp dụng ma trận màu 3x3 cho toàn bộ ảnh."""
    if len(img.shape) != 3 or img.shape[2] != 3:
        raise ValueError("Ảnh phải có 3 kênh RGB.")
    if M.shape != (3, 3):
        raise ValueError("Ma trận lọc phải có kích thước 3x3.")

    # Đổi sang số thực trước khi nhân ma trận.
    result = img.astype(float) @ M.T
    return to_uint8(result)


def apply_filter_loop(img, M):
    """Áp dụng ma trận màu bằng hai vòng lặp, từng pixel một."""
    if len(img.shape) != 3 or img.shape[2] != 3:
        raise ValueError("Ảnh phải có 3 kênh RGB.")
    if M.shape != (3, 3):
        raise ValueError("Ma trận lọc phải có kích thước 3x3.")

    height, width, _ = img.shape
    result = np.zeros(img.shape, dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            pixel = img[i, j].astype(float).reshape(3, 1)
            new_pixel = M @ pixel
            result[i, j] = to_uint8(new_pixel).flatten()

    return result


def show(img, title):
    """Hiển thị ảnh."""
    plt.figure()
    if len(img.shape) == 2:
        plt.imshow(img, cmap="gray")
    else:
        plt.imshow(img)
    plt.title(title)
    plt.axis("off")
