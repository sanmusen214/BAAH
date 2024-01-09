from nicegui import ui

def set_task_order(config, real_taskname_to_show_taskname):
    with ui.row():
        ui.link_target("TASK_ORDER")
        ui.label('任务执行顺序').style('font-size: x-large')
    
    
    def select_clear_all_and_refresh_task_order(type="select"):
        if type == "select":
            for i in range(1, len(config.userconfigdict["TASK_ACTIVATE"])):
                config.userconfigdict["TASK_ACTIVATE"][i] = True
        else:
            for i in range(1, len(config.userconfigdict["TASK_ACTIVATE"])):
                config.userconfigdict["TASK_ACTIVATE"][i] = False
        task_order.refresh()
    
    with ui.row():
        ui.button("全选", on_click=lambda: select_clear_all_and_refresh_task_order("select"))
        ui.button("全不选", on_click=lambda: select_clear_all_and_refresh_task_order("unselect"))
    
    @ui.refreshable
    def task_order():
        for i in range(len(config.userconfigdict["TASK_ORDER"])):
            with ui.row():
                ui.label(f'第{i+1}个任务:')
                atask = ui.select(real_taskname_to_show_taskname,
                            value=config.userconfigdict["TASK_ORDER"][i],
                            on_change=lambda v,i=i: config.userconfigdict["TASK_ORDER"].__setitem__(i, v.value),
                            )
                acheck = ui.checkbox('启用', value=config.userconfigdict["TASK_ACTIVATE"][i], on_change=lambda v,i=i: config.userconfigdict["TASK_ACTIVATE"].__setitem__(i, v.value))
                if i==0:
                    atask.set_enabled(False)
                    acheck.set_enabled(False)
                ui.button("添加任务", on_click=lambda i=i+1: add_task(i))
                if len(config.userconfigdict["TASK_ORDER"]) > 0 and i > 0:
                    ui.button("删除任务", on_click=lambda i=i: del_task(i), color="red")

    def add_task(i):
        config.userconfigdict["TASK_ORDER"].insert(i, "邮件")
        config.userconfigdict["TASK_ACTIVATE"].insert(i, True)
        task_order.refresh()
    
    def del_task(i):
        config.userconfigdict["TASK_ORDER"].pop(i)
        config.userconfigdict["TASK_ACTIVATE"].pop(i)
        task_order.refresh()
    
    task_order()
    
    with ui.row():
        ui.link_target("NEXT_CONFIG")
        ui.label('后续配置文件').style('font-size: x-large')
    
    ui.label("注意：此项配置文件会在当前配置文件执行完毕后继续执行，比如config_global.json是登录的国际服，那么你可以把config_global.json复制一份重命名为config_jp.json。在config_jp.json里将区服改为日服").style('color: red')
    ui.label("如果你只想运行此配置文件的话此项直接不填").style('color: red')
    
        
    ui.input('执行完此配置文件过后，继续执行配置文件').bind_value(config.userconfigdict, 'NEXT_CONFIG',forward=lambda v: v.replace("\\", "/")).style('width: 400px')