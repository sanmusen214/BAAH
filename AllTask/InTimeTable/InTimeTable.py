from typing import override

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task
import config

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_number
import logging
from .LocationSelect import LocationSelect

class InTimeTable(Task):
    def __init__(self, name="InTimeTable") -> None:
        super().__init__(name)

    @override
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
    @override
    def on_run(self) -> None:
        self.run_until(
            lambda: click((212, 669)),
            lambda: Page.is_page(PageName.PAGE_TIMETABLE)
        )
        # for each TIMETABLE_TASK, determine whether need to click in
        for i in range(len(config.TIMETABLE_TASK)):
            # determine tickets left
            lefttickets:str = ocr_number((159,90),(175, 109))
            if lefttickets == "0":
                logging.warn("没有课程表票卷了，开始返回主页")
                break
            # 如果这一location没有任务，就不点进去
            if len(config.TIMETABLE_TASK[i]) == 0:
                continue
            LocationSelect(location=i, classrooms=config.TIMETABLE_TASK[i]).run()
        self.back_to_home()

    @override
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)