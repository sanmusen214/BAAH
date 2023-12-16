 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
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
        ScrollSelect(self.levelnum, 132, 236, 684, 1119, lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))).run()
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