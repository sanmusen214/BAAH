 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InCafe.InviteStudent import InviteStudent
from modules.AllTask.Task import Task
import logging
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, config

# =====

from .CollectPower import CollectPower
from .TouchHead import TouchHead

class InCafe(Task):
    def __init__(self, collect=True, touch=True, name="InCafe", pre_times = 3, post_times = 3) -> None:
        super().__init__(name, pre_times, post_times)
        self.collect = collect
        self.touch = touch

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
     
    def on_run(self) -> None:
        # 进入咖啡厅
        self.run_until(
            # 恰好是主页中的咖啡厅按钮，而又不是咖啡厅里的编辑按钮
            lambda: click((116, 687)) and click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE),
        ) 
        # 清除"今天到场的学生"弹窗
        if match(popup_pic(PopupName.POPUP_CAFE_VISITED)):
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: not match(popup_pic(PopupName.POPUP_CAFE_VISITED)),
            ) 
        if self.collect:
            # 收集体力
            CollectPower().run()
        if self.touch:
            # 摸第一个咖啡厅头
            TouchHead().run()
            config.sessiondict["CAFE_HAD_INVITED"] = False
            InviteStudent(0).run()
            if config.sessiondict["CAFE_HAD_INVITED"]:
                TouchHead(try_touch_epoch=1).run()
            else:
                logging.warn("邀请学生失败，跳过第二次摸头")
        # 检测是否有第二个咖啡厅
        if match(button_pic(ButtonName.BUTTON_CAFE_SET_ROOM)):
            # 进入第二个咖啡厅
            logging.info("进入第二个咖啡厅")
            click(button_pic(ButtonName.BUTTON_CAFE_SET_ROOM))
            click((247, 165))
            if self.touch:
                # 摸第二个咖啡厅头
                TouchHead().run()
                config.sessiondict["CAFE_HAD_INVITED"] = False
                InviteStudent(1).run()
                if config.sessiondict["CAFE_HAD_INVITED"]:
                    TouchHead(try_touch_epoch=1).run()
                else:
                    logging.warn("邀请学生失败，跳过第二次摸头")
        # 返回主页
        Task.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)