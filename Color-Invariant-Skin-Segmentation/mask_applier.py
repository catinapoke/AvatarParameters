import os
import cv2
import numpy as np
from typing import Tuple, List


def masked_img_path(original_img_path: str) -> str:
    filename = os.path.splitext(original_img_path)[0]  # original_img_path.split('.')[:-1][0]
    extension = original_img_path.split('.')[-1:][0]

    return filename + '_masked.' + extension


def save_masked(original_img_path: str, mask_img_path: str):
    # https://pyimagesearch.com/2021/01/19/image-masking-with-opencv/
    image: cv2.Mat = cv2.imread(original_img_path)

    mask_img: cv2.Mat = cv2.imread(mask_img_path, 0)
    mask = np.zeros(mask_img.shape[:2], dtype="uint8")

    masked = cv2.bitwise_and(image, image, mask=mask_img)
    cv2.imwrite(masked_img_path(original_img_path), masked)
    print(f'Saved masked at {masked_img_path(original_img_path)}')
    pass


def count_pixels_from(img_path: str) -> int:
    # https://stackoverflow.com/questions/43519015/accessing-a-pixel-of-an-image-with-cv2
    image = cv2.imread(img_path)

    count = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if not all(image[i][j] == [0, 0, 0]):
                count = count + 1

    return count
    pass


def get_gradient_path():
    dirname, _ = os.path.split(os.path.realpath(__file__))
    return dirname + "\\gradient.png"


def difference(one: List[int], two: List[int]) -> int:
    subtracted = [element1 - element2 for (element1, element2) in zip(one, two)]
    return abs(sum(subtracted))


def get_coords(hex_color_str: str, pallete_path: str) -> Tuple[int, int]:
    if len(hex_color_str) != 6:
        print("Color string has wrong length! (not 6 with format ffffff)")
        return 0, 0

    print(f'Looking for color: {hex_color_str}')

    image = cv2.imread(pallete_path)

    color = [int(x, 16) for x in [hex_color_str[0:2], hex_color_str[2:4], hex_color_str[4:6]]]

    pos = (0, 0)
    count = 0

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if difference(image[i][j], color) < 2:
                # print(i, j)
                pos = (pos[0] + i, pos[1] + j)
                count = count + 1

    if count == 0:
        return 0, 0

    return round(pos[0] / count), round(pos[1] / count)


def print_pixels_from(img_path: str):
    # https://stackoverflow.com/questions/43519015/accessing-a-pixel-of-an-image-with-cv2
    image = cv2.imread(img_path)

    colors = dict()
    count = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if not sum(image[i][j] < 20): # image[i][j] == [0, 0, 0]
                color_str = f'{("0x%0.2X" % image[i][j][2])[2:]}{("0x%0.2X" % image[i][j][1])[2:]}{("0x%0.2X" % image[i][j][0])[2:]}'
                if color_str not in colors:
                    colors[color_str] = 0

                colors[color_str] = colors[color_str] + 1

    filename = os.path.splitext(img_path)[0]  # original_img_path.split('.')[:-1][0]

    colors_output = filename + '_colors.txt'
    color_file = open(colors_output, 'w')
    sorted_keys = sorted(colors.keys(), key=lambda x: colors.get(x))[::-1]
    for x in sorted_keys:
        color_file.write(f'{x}:{colors[x]}\n')
    color_file.close()

    return sorted_keys[0]


def mask_and_count_from(original_img_path: str, mask_img_path: str):
    save_masked(original_img_path, mask_img_path)
    print(f'Counted non-masked {count_pixels_from(masked_img_path(original_img_path))} from {masked_img_path(original_img_path)}')
    print(f'Counted all {count_pixels_from(original_img_path)} from {original_img_path}')

    color = print_pixels_from(masked_img_path(original_img_path))
    # os.remove(masked_img_path(original_img_path))
    return color
