from nicegui import ui

def set_craft(config):
    with ui.row():
        ui.link_target("CRAFT")
        ui.label(config.get_text("task_craft")).style('font-size: x-large')
    
    
    ui.label(config.get_text("config_craft_desc"))
    
    ui.number(config.get_text("config_craft_max_times"),
                step=1,
                precision=0,
                min=1,
                max=3
                ).bind_value(config.userconfigdict, 'CRAFT_TIMES', forward=lambda v: int(v), backward=lambda v:int(v)).style('width: 400px')
    
    ui.checkbox(config.get_text("config_use_quick_craft")).bind_value(config.userconfigdict, 'CRAFT_USE_QUICK')