from .json_file_docker import get_json_list

from nicegui import ui


@ui.page("/")
def home_page():
    for i in get_json_list():
        ui.link(i, f"/panel/{i}")
