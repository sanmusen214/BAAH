from nicegui import ui

def set_assault(config):
    with ui.row():
        ui.link_target("ASSAULT")
        ui.label(config.get_text("task_assault")).style('font-size: x-large')
    
    ui.label(config.get_text("desc_assault"))
    
    ui.label('1:"Normal", 2:"Hard", 3:"Very Hard", 4: "Hardcore", 5: "Extreme", 6: "Insane", 7: "Torment"')
    ui.number(
        "",
        min=1,
        precision=0,
        step=1
    ).bind_value(config.userconfigdict, "AUTO_ASSAULT_LEVEL", forward=lambda x: int(x)).style("width: 100px")