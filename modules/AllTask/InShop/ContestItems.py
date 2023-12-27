 
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
        return Page.is_page(PageName.PAGE_SHOP) and hasattr(config, "SHOP_CONTEST") and len(config.configdict["SHOP_CONTEST"]) > 0
    
    
    def on_run(self) -> None:
        logging.info("开始竞技场商店购买")
        BuyItems(config.SHOP_CONTEST).run()
        for i in range(config.configdict["SHOP_CONTEST_REFRESH_TIME"]):
            logging.info("刷新")
            # 点击刷新按钮
            showconfirm = self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_SHOP_REFRESH)),
                lambda: match(button_pic(ButtonName.BUTTON_CONFIRMY)),
                times=3
            )
            if not showconfirm:
                logging.error("刷新按钮无反应，可能刷新次数用光了")
                click(Page.MAGICPOINT)
                return
            else:
                clickconfirm = self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_CONFIRMY)),
                    lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMY)),
                    times=3
                )
                # 成功刷新
                if clickconfirm:
                    logging.info("刷新成功")
                    BuyItems(config.SHOP_CONTEST).run()
                else:
                    logging.error("刷新失败")
                    click(Page.MAGICPOINT)
                    return

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_SHOP)