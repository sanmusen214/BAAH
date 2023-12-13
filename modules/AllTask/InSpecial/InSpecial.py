 
import logging
import time

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InSpecial.RunSpecialFight import RunSpecialFight
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config

import numpy as np

class InSpecial(Task):
    def __init__(self, name="InSpecial") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        if not config.SPECIAL_HIGHTEST_LEVEL or len(config.SPECIAL_HIGHTEST_LEVEL)==0:
            logging.warn("未配置特殊关卡")
            return False
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        # 得到今天是几号
        today = time.localtime().tm_mday
        # 选择一个location的下标
        target_loc = today%len(config.SPECIAL_HIGHTEST_LEVEL)
        target_info = config.SPECIAL_HIGHTEST_LEVEL[target_loc]
        # 序号转下标
        target_info[0] -= 1
        target_info[1] -= 1
        # 从主页进入战斗池页面
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入特殊任务页面
        self.run_until(
            lambda: click((721, 507)),
            lambda: Page.is_page(PageName.PAGE_SPECIAL),
        )
        # 可点击的一列点
        points = np.linspace(213, 315, 2)
        # 点击location
        self.run_until(
            lambda: click((959, points[target_info[0]])),
            # 重复使用关卡目录这个pattern
            lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB),
        )
        # 扫荡对应的level
        RunSpecialFight(levelnum = target_info[1], runtimes = target_info[2]).run()
        # 回到主页
        self.back_to_home()


    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)