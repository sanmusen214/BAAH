from utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_number
from AllTask.Task import Task
from AllPage.Page import Page
import logging

def jump_to_page(to_num: int) -> bool:
    """
    Jump to page
    
    return True if it is in the page finally
    """
    return Task.run_until(
        lambda: jump_to_neighbour_page(to_num),
        lambda: ocr_number((122, 179), (165, 211)) == str(to_num),
        sleeptime=0.5
    )
     
def jump_to_neighbour_page(to_num: int) -> bool:
    """
    Jump to neighbour page
    
    return True if it is already in the page
    """
    ocr_str = ocr_number((122, 179), (165, 211))
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