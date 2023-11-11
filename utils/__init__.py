from typing import Tuple, Union
from .adb_utils import *
from .GlobalState import *
from .image_processing import *
from .subprocess_helper import *

import logging
import time
import config

def click(item:Union[str, Tuple[float, float]], sleeptime = -1) -> bool:
    """
    Task: click the position (x, y) or the center of a picture (given by a str)
    
    This action will sleep for a while after click
    """
    # check if the item is a str
    if isinstance(item, str):
        matchRes = match(item, returnpos=True)
        if matchRes[0]:
            click_on_screen(matchRes[1][0], matchRes[1][1])
            time.sleep(config.TIME_AFTER_CLICK)
            return True
        else:
            logging.warning("Cannot find the target pattern {} when try to click".format(item))
            return False
    else:
        click_on_screen(item[0], item[1])
        if(sleeptime!=-1):
            time.sleep(sleeptime)
        else:
            time.sleep(config.TIME_AFTER_CLICK)
        return True

def swipe(item:Union[str, Tuple[float, float]], toitem: Union[str, Tuple[float, float]], durationtime = 0.3, sleeptime = -1) -> bool:
    """
    Task: swipe the position (x, y) or the center of a picture to a position or a picture
    
    time: seconds
    """
    frompos = None
    topos = None
    # check if the item is a str
    if isinstance(item, str):
        (res, pos) = match_pattern(item)
        if res:
            frompos = (pos[0], pos[1])
    else:
        frompos = (item[0], item[1])
    if isinstance(toitem, str):
        (res, pos) = match_pattern(toitem)
        if res:
            topos = (pos[0], pos[1])
    else:
        topos = (toitem[0], toitem[1])
    if(frompos and topos):
        swipe_on_screen(frompos[0], frompos[1], topos[0], topos[1], durationtime*1000)
        if sleeptime == -1:
            sleep(config.TIME_AFTER_CLICK)
        else:
            sleep(sleeptime)
        return True
    else:
        logging.warning("Cannot find the target pattern {} and {} when try to swipe".format(item, toitem))
        return False

def match(imgurl:str, threshold:float = 0.9, returnpos = False, rotate_trans=False) -> bool | Tuple[bool, Tuple[float, float], float]:
    """
    Task: given a pattern picture url match it
    
    match result will only differ a little if there just have a light change
    
    if returnpos is True,
        return whether the pattern is found and the position of the pattern and the max_val
    else:
        return boolean
        
    if rotate_trans is True, the pattern will be rotated if it is transparent
    """
    # check if the item is a str
    if returnpos:
        return match_pattern("./screenshot.png",imgurl, threshold=threshold, auto_rotate_if_trans=rotate_trans)
    else:
        return match_pattern("./screenshot.png",imgurl, threshold=threshold, auto_rotate_if_trans=rotate_trans)[0]

def ocr_area(frompixel, topixel) -> Tuple[str, float]:
    """
    OCR the area in the given rectangle area of screenshot
    
    frompixel: (x, y)
    topixel: (x, y)
    
    axis is in image form, x axis is the horizontal axis, y axis is the vertical axis
    """
    lowerpixel = (min(frompixel[0], topixel[0]), min(frompixel[1], topixel[1]))
    highterpixel = (max(frompixel[0], topixel[0]), max(frompixel[1], topixel[1]))
    return ocr_pic_area("./screenshot.png", lowerpixel[0], lowerpixel[1], highterpixel[0], highterpixel[1]).strip()

def ocr_area_0(frompixel, topixel) -> bool:
    """
    OCR the number in the given rectangle area of screenshot whether it is 0
    
    frompixel: (x, y)
    topixel: (x, y)
    
    axis is in image form, x axis is the horizontal axis, y axis is the vertical axis
    """
    lowerpixel = (min(frompixel[0], topixel[0]), min(frompixel[1], topixel[1]))
    highterpixel = (max(frompixel[0], topixel[0]), max(frompixel[1], topixel[1]))
    res_str = ocr_pic_area("./screenshot.png", lowerpixel[0], lowerpixel[1], highterpixel[0], highterpixel[1]).strip()
    if res_str=="0" or res_str=="O" or res_str=="o" or res_str=="Q":
        return True
    return False

def match_pixel(x, y, color):
    """
        match whether the pixel is the given color
        
        color: Page.COLOR_*
        axis is in image form
    """
    # TODO
    # ...
    pass

def page_pic(picname):
    """
    给定页面的图片名称，得到图片的路径
    """
    return config.PIC_PATH + "/PAGE" + f"/{picname}.png"

def button_pic(buttonname):
    """
    给定按钮的图片名称，得到图片的路径
    """
    return config.PIC_PATH + "/BUTTON" + f"/{buttonname}.png"

def popup_pic(popupname):
    """
    给定弹窗的图片名称，得到图片的路径
    """
    return config.PIC_PATH + "/POPUP" + f"/{popupname}.png"

def sleep(seconds:float):
    """
    Task: sleep for seconds
    """
    time.sleep(seconds)
    
def screenshot():
    """
    Task: take a screenshot
    """
    screen_shot_to_file()