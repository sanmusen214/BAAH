import multiprocessing
import PySimpleGUI as sg
import logging

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

def runGUI(mainfunc):
    layout = [
            [sg.Button("运行", key="run", size=(20,5)), sg.Button("停止", key="stop", disabled=True, size=(20,5))],
            ]
    window = sg.Window('BAAH', layout, finalize=True, size=(720, 460))
    # 
    runtask = None
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            # 如果子进程还在运行，终止子进程
            if runtask and runtask.is_alive():
                runtask.terminate()
            window.close()
            break
        elif event == "run":
            # 运行main
            if not runtask or not runtask.is_alive():
                runtask = multiprocessing.Process(target=mainfunc)
                logging.info("开始运行")
                runtask.start()
                window["run"].update(disabled=True)
                window["stop"].update(disabled=False)
        elif event == "stop":
            if runtask and runtask.is_alive():
                runtask.terminate()
                logging.info("已停止")
                window["run"].update(disabled=False)
                window["stop"].update(disabled=True)
                