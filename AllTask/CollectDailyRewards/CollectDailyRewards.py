from typing import override

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class CollectDailyRewards(Task):
    def __init__(self, name="CollectDailyRewards") -> None:
        super().__init__(name)

    @override
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
    @override
    def on_run(self) -> None:
        self.run_until(
            lambda: click((66, 237)),
            lambda: Page.is_page(PageName.PAGE_TASK_CENTER),
        )
        # collect all
        click((1150, 671))
        sleep(1)
        click(Page.MAGICPOINT)
        # collect 20
        click((975, 668))
        self.back_to_home()
        # collect all
        click((1150, 671))
        sleep(1)
        click(Page.MAGICPOINT)

    @override
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)