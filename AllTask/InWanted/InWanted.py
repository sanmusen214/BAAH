from typing import override

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

import time
import numpy as np
from .RunWantedFight import RunWantedFight
import config

class InWanted(Task):
    def __init__(self, name="InWanted") -> None:
        super().__init__(name)

    @override
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
    @override
    def on_run(self) -> None:
        # 从主页进入战斗池页面
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=5
        )
        # 进入悬赏通缉页面
        self.run_until(
            lambda: click((741, 424)),
            lambda: Page.is_page(PageName.PAGE_WANTED),
        )
        # 得到今天时间
        today = time.localtime().tm_mday
        # 选择一个地点进入
        target_loc = today%3
        
        points = np.linspace(206, 422, 3)
        
        self.run_until(
            lambda: click((959, points[target_loc])),
            lambda: Page.is_page(PageName.PAGE_WANTED_SUB),
        )
        RunWantedFight(config.WANTED_HIGHEST_LEVEL[target_loc]).run()
        self.back_to_home()

    @override
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)