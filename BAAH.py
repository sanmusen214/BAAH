import sys
import os

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

import logging
from modules.utils.MyConfig import config
from modules.utils import *
from modules.AllTask.myAllTask import my_AllTask


def BAAH_main():
    # 启动模拟器
    if hasattr(config, "TARGET_EMULATOR_PATH") and config.TARGET_EMULATOR_PATH != "":
        logging.info("启动模拟器")
        try:
            subprocess_run(["{}".format(config.TARGET_EMULATOR_PATH)], isasync=True)
            for i in range(3):
                logging.info("等待{}...".format(i+1))
                sleep(2)
        except Exception as e:
            logging.error("启动模拟器失败, 可能是没有以管理员模式运行 或 配置的模拟器路径有误")
            logging.warn("检查是否能够建立与模拟器的连接...")
    else:
        logging.info("未配置模拟器路径")
    # 检查adb连接
    disconnect_all_devices()
    max_try = 5
    for i in range(max_try):
        logging.info(f"检查连接{i+1}/{max_try}...")
        if check_connect():
            # 连接成功
            # 使用adb打开包名为com.nexon.bluearchive的app
            # 检查这个app是否在运行
            for i in range(5):
                # 打开游戏
                open_app(config.ACTIVITY_PATH)
                sleep(3)
                # TODO: 不在视野内在后台也会被识别？？？
                if not check_app_running(config.ACTIVITY_PATH):
                    if i>=2:
                        yorn = input("连接后多次打开失败，是否重启adb服务？(y/n):")
                        if yorn == "y" or yorn == "Y":
                            logging.warn("重启adb服务")
                            kill_adb_server()
                            raise Exception("由于重启了adb服务，请重新运行脚本")
                    logging.info("尝试打开游戏...")
                    open_app(config.ACTIVITY_PATH)
                    sleep(3)
                else:
                    logging.info("打开游戏")
                    break
            # 运行任务
            logging.info("运行任务")
            my_AllTask.run()
            logging.info("所有任务结束")
            break
        else:
            if i == 2:
                yorn = input("多次连接失败，是否重启adb服务？(y/n):")
                if yorn == "y" or yorn == "Y":
                    logging.warn("重启adb服务")
                    kill_adb_server()
                    continue
            if i == max_try-1:
                logging.error("达到最大尝试次数，连接失败")
                break
            port = input("未能连接至模拟器，请输入模拟器端口号并修改config.json(留空以继续使用配置文件)：")
            if port=="":
                continue
            else:
                try:
                    port = int(port)
                    config.TARGET_PORT = port
                except:
                    logging.error("端口号输入错误")


if __name__ in ["__main__", "__mp_main__"]:
    # 不带GUI运行
    BAAH_main()