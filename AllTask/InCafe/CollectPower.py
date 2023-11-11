 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

import logging

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class CollectPower(Task):
    def __init__(self, name="CollectPower", pre_times = 3, post_times = 3) -> None:
        super().__init__(name, pre_times, post_times)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE) and match(button_pic(ButtonName.BUTTON_CAFE_CAN_COLLECT))
    
     
    def on_run(self) -> None:
        # 清除学生入场弹窗
        click(Page.MAGICPOINT)
        # 重复点收集直到出现弹窗
        self.run_until(
            lambda :click((1156, 648)), 
            lambda: match(popup_pic(PopupName.POPUP_CAFE_INFO)), 
            times = 3
        )
        logging.info("成功点击右下角收集")
        # 重复点领取直到领取按钮变灰
        self.run_until(
            lambda :click((640, 520)), 
            lambda: Page.is_page(PageName.PAGE_CAFE) and match(button_pic(ButtonName.BUTTON_COLLECT_GRAY), returnpos=True)[2] > match(button_pic(ButtonName.BUTTON_COLLECT), returnpos=True)[2],
            times = 5)
        logging.info("成功点击领取")
        # 点魔法点去弹窗
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE) and not match(popup_pic(PopupName.POPUP_CAFE_INFO))
        )

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)