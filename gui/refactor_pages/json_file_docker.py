from ..show_gui import show_gui
from modules.configs.MyConfig import MyConfigger

from nicegui import ui
import os


DEFAULT_CONFIG_JSON_NAME = "config.json"
LETTERS_NOT_UPPER_STYLE = "text-transform: none;"


def get_json_list():
    """
    can get all json file names list in BAAH_CONFIGS dir, if not exits, create a config.json, make the list not empty
    Returns:
        a list that all json file name from BAAH_CONFIGS dir
    """
    arr = [i for i in os.listdir(MyConfigger.USER_CONFIG_FOLDER) if i.endswith(".json")]
    if len(arr) == 0:
        with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, DEFAULT_CONFIG_JSON_NAME), 'w') as f:
            f.write("{}")
        arr.append(DEFAULT_CONFIG_JSON_NAME)
    return arr


alljson_list = get_json_list()
alljson_tab_list: list[ui.tab] = []


@ui.refreshable
def tab_area():
    """
    start render the web components, use alljson_list to create, have one create one
    """
    global alljson_tab_list
    with ui.tabs().classes('w-full') as tabs:
        for json_name in alljson_list:
            alljson_tab_list.append(ui.tab(json_name, label=json_name).style(LETTERS_NOT_UPPER_STYLE))
        # 新建配置，用加号添加
        ui.button("+", on_click=add_new_config).style(
            "width: 30px; height: 30px; line-height: 30px; text-align: center; cursor: pointer;")
    with ui.tab_panels(tabs, value=alljson_list[0]).classes('w-full'):
        for i, tab_panel in enumerate(alljson_tab_list):
            with ui.tab_panel(tab_panel).style("height: 88vh; overflow: auto;"):
                show_gui(alljson_list[i])


async def add_new_config():
    """
    点击加号后，添加一个新的json配置文件到alljson_list和alljson_tab_list里，然后让Configger类去新建这个json文件
    """
    response = await ui.run_javascript('''
        return await window.prompt("请输入新配置名/Please input new config name")
    ''', timeout=60.0)
    if not response:
        print("未输入配置名/No config name input")
        return
    print("输入的配置名/Input config name:", response)
    response = response.strip().replace(".json", "")
    response = response + ".json"
    if response in alljson_list:
        await ui.alert("配置名已存在/Config name already exists")
    else:
        # 创建一个新的json文件，延长alljson_list和alljson_tab_list
        alljson_list.append(response)
        alljson_tab_list.append(None)
        tab_area.refresh()
