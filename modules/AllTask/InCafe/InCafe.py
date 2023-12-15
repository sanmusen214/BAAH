 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InCafe.InviteStudent import InviteStudent
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

# =====

from .CollectPower import CollectPower
from .TouchHead import TouchHead

class InCafe(Task):
    def __init__(self, name="InCafe", pre_times = 3, post_times = 3) -> None:
        super().__init__(name, pre_times, post_times)

     
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
        CollectPower().run()
        InviteStudent().run()
        TouchHead().run()
        # 返回主页
        Task.back_to_home()

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)