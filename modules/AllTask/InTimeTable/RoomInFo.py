import numpy


HEART_RATE = 0.5
MATERIAL_RATE = 0.5


class RoomInFo:
    def __init__(self, school_idx: int, room_idx: int, heart_num: int):
        self.school_idx = school_idx
        self.room_idx = room_idx
        self.heart_num = heart_num

    def calculate_value(self):
        return self.heart_num * HEART_RATE + self.room_idx * MATERIAL_RATE
