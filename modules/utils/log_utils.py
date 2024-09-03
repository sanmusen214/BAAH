import sys
from time import strftime
from modules.configs.MyConfig import config
from modules.utils.I18nstr import EN, CN, JP

import hashlib

# 构建日志类
class MyLogger:
    """
    日志类，包装常用的日志类方法，info, debug, warn, warning, error
    """
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARN = "WARN"
    ERROR = "ERROR"
    
    def __init__(self) -> None:
        self.info_list = []
        self.debug_list = []
        self.warn_list = []
        self.error_list = []
        self.lang = config.softwareconfigdict["LANGUAGE"]
        print("使用语言/Use language: ", self.lang)
        
    def hash_str(self, data):
        """得到字符串的哈希值"""
        return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
    
    def format_msg(self, msg, level):
        """加入时间，错误级别"""
        if isinstance(msg, dict):
            if self.lang in msg:
                msg = msg[self.lang]
            else:
                # 没有对应语言的情况下，使用英文
                # 目前EN = "en_US"，与传入的json的代表英语的key是对应的
                if EN in msg:
                    msg = msg[EN]
        return f"{config.NOWVERSION} - {strftime('%M:%S')} - {level} : {str(msg)}"
    
    def colorful_print(self, msg, level):
        """
        30 黑色，31 红色，32 绿色，33 黄色，34 蓝色，35 紫色，36 青色，37 白色
        
        cmd 用不了
        """
        # if level == self.INFO:
        #     print(f"\033[1;32m{msg}\033[0m")
        # elif level == self.DEBUG:
        #     print(f"\033[1;34m{msg}\033[0m")
        # elif level == self.WARN:
        #     print(f"\033[1;33m{msg}\033[0m")
        # elif level == self.ERROR:
        #     print(f"\033[1;31m{msg}\033[0m")
        # else:
        #     print(msg)
        print(msg)
        # flush
        sys.stdout.flush()
        
    
    def info(self, msg):
        formatted_msg = self.format_msg(msg, self.INFO)
        self.info_list.append(formatted_msg)
        self.colorful_print(formatted_msg, self.INFO)
    
    def debug(self, msg):
        formatted_msg = self.format_msg(msg, self.DEBUG)
        self.debug_list.append(formatted_msg)
        # self.colorful_print(formatted_msg, self.DEBUG)
    
    def warn(self, msg):
        formatted_msg = self.format_msg(msg, self.WARN)
        self.warn_list.append(formatted_msg)
        self.colorful_print(formatted_msg, self.WARN)
    
    def warning(self, msg):
        self.warn(msg)
        
    def error(self, msg):
        formatted_msg = self.format_msg(msg, self.ERROR)
        self.error_list.append(formatted_msg)
        self.colorful_print(formatted_msg, self.ERROR)
    
logging = MyLogger()