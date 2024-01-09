from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_special(config):
    with ui.row():
        ui.link_target("SPECIAL_TASK")
        ui.label(config.get_text("task_special")).style('font-size: x-large')
    
    ui.label(config.get_text("config_desc_times"))
    
    list_edit_area(
        config.userconfigdict["SPECIAL_HIGHTEST_LEVEL"], 
        [
            config.get_text("config_day"), 
            "",
            [
                config.get_text("config_location"),
                config.get_text("config_level"),
                config.get_text("config_times")
            ]
        ], 
        config.get_text("config_desc_list_edit")
    )
            