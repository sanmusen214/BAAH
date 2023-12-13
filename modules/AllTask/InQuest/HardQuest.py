 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area
from modules.utils.GlobalState import raidstate
from .Questhelper import jump_to_page,close_popup_until_see
import numpy as np

class HardQuest(Task):
    def __init__(self, questlist, name="HardQuest") -> None:
        super().__init__(name)
        self.questlist = questlist

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)
    
     
    def on_run(self) -> None:
        logging.info("switch to hard quest")
        self.run_until(
            lambda: click((1064, 161)),
            lambda: match(button_pic(ButtonName.BUTTON_HARD))
        )
        # after switch to hard, go to the page
        for each_quest in self.questlist:
            to_page_num = each_quest[0]+1
            level_ind = each_quest[1]
            repeat_times = each_quest[2]
            if repeat_times == 0:
                # if repeat_times == 0, means this quest is not required to do
                continue
            jumpres = jump_to_page(to_page_num)
            if not jumpres:
                logging.error("无法到达页面{}, 忽略这关扫荡".format(to_page_num))
                continue
            # clickable points
            logging.info("点击从上往下第{}关".format(level_ind+1))
            ypoints = np.linspace(248, 480, 3)
            self.run_until(
                lambda: click((1118, ypoints[level_ind])),
                lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))
            )
            # 扫荡
            RaidQuest(raidstate.HardQuest, repeat_times).run()
            if not raidstate.get(raidstate.HardQuest, True):
                break
            
            # 关闭弹窗，直到看到hard按钮
            close_popup_until_see(button_pic(ButtonName.BUTTON_HARD))
        # 体力不足，也关闭弹窗，直到看到hard按钮
        close_popup_until_see(button_pic(ButtonName.BUTTON_HARD))
            
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)