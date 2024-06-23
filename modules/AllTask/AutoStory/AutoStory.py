from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.FightQuest import FightQuest
from modules.AllTask.SubTask.SkipStory import SkipStory
from modules.AllTask.Task import Task

from modules.utils import (click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot,
                           match_pixel)


class AutoStory(Task):
    """
        主线剧情自动化

        剧情总页-主线剧情（篇，章，PAGE_STORY.png）-小节目录列表（PAGE_STORY_SELECT_SECTION.png）
    """

    def __init__(self, name="AutoStory") -> None:
        super().__init__(name)
        self.yellow_points = [
            (975, 297),
            (939, 359),
            (903, 422),
            (866, 485),
        ]
        # 黄色提示点的bgr值
        self.yellow_bgr = ((0, 170, 250), (30, 200, 255))

    def try_to_solve_new_section(self):
        """
        尝试处理完当前章节所有可点的New小节，此操作会退出小节选择页面返回上级
        """
        # 来到小节页面
        sleep(3)  # 等动画
        screenshot()
        initial_enter = True
        while True:
            # 点击New章节
            new_bool, new_pos, new_val = match(button_pic(ButtonName.BUTTON_NEW_STORY_LEVEL), returnpos=True)
            if new_bool:
                logging.info({"zh_CN": "检测到新小节，点击进入", "en_US": "New section detected, tap to enter"})
                # 点击入场
                enter_popup = self.run_until(
                    lambda: click([new_pos[0] + 467, new_pos[1] + 46]),
                    lambda: match(popup_pic(PopupName.POPUP_CHAPTER_INFO)),
                    times=3
                )
            elif not new_bool and initial_enter:
                # 如果第一次进入循环但是没有匹配上New标识，那么可能已经推到了最后一节，但是New无法识别出来
                # 手动点顶部的那一节
                logging.warn({"zh_CN": "暂未能匹配到New标识符，尝试进入最顶部小节",
                              "en_US": "Cannot match New button, try to enter the top section manually"})
                # 点击入场
                enter_popup = self.run_until(
                    lambda: click((1170, 254)),
                    lambda: match(popup_pic(PopupName.POPUP_CHAPTER_INFO)),
                    times=3
                )
            else:
                # 返回上级到主线剧情页面，离开剧情页面
                break
            # 如果匹配到章节资讯弹窗
            if enter_popup:
                # 点击开始
                logging.info({"zh_CN": "点击进入小节", "en_US": "Tap to enter the section"})
                self.run_until(
                    lambda: click((637, 518)),
                    lambda: not match(popup_pic(PopupName.POPUP_CHAPTER_INFO)),
                )
                # 进入章节后先剧情，然后可能有战斗
                SkipStory().run()
                # 尝试回到选择小节页面，后面战斗完也要考虑这个，不过那里写在FightQuest里面了
                back_to_select = self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: match(page_pic(PageName.PAGE_STORY_SELECT_SECTION)) and match_pixel(Page.MAGICPOINT,
                                                                                                Page.COLOR_WHITE),
                    times=4
                )
                if not back_to_select:
                    # 如果跳过剧情后没有回到小节选择页面，那么就是有战斗，这里传入in_main_story_mode=True让FightQuest知道不需要检测最后的奖励页面
                    # 如果走格子，就报错，目前不支持
                    if Page.is_page(PageName.PAGE_GRID_FIGHT):
                        raise Exception("目前主线章节功能不支持走格子战斗")
                    logging.info({"zh_CN": "检测到战斗，开始战斗", "en_US": "Battle detected and battle started"})
                    # 编辑部队这里左上角页面名字不一样
                    # 点击右下角开始战斗按钮
                    click((1158, 662))
                    click((1158, 662))
                    # 直接开始战斗，然后直接到AUTO切换阶段，最后不用领取奖励判断
                    FightQuest(backtopic=lambda: match(page_pic(PageName.PAGE_STORY_SELECT_SECTION)),
                               start_from_editpage=False, in_main_story_mode=True).run()
            else:
                raise Exception("未匹配到章节资讯弹窗，该剧情可能要解锁主线关卡")
            # 回到小节列表页面，新的NEW button会有一段出现动画，这里确保动画结束
            # 清除弹窗
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE) and Page.is_page(
                    PageName.PAGE_STORY_SELECT_SECTION) and match(button_pic(ButtonName.BUTTON_NEW_STORY_LEVEL)),
                times=10,
                sleeptime=1
            )
            initial_enter = False
        # 返回上级到主线剧情页面，离开剧情小节页面
        self.run_until(
            lambda: click(Page.TOPLEFTBACK),
            lambda: not Page.is_page(PageName.PAGE_STORY_SELECT_SECTION),
            times=4,
            sleeptime=2
        )

    def recognize_max_chapter(self):
        """
        在主线剧情页面识别最大的章节数
        """
        self.scroll_to_right()
        screenshot()
        lines = ocr_area((212, 296), (793, 574), multi_lines=True)
        print("ocr结果", lines)
        maxnum = 0
        for line in lines:
            if len(line[0]) >= 5 and line[0][3] == "." and line[0][4].isdigit():
                maxnum = max(maxnum, int(line[0][4]))
            # 国服直接以数字开头
            if len(line[0]) >= 2 and line[0][0].isdigit() and line[0][1] == ".":
                maxnum = max(maxnum, int(line[0][0]))
        logging.info({"zh_CN": f"最大篇章数为{maxnum}", "en_US": f"The maximum number of chapters is {maxnum}"})
        return maxnum

    def pre_condition(self) -> bool:
        return self.back_to_home()

    def on_run(self) -> None:
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            times=4,
            sleeptime=2
        )
        # 进入总剧情页面
        self.run_until(
            lambda: click(page_pic(PageName.PAGE_FIGHT_CENTER)),
            lambda: not match(page_pic(PageName.PAGE_FIGHT_CENTER)),
            times=3,
            sleeptime=2
        )
        logging.info({"zh_CN": "进入剧情页面", "en_US": "Enter Story Page"})
        # 进入主线剧情
        click((359, 368), sleeptime=0.5)
        click((359, 368), sleeptime=0.5)
        click((359, 368), sleeptime=1)
        # 可能在最终篇页面，点击左上角返回到Vol主线篇章选择页面
        click((84, 111), sleeptime=0.5)
        logging.info({"zh_CN": "进入主线剧情", "en_US": "Enter the main storyline"})
        # 一共四篇主线
        for i in range(self.recognize_max_chapter()):
            # 点下下每篇的章节，然后看右侧黄点
            if i == 0:
                # 滑动到最左边Vol1
                self.scroll_to_left()
                click((396, 242))  # Vol1
            elif i == 1:
                click((621, 464))  # Vol2
            elif i == 2:
                click((860, 250))  # Vol3
            elif i == 3:
                # 往右滑动到Vol3
                swipe((830, 375), (280, 375), durationtime=1)
                click((621, 464))  # Vol4
            elif i == 4:
                click((860, 250))  # Vol5
            sleep(1)
            screenshot()
            # 尝试匹配右侧黄点篇章-大章节
            for ind, point_pos in enumerate(self.yellow_points):
                if match_pixel(point_pos, self.yellow_bgr):
                    logging.info({"zh_CN": f"检测到篇章{i+1}新章节{ind+1}，点击进入",
                                  "en_US": "Detected chapter {i+1} New chapter {ind+1}, click to enter"})
                    self.run_until(
                        lambda: click((point_pos[0] + 10, point_pos[1] + 5)),
                        lambda: Page.is_page(PageName.PAGE_STORY_SELECT_SECTION),
                        sleeptime=1
                    )
                    # 尝试处理完当前黄点篇章所有可点的New小节
                    self.try_to_solve_new_section()
                    screenshot()
            # 全部章节都处理完了
            logging.info({"zh_CN": f"篇章{i+1}所有章节处理完毕", "en_US": f"Chapter {i+1} All chapters have been processed"})

        # 处理最终篇
        logging.info({"zh_CN": "处理最终篇","en_US": "Process final"})
        logging.warn({"zh_CN": "最终篇涉及到走格子以及攻略战，暂不支持以上部分",
                      "en_US": "The final chapter involves grid walking and strategy battles, "
                               "which are not currently supported"})
        # 点击底部最终篇蓝色按钮
        click((846, 634))
        click((846, 634))
        sleep(2)
        screenshot()
        # 尝试匹配右侧黄点篇章-大章节
        for ind, point_pos in enumerate(self.yellow_points):
            if match_pixel(point_pos, self.yellow_bgr):
                logging.info({"zh_CN": f"检测到最终篇新章节{ind+1}，点击进入",
                              "en_US": f"Detect the final new chapter {ind+1}, click to enter"})
                self.run_until(
                    lambda: click((point_pos[0] + 10, point_pos[1] + 5)),
                    lambda: Page.is_page(PageName.PAGE_STORY_SELECT_SECTION),
                    sleeptime=1
                )
                # 尝试处理完当前黄点篇章所有可点的New小节
                self.try_to_solve_new_section()
                screenshot()
        logging.info({"zh_CN": f"最终篇所有章节处理完毕", "en_US": "All chapters of the final chapter have been processed"})

    def post_condition(self) -> bool:
        return self.back_to_home()