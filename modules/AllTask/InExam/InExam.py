import numpy as np
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.FightQuest import FightQuest
from modules.AllTask.SubTask.SkipStory import SkipStory
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel, istr, CN, EN, JP
from modules.utils.log_utils import logging

class InExam(Task):
    def __init__(self, name="InExam") -> None:
        super().__init__(name)
        self.ENTER_EXAM = [1052, 450]
        # 三个考试地区的判断点
        self.AREAS_POINTS = [
            [102, 375],
            [635, 394],
            [1030, 366]
        ]
        self.COLOT_GIVEUP_POINT = {"pos": [1100, 669], "color":([220, 210, 200], [255, 255, 235])}
        # 入场四个按钮
        y_list = np.linspace(189, 482, 4, dtype=int)
        self.enter_buttons_pos_list = [(1145, y) for y in y_list]
        # 扫荡按钮
        self.COLOR_RAID_POINT = {"pos": [783, 669], "color": ([245, 200, 100], [255, 240, 130])}


    def pre_condition(self) -> bool:
        return self.back_to_home()
    
    def do_a_new_exam(self) -> bool:
        # 按钮位置相同，开始新的一次考试
        self.run_until(
            lambda: click(self.COLOT_GIVEUP_POINT["pos"]),
            lambda: self.has_popup()
        )
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CONFIRMY)),
            lambda: not self.has_popup()
        )
        for t in range(3):
            self.clear_popup()
            # 点第二关
            self.run_until(
                lambda: click(self.enter_buttons_pos_list[1]),  # 点击第二个按钮
                lambda: self.has_popup()
            )
            # 点考试开始
            self.run_until(
                lambda: click([639, 508]),
                lambda: not self.has_popup()
            )
            # =====配队页面=======
            # 切队伍
            click(Page.LEFT_FOUR_TEAMS_POSITIONS[t])
            # 出击打架
            FightQuest(backtopic=lambda: Page.is_page(PageName.PAGE_EXAM)).run()

    def can_exam_raid(self):
        if match_pixel(self.COLOR_RAID_POINT["pos"], self.COLOR_RAID_POINT["color"]):
            # 扫荡按钮亮了
            return True
        return False

    def do_exam_raid(self):
        # 进行考试扫荡
        open_raid_popup = self.run_until(
            lambda: click(self.COLOR_RAID_POINT["pos"]),
            lambda: self.has_popup()
        )
        if not open_raid_popup:
            # 扫荡弹窗没有
            logging.warn(istr({
                CN: "扫荡弹窗没打开",
                EN: "Raid popup not found",
            }))
            return False
        # 按 + 号
        click([991, 359])
        click([991, 359])
        click([991, 359])
        click([991, 359])
        # 点击扫荡
        self.run_until(
            lambda: click([897, 465]),
            lambda: match(button_pic(ButtonName.BUTTON_CONFIRMB))
        )
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
            lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMB))
        )
        self.clear_popup()
     
    def on_run(self) -> None:
        # 进到中心
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # =====进入综合战术测试/合同火力演习======
        self.run_until(
            lambda: click(self.ENTER_EXAM),
            lambda: not Page.is_page(PageName.PAGE_FIGHT_CENTER),
        )
        self.clear_popup()
        # 第一次可能有剧情
        story = SkipStory()
        if story.pre_condition():
            story.on_run()
            self.clear_popup()
        # 两个页面，一个是地区选择，一个是考试选择
        if match_pixel([374, 681], Page.COLOR_WHITE):
            # 考试选择页面
            pass
        else:
            # 地区选择
            # 判断开放的考试区域
            can_enter = False
            for i in range(len(self.AREAS_POINTS)):
                if match_pixel(self.AREAS_POINTS[i], Page.COLOR_WHITE):
                    # 亮的区域
                    can_enter = True
                    # 进入考试
                    click([self.AREAS_POINTS[i][0] + 50, self.AREAS_POINTS[i][1]])
                    break
            if not can_enter:
                logging.info(istr({
                    CN: "没有可进入的考试区域",
                    EN: "No available exam area",
                }))
                return
        # ======考试选择页面=======
        # 上次考试可能没结束，点结束上次的
        if match_pixel(self.COLOT_GIVEUP_POINT["pos"], self.COLOT_GIVEUP_POINT["color"]):
            # 结束上次的考试
            self.run_until(
                lambda: click(self.COLOT_GIVEUP_POINT["pos"]),
                lambda: self.has_popup()
            )
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMB))
            )
            sleep(2)
            self.clear_popup()
        if not self.can_exam_raid():
            # 开始新考试
            self.do_a_new_exam()
        # 考试扫荡
        self.do_exam_raid()
            

            

     
    def post_condition(self) -> bool:
        return self.back_to_home()