from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_oneclick_raid(config):
    # 一键扫荡
    ui.label(config.get_text("task_oneclick_raid")).style('font-size: x-large')
    # ui.switch(config.get_text("config_event_status")).bind_value(config.userconfigdict, "DO_ONE_CLICK_RAID_ONLY_DURING_TRIPLE") 
    list_edit_area(
        config.userconfigdict["ONE_CLICK_RAID"],
        [
            config.get_text("config_day"), 
            "",
            [
                config.get_text("config_task"),
                config.get_text("config_times")
            ]
        ],
        config.get_text("desc_one_click_raid"),
        has_switch=True
    )