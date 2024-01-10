from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep
# =====
from .Loginin import Loginin
from .CloseInform import CloseInform

class EnterGame(Task):
    def __init__(self, name="EnterGame" , pre_times = 1, post_times = 10) -> None:
        super().__init__(name, pre_times, post_times)
    
     
    def pre_condition(self) -> bool:
        if Page.is_page(PageName.PAGE_HOME):
            return False
        if match(button_pic(ButtonName.BUTTON_HOME_ICON)):
            return not self.back_to_home()
        return True
    
     
    def on_run(self) -> None:
        Loginin().run()
        CloseInform().run()
        
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)