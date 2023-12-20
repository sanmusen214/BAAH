 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InShop.ContestItems import ContestItems
from modules.AllTask.InShop.NormalItems import NormalItems
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.Task import Task

import numpy as np

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config

class InShop(Task):
    def __init__(self, name="InShop") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
     
    def on_run(self) -> None:
        # 进入商店
        self.run_until(
            lambda: click((795, 667)),
            lambda: Page.is_page(PageName.PAGE_SHOP),
        )
        NormalItems().run()
        switchres = self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_SHOP_CONTEST_W)),
            lambda: match(page_pic(PageName.PAGE_SHOP_CONTEST)),
        )
        if not switchres:
            logging.error("切换到竞技场商店失败，中止任务")
            return
        ContestItems().run()

        
            

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)