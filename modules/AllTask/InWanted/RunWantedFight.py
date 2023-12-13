 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.RaidQuest import RaidQuest
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
        if self.levelnum <= 4:
            self.scroll_right_up()
            clickind = self.levelnum
        else:
            self.scroll_right_down()
            clickind = self.levelnum - 4
        points = np.linspace(209, 605, 5)
        logging.info("click level {}".format(self.levelnum+1))
        self.run_until(
            lambda: click((1118, points[clickind])),
            lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))
        )
        # 扫荡
        RaidQuest(raidstate.Wanted, self.runtimes).run()
        
        # 关闭弹窗，回到WANTED_SUB页面
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_WANTED_SUB)
        )
        
        
        
    
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_WANTED_SUB)
