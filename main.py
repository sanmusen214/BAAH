import sys
import os
from time import sleep

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

def print_BAAH_start():
    print("+"+"BAAH".center(80, "="), "+")
    print("||"+f"Version: {config.softwareconfigdict['NOWVERSION']}".center(80, " ")+"||")
    print("||"+"Bilibili: https://space.bilibili.com/7331920".center(80, " ")+"||")
    print("||"+"Github: https://github.com/sanmusen214/BAAH".center(80, " ")+"||")
    print("||" + "QQ群: 441069156".center(80, " ") + "||")
    print("||"+"".center(80, " ")+"||")
    print("+"+"".center(80, "=")+"+")

def print_BAAH_finish():
    print("\n程序运行结束，如有问题请加群(441069156)反馈，在Github上检查下是否有版本更新")
    print("https://github.com/sanmusen214/BAAH")

if __name__ in ["__main__", "__mp_main__"]:
    try:
        # config logging before all imports
        import logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')
        # 从命令行参数获取要运行的config文件名，并将config实例parse为那个config文件
        from modules.configs.MyConfig import config
        if len(sys.argv) > 1:
            configname = sys.argv[1]
            logging.info("读取指定的config文件: "+configname)
            config.parse_user_config(configname)
        else:
            configname = "config.json"
            logging.info("读取默认config文件: "+configname)
            config.parse_user_config(configname)
        
        
        # 打印config信息
        logging.info(f"模拟器:{config.userconfigdict['TARGET_EMULATOR_PATH']}")
        logging.info(f"端口:{config.userconfigdict['TARGET_PORT']}")
        logging.info(f"区服:{config.userconfigdict['SERVER_TYPE']}")

        from BAAH import BAAH_main, my_AllTask
        
        # 打印BAAH信息
        print_BAAH_start()

        # 不带GUI运行
        # config历史列表
        config_history = [configname]
        while True:
            logging.debug("config历史列表: "+ ",".join(config_history))
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
        # 整体运行结束
        print_BAAH_finish()
        print("10秒后自动退出BAAH")
        sleep(10)
    except Exception as e:
        # 打印完整的错误信息
        import traceback
        traceback.print_exc()
        print_BAAH_finish()
        input("按回车键继续:")
    
    # 运行结束后，删除截图文件
    try:
        # 运行结束后如果截图文件存在，删除截图文件
        if os.path.exists(f"./{config.userconfigdict.get('SCREENSHOT_NAME')}"):
            os.remove(f"./{config.userconfigdict.get('SCREENSHOT_NAME')}")
    except Exception as e:
        logging.error("删除截图文件失败")

