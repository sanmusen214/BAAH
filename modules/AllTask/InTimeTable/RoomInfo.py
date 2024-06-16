import numpy


HEART_RATE = 0.5
MATERIAL_RATE = 0.5


class RoomInfo:
    def __init__(self, school_idx: int, room_idx: int, heart_num: int):
        self.school_idx = school_idx
        self.room_idx = room_idx
        self.heart_num = heart_num

    def calculate_value(self):
        return self.heart_num / 3 * HEART_RATE + self.room_idx / 8 * MATERIAL_RATE

    def __lt__(self, other):
        return self.calculate_value() <= other.calculate_value()

    def __str__(self):
        return f"school:{self.school_idx}, room:{self.room_idx}, heart:{self.heart_num}, value:{self.calculate_value()}"