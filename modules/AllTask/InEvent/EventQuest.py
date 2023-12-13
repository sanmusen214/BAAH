 
import logging
import time
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.utils.GlobalState import raidstate
from modules.utils.MyConfig import config
import numpy as np

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, match_pixel

class EventQuest(Task):
    def __init__(self, level_list, name="EventQuest") -> None:
        super().__init__(name)
        self.level_list = level_list

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EVENT)
    
     
    def on_run(self) -> None:
        # 按level执行
        for level in self.level_list:
            click((944, 98))
            level_ind = level[0]
            repeat_times = level[1]
            ypoints = np.linspace(184, 645, 5)
            if level_ind<=4:
                self.scroll_right_up()
                # clickable points
                logging.info("click level {}".format(level_ind+1))
                self.run_until(
                    lambda: click((1129, ypoints[level_ind])),
                    lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))
                )
            elif level_ind>=5 and level_ind<=6:
                self.scroll_right_up()
                # 通过滑动来翻页level_ind=5的关卡此时从上到下第二关
                swipe((915, 643), (920, 180), 1.5)
                logging.info("click level {}".format(level_ind+1))
                self.run_until(
                    lambda: click((1129, ypoints[level_ind-4])),
                    lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))
                )
            elif level_ind>=7:
                self.scroll_right_down()
                # clickable points
                logging.info("click level {}".format(level_ind+1))
                self.run_until(
                    lambda: click((1129, ypoints[level_ind-7])),
                    lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))
                )
            RaidQuest(raidstate.Event, repeat_times).run()
            # 关闭任务咨询弹窗
            logging.info("关闭任务咨询弹窗")
            Task.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
            )
            if not raidstate.get(raidstate.Event, True):
                return
        

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EVENT)