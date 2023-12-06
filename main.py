import sys
import os

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

import logging
import config
from gui import BAAH_GUI
from modules.utils import *
from modules.AllTask.myAllTask import my_AllTask

def main(handler=None):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')
    if handler:
        logging.getLogger().addHandler(handler)
    disconnect_all_devices()
    # 启动模拟器
    logging.info("启动模拟器，等待十秒")
    subprocess_run(["{}".format(config.TARGET_EMULATOR_PATH),  '--instance', 'Pie64', '--cmd', 'launchApp', '--package', 'com.nexon.bluearchive'], isasync=True)
    sleep(10)
    logging.info("检查连接")
    if check_connect():
        my_AllTask.run()

def main_GUI():
    BAAH_GUI(main)

if __name__ == "__main__":
    main()