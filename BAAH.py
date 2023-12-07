import sys
import os

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

import logging
import config
from modules.utils import *
from modules.AllTask.myAllTask import my_AllTask

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')

def BAAH_main():
    disconnect_all_devices()
    # 启动模拟器
    logging.info("启动模拟器")
    subprocess_run(["{}".format(config.TARGET_EMULATOR_PATH),  '--instance', 'Pie64', '--cmd', 'launchApp', '--package', 'com.nexon.bluearchive'], isasync=True)
    sleep(3)
    for i in range(3):
        logging.info("检查连接")
        if check_connect():
            # 连接成功，运行任务
            my_AllTask.run()
            break
        else:
            port = input("请输入模拟器端口号(留空以继续使用配置文件)：")
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