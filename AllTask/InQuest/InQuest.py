 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area
from .HardQuest import HardQuest
from .NormalQuest import NormalQuest
import time
import config

class InQuest(Task):
    def __init__(self, name="InQuest") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
     
    def on_run(self) -> None:
        # 进入Fight Center
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入Quest 中心
        self.run_until(
            lambda: click((816, 259)),
            lambda: Page.is_page(PageName.PAGE_QUEST_SEL),
        )
        # 当天日期
        today = time.localtime().tm_mday
        # 选择一个HARD QUEST List的下标
        if len(config.QUEST["HARD"]) != 0:
            # 可选任务队列不为空时
            hard_loc = today%len(config.QUEST["HARD"])
            # 得到要执行的HARD QUEST LIST
            # [[13,2,3],[19,2,3]]
            hard_list = config.QUEST["HARD"][hard_loc]
            # 序号转下标
            hard_list_2 = [[x[0]-1,x[1]-1,x[2]] for x in hard_list]
            # do HARD QUEST
            HardQuest(hard_list_2).run()

        # 选择一个NORMAL QUEST List的下标
        if len(config.QUEST["NORMAL"]) != 0:
            # 可选任务队列不为空时
            normal_loc = today%len(config.QUEST["NORMAL"])
            # 得到要执行的NORMAL QUEST LIST
            # [[13,2,3],[19,2,3]]
            normal_list = config.QUEST["NORMAL"][normal_loc]
            # do NORMAL QUEST
            # 序号转下标
            normal_list_2 = [[x[0]-1,x[1]-1,x[2]] for x in normal_list]
            NormalQuest(normal_list_2).run()
        self.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)