from typing import override

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName
import config
from AllPage.Page import Page
from AllTask.Task import Task
import logging
from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class TouchHead(Task):
    def __init__(self, name="TouchHead") -> None:
        super().__init__(name)

    @override
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)
    
    def click_head_and_magic(self):
        canmatchRes = match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold=0.95, returnpos=True)
        if(canmatchRes[0]):
            logging.info("匹配到注意力符号，点击头部")
            click((min(canmatchRes[1][0]+50, config.SCREEN_WIDTH),canmatchRes[1][1]))
            # 清除可能的好感度弹窗
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: Page.is_page(PageName.PAGE_CAFE),
            )
            
            
    
    @override
    def on_run(self) -> None:
        for i in range(2):
            # sometimes a speak will cover the NOTICE icon, so we need to double check
            self.run_until(
                lambda: self.click_head_and_magic(),
                lambda: not match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold = 0.95),
                times = 3, # 至多运行3次，直到找不到注意力符号
                sleeptime=2
            )
            logging.info(f"第{i+1}轮摸头结束，尝试第{i+2}轮")
            sleep(2)

    @override
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)