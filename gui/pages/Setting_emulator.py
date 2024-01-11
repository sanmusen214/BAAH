from nicegui import ui

def set_emulator(config):
    with ui.row():
        ui.link_target("EMULATOR")
        ui.label(config.get_text("setting_emulator")).style('font-size: x-large')
        
    with ui.row():
        ui.number(config.get_text("config_emulator_port"),
                step=1,
                precision=0,
                ).bind_value(config.userconfigdict, 'TARGET_PORT', forward=lambda v: int(v)).style('width: 400px')
    with ui.row():    
        ui.input(config.get_text("config_emulator_path"),
                    ).bind_value(config.userconfigdict, 'TARGET_EMULATOR_PATH',forward=lambda v: v.replace("\\", "/").replace('"','')).style('width: 400px')
    
    ui.checkbox(config.get_text("config_close_emulator_and_baah")).bind_value(config.userconfigdict, 'CLOSE_EMULATOR_BAAH')