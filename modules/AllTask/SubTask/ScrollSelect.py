 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

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
        点击的x坐标
    hasexpectimage: function
        期望点击后出现的图片判断函数，返回bool
    """
    def __init__(self, targetind, window_starty, first_item_endy, window_endy, clickx, hasexpectimage, responddis=5, name="ScrollSelect") -> None:
        super().__init__(name)
        self.window_starty = window_starty
        self.first_item_endy = first_item_endy
        self.window_endy = window_endy
        self.targetind = targetind
        self.windowheight = window_endy - window_starty
        self.itemheight = first_item_endy - window_starty
        self.clickx = clickx
        self.hasexpectimage = hasexpectimage
        self.respoddis = responddis

    
    def pre_condition(self) -> bool:
        return True
    
     
    def on_run(self) -> None:
        self.scroll_right_up(scrollx=self.clickx)
        # 计算一个页面包含多少个完整的元素
        itemcount = self.windowheight // self.itemheight
        print("itemcount: ", itemcount)
        # 计算该页面最后那一个不完整的元素占了多高
        lastitemheight = self.windowheight % self.itemheight
        # 不完整的元素下方还有多少
        hiddenlastitemheight = self.itemheight - lastitemheight
        # 第一个元素高度中心点
        start_center_y = self.window_starty + self.itemheight // 2
        print("start_center_y: ", start_center_y)
        # 当页最后一个完整元素高度中心点
        end_center_y = start_center_y + (itemcount - 1) * self.itemheight
        print("end_center_y: ", end_center_y)
        # 如果目标元素就在当前页面
        if self.targetind < itemcount:
            print("targetind: ", self.targetind)
            # 目标元素高度中心点
            target_center_y = start_center_y + self.itemheight * self.targetind
            self.run_until(
                lambda: click((self.clickx, target_center_y)),
                lambda: self.hasexpectimage(),
            )
        else:
            # 重要：从关卡中间的空隙开始滑
            scroll_start_from_y = end_center_y - self.itemheight // 2
            # 目标元素在之后的页面
            # 计算页面应该滑动多少
            scrolltotal_distance = (self.targetind - itemcount) * self.itemheight + hiddenlastitemheight
            print("scrolltotal_distance: ", scrolltotal_distance)
            # 先把hidden滑上来，多一点距离让ba响应这是个滑动事件
            print("self.clickx: ", self.clickx, "scroll_start_from_y: ", scroll_start_from_y, "hiddenlastitemheight: ", hiddenlastitemheight)
            swipe((self.clickx, scroll_start_from_y), (self.clickx, scroll_start_from_y - hiddenlastitemheight - self.respoddis), 2)
            print("hiddenlastitemheight: ", hiddenlastitemheight)
            # 更新scrolltotal_distance
            scrolltotal_distance -= hiddenlastitemheight
            # 还需要往上滑(self.targetind - itemcount) * self.itemheight
            # 重要：每次先划itemcount-1个元素的高度
            scroll_distance = (itemcount - 1) * self.itemheight
            while scroll_distance <= scrolltotal_distance:
                print("scrolltotal_distance: ", scrolltotal_distance)
                swipe((self.clickx, scroll_start_from_y), (self.clickx, scroll_start_from_y - scroll_distance - self.respoddis), 2)
                scrolltotal_distance -= scroll_distance
            if scrolltotal_distance > 5:
                # 最后一次滑动
                swipe((self.clickx, scroll_start_from_y), (self.clickx, scroll_start_from_y - scrolltotal_distance - self.respoddis), 1)
            print(f"滑动结束, {self.window_endy}, {self.itemheight//2}")
            self.run_until(
                lambda: click((self.clickx, self.window_endy - self.itemheight // 2)),
                self.hasexpectimage
            )
            

    
    def post_condition(self) -> bool:
        return True