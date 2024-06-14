from nicegui import ui

def set_emulator(config):
    with ui.row():
        ui.link_target("EMULATOR")
        ui.label(config.get_text("setting_emulator")).style('font-size: x-large')
        
    with ui.row():
        # IP+端口
        ui.number(config.get_text("config_emulator_port"),
                step=1,
                precision=0,
                ).bind_value(config.userconfigdict, 'TARGET_PORT', forward=lambda v: int(v), backward=lambda v:int(v)).style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: not v)
        # 序列号
        ui.input(config.get_text("adb_serial")).bind_value(config.userconfigdict, 'ADB_SEIAL_NUMBER').style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: v)
        
        # 切换使用序列号还是IP+端口
        ui.checkbox(config.get_text("adb_direct_use_serial")).bind_value(config.userconfigdict, 'ADB_DIRECT_USE_SERIAL_NUMBER')
        
    
    with ui.row():
        kill_port = ui.checkbox(config.get_text("config_kill_port")).bind_value(config.userconfigdict, "KILL_PORT_IF_EXIST")
        kill_port.set_value(False)
        kill_port.set_enabled(False)
    
    with ui.row():    
        ui.input(config.get_text("config_emulator_path"),
                    ).bind_value(config.userconfigdict, 'TARGET_EMULATOR_PATH',forward=lambda v: v.replace("\\", "/").replace('"','')).style('width: 400px')
    
    ui.checkbox(config.get_text("config_close_emulator_and_baah")).bind_value(config.userconfigdict, 'CLOSE_EMULATOR_BAAH')