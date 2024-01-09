from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_timetable(config):
    with ui.row():
        ui.link_target("TIME_TABLE")
        ui.label('课程表/日程').style('font-size: x-large')
    
    list_edit_area(config.userconfigdict["TIMETABLE_TASK"], ["个地区", "房间"], "其中地区指课程表/日程右侧那些列表的不同选项卡（夏莱办公室，夏莱居住区等）\n房间指课程表/日程每个学院里的房间，从左往右从上往下数，数字从1到9\n如果某个地区没有设置点击的房间则会跳过那个地区")