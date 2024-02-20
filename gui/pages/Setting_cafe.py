from nicegui import ui

def set_cafe(config):
    with ui.row():
        ui.link_target("CAFE")
        ui.label(config.get_text("task_cafe")).style('font-size: x-large')
    
    ui.label(config.get_text("config_cafe_attention"))
    
    with ui.row():
        ui.checkbox(config.get_text("config_camera_full")).bind_value(config.userconfigdict, "CAFE_CAMERA_FULL")
        ui.checkbox(config.get_text("enable_diff_touch")).bind_value(config.userconfigdict, "CAFE_TOUCH_WAY_DIFF").bind_visibility_from(config.userconfigdict, "CAFE_CAMERA_FULL")