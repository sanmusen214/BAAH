 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.configs.MyConfig import config

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class InClub(Task):
    def __init__(self, name="InClub") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return self.back_to_home()
    
     
    def on_run(self) -> None:
        click((565, 669), sleeptime=3)
        click((299, 330), sleeptime=3)
        
     
    def post_condition(self) -> bool:
        return self.back_to_home()