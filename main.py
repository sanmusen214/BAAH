import sys
import os

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

import logging
import config
from gui import runGUI
from modules.utils import *
from modules.AllTask.myAllTask import my_AllTask

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')

def main():
    disconnect_all_devices()
    # 启动模拟器
    logging.info("启动模拟器")
    subprocess_run(["{}".format(config.TARGET_EMULATOR_PATH),  '--instance', 'Pie64', '--cmd', 'launchApp', '--package', 'com.nexon.bluearchive'], isasync=True)
    sleep(3)
    logging.info("检查连接")
    if check_connect():
        my_AllTask.run()

if __name__ == "__main__":
    runGUI(main)
