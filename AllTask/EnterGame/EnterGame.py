from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep
# =====
from .Loginin import Loginin
from .CloseInfrom import CloseInform

class EnterGame(Task):
    def __init__(self, name="EnterGame" , pre_times = 1, post_times = 10) -> None:
        super().__init__(name, pre_times, post_times)
    
     
    def pre_condition(self) -> bool:
        if self.post_condition():
            return False
        return True
    
     
    def on_run(self) -> None:
        Loginin().run()
        CloseInform().run()
        
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)