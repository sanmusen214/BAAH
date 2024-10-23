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
        with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, response), 'w') as f:
            f.write("{}")
        await ui.run_javascript('location.reload()')
