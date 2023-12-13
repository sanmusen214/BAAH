from modules.AllPage.Page import Page
from assets.PageName import PageName
from assets.PopupName import PopupName
from assets.ButtonName import ButtonName
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot
import logging


class Task:
    # 父类
    def __init__(self, name, pre_times = 2, post_times = 4) -> None:
        self.name = name
        self.pre_times = pre_times
        self.post_times = post_times
        self.click_magic_when_run = True
        """运行时是否点击魔法点重置窗口状态到Page级别"""
        
    def pre_condition(self) -> bool:
        """
        执行任务前的判断，只判断现有情况，不要进行有效操作(截图或点击)

        确认页面，是否需要做此任务，任务是否已经完成
        
        返回true表示可以执行任务，false表示不能执行任务
        """
        return True
        
    def on_run(self) -> None:
        """
        执行任务时需要做的事情，逻辑判断与操作
        
        如果是复杂的任务，尽量用run_until点击
        """
        pass
    
    def post_condition(self) -> bool:
        """
        执行任务后的判断，只判断现有情况，不要进行有效操作(截图或点击)

        看任务是否回到它该在的页面
        
        返回true表示回到它该在的页面成功，false表示回到它该在的页面失败
        """
        return True
    
    def run(self) -> None:
        """
        （不要重写）
        运行一个任务
        """
        logging.info("判断任务{}是否可以执行".format(self.name))
        if(Task.run_until(self.click_magic_sleep,self.pre_condition, self.pre_times)):
            logging.info("执行任务{}".format(self.name))
            self.on_run()
            logging.info("判断任务{}执行结果是否可控".format(self.name))
            if(Task.run_until(self.click_magic_sleep,self.post_condition, self.post_times)):
                logging.info("任务{}执行结束".format(self.name))
            else:
                logging.warn("任务{}执行后条件不成立或超时".format(self.name))
                if not self.back_to_home():
                    raise Exception("任务{}执行后条件不成立或超时，且无法正确返回主页，程序退出".format(self.name))
        else:
            logging.warn("任务{}执行前条件不成立或超时，跳过此任务".format(self.name))

    @staticmethod
    def back_to_home(times = 3) -> bool:
        """
        尝试从游戏内的页面返回主页
        
        返回成功与否
        """
        logging.info("尝试返回主页")
        click(Page.MAGICPOINT)
        if Task.run_until(lambda: click(button_pic(ButtonName.BUTTON_HOME_ICON)), lambda: Page.is_page(PageName.PAGE_HOME), times=times, sleeptime=3):
            logging.info("返回主页成功")
            return True
        else:
            logging.error("返回主页失败")
            return False
    
    @staticmethod
    def close_any_select_popup(yn: bool = False) -> bool:
        """
        关闭任一有选择性按钮的弹窗（确认弹窗，是否弹窗）一次

        yorn: boolean
            True: 关闭所有弹窗, 遇到选择选是
            False: 关闭所有弹窗, 遇到选择选否
        
        返回是否产生了关闭动作
        """
        # ...
        pass
    
    @staticmethod
    def close_any_non_select_popup() -> bool:
        """
        关闭任一非选择性的弹窗一次，如设置栏，桃信等弹窗
        
        返回是否产生了关闭动作
        """
        isSettingRes = match(popup_pic(PopupName.POPUP_SETTING_SELECT), returnpos=True)
        if(isSettingRes[0]):
            click(isSettingRes[1])
            return True
        return False

    def click_magic_sleep(self, sleeptime = 3):
        if self.click_magic_when_run:
            click(Page.MAGICPOINT, sleeptime)
        else:
            sleep(sleeptime)
    
    @staticmethod
    def run_until(func1, func2, times=5, sleeptime = 1.5) -> bool:
        """
        重复执行func1，至多times次或直到func2成立
        
        func1内部应当只产生有效操作一次或内部调用截图函数, func2判断前会先触发截图
        
        每次执行完func1后,等待sleeptime秒

        如果func2成立退出，返回true，否则返回false
        """
        for i in range(times):
            screenshot()
            if(func2()):
                return True
            func1()
            sleep(sleeptime)
        screenshot()
        if(func2()):
            return True
        logging.warning("run_until exceeded max times")
        return False

    @staticmethod
    def scroll_right_up():
        """
        scroll to top
        """
        swipe((928, 226), (942, 561), sleeptime=0.2)
        swipe((928, 226), (942, 561), sleeptime=0.2)
        swipe((928, 226), (942, 561), sleeptime=0.2)
        sleep(0.5)
    
    @staticmethod
    def scroll_right_down():
        """
        scroll to bottom
        """
        swipe((942, 561), (928, 226), sleeptime=0.2)
        swipe((942, 561), (928, 226), sleeptime=0.2)
        swipe((942, 561), (928, 226), sleeptime=0.2)
        sleep(0.5)
        
        
        