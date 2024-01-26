 
import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.SkipStory import SkipStory
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config

class FightQuest(Task):
    """
    从编辑部队页面开始，进入到游戏内战斗，然后到战斗结束，离开战斗结算页面
    
    backtopic: 最后领完奖励回到的页面的匹配图片
    """
    def __init__(self, backtopic, name="FightQuest") -> None:
        super().__init__(name)
        self.backtopic=backtopic

    
    def pre_condition(self) -> bool:
        click(Page.MAGICPOINT)
        click(Page.MAGICPOINT, 1)
        if Page.is_page(PageName.PAGE_EDIT_QUEST_TEAM):
            return True
        # 可能有剧情
        SkipStory(pre_times=1).run()
        return Page.is_page(PageName.PAGE_EDIT_QUEST_TEAM)
    
    
    def on_run(self) -> None:
        # 点击出击按钮
        self.run_until(
            lambda: click((1106, 657)) and click(Page.MAGICPOINT),
            lambda: not Page.is_page(PageName.PAGE_EDIT_QUEST_TEAM),
            sleeptime = 2
        )
        # 战斗中
        logging.info("战斗中...")
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match(button_pic(ButtonName.BUTTON_FIGHT_RESULT_CONFIRMB)) or match(button_pic(ButtonName.BUTTON_CONFIRMY)),
            times = 75,
            sleeptime = 2
        )
        # 结束时如果是黄色确认，那么战斗失败
        if match(button_pic(ButtonName.BUTTON_CONFIRMY)):
            logging.info("战斗失败")
        else:
            # 战斗结算页面
            # 四人界面 右下确认蓝色
            logging.info("战斗胜利")
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_FIGHT_RESULT_CONFIRMB)) and click(Page.MAGICPOINT),
                lambda: not match(button_pic(ButtonName.BUTTON_FIGHT_RESULT_CONFIRMB)),
                times=5,
                sleeptime=1
            )
        # 战斗后可能剧情
        # 先看有没有出现黄色结算，有结算那肯定没剧情
        hasconfirmy = self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match(button_pic(ButtonName.BUTTON_CONFIRMY)),
            times = 3
        )

        if not hasconfirmy:
            SkipStory(pre_times=5).run()
        # 奖励界面 中下确认黄色
        # 获得奖励，右下确认黄色（左边返回大厅）
        logging.info("点击确认...")
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CONFIRMY)) and click(Page.MAGICPOINT),
            lambda: match(self.backtopic),
            times=7,
            sleeptime=1
        )
     
    def post_condition(self) -> bool:
        return match(self.backtopic)