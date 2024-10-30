from enum import Enum


class TaskName(Enum):
    LOGIN_GAME = "登录游戏"
    MOMOTALK = "清momotalk"
    CAFE = "咖啡馆"
    CAFE_ONLY_TOUCH = "咖啡馆只摸头"
    TIMETABLE = "课程表"
    CLUB = "社团"
    MANUFACTURE = "制造"
    STORE = "商店"
    BUY_AP = "购买AP"
    BOUNTY = "悬赏通缉"
    SPECIAL = "特殊任务"
    SCHOOL_EXCHANGE_MEETING = "学园交流会"
    TACTICAL_CHALLENGE = "战术大赛"
    HARD = "困难关卡"
    EVENT = "活动关卡"
    ASSAULT = "总力战"
    DAILY = "每日任务"
    MAIL = "邮件"
    NORMAL = "普通关卡"
    PUSH_NORMAL = "普通推图"
    PUSH_HARD = "困难推图"
    MAIN_STORY = "主线剧情"
    CUSTOM = "自定义任务"