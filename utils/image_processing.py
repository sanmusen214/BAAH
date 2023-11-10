import cv2
import logging
import math
import numpy as np
from typing import Tuple


type Matchresult = (bool, (float, float))

def rotate_image_with_transparency(image_mat, angle):
    """
    给定一个包含透明层的图像Mat，将其旋转angle角度，返回旋转后的图像Mat

    """
    # 获取到图像的对角线长度
    diagonal = int(math.sqrt(pow(image_mat.shape[0], 2) + pow(image_mat.shape[1], 2)))
    # 创建一个diagonal * diagonal的空白含透明度的图像Mat
    rotated_image = np.zeros((diagonal, diagonal, 4), dtype=np.uint8)
    # 将原图像复制到新图像的中心
    x_offset = (diagonal - image_mat.shape[1]) // 2
    y_offset = (diagonal - image_mat.shape[0]) // 2
    rotated_image[y_offset:y_offset+image_mat.shape[0], x_offset:x_offset+image_mat.shape[1]] = image_mat
    # 获取rotated_image的高度、宽度和中心点
    center = (diagonal // 2, diagonal // 2)

    # 定义旋转矩阵
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 执行旋转，多出来的部分全透明
    rotated_image = cv2.warpAffine(rotated_image, rotation_matrix, (diagonal, diagonal), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)
    # 返回中心和原图一样大小的区域
    return rotated_image[y_offset:y_offset+image_mat.shape[0], x_offset:x_offset+image_mat.shape[1]]


def match_pattern(sourcepic: str, patternpic: str,threshold: float = 0.95, show_result:bool = False) -> Tuple[bool, Tuple[float, float], float]:
    """
    Match the pattern picture in the source picture.
    
    If the pattern picture is a transparent picture, it will be rotated to match the source picture.
    """
    screenshot = cv2.imread(sourcepic)
    
    pattern = cv2.imread(patternpic, cv2.IMREAD_UNCHANGED)  # 读取包含透明通道的模板图像
    have_alpha=False
    if(pattern.shape[2] == 4):
        have_alpha = True
        best_max_val = -1
        best_max_loc = (0, 0)
        for i in range(-3, 4):
            degree = i
            # 旋转
            rotate_pattern = rotate_image_with_transparency(pattern, degree)
            # 以透明部分作为mask
            rotate_mask = rotate_pattern[:, :, 3]  # 透明通道
            rotate_mask[rotate_mask>0] = 255
            rotate_pattern = rotate_pattern[:, :, :3] # 去除透明通道
            # https://www.cnblogs.com/FHC1994/p/9123393.html
            result = cv2.matchTemplate(screenshot, rotate_pattern, cv2.TM_CCORR_NORMED, mask=rotate_mask)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            # print("角度为{}时，最大匹配值为{}".format(degree, max_val))
            if max_val>best_max_val:
                best_max_val = max_val
                best_max_loc = max_loc
        min_val, max_val, min_loc, max_loc = 0, best_max_val, 0, best_max_loc
    else:
        result = cv2.matchTemplate(screenshot, pattern, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    h, w, _ = pattern.shape
    top_left = max_loc
    # get the center of the pattern
    center_x = top_left[0] + int(w / 2)
    center_y = top_left[1] + int(h / 2)
    if (show_result):
        bottom_right = (top_left[0] + w, top_left[1] + h)
        # draw a rectangle on the screenshot
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
        # draw a circle on the center of the pattern
        cv2.circle(screenshot, (center_x, center_y), 10, (0, 0, 255), -1)
        print("max_val: ", max_val)
        cv2.imshow('Matched Screenshot', screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    if(max_val >= threshold):
        logging.debug("Pattern of {} and {} matched ({}). Center: ({}, {})".format(sourcepic, patternpic, max_val, center_x, center_y))
        return (True, (center_x, center_y), max_val)
    return (False, (0, 0), 0)