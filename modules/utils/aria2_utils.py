from modules.configs.MyConfig import config
from modules.utils.log_utils import logging, istr, CN, EN
from modules.utils.subprocess_helper import subprocess_run
import time
        
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