 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area
from modules.utils.GlobalState import raidstate
from .Questhelper import jump_to_page, close_popup_until_see
import numpy as np

class NormalQuest(Task):
    def __init__(self, questlist, name="NormalQuest") -> None:
        super().__init__(name)
        self.questlist = questlist

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)
    
     
    def on_run(self) -> None:
        logging.info("switch to normal quest")
        self.run_until(
            lambda: click((798, 159)),
            lambda: match(button_pic(ButtonName.BUTTON_NORMAL))
        )
        # after switch to normal, go to the page
        for each_quest in self.questlist:
            to_page_num = each_quest[0]+1
            level_ind = each_quest[1]
            repeat_times = each_quest[2]
            if repeat_times == 0:
                # if repeat_times == 0, means this quest is not required to do
                continue
            jumpres = jump_to_page(to_page_num)
            if not jumpres:
                logging.error("go to page {} failed, ignore this quest".format(to_page_num))
                continue
            
            ScrollSelect(level_ind, 190, 288, 628, 1115, lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))).run()
            # 扫荡
            RaidQuest(raidstate.NormalQuest, repeat_times).run()
            if not raidstate.get(raidstate.NormalQuest, True):
                break
            # 清除所有弹窗
            close_popup_until_see(button_pic(ButtonName.BUTTON_NORMAL))
        # 清除所有弹窗
        close_popup_until_see(button_pic(ButtonName.BUTTON_NORMAL))
            
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)