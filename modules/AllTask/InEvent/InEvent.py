 
import logging
import random
import time
import requests
import config

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InEvent.EventQuest import EventQuest
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area

class InEvent(Task):
    def __init__(self, name="InEvent") -> None:
        super().__init__(name)
        self.try_enter_times = 5

     
    def pre_condition(self) -> bool:
        # 通过get请求https://arona.diyigemt.com/api/v2/image?name=%E5%9B%BD%E9%99%85%E6%9C%8D%E6%B4%BB%E5%8A%A8
        # 获取国际服活动，判断是否有活动
        
        request_url = "https://arona.diyigemt.com/api/v2/image?name=%E5%9B%BD%E9%99%85%E6%9C%8D%E6%B4%BB%E5%8A%A8"
        response = requests.get(request_url)
        if response.status_code == 200:
            if len(response.json()['data']) != 0:
                logging.info("存在国际服活动")
                self.try_enter_times = 20
                return Page.is_page(PageName.PAGE_HOME)
            else:
                logging.warn("不存在国际服活动")
                self.try_enter_times = 0
                return False
        return Page.is_page(PageName.PAGE_HOME)
    
    def goto_or_back(self):
        """
        点击滚动栏，前往活动页面，否则返回上一级
        """
        if not Page.is_page(PageName.PAGE_FIGHT_CENTER) and not Page.is_page(PageName.PAGE_EVENT):
            # 如果不在Fight Center页面，返回主页然后来到Fight Center页面
            logging.warn("页面发生未知偏移，尝试修正")
            self.back_to_home()
            self.run_until(
                lambda: click((1196, 567)),
                lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            )
        # 尝试前往活动页面
        logging.info("尝试前往活动页面")
        self.run_until(
            lambda: click((105, 162), sleeptime=1.5),
            lambda: not Page.is_page(PageName.PAGE_FIGHT_CENTER)
        )
        # 如果不是活动页面，返回上一级
        if not Page.is_page(PageName.PAGE_EVENT):
            logging.info("不是活动页面，返回上一级")
            click(Page.TOPLEFTBACK, sleeptime=random.random()*6)
        else:
            return
            
     
    def on_run(self) -> None:
        # 进入Fight Center
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
        )
        # 进入Event
        self.run_until(
            lambda: self.goto_or_back(),
            lambda: Page.is_page(PageName.PAGE_EVENT),
            times=self.try_enter_times
        )
        
        if not Page.is_page(PageName.PAGE_EVENT):
            logging.warn("未能成功进入Event页面")
            return
        else:
            logging.info("进入Event页面")
        today = time.localtime().tm_mday
        if len(config.EVENT_QUEST_LEVEL) != 0:
            # 可选任务队列不为空时
            quest_loc = today%len(config.EVENT_QUEST_LEVEL)
            # 得到要执行的QUEST LIST
            # [[10, -1],[11, -1]]
            quest_list = config.EVENT_QUEST_LEVEL[quest_loc]
            # 序号转下标
            quest_list_2 = [[x[0]-1,x[1]] for x in quest_list]
            # do HARD QUEST
            EventQuest(quest_list_2).run()

     
    def post_condition(self) -> bool:
        return self.back_to_home()