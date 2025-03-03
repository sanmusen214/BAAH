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
        self.button_min = [551, 591]
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
                    CN: f"跳过扫荡任务{task}",
                    EN: f"Skip raid {task}"
                }))
                continue
            if index < 0 or index > 6:
                logging.error(istr({
                    CN: f"扫荡任务{task}次数 不合法",
                    EN: f"Raid task {task} times is not legal"
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
                    CN: f"一键扫荡任务{task}次数为0，无体力或次数不足",
                    EN: f"One-click raid task {task} times is 0, no stamina or insufficient times"
                }))
                continue
            self.run_until(
                lambda: click(self.button_min),
                lambda: ocr_area(self.ocr_area[0], self.ocr_area[1])[0].strip() == "1"
            )
            # 点击次数
            if times > 0:
                for _ in range(times - 1):
                    click(self.button_plus)
            elif times < 0:
                click(self.button_max)
                if times < -1:
                    for _ in range(-times):
                        click(self.button_minus)
            # 点击扫荡
            screenshot()
            ocr_str_times = ocr_area(self.ocr_area[0], self.ocr_area[1])[0].strip()
            logging.info(istr({
                CN: f"开始一键扫荡下标{i} 任务{task} 次数{ocr_str_times}",
                EN: f"Start one-click raid index {i} task {task} times {ocr_str_times}"
            }))
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