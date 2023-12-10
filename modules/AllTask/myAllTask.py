from modules.AllTask import *

from modules.AllPage.Page import Page

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot
import logging
import config

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

task_dict= {
    "登录游戏":EnterGame(),
    "咖啡馆":InCafe(),
    "课程表":InTimeTable(),
    "社团":InClub(),
    "悬赏通缉":InWanted(),
    "学园交流会":InExchange(),
    "战术大赛":InContest(),
    "困难关卡":InQuest(types=["hard"]),
    "活动关卡":InEvent(),
    "每日任务":CollectDailyRewards(),
    "邮件":CollectMails(),
    "普通关卡":InQuest(types=["normal"])
}

my_AllTask = AllTask()
for task_name in config.TASK_ORDER:
    if task_name not in task_dict:
        raise Exception(f"任务名:<{task_name}>不存在, 请检查config.py中的TASK_ORDER是否正确, 正确的任务名有: {list(task_dict.keys())}")
    my_AllTask.add_task(task_dict[task_name])