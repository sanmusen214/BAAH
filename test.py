# 图片截取&标注
import threading
import requests
import cv2
from modules.utils.MyConfig import config
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
    # 平均最大最小rgb
    rgb_result = [[],[],[]]
    def mouse_callback_s(event, x, y, flags, param):
        # 截图
        global start_x, start_y, drawing
        if event == cv2.EVENT_RBUTTONDOWN:  # 检查是否是鼠标右键键点击事件
            print(f"Mouse click: ({x}, {y})", f"rgb array of this pixel: {screenshot[y, x]}")
            rgb_result[0].append(screenshot[y, x][0])
            rgb_result[1].append(screenshot[y, x][1])
            rgb_result[2].append(screenshot[y, x][2])
            print("min max avg rgb: ", np.min(rgb_result, axis=1), np.max(rgb_result, axis=1), np.mean(rgb_result, axis=1))
            
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
            print("Selected region saved as 'selected_region.png'")

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

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')



if __name__=="__main__":
    # print(os.path.getsize(f"./{'screenshot.png'}"))
    
    # request_url = "https://arona.diyigemt.com/api/v2/image?name=%E5%9B%BD%E9%99%85%E6%9C%8D%E6%B4%BB%E5%8A%A8"
    # response = requests.get(request_url)
    # if response.status_code == 200:
    #     if len(response.json()['data']) != 0:
    #         print(response.json()['data'])
    
    # connect_to_device()
    # screenshot()
    # print(Page.is_page(PageName.PAGE_CAFE))
    # print(match(button_pic(ButtonName.BUTTON_COLLECT_GRAY)))
    # print(match(button_pic(ButtonName.BUTTON_COLLECT_GRAY), returnpos=True)[2])
    # print(match(button_pic(ButtonName.BUTTON_COLLECT), returnpos=True)[2])
    
    # 测match
    # res1 = match_pattern("./screenshot.png", page_pic(PageName.PAGE_EVENT),  show_result=True, auto_rotate_if_trans=True)
    
    # 比划点
    # main()
    
    # 图像识别
    # rawMat = cv2.imread("./screenshot.png")
    # print(ocr_area((122, 178),(164, 212)))
    # for i in range(10):
        # print(ocr_area((72, 85), (200, 114)))
    
    # 测task
    # swipe((915, 643), (920, 180), 1.5)
    # InEvent().run()
    # NormalQuest(config.QUEST["NORMAL"][1]).run()
    
    
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
    