import json
from typing import Tuple, Union
from .adb_utils import *
from .image_processing import *
from .subprocess_helper import *
from .grid_analyze import *
from .notification import *

import logging
import time
from modules.configs.MyConfig import config

def get_config_time_after_click():
    return config.userconfigdict['TIME_AFTER_CLICK']

def get_config_screenshot_name():
    return config.userconfigdict['SCREENSHOT_NAME']

def get_config_pic_path():
    return config.userconfigdict['PIC_PATH']

def get_pic_data(image_url):
    """
    通过url获取图像的内容
    """
    return cv2.imread(image_url)

def get_screenshot_cv_data():
    """
    获取截图的内容数据
    """
    return get_pic_data(get_config_screenshot_name())

def click(item:Union[str, Tuple[float, float]], sleeptime = -1, threshold=0.9) -> bool:
    """
    Task: click the position (x, y) or the center of a picture (given by a str)
    
    This action will sleep for a while after click
    """
    # check if the item is a str
    if isinstance(item, str):
        matchRes = match(item, returnpos=True, threshold=threshold)
        if matchRes[0]:
            click_on_screen(matchRes[1][0], matchRes[1][1])
            time.sleep(get_config_time_after_click())
            return True
        else:
            logging.warning("试图点击的目标图像不存在: {} ".format(item))
            return False
    else:
        click_on_screen(item[0], item[1])
        if(sleeptime!=-1):
            time.sleep(sleeptime)
        else:
            time.sleep(get_config_time_after_click())
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
            sleep(get_config_time_after_click())
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
        return [whether the pattern is found, (x of the pattern, y of the pattern), the max matching val]
    else:
        return boolean
        
    if rotate_trans is True, the pattern will be rotated if it is transparent
    """
    # check if the item is a str
    if returnpos:
        return match_pattern(f"./{get_config_screenshot_name()}",imgurl, threshold=threshold, auto_rotate_if_trans=rotate_trans)
    else:
        return match_pattern(f"./{get_config_screenshot_name()}",imgurl, threshold=threshold, auto_rotate_if_trans=rotate_trans)[0]

def ocr_area(frompixel, topixel, multi_lines = False) -> Tuple[str, float]:
    """
    OCR the area in the given rectangle area of screenshot
    
    frompixel: (x, y)
    topixel: (x, y)
    
    axis is in image form, x axis is the horizontal axis, y axis is the vertical axis
    """
    lowerpixel = (min(frompixel[0], topixel[0]), min(frompixel[1], topixel[1]))
    highterpixel = (max(frompixel[0], topixel[0]), max(frompixel[1], topixel[1]))
    ocr_result = ocr_pic_area(f"./{get_config_screenshot_name()}", lowerpixel[0], lowerpixel[1], highterpixel[0], highterpixel[1], multi_lines=multi_lines)
    return ocr_result

def ocr_area_0(frompixel, topixel) -> bool:
    """
    OCR the number in the given rectangle area whether it is 0, return False if length>1
    
    frompixel: (x, y)
    topixel: (x, y)
    
    axis is in image form, x axis is the horizontal axis, y axis is the vertical axis
    """
    lowerpixel = (min(frompixel[0], topixel[0]), min(frompixel[1], topixel[1]))
    highterpixel = (max(frompixel[0], topixel[0]), max(frompixel[1], topixel[1]))
    res_str = ocr_pic_area(f"./{get_config_screenshot_name()}", lowerpixel[0], lowerpixel[1], highterpixel[0], highterpixel[1])[0]
    res_str = res_str.strip()
    allpossibles = ["0", "O", "o", "Q", "０"]
    # 如果长度为1，就判断它是不是0
    if len(res_str) == 1:
        if res_str[0] in allpossibles:
            return True
    # # 一长串判断是否有0，必须得是第一个字符或者前面没有数字
    # if len(res_str) >= 2:
    #     if res_str[0] in allpossibles:
    #         return True
    #     for i in range(1, len(res_str)):
    #         if res_str[i] in allpossibles and not res_str[i-1].isdigit():
    #             return True
    # 长度大于1直接返回False
    return False

def match_pixel(xy, color, printit = False):
    """
        match whether the pixel is the given color
        
        color: Page.COLOR_*
        axis is in image form
    """
    return match_pixel_color_range(f"./{get_config_screenshot_name()}", xy[0], xy[1], color[0], color[1], printit=printit)

def page_pic(picname):
    """
    给定页面的图片名称，得到图片的路径
    """
    return get_config_pic_path() + "/PAGE" + f"/{picname}.png"

def button_pic(buttonname):
    """
    给定按钮的图片名称，得到图片的路径
    """
    # 如果是反和谐，就把按钮名称改成反和谐的
    if config.userconfigdict["FANHEXIE"] and buttonname == "BUTTON_CFIGHT_START":
        buttonname = "BUTTON_CFIGHT_START_FANHEXIE"
    return get_config_pic_path() + "/BUTTON" + f"/{buttonname}.png"

def popup_pic(popupname):
    """
    给定弹窗的图片名称，得到图片的路径
    """
    # 如果是反和谐，就把名称改成反和谐的
    if config.userconfigdict["FANHEXIE"] and popupname == "POPUP_MOMOTALK":
        popupname = "POPUP_MOMOTALK_FANHEXIE"
    return get_config_pic_path() + "/POPUP" + f"/{popupname}.png"

def get_grid_solution_json(location, level, ishard=False):
    # 读取DATA/grid_config/quest/里的文件
    ishardstr = "h" if ishard else ""
    filename = f"./DATA/grid_solution/quest/{ishardstr}{location}-{level}.json"
    # 读取并解析json返回
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

def sleep(seconds:float):
    """
    Task: sleep for seconds
    """
    time.sleep(seconds)
    
def screenshot():
    """
    Task: take a screenshot
    """
    start = time.time()
    screen_shot_to_global()
    end = time.time()
    # 输出截图耗时小数点后两位
    logging.debug("截图耗时{:.2f}秒".format(end-start))
    
def check_connect():
    # 检查当前python目录下是否有screenshot.png文件，如果有就删除
    if os.path.exists(f"./{get_config_screenshot_name()}"):
        logging.info(f"删除{get_config_screenshot_name()}")
        os.remove(f"./{get_config_screenshot_name()}")
    connect_to_device()
    # 尝试截图
    screenshot()
    time.sleep(2)
    if os.path.exists(f"./{get_config_screenshot_name()}"):
        logging.info(f"截图文件大小为{os.path.getsize(f'./{get_config_screenshot_name()}')//1024}KB")
        # 检查文件大小
        if os.path.getsize(f"./{get_config_screenshot_name()}") !=0: # 不为0
            logging.info("adb与模拟器连接正常")
            # 检查图片长和宽
            img = cv2.imread(f"./{get_config_screenshot_name()}")
            # 第一维度是高，第二维度是宽
            if img.shape[0] == 720 and img.shape[1] == 1280:
                logging.info("图片分辨率为1280*720")
                return True
            elif img.shape[0] == 1280 and img.shape[1] == 720:
                logging.warn("图片分辨率为720*1280，可能是模拟器设置错误，也可能是模拟器bug")
                logging.warn("继续运行，但是可能会出现问题，请确保模拟器分辨率为1280*720")
                return True
            else:
                logging.error("图片分辨率不为1280*720，请设置模拟器分辨率为1280*720（当前{}*{}）".format(img.shape[1], img.shape[0]))
                raise Exception("图片分辨率不为1280*720，请设置模拟器分辨率为1280*720（当前{}*{}）".format(img.shape[1], img.shape[0]))
    logging.error("adb与模拟器连接失败")
    logging.info("请检查adb与模拟器连接端口号是否正确")
    return False