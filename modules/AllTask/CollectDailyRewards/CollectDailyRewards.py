 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, match_pixel

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
        # 清除弹窗
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
        )
        # collect 20
        self.run_until(
            lambda: click((975, 668)),
            lambda: not match(button_pic(ButtonName.BUTTON_FINISH_9_DAILY))
        )
        
        
        self.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)