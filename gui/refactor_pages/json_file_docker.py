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


async def add_new_config(configname):
    """
    点击加号后，添加一个新的json配置文件到alljson_list和alljson_tab_list里，然后让Configger类去新建这个json文件
    """
    configname = configname.strip()
    if not configname:
        ui.notify("配置名为空！/Config name is None!")
    else:
        configname = configname.replace(".json", "") + ".json"
        if configname in alljson_list:
            ui.notify("配置名已存在/Config name already exists")
        else:
            # 创建一个新的json文件
            with open(os.path.join(MyConfigger.USER_CONFIG_FOLDER, configname), 'w') as f:
                f.write("{}")
            ui.run_javascript('window.location.reload()')
