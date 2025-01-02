from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllTask.SubTask.FightQuest import FightQuest

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import (click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot,
                           match_pixel)


class EventStory(Task):
    """
    判断活动剧情是否推完，如果没推完就推完

    靠蒙版是否存在判断剧情是否看过，默认有9关剧情
    """

    def __init__(self, name="EventStory") -> None:
        super().__init__(name)
        self.last_fight_level_ind = -1
        # 最大关卡数，这里不是下标，是关卡序号
        self.max_level = 9

    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EVENT)

    def do_view(self):
        """弹窗已经打开，观看当前页面的剧情，可能要打架"""
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_TASK_START)) or click((633, 496)),
            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE) or match(popup_pic(PopupName.POPUP_TOTAL_PRICE)),
            times=3,
            sleeptime=2
        )
        # 如果体力不够
        screenshot()
        if match(popup_pic(PopupName.POPUP_TOTAL_PRICE)):
            logging.warn({"zh_CN": "体力不够，结束", "en_US": "Not enough AP, end"})
            return "noap"
        # 剧情这边应该只会有单次战斗
        FightQuest(backtopic=lambda: match(page_pic(PageName.PAGE_EVENT))).run()

    def judge_whether_and_do_view(self, this_level_ind):
        """
        判断并执行观看Story，可能要打架

        观察到下标为this_level_ind的关卡时蒙版是否还在
        """
        screenshot()
        # 这里由于剧情关不能扫荡，所以只能用蒙版判断
        # 如果无蒙版，那么就是有剧情
        if match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE):
            # 跑到下标为this_level_ind的关卡时蒙版消失
            # 所以我们应该打下标为this_level_ind-1的关卡
            logging.info({"zh_CN": f"触发推剧情任务，关卡{this_level_ind}",
                          "en_US": f"Trigger push story quests, levels {this_level_ind}"})
            # 判断推图是否刚才打了一次，但是没三星或打不过去
            if this_level_ind == self.last_fight_level_ind:
                logging.warn({"zh_CN": f"活动剧情推图第{this_level_ind}关刚才打了一次，但是没三星或打不过去，"
                                       f"请配置更好的队伍配置。或已经是最后一关了",
                              "en_US": f"The {this_level_ind}th level of the event story "
                                       f"automatic push map was just played once, "
                                       f"but it did not get three stars or could not pass, "
                                       f"please configure a better team configuration. "
                                       f"Or it is the last level already"})
                return "repeatfight"
            # 这里弹窗已经关了，重新跑到下标为this_level_ind-1的关卡
            self.scroll_right_up()
            click((1130, 200), sleeptime=2)
            for i in range(this_level_ind - 1):
                # 点右边的箭头
                click((1171, 359), sleeptime=1)
            self.do_view()
            # 更新上次自动推剧情的关卡下标
            self.last_fight_level_ind = this_level_ind
            return "yes"
        return "no"

    def get_biggest_level(self):
        """
        通过下滑到底ocr获取最大关卡数

        -1表示没有找到
        """
        self.scroll_right_down()
        sleep(1)
        screenshot()
        reslist = ocr_area((695, 416), (752, 699), multi_lines=True)
        temp_max = -1
        logging.info({"zh_CN": "ocr结果：" + str(reslist), "en_US": "ocr result: " + str(reslist)})
        # 将每一个字母尝试转换成数字，如果是数字就比较目前最大
        for res in reslist:
            try:
                # 最大不过14
                temp_max = min(max(temp_max, int(res[0])), 14)
            except:
                pass
        self.max_level = temp_max
        return temp_max

    def on_run(self) -> None:
        # 点击Story标签
        click((766, 98))
        max_level = self.get_biggest_level()
        if max_level == -1:
            logging.warn({"zh_CN": "无法获取最大关卡数，结束", "en_US": "Failed to get the max level, end"})
            return
        logging.info({"zh_CN": "检查活动剧情是否推完,最大关卡数为"+str(max_level),
                      "en_US": "Check if the event story is completed. "
                               "The maximum number of levels is" + str(max_level)})
        while 1:
            sleep(3)
            # 视角会自动滚动到顶部，等3秒
            click(Page.MAGICPOINT)
            click(Page.MAGICPOINT)
            # 点击Story标签
            click((766, 98))
            self.scroll_right_up()
            # 点击第一个level，第一个level永远不会弹不出来蒙版
            click((1130, 200), sleeptime=2)
            # 往右切换，主要是靠break，循环次数只要大于9就行
            has_do_view = False
            # 稍微设置大一点，让重复打关触发来判定结束
            for i in range(max_level - 1):
                # 点右边的箭头
                click((1171, 359), sleeptime=1)
                # 往右切换后判断是否需要推剧情
                res = self.judge_whether_and_do_view(1 + i)
                if res == "yes":
                    has_do_view = True
                    break
                elif res == "noap":
                    self.run_until(
                        lambda: click(Page.MAGICPOINT),
                        lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
                    )
                    logging.info({"zh_CN": "返回到根页面", "en_US": "Back to Root Page"})
                    return
                elif res == "repeatfight":
                    logging.warn({"zh_CN": "重复打关卡，结束", "en_US": "Repeatedly play the level, end"})
                    return
            # 观看了剧情，那么再尝试继续看后面的关卡剧情
            if has_do_view:
                continue
            # 运行到这，意味着没有通过蒙版检测出有剧情没打。此时处于最后一个剧情的弹窗界面
            # 不过最后一个剧情无法通过弹窗的方式检测，最后一个剧情用奖励文字检测有没有打过
            screenshot()
            # 弹窗大小不同影响到匹配精度，匹配threshold设置为0.8
            if match(button_pic(ButtonName.BUTTON_EVENT_FIRST), threshold=0.8):
                logging.info({"zh_CN": "需要推最后一关剧情",
                              "en_US": "Need to push the last stage of the plot"})
                self.do_view()
            # 如果没有需要看的剧情了，那么就结束
            click(Page.MAGICPOINT)
            click(Page.MAGICPOINT)
            break

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EVENT)