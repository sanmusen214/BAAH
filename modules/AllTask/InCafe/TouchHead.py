 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName
from modules.utils.MyConfig import config
from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
import logging
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot

class TouchHead(Task):
    def __init__(self, name="TouchHead") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)
    
    def click_head_and_magic(self):
        # 清除可能的好感度弹窗
        click(Page.MAGICPOINT)
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE),
        )
        canmatchRes = match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold=0.95, returnpos=True, rotate_trans=True)
        if(canmatchRes[0]):
            logging.info("匹配到注意力符号，点击头部")
            click((min(canmatchRes[1][0]+50, 1280),canmatchRes[1][1]), sleeptime=1.5)
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE),
        )

            
    def swipeRight(self):
        swipe((1116, 129), (431, 129), 0.3)
    
    def swipeLeft(self):
        swipe((431, 129), (1116, 129), 0.3)
    
    def swipeDown(self):
        swipe((751, 420), (431, 129), 0.3)
    
    def swipeUp(self):
        swipe((431, 129), (751, 420), 0.3)
    
     
    def on_run(self) -> None:
        if config.configdict["CAFE_CAMERA_FULL"]:
            # 视角最高直接点
            totalruns = 3
            times_in_run = 3
            for i in range(totalruns):
                # sometimes a speak will cover the NOTICE icon, so we need to double check
                click(Page.MAGICPOINT)
                self.run_until(
                    lambda: self.click_head_and_magic(),
                    lambda: not match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold = 0.95, rotate_trans=True),
                    times = times_in_run, # 直到找不到注意力符号
                    sleeptime=1
                )
                logging.info(f"第{i+1}/{totalruns}轮摸头结束")
                sleep(3)
        else:
            # 左右拖动换视角摸头
            TO_POS_LEFT = [self.swipeLeft, self.swipeLeft, self.swipeLeft]
            TO_POS_BOTTOM = [self.swipeDown, self.swipeDown, self.swipeDown]
            TO_POS_RIGHT = [self.swipeRight, self.swipeRight]
            TO_POS_RIGHT_SIDE = [self.swipeRight, self.swipeRight]
            TO_POS_CENTER = [self.swipeLeft, self.swipeUp, self.swipeUp, self.swipeUp]
            all_pos = [TO_POS_LEFT, TO_POS_BOTTOM, TO_POS_RIGHT,TO_POS_RIGHT_SIDE, TO_POS_CENTER]
            
            for movefuncs in all_pos:
                # 先摸再变视角
                # 这个画面里有多少次没有匹配到注意力符号
                times_not_match = 0
                for tt in range(8):
                    # 清除可能的好感度弹窗
                    self.run_until(
                        lambda: click(Page.MAGICPOINT),
                        lambda: Page.is_page(PageName.PAGE_CAFE),
                    )
                    screenshot()
                    if (match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold = 0.95, rotate_trans=True)):
                        self.click_head_and_magic()
                    else:
                        # 失败次数超过3次就不再尝试
                        times_not_match += 1
                        if times_not_match == 3:
                            break
                # 变换视角前再次确认关闭弹窗回到咖啡厅页面
                self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: Page.is_page(PageName.PAGE_CAFE),
                )
                logging.info("变换视角")
                for func in movefuncs:
                    func()
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)