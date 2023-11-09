from typing import override

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

    @override
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE) and match(button_pic(ButtonName.BUTTON_CAFE_CAN_COLLECT))
    
    @override
    def on_run(self) -> None:
        # 重复点收集直到出现弹窗
        self.run_until(lambda :click((1156, 648)), lambda: match(popup_pic(PopupName.POPUP_CAFE_INFO)), 3)
        logging.info("成功点击右下角收集")
        # 重复点收集直到收集按钮消失
        self.run_until(lambda :click(button_pic(ButtonName.BUTTON_COLLECT)), lambda: not match(button_pic(ButtonName.BUTTON_COLLECT)), 3)
        # 点两下魔法点去弹窗
        click(Page.MAGICPOINT)
        click(Page.MAGICPOINT)

    @override
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)