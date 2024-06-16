import cv2
import easyocr
import numpy
import re

from .TimeTableConstant import *


def cut_pic_school_name(all_pic: numpy.ndarray) -> numpy.ndarray:
    """学校名范围截图"""
    return all_pic[93:132, 923:1250]


def get_school_name_from_file_path(picture_path: str) -> str:
    """把截图文件用cv2读取 通过另一个函数得到学校名称"""
    img = cv2.imread(picture_path)
    return get_school_name_from_pic_numpy(img)


def clear_school_name(name: str) -> str:
    """读取中包含RANK数字，分割取最后一组属于学校名的一部分 or 全部"""
    res_list = re.split(r'\d|\?| ', name)
    return res_list[-1]


def splice_school_name(easy_read_list: list) -> str:
    """拼接带有标点符号的学校名 like · ——, 符号不体现在学校名内"""
    res_str: str = ""

    for item in easy_read_list:
        if bool(re.search(r'[\d|?]', item)):
            res_str = clear_school_name(item)
        else:
            res_str += item
    return res_str


def get_school_name_from_pic_numpy(picture_numpy: numpy.ndarray) -> str:
    """识别整张截图中的学校名部分，文字识别后返回学校名的字符串"""
    reader = easyocr.Reader(['ja'])
    cut = cut_pic_school_name(picture_numpy)
    res = reader.readtext(cut, detail=False, blocklist="Ig?~[]")
    school_name: str
    if len(res) == 1:
        school_name = clear_school_name(res[0])
    else:
        school_name = splice_school_name(res)
    return school_name


def get_school_number(pic_path: str) -> int:
    school_name = get_school_name_from_file_path(pic_path)
    return JP_SCHOOL_NUM_DICT[school_name]
