import subprocess
from modules.configs.MyConfig import config
from modules.utils.log_utils import logging, istr, CN, EN
import time

class Aria2Utils:
    def __init__(self):
        self.aria2c_path = config.userconfigdict("ARIA2_PATH")
        self.aria2c_theards = config.userconfigdict("ARIA2_THREADS")
        self.aria2c_max_tries = config.userconfigdict("ARIA2_MAX_TRIES")
        self.aria2_failured_wait_time = config.userconfigdict("ARIA2_FAILURED_WAIT_TIME")
        
        def download(url):
            aria2c_try = 0
            while aria2c_try < self.aria2c_max_tries:
                logging.info({"zh_CN": f"开始下载文件: {url}, 线程数: {self.aria2c_theards}, 尝试次数: {aria2c_try + 1}",
                                       "en_US": f"Start downloading file: {url}, thread count: {self.aria2c_theards}, try count: {aria2c_try + 1}"})
                run = subprocess.run([self.aria2c_path, "-x", self.aria2c_theards, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if run.returncode != 0:
                    logging.error({"zh_CN": f"下载文件失败: {url}, 错误信息: {run.stderr.decode('utf-8')}",
                                           "en_US": f"Download file failed: {url}, error message: {run.stderr.decode('utf-8')}"})
                    aria2c_try += 1
                    time.sleep(self.aria2_failured_wait_time)
                else:
                    logging.info({"zh_CN": f"下载文件成功",
                                           "en_US": f"Download file success"})
            