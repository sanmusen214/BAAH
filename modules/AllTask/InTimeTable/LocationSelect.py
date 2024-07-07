from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, config, match_pixel
import numpy as np


class LocationSelect(Task):
    """
    从课程表页面选择一个地点（可跳过），然后点若干个九宫格里的教室

    location: 一个地点
        0表示从上往下第一个地点。-1表示不选择地点，已经在教室选择页面
    classrooms: 那个地点里要点的教室
        (0,7) 表示第1个和第8个教室都要点
    backtoLocationPage: boolean
        是否返回到地点选择页面
    """

    def __init__(self, location, classrooms, backtoLocationPage=True, name="LocationSelect") -> None:
        super().__init__(name)
        self.location = location
        self.classrooms = classrooms
        self.backtoLocationPage = backtoLocationPage

    def pre_condition(self) -> bool:
        if self.location == -1 and Page.is_page(PageName.PAGE_TIMETABLE_SEL):
            return True
        if not Page.is_page(PageName.PAGE_TIMETABLE):
            return False
        # 如果没票了也False
        return True

    def on_run(self) -> None:

        # 点击地点，直到跳到地区里
        if self.location != -1:
            ScrollSelect(self.location, 130, 236, 669, 1114, lambda: Page.is_page(PageName.PAGE_TIMETABLE_SEL)).run()
            if not match(page_pic(PageName.PAGE_TIMETABLE_SEL)):
                logging.error({"zh_CN": "无法跳转到第{}地区页面".format(self.location + 1),
                               "en_US": "Cannot jump to the {}th location page".format(self.location + 1)})
                return
            logging.info({"zh_CN": "进入到第{}个地区".format(self.location + 1),
                          "en_US": "Enter Region {}".format(self.location + 1)})
        # 来到
        logging.info({"zh_CN": "尝试到全体课程表弹窗页面", "en_US": "Try to go to the All Curriculums pop-up page"})
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ALL_TIMETABLE)),
            lambda: match(popup_pic(PopupName.POPUP_TIMETABLE_ALL))
        )
        for classroom in self.classrooms:
            # 序号转下标
            if isinstance (classroom, bool):
                continue
            classroom -= 1
            # 每个classroom都从出现3x3的教室选择页面的地方开始循环
            if not match(popup_pic(PopupName.POPUP_TIMETABLE_ALL)):
                # 如果3x3界面没有打开或被遮蔽
                # 尝试点掉遮蔽界面
                logging.info({"zh_CN": "尝试到全体课程表弹窗页面",
                              "en_US": "Try to go to the All Curriculums pop-up page"})
                # 点右下固定点
                self.run_until(
                    lambda: click(Page.MAGICPOINT) and click((1162, 664)),
                    lambda: Page.is_page(PageName.PAGE_TIMETABLE_SEL) and match(popup_pic(PopupName.POPUP_TIMETABLE_ALL)),
                    times = 15
                )
                # 尝试点进九宫格选取页面
                logging.info({"zh_CN": "打开九宫格选取页面", "en_US": "Open the nine palaces selection page"})
                # 点右下按钮
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_ALL_TIMETABLE)),
                    lambda: match(popup_pic(PopupName.POPUP_TIMETABLE_ALL))
                )
            logging.info({"zh_CN": "进入到全体课程表弹窗页面", "en_US": "Go to Full Course Schedule Popup"})
            xs = np.linspace(299, 995, 3, dtype=int)
            ys = np.linspace(268, 573, 3, dtype=int)
            col = int(classroom % len(xs))
            row = int((classroom - col) / len(ys))
            targetloc = (xs[col], ys[row])
            # 点教室直到出现可获得奖励的弹窗
            logging.info({"zh_CN": "点击教室{}".format(classroom + 1),
                          "en_US": "Click on classroom {}" .format (classroom + 1)})
            havepopup = self.run_until(
                lambda: click(targetloc),
                lambda: match(popup_pic(PopupName.POPUP_TIMETABLE_INFO)),
                times=3
            )
            if not havepopup:
                logging.info({"zh_CN": f"教室{classroom + 1}不存在或已经被点过了",
                              "en_US": f"Classroom {classroom + 1} does not exist or has been ordered"})
                continue
            # 点击弹窗里的课程表开始
            logging.info({"zh_CN": "点击课程表开始", "en_US": "Click on Curriculum to begin"})
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TIMETABLE_START)),
                lambda: not match(button_pic(ButtonName.BUTTON_TIMETABLE_START)),
                times=3
            )
            # 如果点完开始发现购买弹窗
            if (match(popup_pic(PopupName.POPUP_TOTAL_PRICE)) or match(popup_pic(PopupName.POPUP_NOTICE))):
                logging.info({"zh_CN": f"教室{classroom + 1}由于票卷不足，执行失败",
                              "en_US": f"Classroom {classroom + 1} execution failed due to insufficient tickets"})
                config.sessiondict["TIMETABLE_NO_TICKET"] = True
                break
            else:
                # 课程表执行后狂点魔法点跳过弹窗, 回到无弹窗界面
                sleep(1)
                click(Page.MAGICPOINT)
                click(Page.MAGICPOINT)
                click(Page.MAGICPOINT)

                self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: not match(popup_pic(PopupName.POPUP_TIMETABLE_ALL)) and Page.is_page(PageName.PAGE_TIMETABLE_SEL),
                    times=8
                )
        # 清除弹窗
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_TIMETABLE_SEL) and match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
            times=15,
            sleeptime=2
        )
        if self.backtoLocationPage:
            logging.info({"zh_CN": "返回到课程表页面", "en_US": "Back to Curriculum"})
            # 返回到课程表页面
            self.run_until(
                lambda: click(Page.TOPLEFTBACK),
                lambda: Page.is_page(PageName.PAGE_TIMETABLE),
                times=2,
                sleeptime=2
            )

    def post_condition(self) -> bool:
        if not self.backtoLocationPage:
            return Page.is_page(PageName.PAGE_TIMETABLE_SEL)
        return Page.is_page(PageName.PAGE_TIMETABLE)