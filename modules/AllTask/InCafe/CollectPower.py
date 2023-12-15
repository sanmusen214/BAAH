 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

import logging

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class CollectPower(Task):
    def __init__(self, name="CollectPower", pre_times = 3, post_times = 3) -> None:
        super().__init__(name, pre_times, post_times)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)
    
     
    def on_run(self) -> None:
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE),
        )
        sleep(2)
        if match(button_pic(ButtonName.BUTTON_CAFE_CANNOT_COLLECT)):
            logging.info("咖啡馆没有可领取的物品")
            return
        
        # 重复点收集直到出现弹窗
        self.run_until(
            lambda :click((1156, 648)), 
            lambda: match(popup_pic(PopupName.POPUP_CAFE_INFO)), 
            times = 3
        )
        logging.info("成功点击右下角收集")
        # 重复点领取直到领取按钮变灰，这之间其实也关闭了领取成功的弹窗
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_COLLECT)), 
            lambda: match(button_pic(ButtonName.BUTTON_COLLECT_GRAY)),
            times = 5)
        logging.info("成功点击领取")
        # 点魔法点去收益情况弹窗
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE) and not match(popup_pic(PopupName.POPUP_CAFE_INFO))
        )

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)