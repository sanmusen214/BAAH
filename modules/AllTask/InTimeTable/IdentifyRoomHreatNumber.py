import numpy as np

from modules.utils import (screenshot, match_pixel)


def get_hearts_of_rooms() -> dict:
    """
    截图并返回所有房间的爱心数，返回一个键值对，{房间的序号:爱心数}
    """
    # 每个房间最右侧学生大头的爱心位置， x：[445, 788, 1133], y: [290, 442, 594]
    baseX = np.linspace(445, 1133, 3, dtype=int)
    baseY = np.linspace(290, 594, 3, dtype=int)
    # 单个房间内爱心x坐标挨个的偏移量 51
    OFFSET_X = -51
    # 爱心的BGR值 [144 118 255]
    COLOR_HEART = [[140, 115, 253], [145, 120, 255]]
    
    total_counts = dict()
    
    for (j, y) in enumerate(baseY):
        for (i, x) in enumerate(baseX):
            # 一个房间最多三个爱心，向左最多偏移次数3次
            heart_count = 0
            for t in range(3):
                if match_pixel((x + t * OFFSET_X, y), COLOR_HEART):
                    heart_count += 1
            # 序号从1开始
            total_counts[j * 3 + i + 1] = heart_count
    # print("爱心数量", total_counts)
    
    return total_counts

def get_open_status_of_rooms() -> dict:
    """
    得到所有房间的开放状态，返回一个键值对，{房间的序号:是否开放}
    
    0表示解锁且未点击过 0.5表示解锁但是已被点击了 1表示未解锁
    """
    # 每个房间右上部分空白处， x：[445, 788, 1133], y: [270, 422, 574]
    baseX = np.linspace(445, 1133, 3, dtype=int)
    baseY = np.linspace(270, 574, 3, dtype=int)
    # 白色部分的BGR值 [253 255 255]
    COLOR_OPEN = [[250, 250, 250], [255, 255, 255]]
    # 已解锁但是被点击过的BGR值 [237 239 239]
    COLOR_CLICKED = [[230, 230, 230], [245, 245, 245]]
    # 未解锁部分的BGR值  [41 42 42]
    COLOR_LOCK = [[38, 38, 38], [45, 45, 45]]
    # 不存在教室的BGR值 [205 207 207]
    COLOR_NOROOM = [[200, 200, 200], [210, 210, 210]]
    
    total_counts = dict()
    
    for (j, y) in enumerate(baseY):
        for (i, x) in enumerate(baseX):
            if match_pixel((x, y), COLOR_NOROOM):
                print(f"rooms unlock/lock status：{total_counts}")
                return total_counts
            # 0表示解锁且未点击过 0.5表示解锁但是已被点击了 1表示未解锁
            total_counts[j * 3 + i + 1] = 0
            if match_pixel((x, y), COLOR_CLICKED):
                total_counts[j * 3 + i + 1] = 0.5
            if match_pixel((x, y), COLOR_LOCK):
                total_counts[j * 3 + i + 1] = 1
    # print(f"房间开启状态：{total_counts}")
    return total_counts
    