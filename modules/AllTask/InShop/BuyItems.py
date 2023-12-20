 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config
import numpy as np

class BuyItems(Task):
    def __init__(self, buyitems, name="BuyItems") -> None:
        super().__init__(name)
        self.buyitems = buyitems

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_SHOP)
    
    
    def on_run(self) -> None:
        if hasattr(config, "RESPOND_Y"):
            responsey = config.RESPOND_Y
        else:
            responsey = 40
        # 横着的四个物品的中心点
        clickable_xs = np.linspace(703, 1166, 4, dtype=int)
        for i in range(len(self.buyitems)):
            lineitems = self.buyitems[i]
            # 第一行不用翻页
            if i == 0:
                if len(lineitems) != 0:
                    for j in range(len(lineitems)):
                        itemind = lineitems[j]-1
                        logging.info(f"购买第{i+1}行第{itemind+1}个物品")
                        click((clickable_xs[itemind], 246))
            else:
                # 其他行不管点不点都翻页
                if len(lineitems) != 0:
                    for j in range(len(lineitems)):
                        itemind = lineitems[j]-1
                        logging.info(f"购买第{i+1}行第{itemind+1}个物品")
                        click((clickable_xs[itemind], 508))
                # 往下翻一行
                ScrollSelect.compute_swipe(930, 532, 260, responsey)
        # 点击购买
        # 刷新和购买按钮的中心点
        buypop = self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_SHOP_BUY)),
            lambda: match(button_pic(ButtonName.BUTTON_CONFIRMY))
        )
        if not buypop:
            logging.warn("未识别到购买按钮或弹窗中的黄色确认按钮，跳过购买")
            click(Page.MAGICPOINT)
            return
        logging.info("成功点击右下角购买")
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CONFIRMY)),
            lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMY))   
        )
        click(Page.MAGICPOINT)
        click(Page.MAGICPOINT)
        click(Page.MAGICPOINT)
        
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_SHOP)