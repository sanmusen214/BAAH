from nicegui import ui

def set_exam(config):

    with ui.row():
        ui.link_target("EXAM")
        ui.label(config.get_text("task_exam")).style('font-size: x-large')

    # 设置考试关卡
    ui.number(config.get_text("config_level"),
              min=1, max=4, step=1, precision=0).bind_value(
                  config.userconfigdict, "EXAM_TARGET_LEVEL",
                  forward=lambda x: int(x)
                  ).style('width: 200px')
    # 设置考试的队伍数量
    ui.number(config.get_text("desc_exam_times"), 
              min=1, max=3, step=1, precision=0).bind_value(
                  config.userconfigdict, "EXAM_TEAM_COUNT",
                  forward=lambda x: int(x)
                  ).style('width: 200px')
