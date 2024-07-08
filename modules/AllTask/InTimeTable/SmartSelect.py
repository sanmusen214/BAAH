from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InTimeTable.LocationSelect import LocationSelect
from modules.AllTask.Task import Task
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect

from modules.utils import (click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot,
                           match_pixel, ocr_area_0, get_screenshot_cv_data)
from .IdentifyRoomHreatNumber import get_hearts_of_rooms, get_open_status_of_rooms
from modules.utils.log_utils import logging
import numpy as np


class SmartSelect(Task):
    def __init__(self, name="SmartSelect") -> None:
        super().__init__(name)
        # 每个地区右上角的名字区域
        self.location_name_area = ((923, 94), (1132, 130))

    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_TIMETABLE)

    def get_tickets_number(self) -> int:
        """
        获取票卷数量，然后关闭弹窗
        """
        self.clear_popup()
        # 点票卷详情
        self.run_until(
            lambda: click((110, 99)),
            lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
        )
        # 识别
        if ocr_area_0((580, 333), (628, 368)):
            self.clear_popup()
            return 0
        ticket_num = ocr_area((580, 333), (628, 368))[0]
        try:
            ticket_num = int(ticket_num)
        except:
            logging.error({"zh_CN": f"识别票卷数量失败，识别结果：{ticket_num}, 请反馈",
                           "en_US": f"Cannot recognize ticket number, result: {ticket_num}, please feedback"})
            ticket_num = 8
        # 关闭弹窗
        self.clear_popup()
        return ticket_num

    def evaluate_score(self, seq_this_room: int, heart_of_this_room: int, lock_num_of_this_area: int) -> int:
        """给格子打分, seq_this_room房子序号从1开始"""
        # 奖励
        weight_of_reward = config.userconfigdict["TIMETABLE_WEIGHT_OF_REWARD"]
        # 爱心
        weight_of_heart = config.userconfigdict["TIMETABLE_WEIGHT_OF_HEART"]
        # 未解锁房间
        weight_of_lock = config.userconfigdict["TIMETABLE_WEIGHT_OF_LOCK"]
        row_ind = (seq_this_room - 1) // 3
        score = weight_of_reward * row_ind + weight_of_heart * heart_of_this_room + weight_of_lock * lock_num_of_this_area
        return score

    def on_run(self) -> None:
        # 获取现在票数
        tickets = self.get_tickets_number()
        logging.info({"zh_CN": f"当前票卷数量：{tickets}",
                      "en_US": f"Current ticket quantity: {tickets}"})
        if tickets == 0:
            logging.warn({"zh_CN": "卷票数量为0，无法选择教室", "en_US": "Tickets number is 0, cannot select room"})
            return
        # 存储各个下标教室对应的教室的分数，[地区下标，教室序号，分数]
        rooms_scores = []
        # 第一个地区
        ScrollSelect(0, 130, 236, 669, 1114, lambda: Page.is_page(PageName.PAGE_TIMETABLE_SEL)).run()

        # 存右上角图像，这里使用数组下标
        def cut_location_name_area():
            return get_screenshot_cv_data()[self.location_name_area[0][1]:self.location_name_area[1][1],
                   self.location_name_area[0][0]:self.location_name_area[1][0]]

        sleep(1)
        screenshot()
        initial_area_data = cut_location_name_area()

        # 最多循环15次
        for i in range(15):
            # 判断是否中断搜索
            if i != 0:
                # 存右上角图像，比较差异
                screenshot()
                current_area_data = cut_location_name_area()
                similar = 1 - np.sum(np.abs(initial_area_data - current_area_data)) / np.sum(initial_area_data)
                logging.info(f"similar: {similar}")
                # 如果回到了第一个地区
                if similar > 0.99:
                    break
            # 获取当前地区的教室的心数
            # 点右下按钮
            self.run_until(
                lambda: click(button_pic(ButtonName.BUTTON_ALL_TIMETABLE)),
                lambda: match(popup_pic(PopupName.POPUP_TIMETABLE_ALL))
            )
            heartdict = get_hearts_of_rooms()
            opendict = get_open_status_of_rooms()
            # 计算分数
            for room_num in range(1, 10):
                if room_num not in opendict or opendict[room_num] == 1:
                    # 不存在的房间 或 房间未解锁，结束
                    break
                else:
                    lockednum = sum(opendict.values())
                    rooms_scores.append([i, room_num, self.evaluate_score(room_num, heartdict[room_num], lockednum)])
            # 清除弹窗
            self.clear_popup()
            # 往后翻页
            click((1248, 362), sleeptime=1)
        # 此时回到第一个地区
        # print(rooms_scores)
        # 大到小排序, 取前tickets个
        rooms_scores.sort(key=lambda x: x[2], reverse=True)
        rooms_scores = rooms_scores[:tickets]
        logging.info({"zh_CN": f"最终选择的教室：{rooms_scores}",
                      "en_US": f"Final classrooms selected: {rooms_scores}"})
        max_location_ind = max(rooms_scores, key=lambda x: x[0])[0]
        # 整合成字典 {地区下标: [教室序号, ...]}
        timetable_dict = {}
        for i, room_num, score in rooms_scores:
            if i not in timetable_dict:
                timetable_dict[i] = []
            timetable_dict[i].append(room_num)
        print(timetable_dict)
        # 点击
        for i in range(max_location_ind + 1):
            # 处理i地区
            if i in timetable_dict:
                LocationSelect(location=-1, classrooms=timetable_dict[i], backtoLocationPage=False).run()
            # 右边箭头
            click((1248, 362), sleeptime=1)

    def post_condition(self) -> bool:
        return super().post_condition()