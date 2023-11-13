 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep
import logging

class InContest(Task):
    def __init__(self, name="InContest") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
     
    def on_run(self) -> None:
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        canincontest = self.run_until(
            lambda: click((1093, 500)),
            lambda: Page.is_page(PageName.PAGE_CONTEST)
        )
        if not canincontest:
            logging.warning("Can't open contest page, task quit")
            self.back_to_home()
            return
        # click the first enemy
        self.run_until(
            lambda: click((994, 241)),
            lambda: match(popup_pic(PopupName.POPUP_CONTEST_TARGET))
        )
        # click the start button in the popup
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_EDIT)),
            lambda: Page.is_page(PageName.PAGE_EDIT_TEAM) or match(popup_pic(PopupName.POPUP_NOTICE))
        )
        
        if match(popup_pic(PopupName.POPUP_NOTICE)):
            # if no ticket
            logging.warning("No ticket, try to collect rewards and quit this task...")
            # close all popup
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: not match(popup_pic(PopupName.POPUP_CONTEST_TARGET))
            )
        else:
            # Enter Editting Team Page
            # check whether jump option is open
            # if not, tick it
            self.run_until(
                lambda: click((1144, 602)),
                lambda: match(button_pic(ButtonName.BUTTON_JUMP), returnpos=True)[2]>match(button_pic(ButtonName.BUTTON_NOT_JUMP), returnpos=True)[2]
            )
            # go fight and return to the Fight Result Popup
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_GOFIGHT)),
                lambda: match(popup_pic(PopupName.POPUP_FIGHT_RESULT))
            )
            # click magic point to close the Result popup, back to pure contest page
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: not match(popup_pic(PopupName.POPUP_FIGHT_RESULT))
            )
        # receive the reward
        self.run_until(
            self.collect_and_magic,
            lambda: match(button_pic(ButtonName.BUTTON_CONTEST_COLLECT_BOTH_GRAY)),
            times = 4
        )
        self.back_to_home()

    def collect_and_magic(self):
        click((352, 388))
        click((354, 467))
        sleep(1)
        click(Page.MAGICPOINT)



     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)