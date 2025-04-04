
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel, istr, CN, EN, JP
from modules.utils.log_utils import logging

import numpy as np

class InCraft(Task):
    STATUS_CRAFT_NOTHING = 0
    STATUS_CRAFT_DOING = 1
    STATUS_CRAFT_DONE = 2
    def __init__(self, name="InCraft") -> None:
        super().__init__(name)
        self.COLOR_CRAFT_NOTHING = ((226, 228, 228), (235, 235, 235))
        self.COLOR_CRAFT_DOING = ((250, 215, 110), (255, 222, 115))
        self.COLOR_CRAFT_DONE = ((60, 220, 240), (77, 236, 250))
        self.BUTTON_CRAFT = (1029, 678)
        self.COLOR_BUTTON_CRAFT_YELLOW = self.COLOR_CRAFT_DONE
        # 制造材料清单从上到下三个点的位置
        # 国服下方没有一键收集按钮，因此三个点偏下
        offsetY = 0
        items_ys = np.linspace(285, 530, 3, dtype=int)
        self.items_pos = [(1130, y+offsetY) for y in items_ys]
     
    def pre_condition(self) -> bool:
        return self.back_to_home()
    
    def getNowCraftStatus(self):
        screenshot()
        reslist = []
        for item in self.items_pos:
            res = match_pixel(item, self.COLOR_CRAFT_NOTHING, printit=True)
            if res:
                reslist.append(self.STATUS_CRAFT_NOTHING)
                continue
            res = match_pixel(item, self.COLOR_CRAFT_DONE, printit=True)
            if res:
                reslist.append(self.STATUS_CRAFT_DONE)
                continue
            reslist.append(self.STATUS_CRAFT_DOING)
        return reslist
    
    def dealing_with_quick_craft(self):
        """
        点击快速制造按钮，并完成快速制造
        """
        # 点开快速制造弹窗
        self.run_until(
            lambda: click([893, 619]),
            lambda: self.has_popup(),
            times=4
        )
        # 判断是否有黄色开始制造按钮
        has_yellow_button = match_pixel([1009, 593], self.COLOR_BUTTON_CRAFT_YELLOW)
        if not has_yellow_button:
            warning_str = istr({
                CN: "无法匹配快速制造弹窗，或没有足够的材料进行快速制造",
                EN: "Can not match popup, or not enough materials for quick crafting"
            })
            config.append_noti_sentence(
                key="CRAFT_FAILED", 
                sentence=warning_str)
            logging.warn(warning_str)
            self.status=Task.STATUS_SKIP
            return
        # 点击开始制造按钮，出现蓝色确认
        self.run_until(
            lambda: click([1009, 593]),
            lambda: match(button_pic(ButtonName.BUTTON_CONFIRMB)),
            times=4
        )
        # 点击确认按钮，直到返回制造页面
        can_confirm = self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
            lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMB)),
            times=4,
            sleeptime=1.5
        )
        if can_confirm:
            logging.info(istr({
                CN: "快速制造成功",
                EN: "Quick crafting success"
            }))
        else:
            logging.warn(istr({
                CN: "快速制造失败",
                EN: "Quick crafting failed"
            }))
            self.status=Task.STATUS_SKIP
        # 可能多点到空白格子，进入制造清单;返回
        if match_pixel([329, 381], Page.COLOR_WHITE):
            click(Page.TOPLEFTBACK, sleeptime=1)
    
    def dealing_with_craft(self):
        """
        进入到添加制造石头的页面
        """
        # 点击一号位添加直到匹配到开放按钮亮起来
        button_light = self.run_until(
            lambda: click((767, 204)),
            lambda: match_pixel(self.BUTTON_CRAFT, self.COLOR_BUTTON_CRAFT_YELLOW)
        )
        if not button_light:
            warning_str = istr({
                CN: "点击制造失败",
                EN: "Failed to click craft button"
            })
            logging.warn(warning_str)
            config.append_noti_sentence(
                key="CRAFT_FAILED",
                sentence=warning_str)
            # 没制造材料，跳过之后的制造任务
            self.status=Task.STATUS_SKIP
            return
        # 点击开放按钮
        click(self.BUTTON_CRAFT)
        self.dealing_with_craft_details()
    
    def dealing_with_craft_details(self):
        """
        选择制造内容，确定制造
        """
        #! 点击开放节点按钮后，如果没有走到最后一步，那么下次进入制造页面时，会直接跳转到这里
        # 点左下角节点，使左上角超大一个UI节点左移
        COLOR_W_CIRCLE = ((252, 252, 245), (255, 255, 252))
        POS_W_LEFT = (156, 109)
        # 黄色小节点
        COLOR_YELLOW_CRAFT_POINT = ((120, 180, 250), (190, 255, 255))
        # 五个节点坐标
        ALL_POINTS = (
            (174, 554),
            (303, 531),
            (413, 474),
            (505, 388),
            (570, 276)
        )
        self.run_until(
            lambda: click((444, 554)),
            lambda: match_pixel(POS_W_LEFT, COLOR_W_CIRCLE),
            times=3
        )
        sleep(0.7)
        # 选择具体节点 并确定
        # 从五个节点里面挑黄的出来，没有的话就第一个
        logging.info(istr({
            CN:"进入节点页面，选择制造节点",
            EN:"At Node Selection Page, select the craft node"
        }))
        for point in ALL_POINTS:
            if match_pixel(point, COLOR_YELLOW_CRAFT_POINT):
                click(point)
                break
        # 第一个制造节点结束
        # 点击右下角按钮, 直到出现弹窗
        logging.info(istr({
            CN:"开始制造",
            EN:"Start crafting"
        }))
        self.run_until(
            lambda: click(self.BUTTON_CRAFT, sleeptime=1.5),
            lambda: self.has_popup(),
            sleeptime = 0.5
        )
        # 点击确认按钮，直到返回制造页面
        self.run_until(
            lambda: click(button_pic(ButtonName.BUTTON_CONFIRMB)),
            lambda: not match(button_pic(ButtonName.BUTTON_CONFIRMB))
        )
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CRAFT)
        )
        
        
        
        
     
    def on_run(self) -> None:
        # 进入制造页面
        enter_page = self.run_until(
            lambda: click((678, 667)),
            lambda: Page.is_page(PageName.PAGE_CRAFT)
        )
        if not enter_page:
            logging.warn(istr({
                CN: "进入制造页面失败",
                EN: "Failed to enter craft page"
            }))
            self.dealing_with_craft_details()
        # 获取当前制造状态
        sleep(1.5)  # 留足时间过动画
        status_list = self.getNowCraftStatus()
        logging.info(status_list)
        now_craft_number = 0
        for ind, item in enumerate(status_list):
            # 处理每一个位置
            if item == self.STATUS_CRAFT_DOING:
                # 正在制造：不管跳过
                continue
            elif item == self.STATUS_CRAFT_DONE:
                # 制造完成：点击领取
                self.run_until(
                    lambda: click(self.items_pos[ind]),
                    lambda: self.has_popup(),
                    sleeptime = 1.5
                )
                self.clear_popup()
                # 随后制造
            # 尚未制造：开始制造
            # 如果使用快速制造
            if config.userconfigdict["CRAFT_USE_QUICK"]:
                logging.info(istr({
                    CN: "使用快速制造",
                    EN: "Use quick crafting"
                }))
                self.dealing_with_quick_craft()
            else:
                logging.info(istr({
                    CN: "使用普通制造",
                    EN: "Use normal crafting"
                }))
                self.run_until(
                    lambda: click(self.items_pos[ind]),
                    lambda: not Page.is_page(PageName.PAGE_CRAFT)
                )
                self.dealing_with_craft()
            if self.status == Task.STATUS_SKIP:
                logging.warn(istr({
                    CN: "制造材料不足，跳过之后的制造任务",
                    EN: "Insufficient crafting materials, skip subsequent crafting tasks"
                }))
                return 
            now_craft_number += 1
            if now_craft_number >= config.userconfigdict["CRAFT_TIMES"]:
                logging.info(istr({
                    CN: f"制造次数已达上限 {config.userconfigdict['CRAFT_TIMES']}",
                    EN: f"The number of crafting has reached the upper limit  {config.userconfigdict['CRAFT_TIMES']}"
                }))
                return
                

     
    def post_condition(self) -> bool:
        return self.back_to_home()