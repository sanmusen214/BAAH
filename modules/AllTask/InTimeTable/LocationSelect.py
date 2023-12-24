import logging
 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep
import numpy as np

class LocationSelect(Task):
    """
    从课程表页面选择一个地点，然后点若干个里面的教室
    
    location: 一个地点
        0表示从上往下第一个地点
    classrooms: 那个地点里要点的教室
        (0,7) 表示第1个和第8个教室都要点
    """
    def __init__(self, location, classrooms, name="LocationSelect") -> None:
        super().__init__(name)
        self.location = location
        self.classrooms = classrooms

     
    def pre_condition(self) -> bool:
        if not Page.is_page(PageName.PAGE_TIMETABLE):
            return False
        # 如果没票了也False
        return True
    
     
    def on_run(self) -> None:
        
        # 点击地点，直到跳到地区里
        ScrollSelect(self.location, 130, 236, 669, 1114, lambda: Page.is_page(PageName.PAGE_TIMETABLE_SEL)).run()
        if not match(page_pic(PageName.PAGE_TIMETABLE_SEL)):
            logging.error("无法跳转到第{}地区页面".format(self.location+1))
            return
        logging.info("进入到第{}个地区".format(self.location+1))
        # 来到
        logging.info("尝试到全体课程表弹窗页面")
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ALL_TIMETABLE)),
            lambda: match(popup_pic(PopupName.POPUP_TIMETABLE_ALL))
        )     
        for classroom in self.classrooms:
            # 序号转下标
            classroom -= 1
            # 每个classroom都从出现3x3的教室选择页面的地方开始循环
            if not match(popup_pic(PopupName.POPUP_TIMETABLE_ALL)):
                # 如果3x3界面没有打开或被遮蔽
                # 尝试点掉遮蔽界面
                logging.info("尝试到全体课程表弹窗页面")
                self.run_until(
                    lambda: click((1162, 664), sleeptime=1),
                    lambda: Page.is_page(PageName.PAGE_TIMETABLE_SEL) and match(popup_pic(PopupName.POPUP_TIMETABLE_ALL)),
                    times = 6
                )
                # 尝试点进九宫格选取页面
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_ALL_TIMETABLE)),
                    lambda: match(popup_pic(PopupName.POPUP_TIMETABLE_ALL))
                )   
            logging.info("进入到全体课程表弹窗页面")
            xs = np.linspace(299, 995, 3, dtype=int)
            ys = np.linspace(268, 573, 3, dtype=int)
            col = int(classroom%len(xs))
            row = int((classroom-col)/len(ys))
            targetloc = (xs[col], ys[row])
            # 点教室直到出现可获得奖励的弹窗
            logging.info("点击教室{}".format(classroom+1))
            havepopup = self.run_until(
                lambda: click(targetloc),
                lambda: match(popup_pic(PopupName.POPUP_TIMETABLE_INFO)),
                times=2
            )
            if not havepopup:
                logging.info(f"教室{classroom+1}不存在或已经被点过了")
                continue
            # 点击弹窗里的课程表开始
            logging.info("点击课程表开始")
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_TIMETABLE_START)),
                lambda: not match(button_pic(ButtonName.BUTTON_TIMETABLE_START)),
                times=2
            )
            # 如果点完开始发现购买弹窗
            if(match(popup_pic(PopupName.POPUP_TOTAL_PRICE))):
                logging.info(f"教室{classroom+1}由于票卷不足，执行失败")
                continue
            else:
                # 课程表执行后狂点魔法点跳过弹窗, 回到无弹窗界面
                sleep(1)
                click(Page.MAGICPOINT)
                click(Page.MAGICPOINT)
                click(Page.MAGICPOINT)

                self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: not match(popup_pic(PopupName.POPUP_TIMETABLE_ALL)) and Page.is_page(PageName.PAGE_TIMETABLE_SEL),
                    times=4
                )
        logging.info("返回到课程表页面")
        # 清除弹窗
        self.run_until(
            lambda: click(Page.TOPLEFTBACK) and click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_TIMETABLE) and not match(popup_pic(PopupName.POPUP_TIMETABLE_ALL)),
            times = 10,
            sleeptime=1.5
        )
        
                    
        

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_TIMETABLE)