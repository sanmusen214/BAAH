 
import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.SkipStory import SkipStory
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot

class GridQuest(Task):
    """
    进行一次走格子战斗，一般可以从点击任务资讯里的黄色开始战斗按钮后接管
    
    从走格子界面开始到走格子战斗结束，离开战斗结算页面
    
    backtopic: 最后领完奖励回到的页面的匹配逻辑，回调函数
    """
    def __init__(self, backtopic, name="GridQuest") -> None:
        super().__init__(name)
        self.backtopic=backtopic
        self.click_magic_when_run = False

    
    def pre_condition(self) -> bool:
        click(Page.MAGICPOINT, 1)
        click(Page.MAGICPOINT, 1)
        screenshot()
        if Page.is_page(PageName.PAGE_GRID_FIGHT):
            return True
        # 可能有剧情
        SkipStory(pre_times=2).run()
        sleep(1)
        return Page.is_page(PageName.PAGE_GRID_FIGHT)
    
    
    def on_run(self) -> None:
        return
     
    def post_condition(self) -> bool:
        return True