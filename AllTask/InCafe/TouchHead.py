from typing import override

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName
import config
from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class TouchHead(Task):
    def __init__(self, name="TouchHead") -> None:
        super().__init__(name)

    @override
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)
    
    def click_head_and_magic(self):
        (canmatch, loc) = match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold=0.8, returnpos=True)
        if(canmatch):
            click((min(loc[0]+50, config.SCREEN_WIDTH),loc[1]))
            # 清除好感度弹窗
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: Page.is_page(PageName.PAGE_CAFE),
            )
    
    @override
    def on_run(self) -> None:
        self.run_until(
            lambda: self.click_head_and_magic(),
            lambda: not match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold = 0.9),
            times = 2, # 两次没找到注意符号就退出
            sleeptime=2
        )

    @override
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)