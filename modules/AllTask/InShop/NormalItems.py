 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InShop.BuyItems import BuyItems
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config

class NormalItems(Task):
    def __init__(self, name="NormalItems") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_SHOP) and config.userconfigdict["SHOP_NORMAL"] and len(config.userconfigdict["SHOP_NORMAL"]) > 0
    
     
    def on_run(self) -> None:
        logging.info("开始普通商店购买")
        BuyItems(config.SHOP_NORMAL).run()
        for i in range(config.userconfigdict["SHOP_NORMAL_REFRESH_TIME"]):
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
                    BuyItems(config.SHOP_NORMAL).run()
                else:
                    logging.error("刷新失败")
                    click(Page.MAGICPOINT)
                    return

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_SHOP)