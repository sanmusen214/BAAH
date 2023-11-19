 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area_0
import logging
import time
import numpy as np

import config
from .RunExchangeFight import RunExchangeFight

class InExchange(Task):
    def __init__(self, name="InExchange") -> None:
        super().__init__(name)
        

     
    def pre_condition(self) -> bool:
        if len(config.EXCHANGE_HIGHEST_LEVEL) == 0:
            logging.warn("没有配置学院交流会的level")
            return False
        return Page.is_page(PageName.PAGE_HOME)
    
     
    def on_run(self) -> None:
        # 得到今天是几号
        today = time.localtime().tm_mday
        # 选择一个location的下标
        target_loc = today%len(config.EXCHANGE_HIGHEST_LEVEL)
        target_info = config.EXCHANGE_HIGHEST_LEVEL[target_loc]
        # 序号转下标
        target_info[0] -= 1
        target_info[1] -= 1
        # 从主页进入战斗池页面
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入学院交流会页面
        self.run_until(
            lambda: click((712, 592)),
            lambda: Page.is_page(PageName.PAGE_EXCHANGE),
        )
        # check whether there is a ticket
        if ocr_area_0((72, 85), (200, 114)):
            logging.warn("没有学院交流会券")
        else:
            # 可点击的一列点
            points = np.linspace(208, 421, 3)
            # 点击location
            self.run_until(
                lambda: click((963, points[target_info[0]])),
                lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB),
            )
            # 扫荡对应的level
            RunExchangeFight(levelnum = target_info[1], runtimes = target_info[2]).run()
        self.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)