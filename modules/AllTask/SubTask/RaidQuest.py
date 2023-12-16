 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area
from modules.utils.GlobalState import raidstate

class RaidQuest(Task):
    """
    从看到扫荡弹窗开始，到点击了扫荡按钮或购买按钮结束，默认不包含后续关闭收获弹窗/购买弹窗的操作。

    Parameters
    ==========
    raidname: String
        扫荡的关卡名称
    raidtimes: int
        扫荡次数，-1为最大次数，-n为最大次数减去若干次，0为不扫荡，正数为具体扫荡次数
    recall_close：function
        回调函数，用于后续关闭弹窗，通常建议将关闭操作放在此class外部
    """
    def __init__(self, raidname,raidtimes, recall_close=None, name="RaidQuest") -> None:
        super().__init__(name)
        self.raidname = raidname
        self.raidtimes = raidtimes
        self.click_magic_when_run = False
        # 回调函数，用于关闭弹窗
        self.recall_close = recall_close

    def pre_condition(self) -> bool:
        return match(popup_pic(PopupName.POPUP_TASK_INFO))
    
    
    def on_run(self) -> None:
        # 全局变量存储当前这次任务是否可继续扫荡的信息
        # 但不应当在开始就判断是否不合法，因为可能config.TASK_ORDER里有多次同名任务
        # 判断是否提前中止的操作应当交给外部循环层考虑
        # # if not raidstate.get(self.raidname, True):
        #     # logging.info("记录到此类关卡（{}）已不可扫荡，取消扫荡任务".format(self.raidname))
        #     # return
        repeat_times = self.raidtimes
        # 弹出任务咨询页面后选择次数
        if repeat_times < 0:
            # max times
            click((1084, 299))
            if repeat_times < -1:
                # max times - Math.abs(repeat_times)
                # 按减号
                # decrease times
                for t in range(abs(repeat_times)):
                    click((857, 301))
        elif repeat_times == 0:
            logging.info("扫荡次数为0，不扫荡")
            return
        else:
            for t in range(max(0,repeat_times-1)):
                # increase times
                click((1014, 300))
        # 扫荡按钮点击后，有三个可能，一个是弹出确认提示，一个是弹出购买体力的提示，还有个是购买困难扫荡券的提示
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CFIGHT_START)),
            lambda: match(popup_pic(PopupName.POPUP_NOTICE)) or match(popup_pic(PopupName.POPUP_TOTAL_PRICE), threshold=0.9) or match(popup_pic(PopupName.POPUP_USE_DIAMOND))
        )
        # 如果弹出购买体力/票卷的弹窗，取消任务
        if match(popup_pic(PopupName.POPUP_TOTAL_PRICE), threshold=0.9):
            logging.warn("检测到购买体力/卷票弹窗，取消此类（{}）扫荡任务".format(self.raidname))
            raidstate.set(self.raidname, False)
        elif match(popup_pic(PopupName.POPUP_USE_DIAMOND)):
            logging.warn("检测到需要消耗钻石，跳过关卡扫荡")
            raidstate.set(self.raidname, False)
        else:
            # 弹出确认框，点击确认
            logging.info("点击弹窗内的确认")
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                lambda: not match(popup_pic(PopupName.POPUP_NOTICE))
            )
            raidstate.set(self.raidname, True)
        # 如果传入了回调函数，则调用它来关闭弹窗
        if self.recall_close:
            self.recall_close()

     
    def post_condition(self) -> bool:
        return True