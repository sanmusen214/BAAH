 
import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot

class SkipStory(Task):
    """
    前置条件为存在右上角Menu按钮
    
    点击跳过那个弹窗里的蓝色按钮并识别不到蓝色确认按钮后结束
    """
    def __init__(self, pre_times=10, name="SkipStory") -> None:
        # 前置判断时间弄久一点
        super().__init__(name, pre_times=pre_times)

     
    def pre_condition(self) -> bool:
        # 这里不能点击MAGICPOINT，因为有可能关闭momotalk弹窗
        return match(button_pic(ButtonName.BUTTON_STORY_MENU))
    
     
    def on_run(self) -> None:
        for i in range(7):
            screenshot()
            # 记住MENU的位置
            menures = match(button_pic(ButtonName.BUTTON_STORY_MENU), returnpos=True)
            if not menures[0]:
                logging.info("跳过剧情被打断，重试")
                click(Page.MAGICPOINT, sleeptime=1.5)
                continue
            menupos = menures[1]
            # 按MENU直到MENU变深色匹配不出来
            clickmenu = self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_STORY_MENU), sleeptime=1),
                lambda: not match(button_pic(ButtonName.BUTTON_STORY_MENU))
            )
            # 点击跳过直到看到蓝色确认按钮
            clickskip = self.run_until(
                lambda: click((menupos[0], menupos[1] + 80), sleeptime=1),
                lambda: match(button_pic(ButtonName.BUTTON_CONFIRMB)),
                times=3
            )
            if not clickskip:
                logging.info("跳过剧情被打断，重试")
                continue
            # 点击蓝色确认按钮，直到看不到蓝色确认按钮
            clickconfirmb = self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB), sleeptime=1),
                lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMB)),
                times=3
            )
            if clickmenu and clickskip and clickconfirmb:
                logging.info("跳过剧情成功")
                return
            else:
                logging.info("跳过剧情被打断，重试")
        raise Exception("跳过剧情失败，可能是剧情按钮的图片变化了，请反馈")
     
    def post_condition(self) -> bool:
        return not match(button_pic(ButtonName.BUTTON_CONFIRMB))