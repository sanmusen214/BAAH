from typing import override

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class CollectMails(Task):
    def __init__(self, name="CollectMails") -> None:
        super().__init__(name)

    @override
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
    @override
    def on_run(self) -> None:
        self.run_until(
            lambda: click((1143, 38)),
            lambda: Page.is_page(PageName.PAGE_MAILBOX)
        )
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_ONE_COLLECT)),
            lambda: not match(button_pic(ButtonName.BUTTON_ONE_COLLECT)),
            times=2
        )
        self.back_to_home()

    @override
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)