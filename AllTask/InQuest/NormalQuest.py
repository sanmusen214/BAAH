from typing import override
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_number
from .Questhelper import jump_to_page, close_popup_until_see
import numpy as np

class NormalQuest(Task):
    def __init__(self, questlist, name="NormalQuest") -> None:
        super().__init__(name)
        self.questlist = questlist

    @override
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)
    
    @override
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
            
            # 前四个直接点击
            self.scroll_right_up()
            ypoints = np.linspace(242, 539, 4)
            if level_ind <= 3:
                # clickable points
                logging.info("click level {}".format(level_ind+1))
                self.run_until(
                    lambda: click((1115, ypoints[level_ind])),
                    lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))
                )
            else:
                # 后面的关卡通过点开第四关后点右箭头访问
                self.run_until(
                    lambda: click((1115, ypoints[3])),
                    lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))
                )
                logging.info("click right arrow to level {}".format(level_ind))
                for i in range(level_ind-3):
                    click((1197, 359))

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
                logging.warn("体力不足，取消所有Normal扫荡任务")
                break
            else:
                # 弹出确认框，点击确认
                logging.info("点击弹窗内的确认")
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                    lambda: not match(popup_pic(PopupName.POPUP_NOTICE))
                )
            # 清除所有弹窗
            close_popup_until_see(button_pic(ButtonName.BUTTON_NORMAL))
        # 清除所有弹窗
        close_popup_until_see(button_pic(ButtonName.BUTTON_NORMAL))
            
    @override
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)