 
import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
import numpy as np

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config

class ScrollSelect(Task):
    """
    滑动右侧窗口点击对应关卡
    
    Parameters
    ----------
    targetind : int
        目标关卡的下标
    window_starty: 
        窗口上边缘y坐标
    first_item_endy: 
        第一个元素下边缘y坐标
    window_endy:
        窗口下边缘y坐标
    clickx: int
        滑动的基础x坐标，点击按钮的x坐标
    hasexpectimage: function
        期望点击后出现的图片判断函数，返回bool
    swipeoffsetx: int
        滑动时基础x坐标的x偏移量，防止滑动时意外点击按钮
    finalclick: bool
        是否滑动结束后点击clickx与最后一行的y
    """
    def __init__(self, targetind, window_starty, first_item_endy, window_endy, clickx, hasexpectimage, swipeoffsetx = -100, finalclick = True, name="ScrollSelect") -> None:
        # TODO: 其实只关心一个元素的高度，完全显示第一个按钮的y，完全显示贴底按钮的y,窗口容纳的完整的元素个数，最后一个元素在窗口里的那部分高度，以及向左偏移量和响应距离
        super().__init__(name)
        self.window_starty = window_starty
        self.first_item_endy = first_item_endy
        self.window_endy = window_endy
        self.targetind = targetind
        self.windowheight = window_endy - window_starty
        self.itemheight = first_item_endy - window_starty
        self.clickx = clickx
        self.hasexpectimage = hasexpectimage
        self.swipeoffsetx = swipeoffsetx
        if config.userconfigdict["RESPOND_Y"]:
            self.responsey = config.userconfigdict['RESPOND_Y']
        else:
            logging.warn("未设置滑动触发距离RESPOND_Y，使用默认值40")
            self.responsey = 40
        self.finalclick = finalclick

    
    def pre_condition(self) -> bool:
        return True
    
    @staticmethod
    def compute_swipe(x1, y1, distance, responsey):
        """
        纵向从下向上滑动，实际滑动距离根据两目标点距离distance计算，考虑惯性
        """
        distance = abs(distance)
        logging.debug(f"滑动距离: {distance}")
        # 0-50
        if distance<50:
            swipe((x1, y1), (x1, y1-(distance+responsey)), 2)
        else:
            # 国服滑动有效距离为60
            swipe((x1, y1), (x1, int(y1-(distance+responsey-4*(1+distance/100)))), 1+distance/100)
            # swipe((x1, y1), (x1, y1-(200+40-4*3)), 3)
            # swipe((x1, y1), (x1, y1-(300+40-4*4)), 4)
            # swipe((x1, y1), (x1, y1-(400+40-4*5)), 5)
    
    def on_run(self) -> None:
        logging.info("滑动选取第{}个关卡".format(self.targetind+1))
        self.scroll_right_up(scrollx=self.clickx + self.swipeoffsetx)
        # 计算一个页面包含多少个完整的元素
        itemcount = self.windowheight // self.itemheight
        # 计算该页面最后那一个不完整的元素占了多高
        lastitemheight = self.windowheight % self.itemheight
        # 不完整的元素下方还有多少
        hiddenlastitemheight = self.itemheight - lastitemheight
        # 第一个元素高度中心点
        start_center_y = self.window_starty + self.itemheight // 2
        # 当页最后一个完整元素高度中心点
        end_center_y = start_center_y + (itemcount - 1) * self.itemheight
        # 如果目标元素就在当前页面
        if self.targetind < itemcount:
            # 目标元素高度中心点
            target_center_y = start_center_y + self.itemheight * self.targetind
            if self.finalclick:
                self.run_until(
                    lambda: click((self.clickx, target_center_y)),
                    lambda: self.hasexpectimage(),
                )
        else:
            # 从关卡中间的空隙开始滑
            scroll_start_from_y = self.window_endy - self.itemheight // 2
            # 目标元素在之后的页面
            # 计算页面应该滑动多少
            scrolltotal_distance = (self.targetind - itemcount) * self.itemheight + hiddenlastitemheight
            logging.debug("最后一个元素隐藏高度: %d" % hiddenlastitemheight)
            # 先把hidden滑上来，多一点距离让ba响应这是个滑动事件
            self.compute_swipe(self.clickx+self.swipeoffsetx, scroll_start_from_y,hiddenlastitemheight, self.responsey)
            logging.debug(f"滑动距离: {hiddenlastitemheight}")
            # 更新scrolltotal_distance
            scrolltotal_distance -= hiddenlastitemheight
            # 还需要往上滑(self.targetind - itemcount) * self.itemheight
            # 重要：每次先划itemcount-1个元素的高度
            if itemcount==1:
                scroll_distance = itemcount * self.itemheight
            else:
                scroll_distance = (itemcount - 1) * self.itemheight
            while scroll_distance <= scrolltotal_distance:
                self.compute_swipe(self.clickx+self.swipeoffsetx, scroll_start_from_y, scroll_distance, self.responsey)
                scrolltotal_distance -= scroll_distance
            if scrolltotal_distance > 5:
                # 最后一次滑动
                self.compute_swipe(self.clickx + self.swipeoffsetx, scroll_start_from_y, scrolltotal_distance, self.responsey)
            if self.finalclick:
                # 点击最后一行
                self.run_until(
                    lambda: click((self.clickx, self.window_endy - self.itemheight // 2)),
                    self.hasexpectimage
                )
            

    
    def post_condition(self) -> bool:
        return True