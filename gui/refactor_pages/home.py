from .json_file_docker import get_json_list

from nicegui import ui

from ..components.exec_arg_parse import check_token_dialog

@ui.refreshable
def render_json_list():
    if check_token_dialog(render_json_list):
        for i in get_json_list():
            ui.link(i, f"/panel/{i}")


@ui.page("/")
def home_page():
    render_json_list()