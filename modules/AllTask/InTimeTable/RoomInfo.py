import numpy


# 爱心在计算中占比多少
HEART_RATE = 0.5
# 材料在计算中占比多少
MATERIAL_RATE = 0.5


class RoomInfo:
    """
    课程表上每一个房间的具体信息

    Parameters:
        school_idx: 该room属于哪个学校（的下标）
        room_idx: 该room的位置下标
        heart_num: room房间中学生的爱心数量

    """
    def __init__(self, school_idx: int, room_idx: int, heart_num: int):
        self.school_idx = school_idx
        self.room_idx = room_idx
        self.heart_num = heart_num

    def calculate_value(self):
        """最后课程表的选择根据此函数的返回值进行排序"""
        return self.heart_num / 3 * HEART_RATE + self.room_idx / 8 * MATERIAL_RATE

    def __lt__(self, other):
        return self.calculate_value() <= other.calculate_value()

    def __str__(self):
        return f"school:{self.school_idx}, room:{self.room_idx}, heart:{self.heart_num}, value:{self.calculate_value()}"
