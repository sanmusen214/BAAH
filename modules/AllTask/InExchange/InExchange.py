from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area_0
from modules.utils.log_utils import logging
import time
import numpy as np

from modules.configs.MyConfig import config
from .RunExchangeFight import RunExchangeFight


class InExchange(Task):
    def __init__(self, name="InExchange") -> None:
        super().__init__(name)

    def pre_condition(self) -> bool:
        if not config.userconfigdict['EXCHANGE_HIGHEST_LEVEL'] or len \
                (config.userconfigdict['EXCHANGE_HIGHEST_LEVEL']) == 0:
            logging.warn({"zh_CN": "没有配置学院交流会的level", "en_US":"Didn't set the level of exchange meeting"})
            return False
        return Page.is_page(PageName.PAGE_HOME)

    def on_run(self) -> None:
        # 得到今天是几号
        today = time.localtime().tm_mday
        # 选择一个location的下标
        target_loc = today % len(config.userconfigdict['EXCHANGE_HIGHEST_LEVEL'])
        target_info = config.userconfigdict['EXCHANGE_HIGHEST_LEVEL'][target_loc]
        # 判断这一天是否设置有交流会关卡
        if len(target_info) == 0:
            logging.warn({"zh_CN": "今天轮次中无学院交流会关卡，跳过",
                          "en_US" :"No exchange level in today's round, skip"})
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
        # 进入学院交流会页面
        caninexchange = self.run_until(
            lambda: click((712, 592)),
            lambda: Page.is_page(PageName.PAGE_EXCHANGE),
        )
        if not caninexchange:
            logging.warn({"zh_CN": "无法打开交换页面，任务退出", "en_US": "Can't open exchange page, task quit"})
            self.back_to_home()
            return
        for each_target in target_info:
            # check whether there is a ticket
            # 使用PageName.PAGE_EXCHANGE的坐标判断是国服还是其他服
            if match(page_pic(PageName.PAGE_EXCHANGE), returnpos=True)[1][1]>133:
                # 如果右侧Title较低，说明是老版本的国服
                logging.info({"zh_CN": "点击较低的三个定位点", "en_US": "Click on the three lower anchor points"})
                points = np.linspace(265, 544, 3)
            else:
                # 可点击的一列点
                points = np.linspace(206, 422, 3)
            # 点击location
            self.run_until(
                lambda: click((963, points[each_target[0]])),
                lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB),
            )
            # 扫荡对应的level
            RunExchangeFight(levelnum = each_target[1], runtimes = each_target[2]).run()
            # 如果是回到SUB界面之后，点击一下返回，如果是回到EXCHANGE界面，就不用点击了
            self.run_until(
                lambda: click(Page.TOPLEFTBACK),
                lambda: not Page.is_page(PageName.PAGE_EXCHANGE_SUB),
                sleeptime=3
            )
        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)