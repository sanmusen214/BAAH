from modules.configs.MyConfig import MyConfigger
from common import TaskName

# 构造一个config，用于在tab间共享softwareconfigdict
gui_shared_config = MyConfigger()


def get_task_name_map_dict(config_cls: MyConfigger) -> dict:
    """
    can get a map of task_name(in code) to task_name(diff language from config file set that one)
    Args:
        config_cls(MyConfigger): a MyConfigger class that loaded file name
    Returns:
        a dict that key:val is code task name: language task name
    """
    return {
        TaskName.LOGIN_GAME.value: config_cls.get_text("task_login_game"),
        TaskName.MOMOTALK.value: config_cls.get_text("task_clear_momotalk"),
        TaskName.CAFE.value: config_cls.get_text("task_cafe"),

        # compatibility just change show name
        TaskName.CAFE_ONLY_TOUCH.value: config_cls.get_text("task_cafe_deprecated"),

        TaskName.TIMETABLE.value: config_cls.get_text("task_timetable"),
        TaskName.CLUB.value: config_cls.get_text("task_club"),
        TaskName.MANUFACTURE.value: config_cls.get_text("task_craft"),
        TaskName.STORE.value: config_cls.get_text("task_shop"),
        TaskName.BUY_AP.value: config_cls.get_text("task_buy_ap"),
        TaskName.BOUNTY.value: config_cls.get_text("task_wanted"),
        TaskName.SPECIAL.value: config_cls.get_text("task_special"),
        TaskName.SCHOOL_EXCHANGE_MEETING.value: config_cls.get_text("task_exchange"),
        TaskName.TACTICAL_CHALLENGE.value: config_cls.get_text("task_contest"),
        TaskName.HARD.value: config_cls.get_text("task_hard"),
        TaskName.EVENT.value: config_cls.get_text("task_event"),
        TaskName.ASSAULT.value: config_cls.get_text("task_assault"),
        TaskName.DAILY.value: config_cls.get_text("task_daily"),
        TaskName.MAIL.value: config_cls.get_text("task_mail"),
        TaskName.NORMAL.value: config_cls.get_text("task_normal"),
        TaskName.PUSH_NORMAL.value: config_cls.get_text("push_normal"),
        TaskName.PUSH_HARD.value: config_cls.get_text("push_hard"),
        TaskName.MAIN_STORY.value: config_cls.get_text("push_main_story"),
        TaskName.CUSTOM.value: config_cls.get_text("task_user_def_task"),
    }
