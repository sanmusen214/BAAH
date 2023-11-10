# 图片截取&标注
import cv2
import config
import numpy as np
from utils import *
from assets.ButtonName import ButtonName
from assets.PageName import PageName
from assets.PopupName import PopupName

from AllTask import *

def match2():
    # 读取目标图像和模板图像
    target_image = cv2.imread('./screenshot.png')
    template_image = cv2.imread(button_pic(ButtonName.BUTTON_STU_NOTICE), cv2.IMREAD_UNCHANGED)  # 读取包含透明通道的模板图像
    # template_image = cv2.imread("./selected_region.png", cv2.IMREAD_UNCHANGED)  # 读取包含透明通道的模板图像
    print(template_image.shape)

    # 获取模板图像的宽度和高度
    template_width, template_height = template_image.shape[1], template_image.shape[0]

    # 创建一个掩码，将透明区域设为0，不透明区域设为255
    mask = template_image[:, :, 3]  # 透明通道
    print(mask)
    mask[mask > 0] = 255
    # 将mask在第三维度上复制3份，因为目标图像是3通道的
    mask = cv2.merge((mask, mask, mask))
    print("mask的形状: ", mask.shape)
    # 使用模板匹配
    result = cv2.matchTemplate(target_image, template_image[:, :, :3], cv2.TM_CCORR_NORMED, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    # 设置阈值来筛选匹配结果
    threshold = 0.9
    locations = np.where(result >= threshold)
    # 绘制匹配结果的矩形框
    if max_val > threshold:
        print("Found possible match.")
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        cv2.rectangle(target_image, top_left, bottom_right, (0, 255, 0), 2)

    # 保存带有匹配结果的图像
    cv2.imshow('Image', target_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


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


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')

if __name__=="__main__":
    # connect_to_device()
    # screen_shot_to_file()
    
    # 测match
    # res = match_pattern("./screenshot.png", button_pic(ButtonName.BUTTON_ALL_COLLECT), show_result=True)

    
    # 比划点
    # main()
    
    # 图像识别
    # rawMat = cv2.imread("./screenshot.png")
    # print(get_number(rawMat[49:84,22:71]))
    print(ocr_number((74, 49), (18, 84)))
    
    # 测task
    # InContest().run()
    
    
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