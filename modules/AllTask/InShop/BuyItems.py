from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

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
        if config.userconfigdict["RESPOND_Y"]:
            responsey = config.userconfigdict['RESPOND_Y']
        else:
            responsey = 40
        # 横着的四个物品的中心点
        clickable_xs = np.linspace(703, 1166, 4, dtype=int)
        # 总共购买的物品数量
        totalbuy = 0
        for i in range(len(self.buyitems)):
            lineitems = self.buyitems[i]
            # 重塑linetimes，兼容内部单个物品的元素存储了 数字 或【数字，开关】两种情况
            # 移除开关为False的元素，开关打开的元素只保留数字
            for j in range(len(lineitems)-1, -1, -1):
                if (isinstance(lineitems[j], list) or isinstance(lineitems[j], tuple)):
                    # 元素存储了开关，是列表形式
                    if not lineitems[j][-1]:
                        # 开关关闭，移除该元素
                        lineitems.pop(j)
                    else:
                        # 如果开关打开，那么只保留该元素的数字
                        lineitems[j] = lineitems[j][0]
            # 此时lineitems应该是一个一维数字列表
            logging.info("lineitems: " + str(lineitems))
            # 第一行不用翻页
            if i == 0:
                if len(lineitems) != 0:
                    for j in range(len(lineitems)):
                        itemind = lineitems[j] - 1
                        # 判断itemind是否在clickable_xs有效范围内
                        if itemind < 0 or itemind > 3:
                            logging.warn({"zh_CN": f"第{i + 1}行第{itemind + 1}个物品不在有效范围内，跳过",
                                          "en_US": f"The item is not in the valid range, "
                                                   f"skipping the item in line {i + 1}:{itemind + 1}"})
                        else:
                            logging.info({"zh_CN": f"购买第{i + 1}行第{itemind + 1}个物品",
                                          "en_US": f"Purchase item {itemind + 1} on line {i + 1}"})
                            click((clickable_xs[itemind], 200))
                            totalbuy += 1
            else:
                # 其他行不管点不点都翻页
                if len(lineitems) != 0:
                    for j in range(len(lineitems)):
                        itemind = lineitems[j] - 1
                        # 判断itemind是否在clickable_xs有效范围内
                        if itemind < 0 or itemind > 3:
                            logging.warn({"zh_CN": f"第{i + 1}行第{itemind + 1}个物品不在有效范围内，跳过",
                                          "en_US": f"The item is not in the valid range, "
                                                   f"skipping the item in line {i + 1}:{itemind + 1}"})
                            # 还是要往下翻一行！
                        else:
                            logging.info({"zh_CN": f"购买第{i + 1}行第{itemind + 1}个物品",
                                          "en_US": f"Purchase item {itemind + 1} on line {i + 1}"})
                            click((clickable_xs[itemind], 450))
                            totalbuy += 1
                # 往下翻一行
                click(Page.MAGICPOINT)
                ScrollSelect.compute_swipe(930, 532, 260, responsey)
        # 点击购买
        # 刷新和购买按钮的中心点
        if totalbuy == 0:
            click(Page.MAGICPOINT)
            return
        buypop = self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_SHOP_BUY)),
            lambda: match(button_pic(ButtonName.BUTTON_CONFIRMY)),
            times=3
        )
        if not buypop:
            logging.warn({"zh_CN": "未识别到购买按钮或弹窗中的黄色确认按钮，跳过购买",
                          "en_US": "Could not identify the purchase button or the yellow confirmation button "
                                   "in the popup, skipping purchase"})
            click(Page.MAGICPOINT)
            click(Page.MAGICPOINT)
            click(Page.MAGICPOINT)
            return
        logging.info({"zh_CN": "成功点击右下角购买", "en_US": "Successfully clicked to buy in the lower right corner"})
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CONFIRMY)),
            lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMY)),
            times=3
        )
        click(Page.MAGICPOINT)
        click(Page.MAGICPOINT)
        click(Page.MAGICPOINT)

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_SHOP)