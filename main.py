import sys
import os
# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

from gui import BAAH_GUI
from BAAH import BAAH_main

if __name__ in ["__main__", "__mp_main__"]:
    # BAAH_main()
    # 带GUI运行
    gui = BAAH_GUI(BAAH_main)
    gui.runGUI()
