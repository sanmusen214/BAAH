import json
import logging
import os
import time

class MyConfigger:
    """
    维护一个config字典，同时将config.json的配置项作为实例属性
    
    file_path: config.json的路径
    """
    NOWVERSION="1.1.4"
    # 读取config这个py里面的配置
    def __init__(self, file_path=""):
        if file_path != "":
            self.parse_config(file_path)

    def parse_config(self, file_path):
        """
        读取config文件并解析
        """
        # 绝对路径
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, file_path)
        self.file_path = file_path
        # 在更新字典前，将以前字典里的键从实例的属性里删除
        # 检测self是否有configdict这个属性
        if not hasattr(self, 'configdict'):
            self.configdict = {}
        for key in self.configdict:
            del self.__dict__[key]
        # 字典
        self.configdict = self._read_config_file(file_path)
        # 添加到实例属性
        for key in self.configdict:
            self.__dict__[key] = self.configdict[key]
        logging.debug("config字典内容: "+ ",".join([k for k in self.configdict]))
        logging.debug("config实例属性: "+ ",".join([k for k in self.__dict__]))
        # 检查缺失的配置
        if "ACTIVITY_PATH" not in self.configdict:
            #TODO: 启动游戏这个环节改成TASK
            self.__dict__['ACTIVITY_PATH'] = "com.nexon.bluearchive/.MxUnityPlayerActivity"
            self.configdict['ACTIVITY_PATH'] = "com.nexon.bluearchive/.MxUnityPlayerActivity"
            logging.warn("缺少配置项：ACTIVITY_PATH，已自动设置为默认值(国际服）")

    def _read_config_file(self, file_path):
        try:
            with open(file_path, 'r', encoding="utf8") as f:
                dictconfig = json.load(f)
                print("读取{}文件成功, 读取了{}个配置".format(file_path, len(dictconfig)))
                return dictconfig
        except Exception as e:
            raise Exception(f'读取{file_path}文件时发生错误，请检查{file_path}文件: {str(e)}')
    
    def update_config(self, key, value):
        self.__dict__[key] = value
        self.configdict[key] = value

    def save_config(self, file_path):
        with open(file_path, 'w', encoding="utf8") as f:
            json.dump(self.configdict, f, indent=4, ensure_ascii=False)



config=MyConfigger('config.json')
