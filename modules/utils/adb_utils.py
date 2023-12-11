import subprocess
from modules.utils.MyConfig import config
import logging
from modules.utils.subprocess_helper import subprocess_run
import time
import numpy as np
import cv2

def disconnect_all_devices():
    """Disconnect all devices."""
    subprocess_run([config.ADB_PATH, "disconnect"])
    
def kill_adb_server():
    """Kill the adb server."""
    subprocess_run([config.ADB_PATH, "kill-server"])

def connect_to_device():
    """Connect to a device with the given device port."""
    subprocess_run([config.ADB_PATH, "connect", "127.0.0.1:{}".format(config.TARGET_PORT)])
    
def click_on_screen(x, y):
    """Click on the given coordinates."""
    subprocess_run([config.ADB_PATH, "shell", "input", "tap", str(x), str(y)])

def swipe_on_screen(x1, y1, x2, y2, ms):
    """Swipe from the given coordinates to the other given coordinates."""
    subprocess_run([config.ADB_PATH, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(int(ms))])

def convert_img(path):
    with open(path, "rb") as f:
        bys = f.read()
        bys_ = bys.replace(b"\r\n",b"\n")  # 二进制流中的"\r\n" 替换为"\n"
    with open(path, "wb") as f:
        f.write(bys_)

def screen_shot_to_global():
    """Take a screenshot and save it to the GlobalState."""
    # 方法一，重定向输出到文件
    
    filename = config.SCREENSHOT_NAME
    with open("./{}".format(filename),"wb") as out:
       subprocess_run([config.ADB_PATH, "shell", "screencap", "-p"], stdout=out)
    #adb 命令有时直接截图保存到电脑出错的解决办法-加下面一段即可
    convert_img("./{}".format(filename))
    
    # 方法二，使用cv2提取PIPE管道中的数据
    
    # # 使用subprocess的Popen调用adb shell命令，并将结果保存到PIPE管道中
    # process = subprocess.run([config.ADB_PATH, "shell", "screencap", "-p"], stdout=subprocess.PIPE)
    # # 读取管道中的数据
    # screenshot = process.stdout
    # # 将读取的字节流数据的回车换行替换成'\n'
    # binary_screenshot = screenshot.replace(b'\r\n', b'\n')
    # # 使用numpy和imdecode将二进制数据转换成cv2的mat图片格式
    # img_screenshot = cv2.imdecode(np.frombuffer(binary_screenshot, np.uint8), cv2.IMREAD_COLOR)
    # cv2.imwrite("./{}".format(config.SCREENSHOT_NAME), img_screenshot)
    
def check_app_running(app_name:str) -> bool:
    """
    检查app是否在运行
    """
    # 使用adb获取当前运行的app
    output = subprocess_run([config.ADB_PATH, 'shell', 'dumpsys', 'activity', 'activities']).stdout
    if app_name in output:
        return True
    else:
        return False
    
def open_app(app_name:str, activity_name:str):
    """
    使用adb打开app
    """
    subprocess_run(["{}".format(config.ADB_PATH), 'shell', 'am', 'start', f'{app_name}/.{activity_name}'])