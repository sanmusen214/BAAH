from modules.AllTask import *

from modules.AllPage.Page import Page

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot
import logging

class AllTask:
    # 单例
    def __init__(self) -> None:
        self.taskpool:list[Task] = []
    
    def run(self):
        """
        运行任务
        """
        for task in self.taskpool:
            task.run()
    
    def add_task(self, task:Task) -> None:
        """
        添加任务
        """
        self.taskpool.append(task)


my_AllTask = AllTask()
# my_AllTask.add_task(EnterGame())
# my_AllTask.add_task(InCafe())
# my_AllTask.add_task(InTimeTable())
# my_AllTask.add_task(InClub())


# my_AllTask.add_task(InWanted())
# my_AllTask.add_task(InExchange())
# my_AllTask.add_task(InContest())
my_AllTask.add_task(InEvent())
# my_AllTask.add_task(InQuest())

my_AllTask.add_task(CollectDailyRewards())
my_AllTask.add_task(CollectMails())
