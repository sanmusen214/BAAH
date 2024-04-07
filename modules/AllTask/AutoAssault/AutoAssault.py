
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.AutoAssault.CollectAssaultReward import CollectAssaultReward
from modules.AllTask.SubTask.FightQuest import FightQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.SubTask.SkipStory import SkipStory
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel
from modules.utils.log_utils import logging

class AutoAssault(Task):
    def __init__(self, name="AutoAssault") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return self.back_to_home()
    
    def scroll_to_ind(self, target_ind: int) -> None:
        """定位到目标下标关卡的按钮位置""" 
        # 清除弹窗
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
            sleeptime=0.5
        )
        scroll_to_ind = ScrollSelect(target_ind, 159, 293, 597, 1156, lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE), swipeoffsetx=-200, finalclick=False)
        scroll_to_ind.run()
        return scroll_to_ind.wantclick_pos
    
    def check_unlock(self, target_ind: int) -> int:
        """检查下标处的关卡是否解锁了，返回没有解锁的最小下标"""
        res = -1
        # 先直接检查目标下标，如果能有弹窗，说明已经解锁了
        logging.info(f"检查总力战第{target_ind+1}关是否解锁")
        button_pos = self.scroll_to_ind(target_ind)
        has_popup = self.run_until(
            lambda xy=button_pos: click(xy),
            lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
            times=3,
            sleeptime=0.5
        )
        if has_popup:
            logging.info(f"总力战第{target_ind+1}关已解锁")
            res = -1
        else:
            # 从头开始检查,找到第一个未解锁的关卡
            for ind in range(target_ind):
                # 检查是否解锁
                button_pos = self.scroll_to_ind(ind)
                has_popup = self.run_until(
                    lambda xy=button_pos: click(xy),
                    lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
                    times=3,
                    sleeptime=0.5
                )
                if not has_popup:
                    res = ind
                    break
        # 清除弹窗
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
            sleeptime=0.5
        )
        return res
    
    def on_run(self) -> None:
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入总力战
        # 适配日服
        self.run_until(
            lambda: click((872, 447)) and click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_ASSAULT) or match(button_pic(ButtonName.BUTTON_STORY_MENU)),
        )
        if match(button_pic(ButtonName.BUTTON_STORY_MENU)):
            SkipStory().run()
            # 关闭可能弹窗
            for i in range(5):
                click(Page.MAGICPOINT)
            
        screenshot()
        # 检查是否到总力战界面
        if not Page.is_page(PageName.PAGE_ASSAULT):
            logging.error("未能进入总力战页面，任务结束")
            return
        target_ind = config.userconfigdict["AUTO_ASSAULT_LEVEL"] - 1
        # 检查所需要的下标是否解锁了
        unlock_level = self.check_unlock(target_ind)
        if unlock_level != -1:
            logging.warn("总力战第{}关未解锁，最高解锁关卡为第{}关".format(target_ind+1, unlock_level))
            next_ind = unlock_level - 1
        else:
            next_ind = target_ind
        while(1):
            # 平推一次next_ind
            pos = self.scroll_to_ind(next_ind)
            canopen_popup = self.run_until(
                lambda: click(pos),
                lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
                times = 2,
                sleeptime = 1
            )
            if not canopen_popup:
                logging.error("尝试打开总力战第{}关时未能匹配到弹窗，总力战任务结束".format(next_ind+1))
                CollectAssaultReward().run()
                return
            # 点击入场按钮,离开总力战页面
            logging.info("编辑队伍")
            self.run_until(
                lambda: click((1018, 526)),
                lambda: not Page.is_page(PageName.PAGE_ASSAULT) or match(popup_pic(PopupName.POPUP_NOTICE)),
            )
            if match(popup_pic(PopupName.POPUP_NOTICE)):
                logging.error("总力战第{}关未能进入（或是无票卷了），总力战任务结束".format(next_ind+1))
                CollectAssaultReward().run()
                return
            sleep(2)
            # 配队页面点击右下出击按钮
            logging.info("出击")
            open_confirm = self.run_until(
                lambda: click((1157, 662)),
                lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
            )
            # 如果没有打开确认弹窗，那么此队伍没有配队
            if not open_confirm:
                raise Exception("总力战队伍配置错误，任务结束")
            # 确认 - 跳过演出
            self.run_until(
                lambda: [click(button_pic(ButtonName.BUTTON_CONFIRMB)), click(button_pic(ButtonName.BUTTON_CONFIRMY), threshold=0.85), click((1100, 150))],  # 这里点MAGICPOINT没反应，点屏幕右边
                lambda: FightQuest.judge_whether_in_fight(),
            )
            logging.info("进入到战斗")
            FightQuest(
                backtopic=lambda: Page.is_page(PageName.PAGE_ASSAULT),
                start_from_editpage=False
            ).run()
            # 清除弹窗
            click(Page.MAGICPOINT)
            click(Page.MAGICPOINT)
            # TODO: 判断有没有打死BOSS
            logging.info("总力战第{}关已完成".format(next_ind+1))
            # 根据结果判断是否需要平推还是扫荡
            if next_ind == target_ind:
                # 扫荡
                logging.info("扫荡总力战第{}关".format(next_ind+1))
                button_pos = self.scroll_to_ind(next_ind)
                self.run_until(
                    lambda xy=button_pos: click(xy),
                    lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
                    times=2,
                    sleeptime=1
                )
                # 点两次加号
                click((1072, 301))
                click((1072, 301))
                # 点扫荡按钮
                click((939, 398))
                # 确认
                screenshot()
                click(button_pic(ButtonName.BUTTON_CONFIRMB))
                screenshot()
                click(button_pic(ButtonName.BUTTON_CONFIRMB))
                # 清除弹窗
                self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
                )
                break
            else:
                # 继续平推
                next_ind += 1
                logging.info(f"下一关：{next_ind+1}")
        # 推图结束，领取奖励
        CollectAssaultReward().run()
        
        
     
    def post_condition(self) -> bool:
        return self.back_to_home()
    