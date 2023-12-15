import json
import logging
# this module is load before logging, so we just print things
import os
import time

class MyConfigger:
    """
    维护一个config字典，同时将config.json的配置项作为实例属性
    """
    NOWVERSION="1.0.3"
    # 读取config这个py里面的配置
    def __init__(self, file_path):
        self.file_path = file_path
        # 字典
        self.configdict = self._read_config()
        # 实例属性
        for key in self.configdict:
            self.__dict__[key] = self.configdict[key]
        # 检查缺失的配置
        if "ACTIVITY_PATH" not in self.configdict:
            #TODO: 启动游戏这个环节改成TASK
            self.__dict__['ACTIVITY_PATH'] = "com.nexon.bluearchive/.MxUnityPlayerActivity"
            self.configdict['ACTIVITY_PATH'] = "com.nexon.bluearchive/.MxUnityPlayerActivity"
            logging.warn("缺少配置项：ACTIVITY_PATH，已自动设置为默认值(国际服）：{}".format(self.ACTIVITY_PATH))

    def _read_config(self):
        try:
            with open(self.file_path, 'r', encoding="utf8") as f:
                dictconfig = json.load(f)
                print("读取config.json文件成功, 读取了{}个配置".format(len(dictconfig)))
                return dictconfig
        except Exception as e:
            print(e)
            print('读取config.json文件时发生错误，请检查config.json文件',str(e))
            input("按回车键退出程序")
            # 程序退出
            os._exit(0)
    
    def update_config(self, key, value):
        self.key=value
        self.configdict[key] = value
        self.save_config()
        
    def save_config(self):
        with open(self.file_path, 'w', encoding="utf8") as f:
            json.dump(self.configdict, f, indent=4, ensure_ascii=False)


current_dir = os.getcwd()
config=MyConfigger(os.path.join(current_dir, 'config.json'))
