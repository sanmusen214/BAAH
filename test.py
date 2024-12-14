import sys
from modules.utils.log_utils import logging
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
from modules.utils import *
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PageName import PageName
from DATA.assets.PopupName import PopupName

from modules.AllTask import *

if __name__=="__main__":
    
    connect_to_device()
    screenshot(output_png=True)
    
    # 测match
    # res1 = match_pattern(cv2.imread(config.userconfigdict['SCREENSHOT_NAME']), button_pic(ButtonName.BUTTON_SHOP_CONTEST_B),  show_result=True, auto_rotate_if_trans=False)

    # 比划点
    screencut_tool()

    # 滑动
    # swipe((100, 467),(100, 192), durationtime=0.5)
