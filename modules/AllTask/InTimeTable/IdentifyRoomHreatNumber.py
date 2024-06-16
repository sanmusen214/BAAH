import cv2
import numpy
import os

from DATA.assets.PopupName import PopupName
from modules.utils import (popup_pic)


def split_room_pic(pic_file_path: str) -> list[numpy.ndarray]:
    ret_list = []
    num_pic = cv2.imread(pic_file_path)
    ret_list.append(num_pic[203:335, 135:456])
    ret_list.append(num_pic[204:335, 485:800])
    ret_list.append(num_pic[202:336, 831:1144])
    ret_list.append(num_pic[353:487, 139:458])
    ret_list.append(num_pic[356:487, 484:802])
    ret_list.append(num_pic[355:488, 828:1146])
    ret_list.append(num_pic[507:621, 138:459])
    ret_list.append(num_pic[507:622, 480:807])
    tmp_room = ret_list[-1]
    template = cv2.imread(popup_pic(PopupName.POPUP_NONE_ROOM))
    err = numpy.sum((tmp_room.astype("float") - template.astype("int")) ** 2)
    err /= float(tmp_room.shape[0] * tmp_room.shape[1])
    if err < 0.1:
        ret_list.pop()
    return ret_list


def get_heart_num(room_pic: numpy.ndarray, debug=False) -> int:
    img_gray = cv2.cvtColor(room_pic, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(popup_pic(PopupName.POPUP_TIMETABLE_HEART))
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    locations = numpy.where(res >= 0.9)
    count = 0
    h, w = template.shape[0:2]
    close_list = []
    for x1, y1 in zip(*locations[::-1]):
        close_num = [abs(x1 - i) for i in close_list]
        if any(_ < 10 for _ in close_num):
            continue
        x2 = x1 + w
        y2 = y1 + h
        cv2.rectangle(room_pic, (x1, y1), (x2, y2), (0, 255, 0), 2)
        close_list.append(x1)
        count += 1
    if debug:
        file_num = 0
        time_name = f'heartNum_debug_{file_num}.png'
        while os.path.exists(time_name):
            file_num += 1
            time_name = f'heartNum_debug_{file_num}.png'
        cv2.imwrite(time_name, room_pic)
    return count
