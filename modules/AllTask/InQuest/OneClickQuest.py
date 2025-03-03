import numpy as np
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel, istr, CN, EN, JP
from modules.utils.log_utils import logging

class OneClickQuest(Task):
    def __init__(self, tasklist, name="OneClickQuest") -> None:
        super().__init__(name)
        # [[3,10],[4,-1]]
        # 一件扫荡下标，次数
        self.tasklist = tasklist
        self.selected_tab = [[110, 70, 40], [120, 80, 55]]
        self.button_minus = [620, 591]
        self.button_plus = [772, 592]
        self.button_max = [843, 591]
        self.ocr_area = ([661, 573], [735, 615])

     
    def pre_condition(self) -> bool:
        self.clear_popup()
        return Page.is_page(PageName.PAGE_QUEST_SEL)
    
     
    def on_run(self) -> None:
        logging.info(istr({
            CN: f"开始一键扫荡{self.tasklist}",
            EN: f"Start one-click raid {self.tasklist}"
        }))
        # 点开批量扫荡
        open_popup = self.run_until(
            lambda: click([483, 599]),
            lambda: self.has_popup(),
            times = 4
        )
        if not open_popup:
            logging.error(istr({
                CN: f"无法打开一键扫荡界面",
                EN: f"Cannot open the one-click raid page"
            }))
            return
        # 7个坐标点
        point_y = 165
        points_x = np.linspace(167, 1125, 7, dtype=int)
        for i, task in enumerate(self.tasklist):
            index = task[0]
            times = task[1]
            whether_do = task[2]
            if not whether_do:
                logging.info(istr({
                    CN: f"跳过扫荡下标{index}",
                    EN: f"Skip raid index {index}"
                }))
                continue
            if index < 0 or index > 6:
                logging.error(istr({
                    CN: f"扫荡下标{index} 不合法",
                    EN: f"Raid index {index} is illegal"
                }))
                continue
            # 切换到对应的扫荡任务
            self.run_until(
                lambda: click([points_x[index], point_y]),
                lambda: match_pixel([points_x[index], point_y], self.selected_tab)
            )
            # 扫荡次数
            if ocr_area(self.ocr_area[0], self.ocr_area[1])[0].strip() == "0":
                logging.warn(istr({
                    CN: f"一键扫荡下标{index}次数为0，无体力或次数不足",
                    EN: f"One-click raid index {index} times is 0, no stamina or insufficient times"
                }))
                continue
            # 点击次数
            if times > 0:
                for _ in range(times):
                    click(self.button_plus)
            elif times < 0:
                click(self.button_max)
                if times < -1:
                    for _ in range(-times):
                        click(self.button_minus)
            # 点击扫荡
            self.run_until(
                lambda: click([947, 595]),
                lambda: match(button_pic(ButtonName.BUTTON_CONFIRMY))
            )
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CONFIRMY)),
                lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMY))
            )
            self.clear_popup()


     
    def post_condition(self) -> bool:
        self.clear_popup()
        return Page.is_page(PageName.PAGE_QUEST_SEL)