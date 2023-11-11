from typing import override
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from AllPage.Page import Page
from AllTask.Task import Task

from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_number

class NormalQuest(Task):
    def __init__(self, questlist, name="NormalQuest") -> None:
        super().__init__(name)
        self.questlist = questlist

    @override
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)
    
    @override
    def on_run(self) -> None:
        super().on_run()

    @override
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)