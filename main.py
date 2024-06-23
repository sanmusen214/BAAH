import sys
import os
from time import sleep, strftime

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

def print_BAAH_start():
    print("+"+"BAAH".center(80, "="), "+")
    print("||"+f"Version: {config.softwareconfigdict['NOWVERSION']}".center(80, " ")+"||")
    print("||"+"Bilibili: https://space.bilibili.com/7331920".center(80, " ")+"||")
    print("||"+"Github: https://github.com/sanmusen214/BAAH".center(80, " ")+"||")
    print("||" + "QQ group: 441069156".center(80, " ") + "||")
    print("||"+"".center(80, " ")+"||")
    print("+"+"".center(80, "=")+"+")

def print_BAAH_finish():
    print_BAAH_start()
    print("\n程序运行结束，如有问题请加群(441069156)反馈，在Github上检查下是否有版本更新")
    print("https://github.com/sanmusen214/BAAH")

if __name__ in ["__main__", "__mp_main__"]:
    try:
        # config logging before all imports
        from modules.utils.log_utils import logging
        # 从命令行参数获取要运行的config文件名，并将config实例parse为那个config文件
        from modules.configs.MyConfig import config
        if len(sys.argv) > 1:
            config_name = sys.argv[1]
            logging.info({"zh_CN": f"读取指定的配置文件: {config_name}", "en_US": f"loading config from {config_name}"})
            config.parse_user_config(config_name)
        else:
            config_name = input("启动程序时没有指定配置文件, 请手动输入要运行的配置文件名(包含.json后缀): ")
            logging.info({"zh_CN": f"读取指定的配置文件: {config_name}", "en_US": f"loading config from {config_name}"})
            config.parse_user_config(config_name)

        from BAAH import BAAH_main, my_AllTask, create_notificationer
        
        # 打印BAAH信息
        print_BAAH_start()
        
        # 打印config信息
        logging.info({"zh_CN": f"读取的配置文件: {config_name}", "en_US": f"Read config file: {config_name}"})
        logging.info({"zh_CN": f"模拟器:{config.userconfigdict['TARGET_EMULATOR_PATH']}", "en_US":f"Emulator: {config.userconfigdict['TARGET_EMULATOR_PATH']}"})
        logging.info({"zh_CN": f"端口:{config.userconfigdict['TARGET_PORT']}", "en_US":f"Port: {config.userconfigdict['TARGET_PORT']}"})
        logging.info({"zh_CN": f"区服:{config.userconfigdict['SERVER_TYPE']}", "en_US":f"Server: {config.userconfigdict['SERVER_TYPE']}"})

        # 不带GUI运行
        # config历史列表
        config_history = [config_name]
        while True:
            logging.debug("配置文件历史列表: "+ ",".join(config_history))
            BAAH_main()
            # 判断config里是否有next_config文件
            if config.userconfigdict['NEXT_CONFIG'] and len(config.userconfigdict['NEXT_CONFIG']) > 0:
                # 有的话，更新配置项目
                logging.debug("检测到next_config文件: "+config.userconfigdict['NEXT_CONFIG'])
                if config.userconfigdict['NEXT_CONFIG'] in config_history:
                    raise Exception("检测到循环运行，请避免config死循环嵌套")
                # 将新的config文件加入config_history, 防止死循环
                config_history.append(config.userconfigdict['NEXT_CONFIG'])
                # 清空config实例,读取next_config文件，再次运行BAAH_main()
                config.parse_user_config(config.userconfigdict['NEXT_CONFIG'])
                # 清空my_AllTask实例，通过新的config构造新的my_AllTask
                my_AllTask.parse_task()
            else:
                break
        # 此处所有任务已经完成，可以输出版本信息了
        print_BAAH_finish()
        # 结束运行，如果用户没有勾选自动关闭模拟器与BAAH，等待用户按回车键
        if not config.userconfigdict["CLOSE_EMULATOR_BAAH"]:
            input("Press Enter to exit/回车退出:")
        else:
            logging.info({"zh_CN": "10秒后自动关闭", "en_US":"Auto close in 10 seconds"})
            sleep(10)
    except Exception as e:
        # 打印完整的错误信息
        import traceback
        traceback.print_exc()
        print_BAAH_finish()
        # 发送错误通知邮件
        if config.userconfigdict["ENABLE_MAIL_NOTI"]:
            logging.info({"zh_CN": "发送错误通知邮件", "en_US":"Send error notification email"})
            try:
                # 构造通知对象
                notificationer = create_notificationer()
                # 构造邮件内容
                content = []
                content.append("BAAH任务出现错误")
                content.append("配置文件名称: "+config.nowuserconfigname)
                content.append("游戏区服: "+config.userconfigdict["SERVER_TYPE"])
                content.append("错误信息: "+str(e))
                print(notificationer.send("\n".join(content)))
                logging.info({"zh_CN": "邮件发送结束", "en_US":"The email has been sent"})
            except Exception as eagain:
                logging.error({"zh_CN": "发送邮件失败", "en_US":"Failed to send email"})
                logging.error(eagain)
        input("Error, Enter to exit/错误，回车退出:")
    
    # 运行结束后，删除截图文件
    try:
        # 运行结束后如果截图文件存在，删除截图文件
        if os.path.exists(f"./{config.userconfigdict.get('SCREENSHOT_NAME')}"):
            os.remove(f"./{config.userconfigdict.get('SCREENSHOT_NAME')}")
    except Exception as e:
        logging.error({"zh_CN": "删除截图文件失败", "en_US":"Failed to delete screenshot file"})
        
        

