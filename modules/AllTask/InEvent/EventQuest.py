 
import logging
import time
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.configs.MyConfig import config
import numpy as np

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

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
            click(Page.MAGICPOINT)
            click((944, 98))
            level_ind = level[0]
            repeat_times = level[1]
            self.scroll_right_up()
            # 点击第一个level
            click((1130, 200), sleeptime=2)
            logging.info(f"尝试跳转到第{level_ind+1}个level")
            # 向右挪到第level_ind个level
            for i in range(level_ind):
                click((1171, 359), sleeptime=1)
            RaidQuest(repeat_times).run()
            # 关闭任务咨询弹窗
            logging.info("关闭任务咨询弹窗")
            Task.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
            )
        Task.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
        )
        

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EVENT)