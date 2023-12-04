 
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
                return False
        return Page.is_page(PageName.PAGE_HOME)
    
    def goto_or_back(self):
        """
        点击滚动栏，前往活动页面，否则返回上一级
        """
        for i in range(self.try_enter_times):
            logging.info("尝试第{}次进入活动页面".format(i+1))
            self.run_until(
                lambda: click((105, 162)),
                lambda: not Page.is_page(PageName.PAGE_FIGHT_CENTER)
            )
            if not Page.is_page(PageName.PAGE_EVENT):
                click(Page.TOPLEFTBACK, sleeptime=random.random()*5)
            else:
                return
            
     
    def on_run(self) -> None:
        # 进入Fight Center
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER)
        )
        # 进入Event
        self.goto_or_back()
        
        if not Page.is_page(PageName.PAGE_EVENT):
            logging.warn("Reach max try times, Can not enter Event page")
            return
        else:
            logging.info("Enter Event page")
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