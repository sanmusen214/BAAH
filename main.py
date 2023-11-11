import sys
import os

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

import logging
import config
from utils import *
from AllTask.myAllTask import my_AllTask


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')

def main():
    # 检查当前python目录下是否有screenshot.png文件，如果有就删除
    while(1):
        if os.path.exists("./screenshot.png"):
            logging.info("删除screenshot.png")
            os.remove("./screenshot.png")
        connect_to_device()
        # 尝试截图
        screen_shot_to_file()
        if os.path.exists("./screenshot.png"):
            logging.info("adb与模拟器连接正常")
            os.remove("./screenshot.png")
            break
        else:
            logging.error("adb与模拟器连接失败")
            logging.info("请检查adb与模拟器连接端口号是否正确，你也可以在这里修改端口号")
            input_port = input("请输入端口号（留空以继续使用config.py中的端口号）：")
            config.TARGET_PORT = int(input_port) if input_port != "" else config.TARGET_PORT

    my_AllTask.run()

if __name__ == "__main__":
    main()