import sys
import os

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

import logging
from modules.utils.MyConfig import config
from modules.utils import *
from modules.AllTask.myAllTask import my_AllTask

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')

def BAAH_main():
    disconnect_all_devices()
    # 启动模拟器
    if config.TARGET_EMULATOR_PATH != "":
        logging.info("启动模拟器")
        subprocess_run(["{}".format(config.TARGET_EMULATOR_PATH)], isasync=True)
        for i in range(3):
            logging.info("等待模拟器启动中...{}".format(i+1))
            sleep(2)
    else:
        logging.info("未配置模拟器路径")
    while 1:
        logging.info("检查连接")
        if check_connect():
            # 连接成功
            # 使用adb打开包名为com.nexon.bluearchive的app
            # 检查这个app是否在运行
            logging.info("连接成功，尝试进入游戏...")
            while not check_app_running("com.nexon.bluearchive"):
                subprocess_run(["{}".format(config.ADB_PATH), 'shell', 'am', 'start', 'com.nexon.bluearchive/.MxUnityPlayerActivity'])
                sleep(3)
            # 运行任务
            logging.info("运行任务")
            my_AllTask.run()
            break
        else:
            port = input("未能连接至模拟器，可能由于请输入模拟器端口号(留空以继续使用配置文件)：")
            if port=="":
                continue
            else:
                try:
                    port = int(port)
                    config.TARGET_PORT = port
                except:
                    logging.error("端口号输入错误")

if __name__ in ["__main__", "__mp_main__"]:
    # 不带GUI运行
    BAAH_main()