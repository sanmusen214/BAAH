from nicegui import ui

def set_emulator(config):
    with ui.row():
        ui.link_target("EMULATOR")
        ui.label('模拟器配置').style('font-size: x-large')
        
    with ui.row():
        ui.number('模拟器端口',
                step=1,
                precision=0,
                ).bind_value(config.userconfigdict, 'TARGET_PORT', forward=lambda v: int(v)).style('width: 400px')
    with ui.row():    
        ui.input('模拟器路径'
                    ).bind_value(config.userconfigdict, 'TARGET_EMULATOR_PATH',forward=lambda v: v.replace("\\", "/").replace('"','')).style('width: 400px')