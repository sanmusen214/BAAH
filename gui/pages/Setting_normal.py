from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_normal(config):
    
    with ui.row():
        ui.link_target("NORMAL")
        ui.label(config.get_text("task_normal")).style('font-size: x-large')
    
    ui.label(config.get_text("config_desc_times"))
    ui.switch(config.get_text("config_event_status")).bind_value(config.userconfigdict, "NORMAL_QUEST_EVENT_STATUS") 
    list_edit_area(
        config.userconfigdict["NORMAL"], 
        [
            config.get_text("config_day"), 
            "",
            [
                config.get_text("config_location"),
                config.get_text("config_level"),
                config.get_text("config_times")
            ]
        ], 
        config.get_text("config_desc_list_edit"),
        has_switch=True
    )
    # explore
    ui.label(config.get_text("push_normal")).style('font-size: x-large')
    
    ui.label(config.get_text("config_explore_attention"))
    
    with ui.card():
        ui.checkbox(config.get_text("config_rainbow_teams_desc")).bind_value(config.userconfigdict, "EXPLORE_RAINBOW_TEAMS")
        ui.number(config.get_text("config_push_normal_desc"), min=4, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_NORMAL_QUEST", forward=lambda x: int(x)).style("width: 300px")
        ui.number(config.get_text("config_level"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_NORMAL_QUEST_LEVEL", forward=lambda x:int(x)).style("width: 300px")
    