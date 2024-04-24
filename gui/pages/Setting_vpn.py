from nicegui import ui, run
from modules.utils import connect_to_device, get_now_running_app,  get_now_running_app_entrance_activity, screen_shot_to_global, screencut_tool

def set_vpn(config):
    async def connect_and_get_now_app(enter_activity = True):
        """
        链接并获取当前运行的app
        """
        connect_to_device(config)
        if enter_activity:
            app = get_now_running_app_entrance_activity(config)
        else:
            app = get_now_running_app(config)
        if app:
            config.userconfigdict['VPN_CONFIG']['VPN_ACTIVITY'] = app
        
    
    def list_of_click_and_sleep():
        """
        用于编辑的表格
        """
        click_and_wait_list = config.userconfigdict['VPN_CONFIG']['CLICK_AND_WAIT_LIST']
        
        def change_click_pos_x(lineind, itemind, val):
            """
            改变点击位置的x坐标或y坐标
            """
            if itemind == None:
                # 如果itemind为None，表示是图片路径
                click_and_wait_list[lineind][0] = val
            else:
                click_and_wait_list[lineind][0][itemind] = int(val)
        
        def change_wait_time(lineind, val):
            """
            改变等待时间
            """
            click_and_wait_list[lineind][1] = int(val)
            
        async def set_click_pos_of_line(lineind):
            """
            设置点击位置
            """
            connect_to_device(use_config=config)
            screen_shot_to_global(use_config=config)
            screenshotname = config.userconfigdict['SCREENSHOT_NAME']
            click_and_wait_list[lineind][0] = await run.io_bound(
                screencut_tool,
                left_click=True,
                right_click=True,
                img_path=screenshotname,
                quick_return=True
            )
            show_table.refresh()
            
        def add_line(line_index):
            """
            添加一行
            """
            # click_and_wait_list.append([[-1, -1], 1])
            click_and_wait_list.insert(line_index+1, [[-1, -1], 1])
            show_table.refresh()
        
        def del_line(line_index):
            """
            删除一行
            """
            click_and_wait_list.pop(line_index)
            show_table.refresh()
        
        @ui.refreshable
        def show_table():
            for i, line in enumerate(click_and_wait_list):
                # 分割出点击位置和等待时间
                click_pos, sleep_time = line
                with ui.row():
                    # 如果click_pos是列表
                    if isinstance(click_pos, list):
                        ui.number("X", min=-1, value=click_pos[0], on_change=lambda x,i=i: change_click_pos_x(i, 0, x.value))
                        ui.number("Y", min=-1, value=click_pos[1], on_change=lambda x,i=i: change_click_pos_x(i, 1, x.value))
                    else:
                        ui.image(click_pos).style("max-width: 100px; max-height: 100px")
                        ui.input("Pic", value=click_pos, on_change=lambda x,i=i: change_click_pos_x(i, None, x.value)).style('width: 400px')
                    ui.number("Wait", min=0, value=sleep_time, on_change=lambda x,i=i: change_wait_time(i, x.value))
                    ui.button(config.get_text("button_edit"), on_click=lambda x,i=i: set_click_pos_of_line(i))
                    ui.button(config.get_text("button_add"), on_click=lambda x, i=i:add_line(i))
                    ui.button(config.get_text("button_delete"), on_click=lambda x,i=i: del_line(i))
            # 最后一行，添加按钮
            ui.button(config.get_text("button_add"), on_click=lambda x:add_line(len(click_and_wait_list)-1))
        
        show_table()
        

    with ui.row():
        ui.link_target("VPN")
        ui.label(config.get_text("setting_vpn")).style('font-size: x-large')
    
    # 选择是否使用
    ui.checkbox(config.get_text("vpn_desc")).bind_value(config.userconfigdict, "USE_VPN")
    with ui.row():
        # 选择加速器包名
        ui.input("APP").bind_value(config.userconfigdict['VPN_CONFIG'], "VPN_ACTIVITY").style('width: 400px')
        ui.button(config.get_text("button_get_now_app_enter"), on_click=lambda : connect_and_get_now_app(enter_activity=True))
        ui.button(config.get_text("button_get_now_app"), on_click=lambda : connect_and_get_now_app(enter_activity=False))
    # 一系列点击操作
    list_of_click_and_sleep()