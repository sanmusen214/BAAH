 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName
import config
from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
import logging
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class TouchHead(Task):
    def __init__(self, name="TouchHead") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)
    
    def click_head_and_magic(self):
        canmatchRes = match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold=0.95, returnpos=True, rotate_trans=True)
        if(canmatchRes[0]):
            logging.info("匹配到注意力符号，点击头部")
            click((min(canmatchRes[1][0]+50, 1280),canmatchRes[1][1]), sleeptime=3)
            # 清除可能的好感度弹窗
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: Page.is_page(PageName.PAGE_CAFE),
            )
            
            
    
     
    def on_run(self) -> None:
        totalruns = 3
        times_in_run = 3
        for i in range(totalruns):
            # sometimes a speak will cover the NOTICE icon, so we need to double check
            self.run_until(
                lambda: self.click_head_and_magic(),
                lambda: not match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold = 0.95, rotate_trans=True),
                times = times_in_run, # 直到找不到注意力符号
                sleeptime=1
            )
            logging.info(f"第{i+1}/{totalruns}轮摸头结束")

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)