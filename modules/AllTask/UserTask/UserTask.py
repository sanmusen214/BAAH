
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
from modules.AllTask.SubTask.ExecCode import ExecCode

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel, istr, CN, EN, JP
from modules.utils.log_utils import logging

class UserTask(Task):
    def __init__(self, name="UserTask") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return True
    
     
    def on_run(self) -> None:
        content = config.userconfigdict["USER_DEF_TASKS"]
        ExecCode(content).run()

     
    def post_condition(self) -> bool:
        return True