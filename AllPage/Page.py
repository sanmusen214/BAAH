from utils import match, page_pic

import config

class Page:
    CENTER = (config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2)
    """
    Center of the screen
    """
    MAGICPOINT = (498, 30)
    """
    Magicpoint is the point that never contains any activable item
    """
    HOMEPOINT = (1236, 25)
    """
    Most of the time, the home icon on the top right corner
    """
    TOPLEFTBACK = (56, 28)
    """
    The circle back icon on the top left corner
    """

    # 父类
    def __init__(self, pagename) -> None:
        self.name = pagename
        self.topages = dict()
    
    def add_topage(self, pagename, item):
        """
        添加从这一页面到另一页面的链接
        
        page: 另一页面的Page名
        item: 图片地址或坐标元组
        """
        self.topages[pagename]=item
    
    def is_this_page(self) -> bool:
        """
        确定当前截图是否是这一页面
        
        return: 如果是这一页面，返回True，否则返回False
        """
        return match(page_pic(self.name))
    
    @staticmethod
    def is_page(pagename, task = None) -> bool:
        """
        确定当前截图是否是指定页面
        
        pagename: PageName下的页面名
        
        task: 如果传入一个Task对象，则会在判断前调用task.close_any_non_select_popup()确保关闭了所有非选项弹窗
        
        return: 如果是指定页面，返回True，否则返回False
        """
        if task:
            # 循环清除弹窗
            havefound = True
            while(havefound):
                havefound = task.close_any_non_select_popup()
        return match(page_pic(pagename))