 
import logging

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

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
        中途会试图点击重新排序，最多尝试三次
        """
        hasmomotalk_popup = self.run_until(
            lambda: click(self.momo_title_pos),
            lambda: match(popup_pic(PopupName.POPUP_MOMOTALK)),
            times=3
        )
        if not match(popup_pic(PopupName.POPUP_MOMOTALK)):
            logging.info("未检测到momotalk弹窗")
            return False
        if match_pixel((638, 242), Page.COLOR_RED):
            # logging.info(f"检测到红色标记")
            return True
        # 一开始没检测到，考虑重新排序
        for i in range(3):
            # 点击momotalk标题位置，尝试去除弹窗
            click(self.momo_title_pos)
            # 点击重新排序
            logging.info("重新排序")
            click((623, 177))
            # 检测红标记，手动截图！
            screenshot()
            if match_pixel((638, 242), Page.COLOR_RED):
                # logging.info(f"检测到红色标记")
                return True
        return False
     
    def click_reply(self) -> None:
        """
        点击第一条对话，点击对话框位置或者羁绊按钮，然后点击第二条对话，然后点击第一条对话，
        可能羁绊剧情过后会有一点点新的对话，所以在click_reply内部也要检测第一消息是否有红点，防止过多等待
        
        一般是 回复-》（粉色羁绊-》蓝色进入羁绊剧情）
        """
        # 第一条
        click((263, 253))
        # 如果反复排序后第一条右边还没有红点，说明已经处理完毕，直接return
        if not self.whether_has_red_icon():
            logging.warn("第一条右边没有红点了，跳过此任务，关闭momotalk弹窗")
            # 点击魔法点关闭momotalk弹窗
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: not match(popup_pic(PopupName.POPUP_MOMOTALK))
            )
            return
        # 手动截图！
        screenshot()
        # 回复按钮 +40
        reply_button = match(button_pic(ButtonName.BUTTON_MOMOTALK_REPLY), returnpos=True)
        if reply_button[0]:
            logging.info("检测到回复按钮{:.2f}".format(reply_button[2]))
            self.scroll_right_down(times = 1)
            self.run_until(
                lambda: click((reply_button[1][0], reply_button[1][1]+40)),
                lambda: not match(button_pic(ButtonName.BUTTON_MOMOTALK_REPLY))
            )
        # 羁绊按钮 +40
        partner_button = match(button_pic(ButtonName.BUTTON_MOMOTALK_PARTNER), returnpos=True)
        if partner_button[0]:
            logging.info("检测到羁绊按钮{:.2f}".format(partner_button[2]))
            self.scroll_right_down(times = 1)
            self.run_until(
                lambda: click((partner_button[1][0], partner_button[1][1]+40)),
                lambda: not match(button_pic(ButtonName.BUTTON_MOMOTALK_PARTNER))
            )
            # 羁绊按钮后面必定有羁绊剧情按钮，等待一秒
            sleep(1.5)
        # 前往羁绊剧情按钮
        goto_partner_button = match(button_pic(ButtonName.BUTTON_GO_PARTNER_STORY), returnpos=True)
        if goto_partner_button[0]:
            logging.info("检测到前往羁绊剧情按钮{:.2f}".format(goto_partner_button[2]))
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_GO_PARTNER_STORY)),
                lambda: not match(button_pic(ButtonName.BUTTON_GO_PARTNER_STORY))
            )
            sleep(2)
        # 如果右侧啥按钮都没有，点左侧第二个，然后点左侧第一个，然后右侧往下滚动
        if not reply_button[0] and not partner_button[0] and not goto_partner_button[0]:
            logging.info("回复{:.2f}，羁绊{:.2f}，前往羁绊{:.2f}".format(reply_button[2], partner_button[2], goto_partner_button[2]))
            # 如果进入到剧情里面，这边也就点点左侧中间，无影响
            # 第二条
            click((262, 330), sleeptime=1)
            # 第一条
            click((263, 253))
            # 右侧往下滚动
            self.scroll_right_down(times = 1)
        
        
     
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
                hasstory = self.run_until(
                    lambda: self.click_reply(),
                    lambda: match(button_pic(ButtonName.BUTTON_STORY_MENU)) or not match(popup_pic(PopupName.POPUP_MOMOTALK)),
                    times=10
                )
                # 不管是看到了右上MENU，还是无法匹配到MOMOTALK标题，都尝试跳过剧情
                SkipStory().run()
                # 关闭弹窗, 继续检测第一条消息右侧是不是红色
                matchred = self.whether_has_red_icon()
        logging.info("momotalk处理完毕，返回主页")
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: not match(popup_pic(PopupName.POPUP_MOMOTALK))
        )
        self.back_to_home()
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)