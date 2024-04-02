 
import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.FightQuest import FightQuest
from modules.AllTask.SubTask.SkipStory import SkipStory
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel

class AutoStory(Task):
    """
        主线剧情自动化
    """
    def __init__(self, name="AutoStory") -> None:
        super().__init__(name)
        self.yellow_points = [
            (978, 290),
            (939, 354),
            (903, 419),
            (866, 482),
        ]
        # 黄色提示点的bgr值
        self.yellow_bgr = ((0, 170, 250), (30, 200, 255))
        # 剧情总页-主线剧情-某一篇某一章的章节目录

    def try_to_solve_new_section(self):
        """
        尝试处理完当前章节所有可点的New章节，此操作会退出章节选择页面返回上级
        """
        # 来到选择章节页面
        while(1):
            # 点击New章节
            new_bool, new_pos, new_val = match(button_pic(ButtonName.BUTTON_NEW_STORY_LEVEL), returnpos=True)
            if new_bool:
                logging.info("检测到新小节，点击进入")
                # 点击入场
                enter_popup = self.run_until(
                    lambda: click([new_pos[0]+467, new_pos[1]+46]),
                    lambda: match(popup_pic(PopupName.POPUP_CHAPTER_INFO)),
                    times = 3
                )
                
                # 如果匹配到弹窗，认为需要解锁主线关卡
                # if not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE) and Page.is_page(PageName.PAGE_STORY_SELECT_SECTION):
                #     logging.warn("此主线剧情需要解锁主线关卡")
                #     return
            else:
                # 返回上级到主线剧情页面
                click(Page.TOPLEFTBACK, sleeptime=1)
                return
            # 如果匹配到章节资讯弹窗
            if enter_popup:
                # 点击开始
                logging.info("点击进入章节")
                self.run_until(
                    lambda: click((637, 518)),
                    lambda: not match(popup_pic(PopupName.POPUP_CHAPTER_INFO)),
                )
                # 进入章节后先剧情，然后可能有战斗
                SkipStory().run()
                back_to_select = self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: match(page_pic(PageName.PAGE_STORY_SELECT_SECTION)),
                    times=3
                )
                if not back_to_select:
                    # 如果跳过剧情后没有回到章节选择页面，那么就是有战斗，这里传入in_story_mode=True让FightQuest知道不需要检测最后的奖励页面
                    logging.info("检测到战斗，开始战斗")
                    # 编辑部队这里右上角页面名字不一样
                    # 点击右下角开始战斗按钮
                    click((1158, 662))
                    click((1158, 662))
                    # 直接开始战斗，然后直接到AUTO切换阶段，最后不用领取奖励判断
                    FightQuest(backtopic=lambda: match(page_pic(PageName.PAGE_STORY_SELECT_SECTION)), start_from_editpage=False, in_main_story_mode=True, force_start=True).run()
            else:
                raise Exception("未匹配到章节资讯弹窗，该剧情可能要解锁主线关卡")
            # 回到选择章节页面
            # 清除弹窗
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE) and Page.is_page(PageName.PAGE_STORY_SELECT_SECTION) and match(button_pic(ButtonName.BUTTON_NEW_STORY_LEVEL)),
                times=10,
                sleeptime=1
            )
     
    def pre_condition(self) -> bool:
        return self.back_to_home()
    
     
    def on_run(self) -> None:
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入总剧情页面
        self.run_until(
            lambda: click(page_pic(PageName.PAGE_FIGHT_CENTER)),
            lambda: not match(page_pic(PageName.PAGE_FIGHT_CENTER)),
            sleeptime=3
        )
        logging.info("进入剧情页面")
        # 进入主线剧情
        click((359, 368), sleeptime=1)
        click((359, 368), sleeptime=1)
        click((359, 368), sleeptime=1)
        logging.info("进入主线剧情")
        # 一共四篇主线
        for i in range(4):
            # 点下下每篇的章节，然后看右侧黄点
            if i == 0:
                # 滑动到最左边
                self.scroll_to_left()
                click((396, 242))
            elif i==1:
                # 滑动到最左边
                self.scroll_to_left()
                click((621, 464))
            elif i == 2:
                # 滑动到最右边
                self.scroll_to_right()
                click((396, 242))
            elif i==3:
                # 滑动到最右边
                self.scroll_to_right()
                click((621, 464))
            screenshot()
            # 尝试匹配右侧黄点篇章-大章节
            for ind, point_pos in enumerate(self.yellow_points):
                if match_pixel(point_pos, self.yellow_bgr):
                    logging.info(f"检测到篇章{i+1}新章节{ind+1}，点击进入")
                    self.run_until(
                        lambda: click((point_pos[0]+10, point_pos[1]+5)),
                        lambda: Page.is_page(PageName.PAGE_STORY_SELECT_SECTION),
                        sleeptime=1
                    )
                    # 尝试处理完当前黄点篇章所有可点的New小节
                    self.try_to_solve_new_section()
                    screenshot()
            # 全部章节都处理完了
            logging.info(f"篇章{i+1}所有章节处理完毕")

        
        
     
    def post_condition(self) -> bool:
        return self.back_to_home()