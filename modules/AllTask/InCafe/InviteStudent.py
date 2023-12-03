 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area

class InviteStudent(Task):
    def __init__(self, name="InviteStudent") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE) and match(button_pic(ButtonName.BUTTON_CAFE_CANINVITE))
    
     
    def on_run(self) -> None:
        self.run_until(
            lambda: click((834, 652)),
            lambda: match(popup_pic(PopupName.POPUP_MOMOTALK))
        )
        self.run_until(
            lambda: click((787, 225)),
            lambda: match(popup_pic(PopupName.POPUP_NOTICE))
        )
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
            lambda: not match(popup_pic(PopupName.POPUP_NOTICE))
        )
        click(Page.MAGICPOINT)
        click(Page.MAGICPOINT)
        

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)