 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area

import numpy as np
import logging

from modules.utils.GlobalState import raidstate

class RunWantedFight(Task):
    def __init__(self, levelnum, runtimes, name="RunWantedFight") -> None:
        """
        after enter the location, start to raid
        
        levelnum start from 0
        """
        super().__init__(name)
        self.levelnum = levelnum
        self.runtimes = runtimes

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_WANTED_SUB)
    
     
    def on_run(self) -> None:
        # 找到目标关卡点击
        ScrollSelect(self.levelnum, 131, 230, 684, 1118, lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))).run()
        # 扫荡
        RaidQuest(raidstate.Wanted, self.runtimes).run()
        
        # 关闭弹窗，回到WANTED_SUB页面
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_WANTED_SUB)
        )
        
        
        
    
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_WANTED_SUB)
