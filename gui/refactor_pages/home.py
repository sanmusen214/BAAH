from .json_file_docker import get_json_list
from .json_file_docker import add_new_config

from nicegui import ui

from ..components.exec_arg_parse import check_token_dialog
from ..define import gui_shared_config

@ui.refreshable
def render_json_list():
    if check_token_dialog(render_json_list):

        ui.label(f"Blue Archive Aris Helper {gui_shared_config.NOWVERSION}").style('font-size: xx-large')

        ui.label(gui_shared_config.get_text("BAAH_desc"))

        ui.label(gui_shared_config.get_text("config_file")).style("font-size: xx-large")

        # 配置文件名 卡片
        for config_name in get_json_list():
            with ui.link(target = f"/panel/{config_name}"):
                with ui.card().props('flat bordered'):
                    ui.label(config_name).style("font-size: large;")

        ui.button("+", on_click=add_new_config).style(
            "width: 30px; height: 30px; line-height: 30px; text-align: center; cursor: pointer;")


@ui.page("/")
def home_page():
    render_json_list()
