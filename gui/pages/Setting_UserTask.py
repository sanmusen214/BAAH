from nicegui import ui

def set_usertask(config):
    with ui.row():
        ui.link_target("USER_DEF_TASK")
        ui.label(config.get_text("task_user_def_task")).style('font-size: x-large')
    
    with ui.row():
        ui.textarea(label = config.get_text("task_user_def_task")).bind_value(config.userconfigdict, "USER_DEF_TASKS").style('width: 40vw;')