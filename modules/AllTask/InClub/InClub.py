 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class InClub(Task):
    def __init__(self, name="InClub") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
     
    def on_run(self) -> None:
        
        self.run_until(
            lambda: click((563, 665)),
            lambda: Page.is_page(PageName.PAGE_CLUB),
            sleeptime=2
        )
        self.run_until(
            lambda: self.back_to_home(),
            lambda: Page.is_page(PageName.PAGE_HOME),
        )
        

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)