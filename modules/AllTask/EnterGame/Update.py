import json
import re
import time
import os
import zipfile
import shutil

import requests

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils.log_utils import logging

from modules.utils import subprocess_run, click, swipe, match, page_pic, button_pic, popup_pic, sleep, check_app_running, open_app, config, screenshot, EmulatorBlockError, istr, CN, EN, match_pixel, aria2_download, install_apk, install_dir

from .EnterGame import EnterGame

# =====

class Update(Task):
    def __init__(self, name="Update", pre_times = 3, post_times = 10) -> None:
        super().__init__(name, pre_times, post_times)
        
    def pre_condition(self) -> bool:
        if(self.post_condition()):
            return False
        return True
    
    def htmlread(url):
        if "html://" not in url:
            raise Exception("url must start with html://")
        html = requests.get(url.replace("html://", "")).text
        apk_links = re.findall(r'https://pkg.bluearchive-cn.com[^\s\'"]+?\/com.RoamingStar.BlueArchive.apk', html)
        return apk_links[0]
    
    def jsonread(url):
        """
        从url中获取json数据
        tips,原本想让定位也写在url中的，但是不会写。 ——By BlockHaity
        """
        if "json://" not in url:
            return Exception("url must start with json://")
        url = url.replace("json://", "")
        jsondata = json.loads(requests.get(url).text)
        return jsondata['data']['android_download_link']
    
    
    def aria2_download(url, filename):
        aria2c_try = 0
        while aria2c_try < config.userconfigdict("ARIA2_MAX_TRIES"):
            logging.info({"zh_CN": f"开始下载文件: {url}, 线程数: {config.userconfigdict("ARIA2_THREADS")}, 尝试次数: {aria2c_try + 1}",
                                   "en_US": f"Start downloading file: {url}, thread count: {config.userconfigdict("ARIA2_THREADS")}, try count: {aria2c_try + 1}"})
            run = subprocess_run([config.userconfigdict("ARIA2_PATH"), "-x", config.userconfigdict("ARIA2_THREADS"), url, "-o", filename])
            if run.returncode != 0:
                logging.error({"zh_CN": f"下载文件失败: {url}, 错误信息: {run.stderr.decode('utf-8')}",
                                         "en_US": f"Download file failed: {url}, error message: {run.stderr.decode('utf-8')}"})
                aria2c_try += 1
                time.sleep(config.userconfigdict("ARIA2_FAILURED_WAIT_TIME"))
            else:
                logging.info({"zh_CN": f"下载文件成功",
                                       "en_US": f"Download file success"})
                break
        else:
            raise Exception(istr({"zh_CN": f"下载文件失败: {url}, 尝试次数: {aria2c_try + 1} 次, 超出最大尝试次数",
                                 "en_US": f"Download file failed: {url}, try count: {aria2c_try + 1}, exceed max try count"
            }))
            
    def on_run(self):
        if 'html://' in config.userconfigdict["UPDATE_API_URL"]:
            url = Update.htmlread(config.userconfigdict["UPDATE_API_URL"])
            xapk = False
        elif 'json://' in config.userconfigdict["UPDATE_API_URL"]:
            url = Update.jsonread(config.userconfigdict["UPDATE_API_URL"])
            xapk = False
        else:
            url = config.userconfigdict["UPDATE_API_URL"]
            xapk = True
        
        self.task_start_time = time.time()
        logging.info({
             "zh_CN": "检测到有APP更新，开始下载更新",
             "en_US": "Detected that there is an APP update, start downloading the update"
        })
        
        if not os.path.exists("DATA/tmp"):
            os.mkdir("DATA/tmp")
        
        if xapk:
            aria2_download(url, "DATA/tmp/update.xapk")
            with zipfile.ZipFile("DATA/tmp/update.xapk", 'r') as zip_ref:
                os.mkdir("DATA/tmp/unzip")
                zip_ref.extractall("DATA/tmp/unzip")
        else:
            aria2_download(url, "DATA/tmp/update.apk")
        
        logging.info({
            "zh_CN":"更新下载完成，开始安装",
            "en_US": "Update download completed, start installation"
        })
        
        if xapk:
            install_dir("DATA/tmp/unzip")
        else:
            install_apk("DATA/tmp/update.apk")
        
        logging.info({
            "zh_CN":"更新完成，清理目录",
            "en_US": "Update completed, clean up directory"
            })
        shutil.rmtree("DATA/tmp")
        EnterGame().run()