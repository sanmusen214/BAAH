import multiprocessing
import time
from nicegui import ui
import logging
from modules.utils.MyConfig import config

# 创建一个自定义的 logging.Handler
class GUISupport(logging.Handler):
    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox
        # 定义formatter
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    def emit(self, record):
        msg = self.format(record)
        self.textbox.print(msg)

class BAAH_GUI:
    def __init__(self, mainfunc) -> None:
        self.runtask = None
        self.title = {"text":"Blue Archive Auto Helper"}
        self.mainfunc = mainfunc

    def run_or_stop(self):
        # 运行main
        if not self.runtask or not self.runtask.is_alive():
            self.runtask = multiprocessing.Process(target=self.mainfunc, daemon=True)
            self.runtask.start()
            ui.notify("开始运行")
            self.title["text"] = "Blue Archive Auto Helper (运行中)"
        # 停止main
        elif self.runtask and self.runtask.is_alive():
            ui.notify("停止运行")
            self.runtask.terminate()
            self.title["text"] = "Blue Archive Auto Helper (停止)"

    def runGUI(self):
        # 创建一个按钮
        ui.label("Blue Archive Auto Helper").bind_text(self.title)
        ui.button("开始/停止", on_click=self.run_or_stop)
        # ui.button("获取子进程信息", on_click=self.get_sub_msg)
        ui.run(reload=False, native=True, title="Blue Archive Auto Helper")
        # ui关闭后，停止main
        # if self.runtask and self.runtask.is_alive():
        #     self.runtask.terminate()
