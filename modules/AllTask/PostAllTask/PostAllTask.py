
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel
from modules.utils.log_utils import logging

class PostAllTask(Task):
    def __init__(self, name="PostAllTask") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return self.back_to_home()
    
    def record_resources(self):
        """
        记录主页中的资源
        """
        # 记录主页中的资源
        power_num = ocr_area((503, 17), (602, 56))[0]
        # print("体力: ", power_num)
        credit_num = ocr_area((688, 19), (832, 59))[0]
        # print("信用点: ", credit_num)
        diamond_num = ocr_area((863, 21), (973, 60))[0]
        # print("钻石: ", diamond_num)
        config.sessiondict["AFTER_BAAH_SOURCES"] = {"power": power_num, "credit": credit_num, "diamond": diamond_num}
     
    def on_run(self) -> None:
        self.record_resources()

     
    def post_condition(self) -> bool:
        return self.back_to_home()