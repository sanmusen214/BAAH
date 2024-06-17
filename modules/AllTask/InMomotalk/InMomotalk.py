 
from modules.utils.log_utils import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.SkipStory import SkipStory
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, match_pixel, screenshot

class InMomotalk(Task):
    def __init__(self, name="InMomotalk") -> None:
        super().__init__(name)
     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
    
    def whether_has_red_icon(self) -> bool:
        """
        检测第一条对话旁边是否有红色标记，
        中途会重新排序，最多尝试三次，
        """
        # 考虑重新排序
        for i in range(3):
            # 点击momotalk标题位置，尝试去除弹窗
            click(self.momo_title_pos)
            # 有时候明明对话结束了，但是还是会有红标记，所以先点一下二号位刷新以下一号位的信息
            # 点第二个
            click((262, 330), 1.2)
            # 点第一个
            click((263, 253))
            # 检测红标记，手动截图！
            screenshot()
            if match_pixel((638, 242), Page.COLOR_RED):
                # logging.info(f"检测到红色标记")
                return True
            # 如果在第二位检测到红标记
            if match_pixel((638, 318), Page.COLOR_RED):
                logging.info("刷新排序")
                click((623, 177))
                click((623, 177))
            else:
                # 点击重新排序
                logging.info("重新排序")
                click((623, 177))
        return False
     
    def click_reply(self) -> None:
        """
        点击第一条对话，点击对话框位置或者羁绊按钮
        
        一般是 回复-》（粉色羁绊-》蓝色进入羁绊剧情）
        """
        # 右侧往下滑动, 在头像框的位置滑
        swipe((727, 460), (727, 243), sleeptime=0.2)
        sleep(2)
        # 手动截图！
        screenshot()
        # 回复按钮 +40
        reply_button = match(button_pic(ButtonName.BUTTON_MOMOTALK_REPLY), threshold=0.87,returnpos=True)
        logging.info("回复按钮匹配度:{:.2f}".format(reply_button[2]))
        if reply_button[0]:
            logging.info("检测到回复按钮")
            self.run_until(
                lambda: click((reply_button[1][0], reply_button[1][1]+40)),
                lambda: not match(button_pic(ButtonName.BUTTON_MOMOTALK_REPLY), threshold=0.87)
            )
        # 羁绊按钮 +40
        partner_button = match(button_pic(ButtonName.BUTTON_MOMOTALK_PARTNER), returnpos=True)
        logging.info("羁绊按钮匹配度:{:.2f}".format(partner_button[2]))
        if partner_button[0]:
            logging.info("检测到羁绊按钮")
            self.run_until(
                lambda: click((partner_button[1][0], partner_button[1][1]+40)),
                lambda: not match(button_pic(ButtonName.BUTTON_MOMOTALK_PARTNER))
            )
            # 羁绊按钮后面必定有羁绊剧情按钮，等待一秒
            sleep(1.5)
            # 前往羁绊剧情按钮
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_GO_PARTNER_STORY)),
                lambda: not match(button_pic(ButtonName.BUTTON_GO_PARTNER_STORY))
            )
            sleep(2)
            # 尝试跳过剧情
            SkipStory().run()

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
        # 记住momotalk标题位置
        self.momo_title_pos = match(popup_pic(PopupName.POPUP_MOMOTALK), returnpos=True)[1]
        # 切换到对话界面
        click((170, 299), 1)
        click((170, 299), 1)
        # 按照未读的momotalk筛选
        click((507, 176), 1)
        click((508, 293))
        click((450, 366)) # 国
        click((450, 421)) # 日
        # 尝试切换排序，多次后还没检测到红标记就放弃
        self.scroll_left_up()
        while(self.whether_has_red_icon()):
            # 处理第一个momotalk
            logging.info("处理第一条momotalk")
            # 按回复框或羁绊框并跳过剧情
            self.click_reply()
            # 剧情过完可能会有个得到回忆大厅的弹窗
            self.run_until(
                lambda: click(self.momo_title_pos),
                lambda: match(popup_pic(PopupName.POPUP_MOMOTALK))
            )
        logging.info("momotalk处理完毕，返回主页")
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: not match(popup_pic(PopupName.POPUP_MOMOTALK))
        )
        self.back_to_home()
        # 递归运行
        InMomotalk().run()
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)