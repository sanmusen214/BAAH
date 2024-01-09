from nicegui import ui
import os
from gui.pages.Setting_cafe import set_cafe
from gui.pages.Setting_emulator import set_emulator
from gui.pages.Setting_event import set_event
from gui.pages.Setting_exchange import set_exchange
from gui.pages.Setting_hard import set_hard
from gui.pages.Setting_normal import set_normal
from gui.pages.Setting_other import set_other
from gui.pages.Setting_server import set_server
from gui.pages.Setting_shop import set_shop
from gui.pages.Setting_special import set_special
from gui.pages.Setting_task_order import set_task_order
from gui.pages.Setting_timetable import set_timetable
from gui.pages.Setting_wanted import set_wanted
from modules.configs.MyConfig import MyConfigger

@ui.refreshable
def show_GUI(load_jsonname):
        
    config = MyConfigger()
    config.parse_user_config(load_jsonname)
    
    with ui.row():
        ui.label("Blue Archive Aris Helper").style('font-size: xx-large')
    
    ui.label("BAAH可以帮助你完成碧蓝档案/蔚蓝档案的日服，国际服，国服官服，国服B服的每日任务")
    ui.label("QQ群：441069156")

    ui.label("获取最新版本可以到Github下载，或进群下载")
    
    ui.label("模拟器分辨率请设置为1280*720，240DPI!").style('color: red; font-size: x-large')

    # myAllTask里面的key与GUI显示的key的映射
    real_taskname_to_show_taskname = {
        "登录游戏":"登录游戏",
        "清momotalk":"清momotalk",
        "咖啡馆":"咖啡馆",
        "咖啡馆只摸头":"咖啡馆只摸头",
        "课程表":"课程表/日程",
        "社团":"社团",
        "商店":"商店",
        "悬赏通缉":"悬赏通缉/指名手配",
        "特殊任务":"特殊任务/委托/依赖",
        "学园交流会":"学园交流会",
        "战术大赛":"战术大赛/竞技场",
        "困难关卡":"困难关卡",
        "活动关卡":"活动关卡",
        "每日任务":"每日任务",
        "邮件":"邮件",
        "普通关卡":"普通关卡",
    }

    # =============================================

    # =============================================

    with ui.row().style('min-width: 800px; display: flex; flex-direction: row;flex-wrap: nowrap;'):
        with ui.column().style('width: 200px; overflow: auto;flex-grow: 1;position: sticky; top: 20px;'):
            with ui.card():
                ui.link('模拟器配置', '#EMULATOR')
                ui.link('服务器配置', '#SERVER')
                ui.link('任务执行顺序', '#TASK_ORDER')
                ui.link('后续配置文件', '#NEXT_CONFIG')
                ui.link('咖啡馆', '#CAFE')
                ui.link('课程表/日程', '#COURSE_TABLE')
                ui.link('商店', '#SHOP_NORMAL')
                ui.link('悬赏通缉/指名手配', '#WANTED')
                ui.link('特殊任务/委托/依赖', '#SPECIAL_TASK')
                ui.link('学园交流会', '#EXCHANGE')
                ui.link('活动关卡', '#ACTIVITY')
                ui.link('困难关卡', '#HARD')
                ui.link('普通关卡', '#NORMAL')
                ui.link('其他设置', '#TOOL_PATH')


        with ui.column().style('flex-grow: 4;'):
            # 模拟器配置
            set_emulator(config)
            
            # 服务器配置
            set_server(config)
            
            # 任务执行顺序，后续配置文件
            set_task_order(config, real_taskname_to_show_taskname)
            
            # 咖啡馆
            set_cafe(config)
            
            # 课程表
            set_timetable(config)
                
            # 商店
            set_shop(config)
            
            # 悬赏通缉
            set_wanted(config)
            
            # 特殊任务
            set_special(config)
            
            # 学园交流会
            set_exchange(config)

            # 活动关卡
            set_event(config)
                
            # 困难关卡
            set_hard(config)
            
            # 普通关卡
            set_normal(config)
            
            # 其他设置
            set_other(config)
            
        with ui.column().style('width: 10vw; overflow: auto; position: fixed; bottom: 40px; right: 20px;min-width: 150px;'):
            def save_and_alert():
                config.save_user_config(load_jsonname)
                ui.notify("保存成功")
            ui.button('保存配置', on_click=save_and_alert)

            def save_and_alert_and_run():
                config.save_user_config(load_jsonname)
                ui.notify("保存成功")
                ui.notify("开始执行")
                # 打开同目录中的BAAH.exe，传入当前config的json文件名
                os.system(f"start BAAH{MyConfigger.NOWVERSION}.exe {load_jsonname}")
            ui.button('保存并执行此配置', on_click=save_and_alert_and_run)
        
    # 加载完毕保存一下config，让新建的config文件有默认值
    config.save_user_config(load_jsonname)