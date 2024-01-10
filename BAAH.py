import sys
import os

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

import logging
from modules.configs.MyConfig import config
from modules.utils import *
from modules.AllTask.myAllTask import my_AllTask

def BAAH_start_emulator():
    """
    启动模拟器
    """
    if config.userconfigdict["TARGET_EMULATOR_PATH"] and config.userconfigdict["TARGET_EMULATOR_PATH"] != "":
        try:
            # 以列表形式传命令行参数
            subprocess_run(config.userconfigdict['TARGET_EMULATOR_PATH'].split(" "), isasync=True)
        except Exception as e:
            logging.error("启动模拟器失败, 可能是没有以管理员模式运行 或 配置的模拟器路径有误")
    else:
        logging.info("未配置模拟器路径，跳过启动模拟器")

def BAAH_check_adb_connect():
    """
    检查adb连接
    """
    # 检查adb连接
    disconnect_this_device()
    for i in range(1, 10):
        sleep(i)
        if check_connect():
            logging.info("adb连接成功")
            return True
        else:
            logging.info("未检测到设备连接, 重试...")
    raise Exception("adb连接失败, 请检查配置里的adb端口")

def BAAH_open_target_app():
    """
    打开游戏
    """
    if check_app_running(config.userconfigdict['ACTIVITY_PATH']):
        logging.info("检测到游戏已经在运行")
        return True
    for i in range(5):
        logging.info("打开游戏")
        open_app(config.userconfigdict['ACTIVITY_PATH'])
        sleep(3)
        if not check_app_running(config.userconfigdict['ACTIVITY_PATH']):
            logging.error("未检测到游戏打开，请检查区服设置")
        else:
            return True
    raise Exception("未检测到游戏打开，请检查区服设置 以及 如果使用的是MuMu模拟器，请关闭后台保活")

def BAAH_kill_emulator():
    if config.userconfigdict["TARGET_EMULATOR_PATH"] and config.userconfigdict["TARGET_EMULATOR_PATH"] != "" and config.userconfigdict["CLOSE_EMULATOR"]:
        try:
            # 以列表形式传命令行参数
            full_path = config.userconfigdict['TARGET_EMULATOR_PATH']
            # 提取出模拟器的exe名字
            emulator_exe=os.path.basename(full_path).split(".exe")[0]+".exe"
            subprocess_run(["taskkill", "/F", "/IM", emulator_exe], encoding="gbk")
        except Exception as e:
            logging.error("关闭模拟器失败, 可能是没有以管理员模式运行 或 配置的模拟器路径有误")
    else:
        logging.info("未配置模拟器路径，跳过关闭模拟器")
    

def BAAH_main():
    BAAH_start_emulator()
    BAAH_check_adb_connect()
    BAAH_open_target_app()
    # 运行任务
    logging.info("运行任务")
    my_AllTask.run()
    logging.info("所有任务结束")
    BAAH_kill_emulator()
            


if __name__ in ["__main__", "__mp_main__"]:
    # 不带GUI运行
    BAAH_main()