 
import logging
import time

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InSpecial.RunSpecialFight import RunSpecialFight
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config

import numpy as np

class InSpecial(Task):
    def __init__(self, name="InSpecial") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        if not config.SPECIAL_HIGHTEST_LEVEL or len(config.SPECIAL_HIGHTEST_LEVEL)==0:
            logging.warn("未配置特殊关卡")
            return False
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        # 得到今天是几号
        today = time.localtime().tm_mday
        # 选择一个location的下标
        target_loc = today%len(config.SPECIAL_HIGHTEST_LEVEL)
        target_info = config.SPECIAL_HIGHTEST_LEVEL[target_loc]
        # 判断这一天是否设置有特殊关卡
        if len(target_info) == 0:
            logging.warn("今天轮次中无特殊关卡，跳过")
            return
        # 这之后target_info是一个list，内部会有多个关卡扫荡
        # 序号转下标
        target_info = [[each[0]-1, each[1]-1, each[2]] for each in target_info]
        # 从主页进入战斗池页面
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入特殊任务页面
        self.run_until(
            lambda: click((721, 538)),
            lambda: Page.is_page(PageName.PAGE_SPECIAL),
        )
        # 开始扫荡target_info中的每一个关卡
        for each_target in target_info:
            # 国服的话区域会大一些
            if config.PIC_PATH == "./assets_cn":
                points = np.linspace(276, 415, 2)
            else:
                # 可点击的一列点
                points = np.linspace(213, 315, 2)
            # 点击location
            self.run_until(
                lambda: click((959, points[each_target[0]])),
                # 重复使用关卡目录这个pattern
                lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB),
            )
            # 扫荡对应的level
            RunSpecialFight(levelnum = each_target[1], runtimes = each_target[2]).run()
            # 回到SUB界面之后，点击一下返回
            self.run_until(
                lambda: click(Page.TOPLEFTBACK),
                lambda: not Page.is_page(PageName.PAGE_EXCHANGE_SUB),
                sleeptime=3
            )
        # 回到主页
        self.back_to_home()


    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)