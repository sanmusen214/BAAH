from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
from modules.configs.MyConfig import config

from modules.utils import (click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area_0,
                           get_config_screenshot_name)
from modules.utils.log_utils import logging
from .LocationSelect import LocationSelect
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from .RoomInfo import RoomInfo
from .IdentifySchoolNumber import get_school_number
from .IdentifyRoomHreatNumber import split_room_pic, get_heart_num

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
        # todo set to UI
        auto_timetable = True

        if not config.sessiondict["TIMETABLE_NO_TICKET"] and auto_timetable:
            # 第一个地区怎么都进得来吧！
            ScrollSelect(0, 130, 236, 669, 1114, lambda: Page.is_page(PageName.PAGE_TIMETABLE_SEL)).run()

            ss_file = get_config_screenshot_name()
            room_info_list = []
            while True:
                school_idx = get_school_number(ss_file)
                if school_idx == 0 and room_info_list:
                    break
                # 打开课程表
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_ALL_TIMETABLE)),
                    lambda: match(popup_pic(PopupName.POPUP_TIMETABLE_ALL))
                )

                room_list = split_room_pic(ss_file)
                for room_idx, room_val in enumerate(room_list):
                    love_num = get_heart_num(room_val)
                    room_info = RoomInfo(school_idx, room_idx, love_num)
                    room_info_list.append(room_info)
                room_info_list.sort(reverse=True)

                # 退出弹框
                self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: not match(popup_pic(PopupName.POPUP_TIMETABLE_ALL)) and Page.is_page(
                        PageName.PAGE_TIMETABLE_SEL),
                    times=2,
                    sleeptime=2
                )
                self.run_until(
                    lambda: click((1253, 362)),
                    lambda: False,
                    times=1,
                    sleeptime=2
                )

            # 退出某个地区的课程表
            self.run_until(
                lambda: click(Page.TOPLEFTBACK),
                lambda: Page.is_page(PageName.PAGE_TIMETABLE),
                times=2,
                sleeptime=2
            )
            timetable_list = [[] for _ in range(10)]
            for room in room_info_list[:7]:
                timetable_list[room.school_idx].append(room.room_idx+1)
            print(timetable_list)
            for i in range(len(timetable_list)):
                if config.sessiondict["TIMETABLE_NO_TICKET"]:
                    logging.info("课程表/时间表 无票卷， 退出此任务")
                    break
                # 如果这一location没有任务，就不点进去
                if len(timetable_list[i]) == 0:
                    continue
                LocationSelect(location=i, classrooms=timetable_list[i]).run()
        else:
            # for each TIMETABLE_TASK, determine whether need to click in
            for i in range(len(config.userconfigdict['TIMETABLE_TASK'])):
                if config.sessiondict["TIMETABLE_NO_TICKET"]:
                    logging.info("课程表/时间表 无票卷， 退出此任务")
                    break
                # 如果这一location没有任务，就不点进去
                if len(config.userconfigdict['TIMETABLE_TASK'][i]) == 0:
                    continue
                LocationSelect(location=i, classrooms=config.userconfigdict['TIMETABLE_TASK'][i]).run()
        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)