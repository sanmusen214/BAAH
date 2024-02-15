 
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
    
    BUTTON_TASK_START_POS = (1171, 668)
    BUTTON_TASK_INFO_POS = (996, 665)
    BUTTON_SEE_OTHER_TEAM_POS = (82, 554)
    
    TEAM_TYPE_NAME = {
        "red":"爆发",
        "blue":"神秘",
        "yellow":"贯穿",
        "purple":"振动",
        "any":"任意"
    }
    
    def __init__(self, grider:GridAnalyzer, backtopic, require_type, name="GridQuest") -> None:
        super().__init__(name)
        self.backtopic=backtopic
        self.grider=grider
        self.require_type = require_type
        
        # 当前关注的队伍下标
        self.now_focus_on_team = 0
        # 用于本策略的队伍名字，字母列表，["A","B","C"...]
        self.team_names = []
        # 上一次action
        self.lastaction = {
            "team":"",
            "action":"",
            "target":""
        }
        # 上一次为了队伍移动点击的位置
        self.last_click_position = [-1, -1]

    
    def pre_condition(self) -> bool:
        click(Page.MAGICPOINT, 1)
        click(Page.MAGICPOINT, 1)
        screenshot()
        if Page.is_page(PageName.PAGE_GRID_FIGHT):
            return True
        # 可能有剧情
        SkipStory(pre_times=2).run()
        return Page.is_page(PageName.PAGE_GRID_FIGHT)
    
    def whether_contain_number(self, string:str):
        """
        判断字符串是否包含数字
        """
        for i in string:
            if i.isdigit():
                return True
        return False
    
    def wait_end(self, possible_fight = False):
        """
        点击右下任务资讯，等待战斗结束可以弹出弹窗，然后点击魔法点关掉弹窗
        """
        # 如果返回到了self.backtopic()指定的页面，那么直接返回
        if self.backtopic():
            return True
        # 自动打斗中也是打不开弹窗，进了局内战斗也是打不开弹窗
        # 判断是否进了局内战斗
        # 如果能点开弹窗且仍然在走格子界面，则必定没有进入局内战斗。
        # 如果没有开关弹窗这个效果，那么继续讨论
        #     如果在走格子界面，那么可能会进入局内战斗可能不会
        #     如果不在走格子界面，上面又已知没有返回backtopic，那么就是进入了局内战斗
        # 局内战斗完应该是直接返回到上级界面，所以局内战斗的话就直接return就行了
        if possible_fight:
            for try_time in range(5):
                # 试试有没有开关弹窗效果
                pre_close = self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
                )
                can_open = self.run_until(
                    lambda: click(self.BUTTON_TASK_INFO_POS, 1.5),
                    lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
                )
                can_close = self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
                )
                if pre_close and can_open and can_close:
                    # 有开关弹窗效果
                    logging.info("有开关弹窗效果")
                    if match(page_pic(PageName.PAGE_GRID_FIGHTING)):
                        # 在走格子界面，铁定没进局内战斗
                        return
                else:
                    # 没有开关弹窗效果
                    if match(page_pic(PageName.PAGE_GRID_FIGHTING)):
                        # 在走格子界面，可能进局内战斗，可能不进，继续判断
                        continue
                    elif not self.backtopic():
                        # 不在走格子界面，没有返回backtopic,那么就是进入了局内战斗
                        FightQuest(self.backtopic, start_from_editpage=False).run()
                        return
        # 清弹窗
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
        )
        # 出弹窗
        self.run_until(
            lambda: click(self.BUTTON_TASK_INFO_POS),
            lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
            times=18,
            sleeptime=1.5
        )
        # 清弹窗
        self.run_until(
            lambda: click(Page.MAGICPOINT),
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
        # 国际服繁中不偏移，其他服往右偏移45
        offsetx = 45
        if config.userconfigdict["SERVER_TYPE"] == "GLOBAL":
            offsetx = 0
        now_team_str, loss = ocr_area((72+offsetx, 544), (91+offsetx, 569), multi_lines=False)
        logging.info(f"ocr结果{now_team_str}")
        try:
            nowteam_ind = int(now_team_str)-1
        except ValueError as e:
            logging.error("识别左下角切换队伍的按钮文字失败")
            raise Exception("识别左下角切换队伍的按钮文字失败")
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
        logging.info(f"成功读取关卡文件{self.grider.jsonfilename}，开始执行")
        # 设置队伍数量
        self.team_names = [item["name"] for item in self.grider.get_initialteams(self.require_type)]
        # ========== 配队 ============
        last_team_set_list = config.sessiondict["LAST_TEAM_SET"]
        now_need_team_set_list = [item["type"] for item in self.grider.get_initialteams(self.require_type)]
        need_user_set_teams = False
        # 判断能否直接用上次的队伍
        for ind in range(len(now_need_team_set_list)):
            if len(last_team_set_list)<=ind or (last_team_set_list[ind]!=now_need_team_set_list[ind] and now_need_team_set_list[ind]!="any"):
                # 让用户去配队！
                need_user_set_teams = True
                break
        # 如果开启了彩虹队配置，则不用配队
        if config.userconfigdict["EXPLORE_RAINBOW_TEAMS"]:
            need_user_set_teams = False
        if need_user_set_teams:
            # 需要用户配队
            logging.info("未保存适合的配置，请按照以下队伍要求配队")
            for ind in range(len(now_need_team_set_list)):
                logging.info(f"    编辑部队-> {ind+1}部队: {now_need_team_set_list[ind]} {self.TEAM_TYPE_NAME[now_need_team_set_list[ind]]} {list(self.grider.get_initialteams(self.require_type))[ind]['position']}")
            logging.info("同时，请确保你的SKIP战斗设置为开启，PHASE自动结束为关闭")
            input("配队结束后请直接返回至走格子界面，不用点击出击。输入回车继续：")
            # 更新队伍信息
            config.sessiondict["LAST_TEAM_SET"] = now_need_team_set_list
            logging.info("配队信息已更新")
        else:
            # 不需要用户配队的话就继续用上次的队伍
            display_str = " ".join([self.TEAM_TYPE_NAME[item] for item in last_team_set_list])
            logging.info(f"使用上次的队伍配置: {display_str}")
        screenshot()
        if match(page_pic(PageName.PAGE_EDIT_QUEST_TEAM)):
            click(Page.TOPLEFTBACK, 2)
        # 选择队伍START
        # 尚未配队的队伍的相对文字化角度描述
        tobe_setted_team_poses = [item["position"] for item in self.grider.get_initialteams(self.require_type)]
        for focus_team_ind in range(len(self.team_names)):
            for try_times in range(3):
                # 设置队伍初始位置的时候，重复尝试三次，如果失败了（无法跳到编辑队伍页面）就点一下切换队伍按钮
                logging.info(f"配置队伍{self.team_names[focus_team_ind]}")
                res_gridpage = self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: match(page_pic(PageName.PAGE_GRID_FIGHT)),
                    sleeptime=1,
                    times=3
                )
                if not res_gridpage:
                    logging.error("未识别到走格子界面")
                    raise Exception("未识别到走格子界面，请确保当前界面是走格子界面且未出击任何队伍")
                # 如果队伍配队配置里面有click参数，那么就点击相对应的位置就行了
                if "click" in list(self.grider.get_initialteams(self.require_type))[focus_team_ind]:
                    target_click_team_center = list(self.grider.get_initialteams(self.require_type))[focus_team_ind]["click"]
                    logging.info(f"使用配置文件中的click参数{target_click_team_center}")
                else:
                    # 如果没有click参数，那么就用knn识别初始方格
                    # 得到初始中心
                    center_poses, loss, global_center = self.grider.multikmeans(self.grider.get_mask(get_screenshot_cv_data(), self.grider.PIXEL_START_YELLOW), len(self.team_names))
                    # 得到相应偏角和距离
                    angles, distances = self.grider.get_angle(center_poses, global_center)
                    # 得到初始中心对应的文字化角度描述
                    directions = self.grider.get_direction(angles, distances, tobe_setted_team_poses)
                    # 接下来为这个队伍设置人员，点击相应的center_poses然后确定即可
                    # 现在要处理的队伍的文字化角度描述
                    now_team_pos = tobe_setted_team_poses[focus_team_ind]
                    # 找到这个角度描述是derections里的第几个
                    now_team_pos_ind = directions.index(now_team_pos)
                    # 点击这个中心
                    target_click_team_center = center_poses[now_team_pos_ind]
                    target_click_team_center = [int(target_click_team_center[1]), int(target_click_team_center[0])]
                # 点击队伍初始位置
                click(target_click_team_center, 1)
                edit_page_result = self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: match(page_pic(PageName.PAGE_EDIT_QUEST_TEAM))
                )
                if edit_page_result:
                    break
                else:
                    click(self.BUTTON_SEE_OTHER_TEAM_POS, 1)
            if not edit_page_result:
                raise Exception("未识别到配队界面，请确保当前界面是配队界面且你未手动出击任何队伍")
            # 点击确定
            logging.info("点击出击")
            self.run_until(
                lambda: click(self.BUTTON_TASK_START_POS),
                lambda: not match(page_pic(PageName.PAGE_EDIT_QUEST_TEAM)),
                sleeptime=3
            )
            
            # 等待回到走格子界面
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match(page_pic(PageName.PAGE_GRID_FIGHT))
            )
        # ==========开打！============
        sleep(1.5)
        logging.info("开始战斗！")
        # 点击任务开始，这边多等一会，有的服战斗开始时会强制转到二队视角
        click(self.BUTTON_TASK_START_POS, sleeptime=4)
        for step_ind in range(self.grider.get_num_of_steps(self.require_type)):
            # 循环每一个回合
            actions = self.grider.get_action_of_step(self.require_type, step_ind)
            for action_ind in range(len(actions)):
                action = actions[action_ind]
                # 循环回合的每一个action
                target_team_ind = self.team_names.index(action["team"])
                # 聚焦到目标队伍，每次都获取最新的当前聚焦队伍
                while(self.get_now_focus_on_team()!=target_team_ind):
                    click(self.BUTTON_SEE_OTHER_TEAM_POS, sleeptime=1)
                logging.info(f'当前聚焦队伍{self.team_names[self.now_focus_on_team]}')
                logging.info(f'执行step:{step_ind} action:{action_ind} 队伍{action["team"]}->{action["action"]} {action["target"]}')
                sleep(1.5)
                # 专注到一个队伍上后，分析队伍当前位置
                screenshot()
                # 先提取，后knn
                try:
                    # 如果有click参数，那么就直接用click参数
                    if "click" in action:
                        logging.info(f"使用配置文件中的click参数{action['click']}")
                        need_click_position = action["click"]
                    else:
                        mode = "head"
                        # 需要蒙版的颜色
                        need_to_mask_color = self.grider.PIXEL_HEAD_YELLOW
                        # 国服的话头顶颜色会深一些
                        if config.userconfigdict["SERVER_TYPE"]=="CN" or config.userconfigdict["SERVER_TYPE"]=="CN_BILI":
                            need_to_mask_color = self.grider.PIXEL_HEAD_YELLOW_CN_DARKER
                        knn_positions, _, _ = self.grider.multikmeans(self.grider.get_mask(get_screenshot_cv_data(), need_to_mask_color, shrink_kernels=[(2, 4), (2,2)]), 1)
                        if knn_positions[0][0]<0 or knn_positions[0][1]<0:
                            mode = "foot"
                            # 如果用头上三角箭头识别队伍位置失败，那么用脚底黄色标识识别
                            logging.info("三角识别失败，尝试使用砖块识别")
                            knn_positions, _, _ = self.grider.multikmeans(self.grider.get_mask(get_screenshot_cv_data(), self.grider.PIXEL_MAIN_YELLOW), 1)
                            if knn_positions[0][0]<0 or knn_positions[0][1]<0:
                                # 如果还是失败，那么就是失败了
                                raise Exception("队伍位置识别失败")
                        # 此处坐标和opencv坐标相反
                        target_team_position = knn_positions[0]
                        # 根据攻略说明，偏移队伍位置得到点击的位置
                        offset_pos = self.grider.WALK_MAP[action["target"]]
                        # 前后反，将数组下标转为图像坐标
                        if mode == "head":
                            # 头部识别三角箭头，需要向下偏移定位到格子
                            offset_from_cnn_to_real = 135
                        else:
                            offset_from_cnn_to_real = 0
                        # 此处need_click_position的轴向就和opencv相同了
                        need_click_position = [int(target_team_position[1]+offset_pos[1]), int(target_team_position[0]+offset_pos[0]+offset_from_cnn_to_real)] # 纵轴从人物头顶三角箭头往下偏移
                except Exception as e:
                    print(e)
                    logging.warn("队伍位置识别失败")
                    if action["team"]==self.lastaction["team"] and action["action"]=="portal" and action["target"]=="center":
                        logging.info("动作为原地传送，尝试点击上次点击位置")
                        # 如果队伍与上一次一样，且是传送门，而且是点击队伍脚底下。
                        # 如果队伍上次是移动到传送门上，则此时会没有脚底黄色标
                        need_click_position = self.last_click_position
                    else:
                        logging.error("队伍位置识别失败，这可能是由于识别参数不正确导致的，请反馈给开发者")
                        raise Exception("队伍位置识别失败")
                # 点击使其移动
                logging.info(f'点击{need_click_position}')
                click(need_click_position, sleeptime=1)
                self.last_click_position = need_click_position
                # 默认是move事件，此外还有portal，exchange需要特殊处理
                if action["action"]=="exchange":
                    sleep(2)
                    exchange_res = self.run_until(
                            lambda: click(button_pic(ButtonName.BUTTON_EXCHANGE_TEAM)),
                            lambda: not match(button_pic(ButtonName.BUTTON_EXCHANGE_TEAM))
                        )
                    if not exchange_res:
                        logging.error(f"{self.grider.jsonfilename}：队伍交换失败")
                        raise Exception("未识别到交换队伍按钮，这可能是由于你的队伍练度过低；或者攻略配置文件不正确导致的，请反馈给开发者（群里或者issue）")
                elif action["action"]=="portal":
                    sleep(2)
                    portal_result = self.run_until(
                        lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                        lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
                    )
                    if not portal_result:
                        logging.error("未识别到传送弹窗")
                        raise Exception("未识别到传送弹窗，这可能是由于攻略配置文件不正确导致的，请反馈给开发者")
                if action_ind==len(actions)-1 and step_ind==self.grider.get_num_of_steps(self.require_type)-1:
                    # 可能局内战斗，自己去碰boss
                    self.wait_end(possible_fight=True)
                else:
                    # 可能触发打斗
                    self.wait_end()
                # action处理完，保存这次action
                self.lastaction = action
            # 回合结束，手动点击PHASE结束，有时候有的队伍还可以走，就点击确认按钮
            logging.info("PHASE结束")
            click(self.BUTTON_TASK_START_POS, sleeptime=2)
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
                lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
            )
            if step_ind==self.grider.get_num_of_steps(self.require_type)-1:
                # 等敌方行动结束，可能是回合结束boss凑过来
                self.wait_end(possible_fight=True)
            else:
                self.wait_end()
        
        
     
    def post_condition(self) -> bool:
        return self.backtopic()