from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_timetable(config):
    with ui.row():
        ui.link_target("TIME_TABLE")
        ui.label(config.get_text("task_timetable")).style('font-size: x-large')
    
    ui.checkbox(config.get_text("config_smart_timetable_desc")).bind_value(config.userconfigdict, "SMART_TIMETABLE")
    
    with ui.column() as smart_area:
        ui.number(config.get_text("config_weight_of_rewards"), precision=0, step=1).bind_value(config.userconfigdict, "TIMETABLE_WEIGHT_OF_REWARD").style("width: 300px")
        ui.number(config.get_text("config_weight_of_hearts"), precision=0, step=1).bind_value(config.userconfigdict, "TIMETABLE_WEIGHT_OF_HEART").style("width: 300px")
        ui.number(config.get_text("config_weight_of_lock"), precision=0, step=1).bind_value(config.userconfigdict, "TIMETABLE_WEIGHT_OF_LOCK").style("width: 300px")
    smart_area.bind_visibility_from(config.userconfigdict, "SMART_TIMETABLE")
    
    with ui.column() as edit_area:
        list_edit_area(config.userconfigdict["TIMETABLE_TASK"], [config.get_text("config_location"), config.get_text("config_room")], config.get_text("config_desc_timetable"))
    edit_area.bind_visibility_from(config.userconfigdict, "SMART_TIMETABLE", backward=lambda x: not x)