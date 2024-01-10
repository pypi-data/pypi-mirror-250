import numpy as np
import cv2


def mask_coloring(src, color):
    max_value = np.max(src)
    src_color = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
    for i in range(1, 1 + max_value):
        src_color[np.where(src == i)] = color[i - 1]
    return src_color
