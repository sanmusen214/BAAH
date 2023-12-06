import threading
import PySimpleGUI as sg
import logging

# 创建一个自定义的 logging.Handler
class GUISupport(logging.Handler):
    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.print(msg)

class BAAH_GUI():
    def __init__(self, mainfunc):
        layout = [
                [sg.Multiline(size=(80, 20), key='-ML-'+sg.WRITE_ONLY_KEY, autoscroll=True)],
                [sg.Button("运行", key="run")]
                ]
        window = sg.Window('My window with logging', layout, finalize=True)
        textbox = window['-ML-'+sg.WRITE_ONLY_KEY]
        self.textbox = textbox
        handler = GUISupport(textbox)
        # 
        runtask = None
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                window.close()
                break
            elif event == "run":
                if not runtask or not runtask.is_alive():
                    # 运行main，将handler传入
                    runtask = threading.Thread(target=mainfunc, kwargs={"handler": handler})
                    runtask.start()