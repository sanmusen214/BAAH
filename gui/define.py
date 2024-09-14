from modules.configs.MyConfig import MyConfigger
from common import TaskName

# 构造一个config，用于在tab间共享softwareconfigdict
gui_shared_config = MyConfigger()


class TaskStr:
    def __init__(self, task_enum: TaskName, json_key_name: str):
        self.task_enum = task_enum
        self.json_key_name = json_key_name


CURR_TASK_LIST: list[TaskStr] = [
    TaskStr(TaskName.LOGIN_GAME, "task_login_game"),
    TaskStr(TaskName.MOMOTALK, "task_clear_momotalk"),
    TaskStr(TaskName.CAFE, "task_cafe"),

    # compatibility, just changed display name
    TaskStr(TaskName.TACTICAL_CHALLENGE, "task_cafe_deprecated"),

    TaskStr(TaskName.TIMETABLE, "task_timetable"),
    TaskStr(TaskName.CLUB, "task_club"),
    TaskStr(TaskName.MANUFACTURE, "task_craft"),
    TaskStr(TaskName.STORE, "task_shop"),
    TaskStr(TaskName.BUY_AP, "task_buy_ap"),
    TaskStr(TaskName.BOUNTY, "task_wanted"),
    TaskStr(TaskName.SPECIAL, "task_special"),
    TaskStr(TaskName.SCHOOL_EXCHANGE_MEETING, "task_exchange"),
    TaskStr(TaskName.TACTICAL_CHALLENGE, "task_contest"),
    TaskStr(TaskName.HARD, "task_hard"),
    TaskStr(TaskName.EVENT, "task_event"),
    TaskStr(TaskName.ASSAULT, "task_assault"),
    TaskStr(TaskName.DAILY, "task_daily"),
    TaskStr(TaskName.MAIL, "task_mail"),
    TaskStr(TaskName.NORMAL, "task_normal"),
    TaskStr(TaskName.PUSH_NORMAL, "push_normal"),
    TaskStr(TaskName.PUSH_HARD, "push_hard"),
    TaskStr(TaskName.MAIN_STORY, "push_main_story"),
    TaskStr(TaskName.CUSTOM, "task_user_def_task"),
]


def get_task_name_map_dict(config_cls: MyConfigger) -> dict:
    """
    can get a map of task_name(in code) to task_name(diff language from config file set that one)
    Args:
        config_cls(MyConfigger): a MyConfigger class that loaded file name
    Returns:
        a dict that key:val is code task name: language task name
    """
    return {i.task_enum.value: config_cls.get_text(i.json_key_name) for i in CURR_TASK_LIST}
