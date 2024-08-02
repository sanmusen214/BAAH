from nicegui import ui
from modules.configs.settingMaps import server2pic, server2activity, server2respond

def set_server(config):
    with ui.row():
        ui.link_target("SERVER")
        ui.label(config.get_text("setting_server")).style('font-size: x-large')
    
    server = ui.radio({
        "JP":config.get_text("config_server_jp"), 
        "GLOBAL":config.get_text("config_server_global"), 
        "GLOBAL_EN":config.get_text("config_server_global_en"),
        "CN":config.get_text("config_server_cn"),
        "CN_BILI":config.get_text("config_server_cn_b")},
                      value=config.userconfigdict['SERVER_TYPE'], on_change=lambda a:set_server_info(a.value)).props('inline')

    fanhexie = ui.checkbox('如果游戏开了反和谐请勾选此项（手机显示“momotalk”勾选，手机显示“桃信”不要勾）').bind_value(config.userconfigdict, "FANHEXIE").bind_visibility_from(config.userconfigdict, "SERVER_TYPE", lambda x: x in ["CN", "CN_BILI"])
    
    def set_server_info(servername):
        config.userconfigdict['SERVER_TYPE'] = servername
        config.userconfigdict["PIC_PATH"] = server2pic[servername]
        config.userconfigdict["ACTIVITY_PATH"] = server2activity[servername]
        if config.userconfigdict["LOCK_SERVER_TO_RESPOND_Y"]:
            config.userconfigdict["RESPOND_Y"] = server2respond[servername]
        # 控制反和谐的值
        if servername not in ["CN", "CN_BILI"]:
            config.userconfigdict["FANHEXIE"] = False