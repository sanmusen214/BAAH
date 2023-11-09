from AllPage.Page import Page
from assets.PageName import PageName

class AllPage:
    # 单例
    def __init__(self) -> None:
        self.nowpage:Page|None = Page(PageName.PAGE_PV_LOGIN)
        self.pageset = set()
    
    def determine_now_page(self,prefer_page=[]) -> Page:
        """
        根据坐标，判断当前页面是啥，更改self.nowpage
        
        prefer_page: 优先判断的页面列表
        """
        # ...
        pass

    def jump_to_page(self, pagename):
        """
        跳转到指定页面
        
        pagename: 页面名
        """
        # ...
        pass
    
    
my_PAGE_PV_LOGIN=Page(PageName.PAGE_PV_LOGIN)
my_PAGE_HOME=Page(PageName.PAGE_HOME)
my_PAGE_CAFE=Page(PageName.PAGE_CAFE)
my_PAGE_TIMETABLE=Page(PageName.PAGE_TIMETABLE)
my_PAGE_TIMETABLE_SEL=Page(PageName.PAGE_TIMETABLE_SEL)
my_PAGE_CLUB=Page(PageName.PAGE_CLUB)
my_PAGE_CRAFT=Page(PageName.PAGE_CRAFT)
my_PAGE_CRAFT_SELECT=Page(PageName.PAGE_CRAFT_SELECT)
my_PAGE_CRAFT_FINISH=Page(PageName.PAGE_CRAFT_FINISH)

my_PAGE_WANTED=Page(PageName.PAGE_WANTED)
my_PAGE_WANTED_1=Page(PageName.PAGE_WANTED_1)
my_PAGE_WANTED_2=Page(PageName.PAGE_WANTED_2)
my_PAGE_WANTED_3=Page(PageName.PAGE_WANTED_3)
my_PAGE_EXCHANGE=Page(PageName.PAGE_EXCHANGE)
my_PAGE_EXCHANGE_1=Page(PageName.PAGE_EXCHANGE_1)
my_PAGE_EXCHANGE_2=Page(PageName.PAGE_EXCHANGE_2)
my_PAGE_ENCHANGE_3=Page(PageName.PAGE_ENCHANGE_3)
my_PAGE_CONTEST=Page(PageName.PAGE_CONTEST)
my_PAGE_EDIT_TEAM=Page(PageName.PAGE_EDIT_TEAM)