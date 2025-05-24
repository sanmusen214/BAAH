import time
import os
import zipfile
import shutil

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils.log_utils import logging

from modules.utils import jsonread, htmlread, click, swipe, match, page_pic, button_pic, popup_pic, sleep, check_app_running, open_app, config, screenshot, EmulatorBlockError, istr, CN, EN, match_pixel, aria2_download, install_apk, install_dir

from .EnterGame import EnterGame

# =====

class Update(Task):
    def __init__(self, name="Update", pre_times = 3, post_times = 10) -> None:
        super().__init__(name, pre_times, post_times)
        
    def pre_condition(self) -> bool:
        if(self.post_condition()):
            return False
        return True
    
    def on_run(self):
        if 'html://' in config.userconfigdict["UPDATE_API_URL"]:
            url = htmlread(config.userconfigdict["UPDATE_API_URL"])
            xapk = False
        elif 'json://' in config.userconfigdict["UPDATE_API_URL"]:
            url = jsonread(config.userconfigdict["UPDATE_API_URL"])
            xapk = False
        else:
            url = config.userconfigdict["UPDATE_API_URL"]
            xapk = True
        
        self.task_start_time = time.time()
        logging.info({
             "zh_CN": "检测到有APP更新，开始下载更新",
             "en_US": "Detected that there is an APP update, start downloading the update"
        })
        
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        
        if xapk:
            aria2_download(url, "tmp/update.xapk")
            with zipfile.ZipFile("tmp/update.xapk", 'r') as zip_ref:
                os.mkdir("tmp/unzip")
                zip_ref.extractall("tmp/unzip")
        else:
            aria2_download(url, "tmp/update.apk")
        
        logging.info({
            "zh_CN":"更新下载完成，开始安装",
            "en_US": "Update download completed, start installation"
        })
        
        if xapk:
            install_dir("tmp/unzip")
        else:
            install_apk("tmp/update.apk")
        
        logging.info({
            "zh_CN":"更新完成，清理目录",
            "en_US": "Update completed, clean up directory"
            })
        shutil.rmtree("tmp")
        EnterGame().run()