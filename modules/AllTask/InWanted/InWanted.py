 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area_0
import logging
import time
import numpy as np
from .RunWantedFight import RunWantedFight
from modules.utils.MyConfig import config

class InWanted(Task):
    def __init__(self, name="InWanted") -> None:
        super().__init__(name)
        

     
    def pre_condition(self) -> bool:
        if len(config.WANTED_HIGHEST_LEVEL) == 0:
            logging.warn("没有配置悬赏通缉的level")
            return False
        return Page.is_page(PageName.PAGE_HOME)
    
     
    def on_run(self) -> None:
        # 得到今天是几号
        today = time.localtime().tm_mday
        # 选择一个location的下标
        target_loc = today%len(config.WANTED_HIGHEST_LEVEL)
        target_info = config.WANTED_HIGHEST_LEVEL[target_loc]
        # 判断target_info的第一个元素是不是数字
        if isinstance(target_info[0], int):
            target_info = [target_info]
        # 这之后target_info是一个list，内部会有多个关卡扫荡
        # 序号转下标
        for i in range(len(target_info)):
            target_info[i][0] -= 1
            target_info[i][1] -= 1
        # 从主页进入战斗池页面
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入悬赏通缉页面
        self.run_until(
            lambda: click((741, 440)),
            lambda: Page.is_page(PageName.PAGE_WANTED),
        )
        # 开始循环扫荡target_info中的每一个关卡
        for each_target in target_info:
            # check whether there is a ticket
            if ocr_area_0((72, 85), (322, 114)):
                logging.warn("没有悬赏通缉券了")
            else:
                # 如果国服，区域会大一些：
                if config.PIC_PATH == "./assets_cn":
                    points = np.linspace(271, 557, 3)
                else:
                    # 可点击的一列点
                    points = np.linspace(206, 422, 3)
                # 点击location
                self.run_until(
                    lambda: click((959, points[each_target[0]])),
                    lambda: Page.is_page(PageName.PAGE_WANTED_SUB),
                )
                # 扫荡对应的level
                RunWantedFight(levelnum = each_target[1], runtimes = each_target[2]).run()
                # 回到SUB界面之后，点击一下返回
                self.run_until(
                    lambda: click(Page.TOPLEFTBACK),
                    lambda: not Page.is_page(PageName.PAGE_WANTED_SUB),
                    sleeptime=3
                )
                
        self.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)