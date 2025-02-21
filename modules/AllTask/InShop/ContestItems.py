from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InShop.BuyItems import BuyItems
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config


class ContestItems(Task):
    def __init__(self, name="ContestItems") -> None:
        super().__init__(name)

    def pre_condition(self) -> bool:
        # 有要购买的物品或者要购买所有物品
        return (Page.is_page(PageName.PAGE_SHOP) and config.userconfigdict["SHOP_CONTEST"] and
                len(config.userconfigdict["SHOP_CONTEST"]) > 0) or config.userconfigdict["SHOP_CONTEST_BUYALL"]

    def on_run(self) -> None:
        logging.info({"zh_CN": "开始竞技场商店购买", "en_US": "start shopping(Arena)"})
        BuyItems(config.userconfigdict['SHOP_CONTEST'], buyall = config.userconfigdict["SHOP_CONTEST_BUYALL"]).run()
        for i in range(config.userconfigdict["SHOP_CONTEST_REFRESH_TIME"]):
            logging.info({"zh_CN": "刷新", "en_US": "refresh"})
            # 点击刷新按钮
            showconfirm = self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_SHOP_REFRESH)),
                lambda: match(button_pic(ButtonName.BUTTON_CONFIRMY)),
                times=3
            )
            if not showconfirm:
                logging.error({"zh_CN": "刷新按钮无反应，可能刷新次数用光了",
                               "en_US": "Refresh button no response, maybe refresh times used up"})
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
                    logging.info({"zh_CN": "刷新成功", "en_US": "Refresh successfully"})
                    BuyItems(config.userconfigdict['SHOP_CONTEST'], buyall = config.userconfigdict["SHOP_CONTEST_BUYALL"]).run()
                else:
                    logging.error({"zh_CN": "刷新失败", "en_US": "Refresh failed"})
                    click(Page.MAGICPOINT)
                    return

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_SHOP)