 
import logging
import time
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
        # 跳到Quest标签
        click((944, 98))
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
            # 弹出任务咨询页面后选择次数
            if repeat_times < 0:
                # max times
                click((1084, 299))
            else:
                for t in range(max(0,repeat_times-1)):
                    # add times
                    click((1014, 300))
            # 扫荡按钮点击后，有三个可能，一个是弹出确认提示，一个是弹出购买体力的提示。一个是弹出购买扫荡卷的提示
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CFIGHT_START)),
                lambda: match(popup_pic(PopupName.POPUP_NOTICE)) or match(popup_pic(PopupName.POPUP_TOTAL_PRICE), threshold=0.9)
            )
            # 如果弹出购买票卷的弹窗，取消任务
            if match(popup_pic(PopupName.POPUP_TOTAL_PRICE), threshold=0.9):
                logging.warn("体力不足，取消扫荡任务")
                break
            else:
                # 弹出确认框，点击确认
                logging.info("点击弹窗内的确认")
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                    lambda: not match(popup_pic(PopupName.POPUP_NOTICE))
                )
            # 关闭任务咨询弹窗
            logging.info("关闭任务咨询弹窗")
            Task.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
            )
        

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EVENT)