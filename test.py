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


from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

if __name__=="__main__":
    
    connect_to_device()
    screenshot()
    
    # 测match
    # res1 = match_pattern(config.userconfigdict['SCREENSHOT_NAME'], button_pic(ButtonName.BUTTON_SHOP_CONTEST_B),  show_result=True, auto_rotate_if_trans=False)

    # 比划点
    screencut_tool()

    # 滑动
    # swipe((100, 467),(100, 192), durationtime=0.5)
