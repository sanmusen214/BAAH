 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

class CloseInform(Task):
    def __init__(self, name="CloseInform", pre_times = 3, post_times = 3) -> None:
        super().__init__(name, pre_times, post_times)

     
    def pre_condition(self) -> bool:
        if not match(popup_pic(PopupName.POPUP_LOGIN_FORM)):
            return False
        return True
    
     
    def on_run(self) -> None:
        click((1226, 56))
        click(Page.MAGICPOINT)

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)