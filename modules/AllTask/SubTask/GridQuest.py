 
import logging
import os

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.FightQuest import FightQuest
from modules.AllTask.SubTask.SkipStory import SkipStory
from modules.AllTask.Task import Task

import json

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, get_screenshot_cv_data, match_pixel

from modules.utils.grid_analyze import GridAnalyzer

class GridQuest(Task):
    """
    进行一次走格子战斗，一般可以从点击任务资讯里的黄色开始战斗按钮后接管
    
    从走格子界面开始到走格子战斗结束，离开战斗结算页面。skip开，phase自动结束关
    
    一个GridQuest实例对应一个目标（三星或拿钻石）
    
    Parameters
    ==========
        grider: 
            读取过json的GridAnalyzer对象
        backtopic: 
            最后领完奖励回到的页面的匹配逻辑，回调函数
    """
    
    BUTTON_TASK_START = (1171, 668)
    BUTTON_TASK_INFO = (996, 665)
    BUTTON_SEE_OTHER_TEAM = (82, 554)
    
    def __init__(self, grider:GridAnalyzer, backtopic, require_type="3star", name="GridQuest") -> None:
        super().__init__(name)
        self.backtopic=backtopic
        self.grider=grider
        self.require_type = require_type
        
        # 当前关注的队伍下标
        self.now_focus_on_team = 0
        # 用于本策略的队伍名字，字母列表，["A","B","C"...]
        self.team_names = []

    
    def pre_condition(self) -> bool:
        click(Page.MAGICPOINT, 1)
        click(Page.MAGICPOINT, 1)
        screenshot()
        if Page.is_page(PageName.PAGE_GRID_FIGHT):
            return True
        # 可能有剧情
        SkipStory(pre_times=2).run()
        return Page.is_page(PageName.PAGE_GRID_FIGHT)
    
    def wait_end(self):
        """
        点击右下任务资讯，等待战斗结束可以弹出弹窗，然后点击魔法点关掉弹窗
        """
        # 如果返回到了self.backtopic()指定的页面，那么直接返回
        if self.backtopic():
            return True
        self.run_until(
            lambda: click(self.BUTTON_TASK_INFO),
            lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
            times=15,
            sleeptime=1.5
        )
        self.run_until(
            lambda: click(Page.MAGICPOINT, 1),
            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
        )
    
    def get_now_focus_on_team(self):
        """
        得到当前注意的队伍
        """
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
        )
        # 识别左下角切换队伍的按钮文字
        now_team_str, loss = ocr_area((72, 544), (91, 569), multi_lines=False)
        nowteam_ind = int(now_team_str)-1
        self.now_focus_on_team = nowteam_ind
        return nowteam_ind
        
    
    def on_run(self) -> None:
        # 尝试读取json文件
        # 没有读取到json文件
        if self.grider.level_data is None:
            logging.error(f"关卡文件{self.grider.jsonfilename}读取失败")
            self.run_until(
                lambda: click(Page.TOPLEFTBACK),
                lambda: self.backtopic(),
                sleeptime=2
            )
            return False
        # 设置队伍数量
        self.team_names = [item["name"] for item in self.grider.get_initialteams(self.require_type)]
        # TODO: 配队
        
        # ==========开打！============
        # 点击任务开始
        click(self.BUTTON_TASK_START, sleeptime=1)
        for step_ind in range(self.grider.get_num_of_steps(self.require_type)):
            # 循环每一个回合
            actions = self.grider.get_action_of_step(self.require_type, step_ind)
            for action_ind in range(len(actions)):
                action = actions[action_ind]
                # 循环回合的每一个action
                target_team_ind = self.team_names.index(action["team"])
                # 聚焦到目标队伍，每次都获取最新的当前聚焦队伍
                while(self.get_now_focus_on_team()!=target_team_ind):
                    click(self.BUTTON_SEE_OTHER_TEAM, sleeptime=1)
                logging.info(f'当前聚焦队伍{self.team_names[self.now_focus_on_team]}')
                logging.info(f'执行step:{step_ind} action:{action_ind} 队伍{action["team"]}->{action["action"]} {action["target"]}')
                sleep(1.5)
                # 专注到一个队伍上后，分析队伍当前位置
                screenshot()
                # 先提取，后knn
                try:
                    knn_positions, _, _ = self.grider.multikmeans(self.grider.get_mask(get_screenshot_cv_data(), self.grider.PIXEL_MAIN_YELLOW), 1)
                    print(knn_positions)
                    target_team_position = knn_positions[0]
                    # 根据攻略说明，偏移队伍位置得到点击的位置
                    offset_pos = self.grider.WALK_MAP[action["target"]]
                    # 前后反，将数组下标转为图像坐标
                    need_click_position = [int(target_team_position[1]+offset_pos[1]), int(target_team_position[0]+offset_pos[0])]
                except Exception as e:
                    logging.error(e)
                    logging.error("队伍位置识别失败，这通常是由于攻略配置文件不正确导致的，请反馈给开发者")
                    raise Exception("队伍位置识别失败")
                # 点击使其移动
                logging.info(f'点击{need_click_position}')
                click(need_click_position, sleeptime=1)
                if action_ind==len(actions)-1 and step_ind==self.grider.get_num_of_steps(self.require_type)-1:
                    # 打boss咯，必须局内
                    sleep(5)
                    FightQuest(self.backtopic, start_from_editpage=False).run()
                else:
                    # 可能触发打斗
                    self.wait_end()
            # 回合结束，手动点击PHASE结束，有时候有的队伍还可以走，就点击确认按钮
            logging.info("PHASE结束")
            click(self.BUTTON_TASK_START, sleeptime=1)
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
            )
            # 一个回合结束，等敌方行动结束
            self.wait_end()
        
        
     
    def post_condition(self) -> bool:
        return self.backtopic()