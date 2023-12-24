 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config

class SkipStory(Task):
    """
    前置条件为存在右上角Menu按钮
    
    点击跳过那个弹窗里的蓝色按钮并识别不到蓝色确认按钮后结束
    """
    def __init__(self, name="SkipStory") -> None:
        super().__init__(name, pre_times=5)

     
    def pre_condition(self) -> bool:
        return match(button_pic(ButtonName.BUTTON_STORY_MENU))
    
     
    def on_run(self) -> None:
        # 记住MENU的位置
        menupos = match(button_pic(ButtonName.BUTTON_STORY_MENU), returnpos=True)[1]
        # 按MENU直到MENU变深色匹配不出来
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_STORY_MENU), sleeptime=1.5),
            lambda: not match(button_pic(ButtonName.BUTTON_STORY_MENU))
        )
        # 点击跳过直到看到蓝色确认按钮
        self.run_until(
            lambda: click((menupos[0], menupos[1] + 80), sleeptime=1.5),
            lambda: match(button_pic(ButtonName.BUTTON_CONFIRMB))
        )
        # 点击蓝色确认按钮，直到看不到蓝色确认按钮
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB), sleeptime=1.5),
            lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMB))
        )

     
    def post_condition(self) -> bool:
        return not match(button_pic(ButtonName.BUTTON_CONFIRMB))