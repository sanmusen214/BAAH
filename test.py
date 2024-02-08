import sys
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')
from modules.configs.MyConfig import config
if len(sys.argv) > 1:
    configname = sys.argv[1]
    config.parse_user_config(configname)
    print("读取指定的config文件: "+configname)
else:
    configname = "config.json"
    config.parse_user_config(configname)
    print("读取默认config文件: "+configname)
# 图片截取&标注
import threading
import requests
import cv2
import os
import time
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.GridQuest import GridQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
import numpy as np
from modules.AllTask.InCafe.InviteStudent import InviteStudent
from modules.AllTask.SubTask.FightQuest import FightQuest
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
def screencut_tool():
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
            nowstr = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            filename = "selected_"+nowstr+".png"
            cv2.imwrite(filename, selected_region)
            print(f"选定区域已被保存为/Saved as {filename}")

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
    # res1 = match_pattern(config.userconfigdict['SCREENSHOT_NAME'], button_pic(ButtonName.BUTTON_CONFIRMB),  show_result=True, auto_rotate_if_trans=False)
    

    # 比划点
    screencut_tool()
    # offset = 40
    
    # matchres = match_pixel((639, 240), Page.COLOR_RED)
    # print(matchres)
    
    # ScrollSelect(9, 148, 262, 694, 1130, lambda: False).run() # Event无进度条
    # ScrollSelect(9, 140, 238, 583, 1130, lambda: False).run() # Event有进度条
    
    # FightQuest(backtopic=page_pic(PageName.PAGE_EVENT)).run()
    # ga = GridAnalyzer("quest","15-4.json")
    # GridQuest(ga, lambda: match(page_pic(PageName.PAGE_QUEST_SEL))).run()
    
    # 扫荡关卡识别地区数字
    # for i in range(20):
    #     screenshot()
    #     print(ocr_area((122, 179), (165, 211)))
    #     # click((1242, 357)) # right
    #     click((40, 357)) # left
    
    
    # 图像识别
    # rawMat = cv2.imread("./screenshot.png")
    # res = ocr_area((327, 257), (353, 288))
    # print(res)
    # for i in range(10):
        # print(ocr_area((72, 85), (200, 114)))
    # reslist = ocr_area((72, 544), (91, 569), multi_lines=False)
    # print(reslist)
    
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
    
    
    # # 截图小工具 screencut.exe
    # print("请手动打开模拟器...\nKeep emulator open")
    # sleep(2)
    # check_connect()
    # while 1:
    #     input(f"按回车键截图\nPress Enter to screencut:")
    #     print("左键拖动区域截图，右键点击获取坐标点信息\nTry left mouse drag or right mouse click")
    #     screenshot()
    #     screencut_tool()
    #     print("==========")
    
    # 走图识别start格子小工具
    # def get_kmeans(img, n, max_iter=5):
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     # 将img看成二维数组
    #     # 非0的像素点就是数据点
    #     # 为0的像素点就是背景
    #     # 随机n类，每类的中心点（x,y坐标）是随机的
    #     initial_centers = []
    #     for i in range(n):
    #         x = np.random.randint(0, img.shape[0])
    #         y = np.random.randint(0, img.shape[1])
    #         initial_centers.append([x, y])
    #     print("initial_centers", initial_centers)
        
    #     centers = initial_centers
    #     # 每次迭代，每个类的中心点都会更新
        
    #     # 将图像数组展平
    #     all_points = img.reshape((-1, 1))
    #     # 在axis=1的方向上，添加两列，range
    #     all_points = np.hstack((all_points, np.arange(all_points.shape[0]).reshape((-1, 1))))
    #     all_points = np.hstack((all_points, np.arange(all_points.shape[0]).reshape((-1, 1))))
        
    #     # 处理第2列数据除以图像宽度得到整数，处理第3列数据除以图像宽度得到余数
    #     all_points[:, 1] = all_points[:, 1] // img.shape[1]
    #     all_points[:, 2] = all_points[:, 2] % img.shape[1]
    #     # 在axis=1的方向上，添加一列，初始值为0，为每个像素点的类别
    #     all_points = np.hstack((all_points, np.zeros((all_points.shape[0], 1))))
    #     # 后续只考虑非0的像素点 np.any(img[i] != 0)
    #     # 去除第一列为0的像素点
    #     all_points = all_points[all_points[:, 0] != 0]
    #     print("all_points.shape", all_points.shape) # (n, 4)
        
    #     if all_points.shape[0] == 0:
    #         print("黄色过滤失败")
    #         return centers
        
    #     for i in range(max_iter):
    #         # 每次迭代，计算每个像素点到每个类的距离，取最小的那个类下标赋值给第4列
    #         for j in range(all_points.shape[0]):
    #             distances = []
    #             for k in range(len(centers)):
    #                 distances.append(np.linalg.norm(all_points[j, 1:3] - centers[k]))
    #             all_points[j, 3] = np.argmin(distances)
    #         # 每次迭代，计算每个类的中心点
    #         for j in range(len(centers)):
    #             # 取出第4列等于j的所有像素点
    #             points = all_points[all_points[:, 3] == j]
    #             # 计算平均值，如果没有像素点（空簇问题），就在其他簇内的点随机挑一个设为这个的中心点
    #             if points.shape[0] != 0:
    #                 centers[j] = np.mean(points[:, 1:3], axis=0)
    #             else:
    #                 centers[j] = all_points[np.random.randint(0, all_points.shape[0]), 1:3]
    #         print("iter centers", centers)
    #     return centers
        


    # # 画出k-means的结果
    # def draw_kmeans(img, centers):
    #     for center in centers:
    #         cv2.circle(img, (int(center[1]), int(center[0])), 15, (0, 0, 255), -1)
    #     return img

    # def show(img):
    #     # 左键点击获取BGRA值
    #     def on_mouse(event, x, y, flags, param):
    #         if event == cv2.EVENT_LBUTTONDOWN:
    #             print("BGR", img[y, x])
            
    #     cv2.namedWindow('image')
    #     cv2.setMouseCallback('image', on_mouse)
    #     cv2.imshow('image', img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    # import numpy as np
    # print("请手动打开模拟器...\nKeep emulator open")
    # sleep(2)
    # check_connect()
    # while 1:
    #     numstr = input(f"输入黄色的开始格子数量\nInput number of start block:")
    #     try:
    #         num = int(numstr)
    #         assert num >= 1 and num <= 5
    #     except:
    #         print("输入有误，请重新输入\nInvalid input, try again")
    #         continue
    #     screenshot()
    #     # 读取
    #     img = cv2.imread("./{}".format(config.userconfigdict['SCREENSHOT_NAME']))
    #     # 黄色蒙版
    #     lower = np.array([125, 250, 250])
    #     upper = np.array([132, 255, 255])
    #     mask = cv2.inRange(img, lower, upper)
    #     # 转成灰度图
    #     mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #     # 腐蚀
    #     kernel = np.ones((3, 3), np.uint8)
    #     masker2 = cv2.erode(mask, kernel)
    #     # k-means，维度是图片的xy坐标，将坐标相近的像素聚类
    #     centers = get_kmeans(masker2, n=num, max_iter=5)
    #     kmeans = draw_kmeans(img.copy(), centers)
    #     show(kmeans)
