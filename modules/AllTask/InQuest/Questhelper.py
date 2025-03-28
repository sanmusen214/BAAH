from modules.utils import click, match_pixel, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area
from modules.AllTask.Task import Task
from modules.AllPage.Page import Page
from modules.utils.log_utils import logging

def jump_to_page(to_num: int) -> bool:
    """
    Jump to page
    
    return True if it is in the page finally
    """
    return Task.run_until(
        lambda: jump_to_neighbour_page(to_num),
        lambda: ocr_area((122, 179), (165, 211))[0] == str(to_num),
        sleeptime=0.6
    )
     
def jump_to_neighbour_page(to_num: int) -> bool:
    """
    Jump to neighbour page
    
    return True if it is already in the page
    """
    # 清除弹窗
    Task.run_until(
        lambda: click(Page.MAGICPOINT),
        lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
    )
    ocr_str = ocr_area((122, 179), (165, 211))[0]
    if ocr_str == "":
        return False
    # 如果字符串无法识别为数字，返回false
    try:
        now_num = int(ocr_str)
    except ValueError:
        return False
    logging.debug(f"now_num: {now_num}, to_num: {to_num}")
    if now_num < to_num:
        for i in range(to_num - now_num):
            click((1242, 357))
    elif now_num > to_num:
        for i in range(now_num - to_num):
            click((40, 357))
    else:
        return True
    return False

def close_popup_until_see(picurl) -> None:
    Task.run_until(
        lambda: click(Page.MAGICPOINT),
        lambda: match(picurl)
    )
    
def judge_whether_3star():
    """
    判断弹窗内是否已经三星
    """
    gray_star = ((195, 195, 195), (205, 205, 205))
    star_positions = ((168, 372), (168, 406), (168, 439))
    has_star_count = 0
    for pos in star_positions:
        if not match_pixel(pos, gray_star):
            has_star_count += 1
    return has_star_count == 3

# 集中指挥
center_tab_pos_L = (589, 180)
# 简易攻略
easy_tab_pos_R = (702, 181)
def quest_has_easy_tab():
    # 集中指挥tab栏未选中时的绿色
    unselect_color_L = ((175, 245, 193), (180, 250, 200))
    # 简易攻略tab未选中的蓝色
    unselect_color_R = ((241, 221, 166), (246, 226, 171))
    has_easy_tab = match_pixel(center_tab_pos_L, unselect_color_L) or match_pixel(easy_tab_pos_R, unselect_color_R)
    return has_easy_tab


def has_triple_result_event():
    """判断普通关和困难关是否处于双/三倍活动中"""
    return match_pixel((155, 266), Page.COLOR_PINK,printit=True) or match_pixel((224, 265), Page.COLOR_PINK,printit=True)