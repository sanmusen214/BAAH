from nicegui import ui

def set_vpn(config):
    
    def list_of_click_and_sleep():
        """
        用于编辑的表格
        """
        click_and_wait_list = config.userconfigdict['VPN_CONFIG']['CLICK_AND_WAIT_LIST']
        
        def change_click_pos_x(lineind, itemind, val):
            """
            改变点击位置的x坐标或y坐标
            """
            click_and_wait_list[lineind][0][itemind] = int(val)
        
        def change_wait_time(lineind, val):
            """
            改变等待时间
            """
            click_and_wait_list[lineind][1] = int(val)
            
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
                    ui.number("X", min=-1, value=click_pos[0], on_change=lambda x,i=i: change_click_pos_x(i, 0, x.value))
                    ui.number("Y", min=-1, value=click_pos[1], on_change=lambda x,i=i: change_click_pos_x(i, 1, x.value))
                    ui.number("Wait", min=0, value=sleep_time, on_change=lambda x,i=i: change_wait_time(i, x.value))
                    ui.button(config.get_text("button_add"), on_click=lambda x, i=i:add_line(i))
                    ui.button(config.get_text("button_delete"), on_click=lambda x,i=i: del_line(i))
        
        show_table()
        

    with ui.row():
        ui.link_target("VPN")
        ui.label(config.get_text("setting_vpn")).style('font-size: x-large')
    
    # 选择是否使用
    ui.checkbox(config.get_text("vpn_desc")).bind_value(config.userconfigdict, "USE_VPN")
    # 选择加速器包名
    ui.input("VPN APP").bind_value(config.userconfigdict['VPN_CONFIG'], "VPN_ACTIVITY").style('width: 400px')
    # 一系列点击操作
    list_of_click_and_sleep()