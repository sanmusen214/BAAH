from ..show_gui import show_gui

from nicegui import ui


@ui.page('/panel/{json_file_name}')
def show_json_panel(json_file_name: str):
    show_gui(json_file_name)
