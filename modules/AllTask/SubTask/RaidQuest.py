 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, ocr_area_0, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, screenshot

class RaidQuest(Task):
    """
    从看到扫荡弹窗开始，到点击了扫荡按钮或购买按钮结束，默认不包含后续关闭收获弹窗/购买弹窗的操作。

    Parameters
    ==========
    raidtimes: int
        扫荡次数，-1为最大次数，-n为最大次数减去若干次，0为不扫荡，正数为具体扫荡次数
    recall_close：function
        回调函数，用于后续关闭弹窗，通常建议将关闭操作放在此class外部
    """
    def __init__(self, raidtimes, recall_close=None, name="RaidQuest") -> None:
        super().__init__(name)
        self.raidtimes = raidtimes
        self.click_magic_when_run = False
        # 回调函数，用于关闭弹窗
        self.recall_close = recall_close

    def pre_condition(self) -> bool:
        # 判断默认的次数不是0才能进入
        return match(popup_pic(PopupName.POPUP_TASK_INFO)) and not ocr_area_0((906, 284),(970, 318))
    
    def check_has_max(self) -> bool:
        """
        通过检查数字是否变化来判断是否可以通过max times来扫荡
        """
        screenshot()
        now_num = ocr_area((906, 284),(970, 318))[0]
        # 点一下max
        click((1084, 299))
        screenshot()
        next_num = ocr_area((906, 284),(970, 318))[0]
        if now_num == next_num:
            return False
        return True
    
    def on_run(self) -> None:
        # 全局变量存储当前这次任务是否可继续扫荡的信息
        # 但不应当在开始就判断是否不合法，因为可能config.userconfigdict['TASK_ORDER']里有多次同名任务
        # 判断是否提前中止的操作应当交给外部循环层考虑
        repeat_times = self.raidtimes
        # 弹出任务咨询页面后选择次数
        if repeat_times < 0:
            # 检测能够通过max times来扫荡
            if self.check_has_max():
                # max times
                click((1084, 299))
            else:
                # 点加号多次然后长按
                click((1017, 300), sleeptime=0.1)
                click((1017, 300), sleeptime=0.1)
                swipe((1017, 300), (1017, 300), durationtime=6)
            # max后反向减少次数
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
                click((1017, 300))
        # 扫荡按钮点击后，有三个可能，一个是弹出确认提示，一个是弹出购买体力的提示，还有个是购买困难扫荡券的提示
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CFIGHT_START)),
            lambda: match(popup_pic(PopupName.POPUP_NOTICE)) or match(popup_pic(PopupName.POPUP_TOTAL_PRICE), threshold=0.9) or match(popup_pic(PopupName.POPUP_USE_DIAMOND))
        )
        # 如果弹出购买体力/票卷的弹窗，取消任务
        if match(popup_pic(PopupName.POPUP_TOTAL_PRICE), threshold=0.9):
            logging.warn("检测到购买体力/卷票弹窗，取消此次扫荡任务")
        elif match(popup_pic(PopupName.POPUP_USE_DIAMOND)):
            # 困难关卡恢复挑战次数
            logging.warn("检测到需要消耗钻石，跳过关卡扫荡")
        else:
            # 弹出确认框，点击确认
            logging.info("点击弹窗内的确认")
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                lambda: not match(popup_pic(PopupName.POPUP_NOTICE))
            )
        # 如果传入了回调函数，则调用它来关闭弹窗
        if self.recall_close:
            self.recall_close()

     
    def post_condition(self) -> bool:
        return True