import sys
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')
from modules.configs.MyConfig import config
if len(sys.argv) > 1:
    configname = sys.argv[1]
    config = config.parse_user_config(configname)
    print("读取指定的config文件: "+configname)
else:
    configname = "config.json"
    config = config.parse_user_config(configname)
    print("读取默认config文件: "+configname)
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
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PageName import PageName
from DATA.assets.PopupName import PopupName

from modules.AllTask import *
from modules.AllTask.InCafe.CollectPower import CollectPower
from modules.AllPage.Page import Page

drawing = False  # 检查是否正在绘制
start_x, start_y = -1, -1
def main():
    # 读取透明度层
    screenshot = cv2.imread("./{}".format(config.userconfigdict['SCREENSHOT_NAME']))
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

    cv2.imshow('Matched Screenshot', screenshot)
    cv2.setMouseCallback("Matched Screenshot", mouse_callback_s)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=="__main__":
    # print([i for i in os.listdir(config.USER_CONFIG_FOLDER) if i.endswith(".json")])
    
    # print(os.path.basename(config.userconfigdict['TARGET_EMULATOR_PATH']+" --instance pie"))
    
    # emulator_instance = subprocess_run(config.userconfigdict['TARGET_EMULATOR_PATH'].split(" "), isasync=True)
    # print("等待模拟器启动")
    # for i in range(10):
    #     time.sleep(1)
    #     print(".")
    # print("\n关闭模拟器")
    # # 关闭模拟器
    # subprocess_run(["taskkill", "/F", "/IM", "HD-Player.exe"], encoding="gbk")
    # print("成功关闭")
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
    # res1 = match_pattern(config.userconfigdict['SCREENSHOT_NAME'], page_pic(PageName.PAGE_FIGHT_CENTER),  show_result=True, auto_rotate_if_trans=False)
    

    # 比划点
    main()
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
    # RaidQuest(-2).run()
    
    
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
    