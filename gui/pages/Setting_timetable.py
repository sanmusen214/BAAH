from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_timetable(config):
    with ui.row():
        ui.link_target("TIME_TABLE")
        ui.label(config.get_text("task_timetable")).style('font-size: x-large')
    
    list_edit_area(config.userconfigdict["TIMETABLE_TASK"], [config.get_text("config_location"), config.get_text("config_room")], config.get_text("config_desc_timetable"))