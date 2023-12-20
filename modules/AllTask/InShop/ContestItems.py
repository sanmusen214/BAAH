 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InShop.BuyItems import BuyItems
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config

class ContestItems(Task):
    def __init__(self, name="ContestItems") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_SHOP) and hasattr(config, "SHOP_CONTEST")
    
    
    def on_run(self) -> None:
        logging.info("开始竞技场商店购买")
        BuyItems(config.SHOP_CONTEST).run()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_SHOP)