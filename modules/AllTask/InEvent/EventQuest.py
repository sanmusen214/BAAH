 
import logging
import time
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
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
            # 判断底部是否有进度条
            if match(button_pic(ButtonName.BUTTON_EVENT_BOTTOM_BAR)):
                logging.info("底部有进度条")
                ScrollSelect(level_ind, 140, 238, 583, 1130, lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))).run() # 活动页面延迟响应要大一点
            else:
                # 没有进度条可滑动区域会更靠下
                logging.info("底部没有进度条")
                ScrollSelect(level_ind, 140, 238, 683, 1130, lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))).run()
            RaidQuest(repeat_times).run()
            # 关闭任务咨询弹窗
            logging.info("关闭任务咨询弹窗")
            Task.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
            )
        

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EVENT)