from modules.AllTask import *

from modules.AllPage.Page import Page

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot
import logging
from modules.utils.MyConfig import config

    
task_dict= {
    "登录游戏":[EnterGame,{}],
    "咖啡馆":[InCafe,{}],
    "咖啡馆只摸头":[InCafe,{'collect':False}],
    "课程表":[InTimeTable,{}],
    "社团":[InClub,{}],
    "商店":[InShop,{}],
    "悬赏通缉":[InWanted,{}],
    "特殊任务":[InSpecial,{}],
    "学园交流会":[InExchange,{}],
    "战术大赛":[InContest, {'collect':False}],
    "困难关卡":[InQuest, {'types':["hard"]}],
    "活动关卡":[InEvent,{}],
    "每日任务":[CollectDailyRewards,{}],
    "邮件":[CollectMails,{}],
    "普通关卡":[InQuest, {'types':["normal"]}],
}

class AllTask:

    # 单例
    def __init__(self) -> None:
        self.parse_task()
        
    def parse_task(self) -> None:
        """
        从config里解析任务列表，覆盖原有的任务列表
        """
        self.taskpool = []
        # 用于保存最后一次战术大赛的任务实例
        last_contest = None
        # GUI之前会运行到这里，所以这里需要判断一下
        if "TASK_ORDER" in config.__dict__ and "TASK_ACTIVATE" in config.__dict__:
            # 把config的任务列表转换成任务实例列表
            for i in range(len(config.TASK_ORDER)):
                task_name = config.TASK_ORDER[i]
                if task_name not in task_dict:
                    raise Exception(f"任务名:<{task_name}>不存在, 请检查config.py中的TASK_ORDER是否正确, 正确的任务名有: {list(task_dict.keys())}")
                # 如果任务对应的TASK_ACTIVATE为False，则不添加任务
                if config.TASK_ACTIVATE[i] == False:
                    continue
                self.add_task(task_dict[task_name][0](**task_dict[task_name][1]))
                if task_name == "战术大赛":
                    last_contest = self.taskpool[-1]
            # 将最后一次战术大赛的收集奖励设置为True
            if last_contest:
                last_contest.set_collect(True)
        else:
            logging.error("配置文件严重错误，请删除config.json后打开GUI.exe生成config.py文件或进群询问")
        
        
    
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