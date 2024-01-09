from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_event(config):
    with ui.row():
        ui.link_target("ACTIVITY")
        ui.label('活动关卡').style('font-size: x-large')

    ui.label('关于次数的说明：4次就是扫荡4次，-1次即为扫荡max次，-2次即为扫荡max-2次。')
    list_edit_area(config.userconfigdict["EVENT_QUEST_LEVEL"], ["天刷取", "", ["关卡", "次数"]], "一个月有30天，如果在这里定义了30天每天刷什么，那么每天都会刷取不同的东西。如果定义了3天，那每三天一轮按照这个来刷取。如果只定义1天，那么每天都按照那个刷。")