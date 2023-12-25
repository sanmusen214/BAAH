import sys
import os

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

if __name__ in ["__main__", "__mp_main__"]:
    try:
        # config logging before all imports
        import logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8')
        # 从命令行参数获取要运行的config文件名，并将config实例parse为那个config文件
        configname = "config.json"
        from modules.utils.MyConfig import config
        logging.info("读取默认config文件: "+configname)
        if len(sys.argv) > 1:
            configname = sys.argv[1]
            config.parse_config(configname)
            logging.info("重新读取指定的config文件: "+configname)
        logging.info(f"模拟器:{config.configdict['TARGET_EMULATOR_PATH']}")
        logging.info(f"端口:{config.configdict['TARGET_PORT']}")

        import base64
        import traceback
        from BAAH import BAAH_main
        from assets.Aris import aris_base64
        from modules.AllTask.myAllTask import my_AllTask
        
        # 打印BAAH信息
        print("+"+"BAAH".center(80, "="), "+")
        print("||"+f"Version: {config.NOWVERSION}".center(80, " ")+"||")
        print("||"+"Bilibili: https://space.bilibili.com/7331920".center(80, " ")+"||")
        print("||"+"Github: https://github.com/sanmusen214/BAAH".center(80, " ")+"||")
        print("||" + "QQ群: 441069156".center(80, " ") + "||")
        print("||"+"".center(80, " ")+"||")
        print("+"+"".center(80, "=")+"+")
        # base64解码
        print(base64.b64decode(aris_base64).decode("utf-8"))
    

        # 不带GUI运行
        # config历史列表
        config_history = [configname]
        while True:
            logging.debug("config历史列表: "+ ",".join(config_history))
            BAAH_main()
            # 判断config里是否有next_config文件
            if hasattr(config, 'NEXT_CONFIG') and len(config.NEXT_CONFIG) > 0:
                # 有的话，更新配置项目
                logging.debug("检测到next_config文件: "+config.NEXT_CONFIG)
                if config.NEXT_CONFIG in config_history:
                    raise Exception("检测到循环运行，请避免config死循环嵌套")
                # 将新的config文件加入config_history, 防止死循环
                config_history.append(config.NEXT_CONFIG)
                # 清空config实例,读取next_config文件，再次运行BAAH_main()
                config.parse_config(config.NEXT_CONFIG)
                # 清空my_AllTask实例，通过新的config构造新的my_AllTask
                my_AllTask.parse_task()

            else:
                break
    except Exception as e:
        # 打印完整的错误信息
        traceback.print_exc()
    try:
        # 如果截图文件存在，删除截图文件
        if os.path.exists(f"./{config.SCREENSHOT_NAME}"):
            os.remove(f"./{config.SCREENSHOT_NAME}")
    except:
        pass
    print("程序运行结束，如有问题请加群(441069156)反馈，在Github上检查下是否有版本更新")
    print("https://github.com/sanmusen214/BAAH")
    input("按回车键退出BAAH:")
