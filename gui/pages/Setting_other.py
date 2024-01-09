from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_other(config):
    with ui.row():
        ui.link_target("TOOL_PATH")
        ui.label('其他设置').style('font-size: x-large')
        
    ui.label("注意：以下设置不建议修改，除非你知道你在干什么").style('color: red')
    
    with ui.row():
        ui.number('点击后停顿时间', 
                    suffix="s",
                    step=0.1,
                    precision=1).bind_value(config.userconfigdict, 'TIME_AFTER_CLICK')
    
    ui.label("滑动过头此项调小60->40，滑动距离不够此项调大40->60")
    with ui.row():
        ui.number("滑动触发距离",
                    step=1,
                    min=1,
                    precision=0).bind_value(config.userconfigdict, 'RESPOND_Y', forward=lambda x:int(x), backward=lambda x:int(x)).bind_enabled(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y', forward=lambda v: not v, backward=lambda v: not v)
        ui.checkbox("与区服绑定(国服官服60，其他40)").bind_value(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y')
        
    with ui.row():
        ui.input("模拟器监听IP地址（此项不包含端口号）").bind_value(config.userconfigdict, 'TARGET_IP_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
    
    with ui.row():
        ui.input('ADB.exe路径').bind_value(config.userconfigdict, 'ADB_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
    
    with ui.row():
        ui.input('截图名称').bind_value(config.userconfigdict, 'SCREENSHOT_NAME',forward=lambda v: v.replace("\\", "/")).style('width: 400px').set_enabled(False)