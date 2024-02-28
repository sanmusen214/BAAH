from nicegui import ui, run
from gui.components.list_edit_area import list_edit_area
import os

from modules.utils import screencut_tool, connect_to_device, screen_shot_to_global

def set_other(config, load_jsonname):
    with ui.row():
        ui.link_target("TOOL_PATH")
        ui.label(config.get_text("setting_other")).style('font-size: x-large')

    ui.label(config.get_text("config_warn_change")).style('color: red')
    
    with ui.row():
        ui.number(config.get_text("config_wait_time_after_click"),
                    suffix="s",
                    step=0.1,
                    precision=1).bind_value(config.userconfigdict, 'TIME_AFTER_CLICK')
    
    ui.label(config.get_text("config_desc_response_y"))
    with ui.row():
        ui.number(config.get_text("config_response_y"),
                    step=1,
                    min=1,
                    precision=0).bind_value(config.userconfigdict, 'RESPOND_Y', forward=lambda x:int(x), backward=lambda x:int(x)).bind_enabled(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y', forward=lambda v: not v, backward=lambda v: not v)
        ui.checkbox(config.get_text("config_bind_response_to_server")).bind_value(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y')
        
    with ui.row():
        ui.input(config.get_text("config_ip_root")).bind_value(config.userconfigdict, 'TARGET_IP_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
    
    with ui.row():
        ui.input(config.get_text("config_adb_path")).bind_value(config.userconfigdict, 'ADB_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
    
    with ui.row():
        ui.input(config.get_text("config_screenshot_name")).bind_value(config.userconfigdict, 'SCREENSHOT_NAME',forward=lambda v: v.replace("\\", "/")).style('width: 400px').set_enabled(False)
    
    # 测试/开发使用
    # 检查当前文件夹下有没有screencut.exe文件
    # whethercut = os.path.exists("./screencut.exe")
    # if whethercut:
    #     with ui.row():
    #         ui.button("测试截图/screencut test", on_click=lambda: os.system(f'start screencut.exe "{load_jsonname}"'))
    
    async def test_screencut():
        connect_to_device(use_config=config)
        screen_shot_to_global(use_config=config)
        screenshotname = config.userconfigdict['SCREENSHOT_NAME']
        await run.io_bound(
            screencut_tool,
            left_click=True,
            right_click=True,
            img_path=screenshotname
        )
    
    # 将截图功能内嵌进GUI
    with ui.row():
        ui.button("测试截图/screencut test", on_click=test_screencut)