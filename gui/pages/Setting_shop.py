from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_shop(config):
    with ui.row():
        ui.link_target("SHOP_NORMAL")
        ui.label('商店（一般）').style('font-size: x-large')
    
    
    ui.number(
            '商店（一般）刷新次数',
            step=1,
            precision=0,
            min=0,
            max=3
            ).bind_value(config.userconfigdict, 'SHOP_NORMAL_REFRESH_TIME', forward=lambda v: int(v)).style('width: 400px')
    
    list_edit_area(config.userconfigdict["SHOP_NORMAL"], ["行", "物品"], "其中行数指普通商店里右侧物品的行，物品指那一行里从左到右四个物品。如果某一行不买物品就把那一行不添加物品就行了")
    
    with ui.row():
        ui.link_target("SHOPCONTEST")
        ui.label('商店（战术大赛）').style('font-size: x-large')
        
    ui.number(
            '商店（战术大赛）刷新次数',
            step=1,
            precision=0,
            min=0,
            max=3
            ).bind_value(config.userconfigdict, 'SHOP_CONTEST_REFRESH_TIME', forward=lambda v: int(v)).style('width: 400px')
        
    list_edit_area(config.userconfigdict["SHOP_CONTEST"], ["行", "物品"], "其中行数指竞技场商店里右侧物品的行，物品指那一行里从左到右四个物品。如果某一行不买物品就把那一行不添加物品就行了")