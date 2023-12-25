import sys
configname = "config.json"
from modules.utils.MyConfig import config
print("读取默认config文件: "+configname)
if len(sys.argv) > 1:
    configname = sys.argv[1]
    config.parse_config(configname)
    print("重新读取指定的config文件: "+configname)
# 图片截取&标注
import threading
import requests
import cv2
import os
import time
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
import numpy as np
from modules.AllTask.InCafe.InviteStudent import InviteStudent
from modules.AllTask.InCafe.TouchHead import TouchHead
from modules.utils import *
from assets.ButtonName import ButtonName
from assets.PageName import PageName
from assets.PopupName import PopupName

from modules.AllTask import *
from modules.AllTask.InCafe.CollectPower import CollectPower
from modules.AllPage.Page import Page

drawing = False  # 检查是否正在绘制
start_x, start_y = -1, -1
def main():
    # connect_to_device()
    # screen_shot_to_file()

    # 读取透明度层
    screenshot = cv2.imread("./{}".format(config.SCREENSHOT_NAME))
    # 平均最大最小bgr
    bgr_result = [[],[],[]]
    def mouse_callback_s(event, x, y, flags, param):
        # 截图
        global start_x, start_y, drawing
        if event == cv2.EVENT_RBUTTONDOWN:  # 检查是否是鼠标右键键点击事件
            print(f"点击位置: ({x}, {y})", f"BGR 数组: {screenshot[y, x]}")
            bgr_result[0].append(screenshot[y, x][0])
            bgr_result[1].append(screenshot[y, x][1])
            bgr_result[2].append(screenshot[y, x][2])
            print("min max avg bgr: ", np.min(bgr_result, axis=1), np.max(bgr_result, axis=1), np.mean(bgr_result, axis=1))
            
        if event == cv2.EVENT_LBUTTONDOWN:  # 检查是否是鼠标左键按下事件
            drawing = True
            start_x, start_y = x, y
        elif event == cv2.EVENT_MOUSEMOVE:  # 检查是否是鼠标移动事件
            if drawing:
                screenshot_copy = screenshot.copy()  # 创建截图的副本
                cv2.rectangle(screenshot_copy, (start_x, start_y), (x, y), (0, 255, 0), 2)
                cv2.imshow('Matched Screenshot', screenshot_copy)
        elif event == cv2.EVENT_LBUTTONUP:  # 检查是否是鼠标左键释放事件
            drawing = False
            end_x, end_y = x, y
            # cv2.rectangle(screenshot, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            cv2.imshow('Matched Screenshot', screenshot)

            # 保存截取的区域到当前目录
            selected_region = screenshot[min(start_y,end_y):max(start_y,end_y), min(start_x,end_x):max(start_x,end_x)]
            cv2.imwrite("./selected_region.png", selected_region)
            print("选定区域已被保存为 'selected_region.png'")

    # cv2.circle(screenshot, (643, 518), 10, (0, 0, 255), -1)

    cv2.imshow('Matched Screenshot', screenshot)
    cv2.setMouseCallback("Matched Screenshot", mouse_callback_s)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # match_pattern("./screenshot.png", "./selected_region.png", show_result=True)

def multi_match(patternurl):
    """
    连续匹配
    """
    matchhis=[]
    for i in range(10):
        screen_shot_to_file()
        res = match_pattern("./screenshot.png", patternurl, show_result=True)
        matchhis.append(res)
    times = [each[0] for each in matchhis]
    print("匹配成功次数: ", times.count(True), "匹配失败次数: ", times.count(False))
    thresholds = [each[2] for each in matchhis]
    print("平均可信度: ", np.mean(thresholds))
    print("最大可信度: ", np.max(thresholds))
    print("最小可信度: ", np.min(thresholds))

# 创建一个自定义的 logging.Handler
class GUISupport(logging.Handler):
    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.print(msg)


def send_event(device, type, code, value):
    cmd = f"adb shell sendevent {device} {type} {code} {value}"
    os.system(cmd)

def touch_move(device, x, y):
    send_event(device, 3, 53, x)  # ABS_MT_POSITION_X
    send_event(device, 3, 54, y)  # ABS_MT_POSITION_Y
    send_event(device, 0, 2, 0)   # SYN_MT_REPORT
    send_event(device, 0, 0, 0)   # SYN_REPORT

def touch_down(device, x, y):
    send_event(device, 3, 57, 1)  # ABS_MT_TRACKING_ID, start of a contact
    touch_move(device, x, y)

def touch_up(device):
    send_event(device, 3, 57, -1) # ABS_MT_TRACKING_ID, end of a contact
    send_event(device, 0, 2, 0)   # SYN_MT_REPORT
    send_event(device, 0, 0, 0)   # SYN_REPORT

