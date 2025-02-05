from nicegui import ui
from gui.components.edit_team_strength import edit_the_team_strength_of_this_config
from gui.components.fast_run_task_buttons import show_fast_run_task_buttons, TaskName

def set_explore(config, real_taskname_to_show_taskname, logArea):
    ui.label(config.get_text("setting_explore")).style('font-size: x-large')
    ui.label(config.get_text("desc_team_strength"))
    ui.checkbox(config.get_text("config_rainbow_teams_desc")).bind_value(config.userconfigdict, "EXPLORE_RAINBOW_TEAMS")
    with ui.card():
        edit_the_team_strength_of_this_config(config, "TEAM_SET_STRENGTH")

    # normal explore
    ui.label(config.get_text("push_normal")).style('font-size: x-large')
    
    ui.label(config.get_text("config_explore_attention"))
    
    with ui.row():
        with ui.card():
            ui.checkbox(config.get_text("config_use_simple_explore")).bind_value(config.userconfigdict, "PUSH_NORMAL_USE_SIMPLE")
            ui.checkbox(config.get_text("config_rainbow_teams_desc")).bind_value(config.userconfigdict, "EXPLORE_RAINBOW_TEAMS")
            ui.number(config.get_text("config_push_normal_desc"), min=4, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_NORMAL_QUEST", forward=lambda x: int(x)).style("width: 300px")
            ui.number(config.get_text("config_level"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_NORMAL_QUEST_LEVEL", forward=lambda x:int(x)).style("width: 300px")
        show_fast_run_task_buttons([TaskName.PUSH_NORMAL], config, real_taskname_to_show_taskname, logArea, show_title=False, show_desc=False)
        
    # hard explore
    ui.label(config.get_text("push_hard")).style('font-size: x-large')
    
    ui.label(config.get_text("config_explore_attention"))
    
    with ui.row():
        with ui.card():
            ui.checkbox(config.get_text("config_use_simple_explore")).bind_value(config.userconfigdict, "PUSH_HARD_USE_SIMPLE")
            ui.checkbox(config.get_text("config_rainbow_teams_desc")).bind_value(config.userconfigdict, "EXPLORE_RAINBOW_TEAMS")
            ui.number(config.get_text("config_push_hard_desc"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_HARD_QUEST", forward=lambda x: int(x)).style("width: 300px")
            ui.number(config.get_text("config_level"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_HARD_QUEST_LEVEL", forward=lambda x:int(x)).style("width: 300px")
        show_fast_run_task_buttons([TaskName.PUSH_HARD], config, real_taskname_to_show_taskname, logArea, show_title=False, show_desc=False)
        
    