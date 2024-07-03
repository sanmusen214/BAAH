 
from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

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
        if config.userconfigdict["SERVER_TYPE"]=="JP":
            # 适配日服新界面
            self.run_until(
                lambda: click((775, 677)),
                lambda: Page.is_page(PageName.PAGE_SHOP),
            )
        else:
            self.run_until(
                lambda: click((795, 667)),
                lambda: Page.is_page(PageName.PAGE_SHOP),
            )
        NormalItems().run()
        if not config.userconfigdict["SHOP_CONTEST_SWITCH"]: # 判断config里的开关是否开启
            logging.info("设置中未开启战术商店购买")
            return
        switchres = self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_SHOP_CONTEST_W)),
            lambda: match(button_pic(ButtonName.BUTTON_SHOP_CONTEST_B)),
        )
        if not switchres:
            logging.error({"zh_CN": "切换到竞技场商店失败，中止任务", "en_US":"Switch to contest shop failed, abort task"})
            return
        ContestItems().run()
        
        # 返回主页
        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)