def pinch_zoom(device, x1_start, y1_start, x2_start, y2_start, x1_end, y1_end, x2_end, y2_end, steps=10):
    """
    Perform a pinch zoom gesture.
    
    :param device: Device path (e.g., '/dev/input/event1')
    :param x1_start, y1_start: Starting coordinates for the first touch point
    :param x2_start, y2_start: Starting coordinates for the second touch point
    :param x1_end, y1_end: Ending coordinates for the first touch point
    :param x2_end, y2_end: Ending coordinates for the second touch point
    :param steps: Number of steps for the zoom gesture
    """
    # Touch down both points
    touch_down(device, x1_start, y1_start)
    touch_down(device, x2_start, y2_start)
    time.sleep(0.1)

    # Perform the zoom gesture
    x1_step = (x1_end - x1_start) / steps
    y1_step = (y1_end - y1_start) / steps
    x2_step = (x2_end - x2_start) / steps
    y2_step = (y2_end - y2_start) / steps

    for _ in range(steps):
        x1_start += x1_step
        y1_start += y1_step
        x2_start += x2_step
        y2_start += y2_step
        touch_move(device, x1_start, y1_start)
        touch_move(device, x2_start, y2_start)
        time.sleep(0.1)

    # Touch up both points
    touch_up(device)
    touch_up(device)

# 使用示例
# device = "/dev/input/event1"
# pinch_zoom(device, 100, 400, 200, 400, 50, 400, 250, 400)


if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')
    # try:
    #     if not check_connect():
    #         print("请手动打开模拟器，adb连接失败，可能config.json端口配置有误")
    #     else:
    #         while 1:
    #             input("按回车键截图:")
    #             print("左键拖动区域截图，右键点击获取坐标点信息")
    #             screenshot()
    #             main()
    # except Exception as e:
    #     pass
    # input("按回车键退出")
    # print(os.path.getsize(f"./{'screenshot.png'}"))
    
    # request_url = "https://arona.diyigemt.com/api/v2/image?name=%E5%9B%BD%E9%99%85%E6%9C%8D%E6%B4%BB%E5%8A%A8"
    # response = requests.get(request_url)
    # if response.status_code == 200:
    #     if len(response.json()['data']) != 0:
    #         print(response.json()['data'])
    
    connect_to_device()
    screenshot()
    # print(Page.is_page(PageName.PAGE_CAFE))
    # print(match(button_pic(ButtonName.BUTTON_COLLECT_GRAY)))
    # print(match(button_pic(ButtonName.BUTTON_COLLECT_GRAY), returnpos=True)[2])
    # print(match(button_pic(ButtonName.BUTTON_COLLECT), returnpos=True)[2])
    
    # 测match
    # res1 = match_pattern(config.SCREENSHOT_NAME, button_pic(ButtonName.BUTTON_STU_NOTICE),  show_result=True, auto_rotate_if_trans=True)

    # 比划点
    # main()
    # offset = 40
    
    # matchres = match_pixel((639, 240), Page.COLOR_RED)
    # print(matchres)
    
    # ScrollSelect(9, 148, 262, 694, 1130, lambda: False).run() # Event无进度条
    # ScrollSelect(9, 140, 238, 583, 1130, lambda: False).run() # Event有进度条
    
    # 扫荡关卡识别地区数字
    # for i in range(20):
    #     screenshot()
    #     print(ocr_area((122, 179), (165, 211)))
    #     # click((1242, 357)) # right
    #     click((40, 357)) # left
    
    
    # 图像识别
    # rawMat = cv2.imread("./screenshot.png")
    # res = ocr_area((901, 88), (989, 123))
    # print(res)
    # for i in range(10):
        # print(ocr_area((72, 85), (200, 114)))
    
    # 测task
    # Event
    # ScrollSelect(7, 130, 235, 674, 1114,  lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))).run()
    # special
    # ScrollSelect(11, 130, 230, 680, 1119, lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))).run()
    # InEvent().run()
    RaidQuest(-2).run()
    
    
    # 测透明图片的旋转
    # mypic = cv2.imread(button_pic(ButtonName.BUTTON_STU_NOTICE), cv2.IMREAD_UNCHANGED)
    # newpic = rotate_image_with_transparency(mypic, 90)
    # cv2.imshow("newpic", newpic)
    # cv2.waitKey(0)
    
    # 画3x3点
    # mypic = cv2.imread("./screenshot.png")
    # xs = np.linspace(299, 995, 3, dtype=int)
    # ys = np.linspace(268, 573, 3, dtype=int)
    
    # for row in range(len(ys)):
    #     for col in range(len(xs)):
    #         # 在点周围标数字
    #         cv2.putText(mypic, str(row*3+col), (xs[col], ys[row]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    #         cv2.circle(mypic, (xs[col], ys[row]), 10, (0, 0, 255), -1)
    # cv2.imshow("newpic", mypic)
    # cv2.waitKey(0)
    