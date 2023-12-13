import json
# this module is load before logging, so we just print things
import os
import time

class MyConfigger:
    NOWVERSION="1.0.2"
    # 读取config这个py里面的配置
    def __init__(self, file_path):
        self.file_path = file_path
        # 字典
        self.configdict = self._read_config()
        # 实例属性
        for key in self.configdict:
            self.__dict__[key] = self.configdict[key]

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
    