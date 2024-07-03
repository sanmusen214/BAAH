from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area
from .HardQuest import HardQuest
from .NormalQuest import NormalQuest
from .PushQuest import PushQuest
import time
from modules.configs.MyConfig import config


class InQuest(Task):
    """
    进入 普通关卡/困难关卡， types=["normal", "hard", "push-normal", "push-hard"]
    """

    def __init__(self, types=["normal", "hard"], name="InQuest") -> None:
        super().__init__(name)
        self.types = types

    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)

    def on_run(self) -> None:
        # 进入Fight Center
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入Quest 中心
        self.run_until(
            lambda: click((816, 259)),
            lambda: Page.is_page(PageName.PAGE_QUEST_SEL),
        )
        if "push-normal" in self.types:
            # 判断配置里的PUSH_NORMAL_QUEST长度是否为0
            if config.userconfigdict['PUSH_NORMAL_QUEST'] != 0:
                # do PUSH NORMAL QUEST
                logging.info({"zh_CN": "设置了推普通图任务，开始推图",
                              "en_US": "Set up the task of pushing the normal diagram to start the thumbnail"})
                # 序号转下标 章节号
                push_normal_ind = config.userconfigdict['PUSH_NORMAL_QUEST'] - 1
                PushQuest("normal", push_normal_ind,
                          level_ind=config.userconfigdict["PUSH_NORMAL_QUEST_LEVEL"] - 1).run()
        if "push-hard" in self.types:
            # 判断配置里的PUSH_HARD_QUEST长度是否为0
            if config.userconfigdict['PUSH_HARD_QUEST'] != 0:
                # do PUSH HARD QUEST
                logging.info({"zh_CN": "设置了推困难图任务，开始推图",
                              "en_US": "Set up the Push Difficulty Diagram task to start pushing the diagram"})
                # 序号转下标，章节号
                push_hard_ind = config.userconfigdict['PUSH_HARD_QUEST'] - 1
                PushQuest("hard", push_hard_ind, level_ind=config.userconfigdict["PUSH_HARD_QUEST_LEVEL"] - 1).run()
        # 当天日期
        today = time.localtime().tm_mday
        if "hard" in self.types:
            # 选择一个HARD QUEST List的下标
            if len(config.userconfigdict['HARD']) != 0:
                # 可选任务队列不为空时
                hard_loc = today % len(config.userconfigdict['HARD'])
                # 得到要执行的HARD QUEST LIST
                # [[13,2,3],[19,2,3]]
                hard_list = config.userconfigdict['HARD'][hard_loc]
                # 序号转下标
                def hard_generator(_list):
                    for  x in _list:
                        if len(x)==4:
                            yield  [x[0]-1,x[1]-1,x[2],x[3]]
                        else: # 兼容老版3个参数不带开关的config
                            yield  [x[0]-1,x[1]-1,x[2]]
                # do HARD QUEST
                HardQuest(hard_generator(hard_list)).run()
        if "normal" in self.types:
            # 选择一个NORMAL QUEST List的下标
            if len(config.userconfigdict['NORMAL']) != 0:
                # 可选任务队列不为空时
                normal_loc = today % len(config.userconfigdict['NORMAL'])
                # 得到要执行的NORMAL QUEST LIST
                # [[13,2,3],[19,2,3]]
                normal_list = config.userconfigdict['NORMAL'][normal_loc]
                # do NORMAL QUEST
                # 序号转下标
                def normal_generator(_list):
                    for  x in _list:
                        if len(x)==4:
                            yield  [x[0]-1,x[1]-1,x[2],x[3]]
                        else: # 兼容老版3个参数不带开关的config
                            yield  [x[0]-1,x[1]-1,x[2]]
                NormalQuest(normal_generator(normal_list)).run()
        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)