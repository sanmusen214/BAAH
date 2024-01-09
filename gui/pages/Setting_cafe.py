from nicegui import ui

def set_cafe(config):
    with ui.row():
        ui.link_target("CAFE")
        ui.label('咖啡馆').style('font-size: x-large')
    
    ui.label("国服目前咖啡馆的视角无法继承，请取消勾选以下这项").style('color: red')
    ui.label("国际服/日服咖啡馆请将视角拉到最高，保持勾选以下这项")
    
    with ui.row():
        ui.checkbox("进入咖啡馆时视角是最高").bind_value(config.userconfigdict, "CAFE_CAMERA_FULL")