 
from modules.utils.log_utils import logging
import time

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InSpecial.RunSpecialFight import RunSpecialFight
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, match_pixel

import numpy as np

class InSpecial(Task):
    def __init__(self, name="InSpecial") -> None:
        super().__init__(name)


    def pre_condition(self) -> bool:
        if not config.userconfigdict['SPECIAL_HIGHTEST_LEVEL'] or len(config.userconfigdict['SPECIAL_HIGHTEST_LEVEL'])==0:
            logging.warn({"zh_CN": "未配置特殊关卡", "en_US":"Didn't set the special level"})
            return False
        return Page.is_page(PageName.PAGE_HOME)


    def on_run(self) -> None:
        # 得到今天是几号
        today = time.localtime().tm_mday
        # 选择一个location的下标
        target_loc = today%len(config.userconfigdict['SPECIAL_HIGHTEST_LEVEL'])
        target_info = config.userconfigdict['SPECIAL_HIGHTEST_LEVEL'][target_loc]
        # 判断这一天是否设置有特殊关卡
        if len(target_info) == 0:
            logging.warn({"zh_CN": "今天轮次中无特殊关卡，跳过", "en_US":"There is no special level in today's round, skip"})
            return
        # 这之后target_info是一个list，内部会有多个关卡扫荡
        # 序号转下标
        target_info=[[each[0]-1, each[1]-1, *each[2:]] for each in target_info]
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入特殊任务页面
        caninspecial = self.run_until(
            lambda: click((721, 538)),
            lambda: Page.is_page(PageName.PAGE_SPECIAL),
        )
        if not caninspecial:
            logging.warning("Can't open special page, task quit")
            self.back_to_home()
            return
     
            
        #用颜色判断是否在活动中
        # 国际服试了可用，其他待测试
        if config.userconfigdict["SPEICAL_EVENT_STATUS"] and not match_pixel((130, 111), Page.COLOR_PINK,printit=True):
            logging.warn({"zh_CN": "今天不在活动中，跳过", "en_US":"Today is not in the activity, skip"})
            return
        # 从主页进入战斗池页面
        # 开始扫荡target_info中的每一个关卡
        for each_target in target_info:
            if each_target[-1] == 'false' or each_target[-1] == False or each_target[-1] == 0 : # 开关关闭
                logging.info(f"特殊作战{each_target[0]+1}-{each_target[1]+1}设置为关, 忽略")
                continue
            # 使用PageName.PAGE_SPECIAL的坐标判断是国服还是其他服
            if match(page_pic(PageName.PAGE_SPECIAL), returnpos=True)[1][1]>133:
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