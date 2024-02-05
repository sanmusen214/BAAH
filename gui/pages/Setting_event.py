from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_event(config):
    with ui.row():
        ui.link_target("ACTIVITY")
        ui.label(config.get_text("task_event")).style('font-size: x-large')

    
    ui.checkbox(config.get_text("config_auto_event_story")).bind_value(config.userconfigdict, "AUTO_EVENT_STORY_PUSH")
    
    ui.label(config.get_text("config_desc_times"))
    list_edit_area(config.userconfigdict["EVENT_QUEST_LEVEL"], [config.get_text("config_day"), "", [config.get_text("config_level"), config.get_text("config_times")]], config.get_text("config_desc_list_edit"))
