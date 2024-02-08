 
import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.SubTask.FightQuest import FightQuest
from modules.AllTask.SubTask.GridQuest import GridQuest

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel
from modules.utils.grid_analyze import GridAnalyzer
from .Questhelper import jump_to_page, close_popup_until_see, judge_whether_3star

class PushQuest(Task):
    """
    从进入关卡选择页面开始托管推图
    
    通过page_ind和level_ind定位到起始关卡，随后每成功推一张图就让level_ind+1，向右多翻一次后，用ocr来更新确切的page_ind和level_ind
    
    Parameters
    ----------
    quest_type : str
        任务类型，normal/hard
        
    page_ind : int
        开始推图的章节下标
    """
    def __init__(self, quest_type, page_ind, level_ind = 0, name="PushQuest") -> None:
        super().__init__(name)
        self.is_normal = quest_type == "normal"
        self.page_ind = page_ind # 初始聚焦章节下标
        self.level_ind = level_ind # 初始聚焦关卡下标
        self.require_type_ind = 0 # 当前需要完成的任务类型下标

    
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)
    
    def on_run(self) -> None:
        if self.is_normal:
            logging.info("switch to normal quest")
            self.run_until(
                lambda: click((798, 159)),
                lambda: match(button_pic(ButtonName.BUTTON_NORMAL))
            )
        else:
            logging.info("switch to hard quest")
            self.run_until(
                lambda: click((1064, 161)),
                lambda: match(button_pic(ButtonName.BUTTON_HARD))
            )
        while 1:
            # ===========尝试定位要推图的章节和关卡===================
            # 跳转到相应地区
            logging.info("尝试跳转至页面 {}".format(self.page_ind + 1))
            jumpres = jump_to_page(self.page_ind + 1) # 下标加1为实际页号数字
            if not jumpres:
                logging.error("跳转至页面 {} 失败，结束此任务".format(self.page_ind + 1))
                return
            click(Page.MAGICPOINT, sleeptime=1)
            self.scroll_right_up()
            sleep(0.5)
            # 点击第一个关卡
            self.run_until(
                lambda: click((1118, 240)),
                lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
            )
            # 此时应该看到扫荡弹窗
            # 向右翻self.level_ind次
            logging.info("尝试翻到关卡 {}".format(self.level_ind + 1))
            for i in range(self.level_ind):
                click((1171, 359), sleeptime=1)
            screenshot()
            # 如果匹配到弹窗消失
            if match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE):
                logging.info("关卡弹窗消失，结束此任务")
                return
            else:
                # 当前关卡就是这次需要推图的关卡
                left_up = ocr_area((139, 197), (216, 232))
                page_level = left_up[0].split("-")
                try:
                    # 这一步更新这次推图的实际章节和关卡下标
                    page_num = int(page_level[0])
                    level_num = int(page_level[1])
                    self.page_ind = page_num - 1
                    self.level_ind = level_num - 1
                    logging.info("关卡：{}-{}，开始推图".format(page_num, level_num))
                except:
                    logging.error("OCR关卡序号识别失败，结束此任务")
                    return
            # ===========正式开始推图===================
            # 看到弹窗，ocr是否有S
            ocr_s = ocr_area((327, 257), (353, 288))
            walk_grid = None
            if ocr_s[0].upper() != "S":
                logging.info("未识别到S等级，判断为普通战斗")
                walk_grid = False
            else:
                logging.info("识别到S标签，判断为走格子战斗")
                walk_grid = True
            if not walk_grid:
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_TASK_START)),
                    lambda: match(page_pic(PageName.PAGE_EDIT_QUEST_TEAM))
                )
                FightQuest(backtopic=lambda: match(page_pic(PageName.PAGE_QUEST_SEL))).run()
                # 普通任务完成后，level下标+1
                self.level_ind += 1
            else:
                jsonname = f"{self.page_ind+1}-{self.level_ind+1}.json"
                if not self.is_normal:
                    jsonname = f"H{jsonname}"
                grider = GridAnalyzer("quest", jsonfilename=jsonname)
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_TASK_START)),
                    lambda: match(page_pic(PageName.PAGE_GRID_FIGHT))
                )
                # 需求列表
                require_types = grider.get_requires_list()
                GridQuest(grider=grider, backtopic=lambda: match(page_pic(PageName.PAGE_QUEST_SEL)), require_type=require_types[self.require_type_ind]).run()
                # 任务完成后，往后切换需求类型下标，如果超出了需求类型列表，就回到0，且level下标+1
                self.require_type_ind += 1
                if self.require_type_ind >= len(require_types):
                    self.require_type_ind = 0
                    self.level_ind += 1
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)