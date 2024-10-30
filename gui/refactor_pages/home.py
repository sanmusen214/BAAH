from .json_file_docker import get_json_list
from .json_file_docker import add_new_config

from nicegui import ui

from ..components.exec_arg_parse import check_token_dialog

@ui.refreshable
def render_json_list():
    if check_token_dialog(render_json_list):

        for i in get_json_list():
            ui.link(i, f"/panel/{i}")

        ui.button("+", on_click=add_new_config).style(
            "width: 30px; height: 30px; line-height: 30px; text-align: center; cursor: pointer;")


@ui.page("/")
def home_page():
    render_json_list()
