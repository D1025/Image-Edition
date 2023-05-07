import numpy as np
from PIL import Image

def static_min_filter(image, size):
    img_array = np.array(image)

    height, width, _ = img_array.shape

    mask_size = size // 2

    result_array = np.zeros_like(img_array)

    for i in range(height):
        for j in range(width):
            min_i = max(i - mask_size, 0)
            max_i = min(i + mask_size + 1, height)
            min_j = max(j - mask_size, 0)
            max_j = min(j + mask_size + 1, width)

            sub_array = img_array[min_i:max_i, min_j:max_j, :]

            min_r = np.min(sub_array[:, :, 0])
            min_g = np.min(sub_array[:, :, 1])
            min_b = np.min(sub_array[:, :, 2])

            result_array[i, j, 0] = min_r
            result_array[i, j, 1] = min_g
            result_array[i, j, 2] = min_b

    result_img = Image.fromarray(result_array.astype(np.uint8))

    return result_img


def static_max_filter(image, mask_size):
    img_array = np.array(image)

    height, width = img_array.shape[:2]

    margin = mask_size // 2

    result_array = np.zeros_like(img_array)

    for i in range(margin, height - margin):
        for j in range(margin, width - margin):
            region = img_array[i - margin:i + margin + 1, j - margin:j + margin + 1]

            max_values = np.max(region, axis=(0, 1))

            result_array[i, j] = max_values

    result_image = Image.fromarray(result_array.astype(np.uint8))

    return result_image


def median_filter(image, mask_size):
    img_array = np.array(image)

    height, width = img_array.shape[:2]

    margin = mask_size // 2

    result_array = np.zeros_like(img_array)

    for i in range(margin, height - margin):
        for j in range(margin, width - margin):
            region = img_array[i - margin:i + margin + 1, j - margin:j + margin + 1]

            median_values = np.median(region, axis=(0, 1))

            result_array[i, j] = median_values

    result_image = Image.fromarray(result_array.astype(np.uint8))

    return result_image