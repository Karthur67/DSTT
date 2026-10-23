"""Project 3 - TV2: Task 4 (grayscale) and Task 11 (UserMatrix)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# This works whether part2.py is in the project folder or in 01_Parts/.
SCRIPT_FOLDER = Path(__file__).resolve().parent
if SCRIPT_FOLDER.name == "01_Parts":
    PROJECT_FOLDER = SCRIPT_FOLDER.parent
else:
    PROJECT_FOLDER = SCRIPT_FOLDER

# The original image must be in 00_DeBai/daylilies.jpg.
IMAGE_PATH = PROJECT_FOLDER / "00_DeBai" / "daylilies.jpg"

# Prefer the repository's 02_Anh folder. Keep support for the local 'ouputs' folder.
if (PROJECT_FOLDER / "02_Anh").is_dir():
    OUTPUT_FOLDER = PROJECT_FOLDER / "02_Anh"
elif (PROJECT_FOLDER / "ouputs").is_dir():
    OUTPUT_FOLDER = PROJECT_FOLDER / "ouputs"
else:
    OUTPUT_FOLDER = PROJECT_FOLDER / "02_Anh"


def to_uint8(values):
    """Round pixel values and keep them between 0 and 255."""
    values = np.rint(values)
    values = np.clip(values, 0, 255)
    return values.astype(np.uint8)


def apply_filter(image, matrix):
    """Apply a 3x3 color matrix to every pixel in an RGB image."""
    image_float = image.astype(float)
    result = image_float @ matrix.T
    return to_uint8(result)


def apply_filter_loop(image, matrix):
    """Apply a color matrix one pixel at a time (used in Task 4)."""
    height, width, _ = image.shape
    result = np.zeros(image.shape, dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            pixel = image[i, j].astype(float)
            result[i, j] = to_uint8(matrix @ pixel)

    return result


def show_image(image, title):
    """Display an image."""
    plt.figure()
    plt.imshow(image)
    plt.title(title)
    plt.axis("off")


def main():
    # Load the required source image.
    if not IMAGE_PATH.is_file():
        raise FileNotFoundError(
            f"Cannot find the source image: {IMAGE_PATH}\n"
            "Please put daylilies.jpg inside the 00_DeBai folder."
        )

    ImJPG = np.array(Image.open(IMAGE_PATH).convert("RGB"), dtype=np.uint8)
    print("Input image:", IMAGE_PATH)
    print("Image size:", ImJPG.shape)
    show_image(ImJPG, "Original image")

    # Task 4: convert the color image to grayscale.
    GrayMatrix = np.array([
        [1 / 3, 1 / 3, 1 / 3],
        [1 / 3, 1 / 3, 1 / 3],
        [1 / 3, 1 / 3, 1 / 3]
    ])
    ImJPG_Gray = apply_filter_loop(ImJPG, GrayMatrix)
    show_image(ImJPG_Gray, "Task 4 - Grayscale")

    # Task 11: mix the three color channels using UserMatrix.
    UserMatrix = np.array([
        [0.70, 0.15, 0.15],
        [0.15, 0.70, 0.15],
        [0.15, 0.15, 0.70]
    ])
    ImJPG_User = apply_filter(ImJPG, UserMatrix)
    show_image(ImJPG_User, "Task 11 - User color filter")

    # Save the two result images.
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    Image.fromarray(ImJPG_Gray).save(OUTPUT_FOLDER / "TV2_Task4.png")
    Image.fromarray(ImJPG_User).save(OUTPUT_FOLDER / "TV2_Task11.png")

    print("Task 4 image saved to:", OUTPUT_FOLDER / "TV2_Task4.png")
    print("Task 11 image saved to:", OUTPUT_FOLDER / "TV2_Task11.png")
    plt.show()


# Answers to the project questions (Q1 and Q4)
#
# Q1: uint8 and double
# uint8 stores image channel values as integers from 0 to 255. We convert the
# image to floating-point numbers (double) before matrix multiplication because
# filter calculations use decimal coefficients and may produce decimal results.
# After filtering, values are rounded, clipped to [0, 255], and converted back
# to uint8. In Python, clipping is important because astype(np.uint8) alone does
# not safely limit values to this range.
#
# Q4: Effect of UserMatrix
# Each output channel keeps 70% of its original value and receives 15% from each
# of the other two channels. For example, R' = 0.70R + 0.15G + 0.15B. Because
# each row sums to 1, neutral gray pixels (R = G = B) keep the same values.
# Mixing the channels makes them more similar, so the image looks less saturated
# and its colors appear softer. The sum of RGB values is also preserved before
# rounding and clipping because each column sums to 1.


if __name__ == "__main__":
    main()
