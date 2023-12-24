 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.SkipStory import SkipStory
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, match_pixel

class InMomotalk(Task):
    def __init__(self, name="InMomotalk") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
    def whether_has_red_icon(self) -> bool:
        """
        检测第一条对话旁边是否有红色标记，
        中途会试图点击重新排序，最多尝试三次
        """
        click(self.momo_title_pos)
        for i in range(3):
            # 点击momotalk标题位置，尝试去除弹窗
            click(self.momo_title_pos)
            # 点击重新排序
            click((623, 177))
            # 检测红标记
            if match_pixel((639, 240), Page.COLOR_RED):
                logging.info(f"检测到红色标记")
                return True
        return False
     
    def click_first_second_first(self) -> None:
        """
        点击第一条对话，然后点击第二条对话，然后点击第一条对话，点击对话框位置
        """
        # 第一条
        click((263, 253), sleeptime=1)
        # 第二条
        click((262, 330), sleeptime=1)
        # 第一条
        click((263, 253), sleeptime=1)
        # 回复框
        click((1110, 577))
        
     
    def on_run(self) -> None:
        # 点击打开momotalk界面
        openmomo = self.run_until(
            lambda: click((172, 174)),
            lambda: match(popup_pic(PopupName.POPUP_MOMOTALK))
        )
        if not openmomo:
            logging.info(f"未检测到momotalk弹窗，跳过此任务")
            self.back_to_home()
            return
        # 记住momotalk位置
        self.momo_title_pos = match(popup_pic(PopupName.POPUP_MOMOTALK), returnpos=True)[1]
        # 切换到对话界面
        gotalk = self.run_until(
            lambda: click((170, 299)),
            lambda: match(page_pic(PageName.PAGE_MOMOTALK))
        )
        if not gotalk:
            logging.info(f"未检测到对话界面，跳过此任务")
            self.back_to_home()
            return
        # 按照未读的momotalk筛选
        click((507, 176), 1.3)
        click((555, 293), 0.5)
        click((450, 421), 0.5)
        # 尝试切换排序，多次后还没检测到红标记就放弃
        self.scroll_left_up()
        matchred = self.whether_has_red_icon()
        # 确认自己的momotalk最新未读消息在顶部
        logging.info(f"检测第一条消息右侧是否为红色:{matchred}")
        if not matchred:
            logging.info(f"未检测到红色标识，跳过此任务")
        else:
            while(matchred):
                # 处理第一个momotalk
                logging.info("处理第一条momotalk")
                # 按回复框直到蹦出剧情右上角的按钮
                self.run_until(
                    lambda: self.click_first_second_first(),
                    lambda: match(button_pic(ButtonName.BUTTON_STORY_MENU)),
                    times=10
                )
                # 跳过剧情
                SkipStory().run()
                # 关闭弹窗, 继续检测第一条消息右侧是不是红色
                matchred = self.whether_has_red_icon()
        logging.info("momotalk处理完毕，返回主页")
        self.back_to_home()
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)