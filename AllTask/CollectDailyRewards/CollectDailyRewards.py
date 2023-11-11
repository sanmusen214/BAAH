 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class CollectDailyRewards(Task):
    def __init__(self, name="CollectDailyRewards") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
     
    def on_run(self) -> None:
        self.run_until(
            lambda: click((66, 237)),
            lambda: Page.is_page(PageName.PAGE_TASK_CENTER),
        )
        # collect rewards
        self.run_until(
            lambda: click(Page.MAGICPOINT) and click((1150, 671)) and click(Page.MAGICPOINT),
            lambda: match(button_pic(ButtonName.BUTTON_ALL_COLLECT_GRAY),returnpos=True)[2] > match(button_pic(ButtonName.BUTTON_ALL_COLLECT),returnpos=True)[2]
        )
        # collect 20
        self.run_until(
            lambda: click((975, 668)),
            lambda: not match(button_pic(ButtonName.BUTTON_FINISH_9_DAILY))
        )
        
        
        self.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)