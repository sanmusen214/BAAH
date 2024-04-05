 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area

import numpy as np
from modules.utils.log_utils import logging


class RunExchangeFight(Task):
    def __init__(self, levelnum, runtimes, name="RunExchangeFight") -> None:
        """
        after enter the location, start to raid
        
        levelnum start from 0
        """
        super().__init__(name)
        self.levelnum = levelnum
        self.runtimes = runtimes

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EXCHANGE_SUB)
    
     
    def on_run(self) -> None:
        # 找到目标关卡点击，不用滚动
        clickind = self.levelnum
        ScrollSelect(clickind, 134, 235, 682, 1115, lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))).run()
        # 扫荡
        RaidQuest(self.runtimes).run()
        # 关闭弹窗，回到EXCHANGE_SUB页面
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB) or Page.is_page(PageName.PAGE_EXCHANGE)
        )
        
        
        
    
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EXCHANGE_SUB) or Page.is_page(PageName.PAGE_EXCHANGE)
