from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
from modules.configs.MyConfig import config

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area_0
import logging
from .LocationSelect import LocationSelect

class InTimeTable(Task):
    def __init__(self, name="InTimeTable") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
     
    def on_run(self) -> None:
        self.run_until(
            lambda: click((212, 669)),
            lambda: Page.is_page(PageName.PAGE_TIMETABLE)
        )
        # for each TIMETABLE_TASK, determine whether need to click in
        for i in range(len(config.userconfigdict['TIMETABLE_TASK'])):
            # determine tickets left
            nolefttickets:bool = ocr_area_0((72, 85), (322, 114))
            if nolefttickets:
                logging.warn("没有课程表票卷了，开始返回主页")
                break
            # 如果这一location没有任务，就不点进去
            if len(config.userconfigdict['TIMETABLE_TASK'][i]) == 0:
                continue
            LocationSelect(location=i, classrooms=config.userconfigdict['TIMETABLE_TASK'][i]).run()
        self.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)