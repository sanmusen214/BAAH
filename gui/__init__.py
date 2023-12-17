from nicegui import ui
import logging
import json
from modules.utils.MyConfig import MyConfigger

def show_GUI():
    config = MyConfigger("config.json")
    # 在GUI里，我们只使用config.configdict这个字典，不用config下的属性
    all_names = [
        "TARGET_PORT",
        "TARGET_EMULATOR_PATH",
        "TIME_AFTER_CLICK",
        "TIMETABLE_TASK",
        "WANTED_HIGHEST_LEVEL",
        "SPECIAL_HIGHTEST_LEVEL",
        "EXCHANGE_HIGHEST_LEVEL",
        "EVENT_QUEST_LEVEL",
        "QUEST",
        "TASK_ORDER",
        "PIC_PATH",
        "ACTIVITY_PATH",
        "ADB_PATH",
        "SCREENSHOT_NAME"
    ]
    
    
    server_pic_folder_map = {
        "国际服": "assets",
        "日服": "assets_jp",
    }
    
    server_app_map = {
        "国际服":"com.nexon.bluearchive/.MxUnityPlayerActivity",
        "日服":"com.YostarJP.BlueArchive/com.yostarjp.bluearchive.MxUnityPlayerActivity"
    }
    
    server_names = list(server_pic_folder_map.keys())

    with ui.row():
        with ui.column():
            with ui.card():
                ui.link('模拟器配置', '#EMULATOR')
                ui.link('服务器配置', '#SERVER')
                ui.link('任务执行顺序', '#TASK_ORDER')
                ui.link('后续配置文件', '#NEXT_CONFIG')
                ui.link('课程表', '#COURSE_TABLE')
                ui.link('悬赏通缉', '#WANTED')
                ui.link('特殊任务', '#SPECIAL_TASK')
                ui.link('学园交流会', '#EXCHANGE')
                ui.link('活动关卡', '#ACTIVITY')
                ui.link('困难关卡', '#HARD')
                ui.link('普通关卡', '#NORMAL')
                ui.link('工具路径', '#TOOL_PATH')

                
            
        with ui.column():
            with ui.row():
                ui.link_target("EMULATOR")
                ui.label('模拟器配置').style('font-size: x-large')
                
            with ui.row():
                ui.number('模拟器端口',
                        step=1,
                        precision=0
                        ).bind_value(config.configdict, 'TARGET_PORT', forward=lambda v: int(v))
            with ui.row():    
                ui.input('模拟器路径'
                         ).bind_value(config.configdict, 'TARGET_EMULATOR_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')

            with ui.row():
                ui.link_target("SERVER")
                ui.label('服务器配置').style('font-size: x-large')
            
            with ui.row():
                ui.link_target("TASK_ORDER")
                ui.label('任务执行顺序').style('font-size: x-large')
            
            with ui.row():
                ui.link_target("NEXT_CONFIG")
                ui.label('后续配置文件').style('font-size: x-large')
            
            with ui.row():
                ui.link_target("COURSE_TABLE")
                ui.label('课程表').style('font-size: x-large')
            
            with ui.row():
                ui.input('课程表点击坐标')
            
            with ui.row():
                ui.link_target("WANTED")
                ui.label('悬赏通缉').style('font-size: x-large')
            
            with ui.row():
                ui.link_target("SPECIAL_TASK")
                ui.label('特殊任务').style('font-size: x-large')
            
            with ui.row():
                ui.link_target("EXCHANGE")
                ui.label('学园交流会').style('font-size: x-large')
                
            with ui.row():
                ui.link_target("ACTIVITY")
                ui.label('活动关卡').style('font-size: x-large')
                
            with ui.row():
                ui.link_target("HARD")
                ui.label('困难关卡').style('font-size: x-large')
                
            with ui.row():
                ui.link_target("NORMAL")
                ui.label('普通关卡').style('font-size: x-large')
                
            with ui.row():
                ui.link_target("TOOL_PATH")
                ui.label('其他设置').style('font-size: x-large')
            
            with ui.row():
                ui.number('点击后停顿间隔', 
                          suffix="s",
                          step=0.1,
                          precision=1).bind_value(config.configdict, 'TIME_AFTER_CLICK')

        with ui.column():
            ui.button("查看", on_click=lambda: print(config.configdict))
            
    ui.run()