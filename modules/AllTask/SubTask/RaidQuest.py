 
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
    从看到扫荡弹窗开始，到点击了扫荡按钮或购买按钮结束，不包含后续关闭收获弹窗/购买弹窗的操作。

    Parameters
    ==========
    raidname: String
        扫荡的关卡名称
    raidtimes: int
        扫荡次数，-1为最大次数，-n为最大次数减去若干次，0为不扫荡，正数为具体扫荡次数
    """
    def __init__(self, raidname,raidtimes,  name="RaidQuest") -> None:
        super().__init__(name)
        self.raidname = raidname
        self.raidtimes = raidtimes
        self.click_magic_when_run = False

    def pre_condition(self) -> bool:
        return match(popup_pic(PopupName.POPUP_TASK_INFO))
    
    
    def on_run(self) -> None:
        # 全局变量存储是否可继续扫荡的信息
        if not raidstate.get(self.raidname, True):
            logging.info("记录到此类关卡（{}）已不可扫荡，取消扫荡任务".format(self.raidname))
            return
        repeat_times = self.raidtimes
        # 弹出任务咨询页面后选择次数
        if repeat_times < 0:
            # max times
            if repeat_times == -1:
                click((1084, 299))
            else:
                decrease_times = -1 - repeat_times
                # 按减号
                
        else:
            for t in range(max(0,repeat_times-1)):
                # add times
                click((1014, 300))
        # 扫荡按钮点击后，有三个可能，一个是弹出确认提示，一个是弹出购买体力的提示，还有个是购买困难扫荡券的提示
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CFIGHT_START)),
            lambda: match(popup_pic(PopupName.POPUP_NOTICE)) or match(popup_pic(PopupName.POPUP_TOTAL_PRICE), threshold=0.9) or match(popup_pic(PopupName.POPUP_USE_DIAMOND))
        )
        # 如果弹出购买票卷的弹窗，取消任务
        if match(popup_pic(PopupName.POPUP_TOTAL_PRICE), threshold=0.9):
            logging.warn("体力不足，取消此类（{}）扫荡任务".format(self.raidname))
            raidstate.set(self.raidname, False)
        elif match(popup_pic(PopupName.POPUP_USE_DIAMOND)):
            logging.warn("当前关卡扫荡卷不足，跳过该关卡扫荡")
        else:
            # 弹出确认框，点击确认
            logging.info("点击弹窗内的确认")
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                lambda: not match(popup_pic(PopupName.POPUP_NOTICE))
            )

     
    def post_condition(self) -> bool:
        return True