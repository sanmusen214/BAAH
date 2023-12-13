 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config

import numpy as np

from modules.utils.GlobalState import raidstate


class RunSpecialFight(Task):
    def __init__(self, levelnum, runtimes, name="RunSpecialFight") -> None:
        super().__init__(name)
        self.levelnum = levelnum
        self.runtimes = runtimes

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EXCHANGE_SUB)
    
     
    def on_run(self) -> None:
        # 找到目标关卡点击
        if self.levelnum <= 5:
            self.scroll_right_up()
            clickind = self.levelnum
            points = np.linspace(162, 670, 6)
        else:
            self.scroll_right_down()
            clickind = self.levelnum-6
            points = np.linspace(151, 650, 6)
        logging.info("点击关卡 {}".format(self.levelnum+1))
        self.run_until(
            lambda: click((1118, points[clickind])),
            lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))
        )
        # 扫荡
        RaidQuest(raidstate.Special, self.runtimes).run()
        # 关闭弹窗，回到底层页面
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            # 复用关卡目录图片
            lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB)
        )

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EXCHANGE_SUB)