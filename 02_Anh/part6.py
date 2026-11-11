"""
part6.py — TV6: Tasks 9 and 10
Project 3: Linear algebra applications in image processing.

Run:
    python part6.py

Dependencies:
    pip install numpy matplotlib pillow

When prompted, enter the path to the image to process.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def to_uint8(x):
    """Round half away from zero, clip to [0, 255], and convert to uint8."""
    x = np.asarray(x, dtype=float)
    rounded = np.where(x >= 0, np.floor(x + 0.5), np.ceil(x - 0.5))
    return np.clip(rounded, 0, 255).astype(np.uint8)


def apply_filter(img, matrix):
    """Apply a 3x3 color transformation matrix to an RGB image."""
    img = np.asarray(img, dtype=float)
    matrix = np.asarray(matrix, dtype=float)

    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("Input must be an RGB image with shape (height, width, 3).")
    if matrix.shape != (3, 3):
        raise ValueError("The transformation matrix must have shape (3, 3).")

    # For row-wise pixels [R, G, B], multiply by the transpose of M.
    return to_uint8(img @ matrix.T)


def show(img, title):
    """Display an image."""
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()


def load_rgb_image():
    """Ask for an image path; use a common default if one is found."""
    candidates = [
        Path("ImJPG.jpg"),
        Path("image.jpg"),
        Path("Images/ImJPG.jpg"),
        Path("images/ImJPG.jpg"),
        Path("../ImJPG.jpg"),
    ]
    default_path = next((p for p in candidates if p.is_file()), None)

    if default_path:
        entered = input(
            f"Image path (press Enter to use {default_path.as_posix()}): "
        ).strip()
        image_path = Path(entered.strip('"').strip("'")) if entered else default_path
    else:
        entered = input("Enter the path to the input image: ").strip()
        image_path = Path(entered.strip('"').strip("'")) if entered else None

    if image_path is None:
        raise FileNotFoundError("No image path was provided.")
    if not image_path.is_file():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with Image.open(image_path) as source:
        image = np.asarray(source.convert("RGB"), dtype=np.uint8)

    return image, image_path


def main():
    ImJPG, image_path = load_rgb_image()
    print(f"Loaded: {image_path}")
    print(f"Image dimensions: {ImJPG.shape[1]} x {ImJPG.shape[0]}")

    # Task 9: Invert the colors
    ImJPG_Invert = 255 - ImJPG
    show(ImJPG, "Original image")
    show(ImJPG_Invert, "Inverted colors")

    # Task 10: Enhance / mute individual colors
    SaturateMatrix = np.array([
        [1.2, 0, 0],
        [0, 0.75, 0],
        [0, 0, 2]
    ], dtype=float)

    ImJPG_Saturate = apply_filter(ImJPG, SaturateMatrix)
    show(ImJPG_Saturate, "Saturate")

    # Q3: Explain what the transformation above does to the image.
    # A3: [R; G; B] -> [1.2R; 0.75G; 2B].
    # Red is increased by 20%, green is reduced to 75%, and blue is doubled.
    # Values greater than 255 are clipped to 255.

    plt.show()


if __name__ == "__main__":
    main()
