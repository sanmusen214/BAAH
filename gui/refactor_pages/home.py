import subprocess
from .json_file_docker import get_json_list
from .json_file_docker import add_new_config

from nicegui import ui, app

from ..components.check_update import get_newest_version
from ..components.exec_arg_parse import check_token_dialog
from ..define import gui_shared_config


def select_language(value):
    gui_shared_config.softwareconfigdict["LANGUAGE"] = value
    gui_shared_config.save_software_config()
    if value == "zh_CN":
        ui.notify("语言已切换为中文，重启生效")
    else:
        ui.notify("Language has been changed, restart to take effect")

@ui.refreshable
def render_json_list():
    if check_token_dialog(render_json_list):
        with ui.splitter(value=50).classes('w-full h-full').style("height: calc(100vh - 2rem)") as splitter:
            with splitter.before:
                with ui.column().style("padding: 10px"):
                    ui.label(f"Blue Archive Aris Helper {gui_shared_config.NOWVERSION}").style('font-size: xx-large')
                    # 语言切换
                    ui.toggle({"zh_CN":"中文", "en_US":"English", "jp_JP":"日本語"}, value=gui_shared_config.softwareconfigdict["LANGUAGE"], on_change=lambda e:select_language(e.value)).bind_value_from(gui_shared_config.softwareconfigdict, "LANGUAGE")

                    ui.label(gui_shared_config.get_text("BAAH_desc"))
                    ui.label("新QQ群：715586983, 另外请关注QQ频道: BAAH 防止走失").style('font-size: xx-large; color: red;')

                    ui.label(gui_shared_config.get_text("BAAH_get_version"))

                    # 下载更新包
                    ui.button(gui_shared_config.get_text("button_check_version"), on_click=lambda e, c=gui_shared_config:get_newest_version(c))
                    
                    # 一键更新，唤起更新程序，结束gui进程
                    def update_advance():
                        try:
                            subprocess.Popen(["BAAH_UPDATE.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE, close_fds=True)
                            # app.shutdown()
                        except Exception as e:
                            ui.notify(f"Failed to start BAAH_UPDATE.exe: {e}", type="warning")
                    # 一键更新按钮
                    ui.button(gui_shared_config.get_text("button_update_advance"), on_click=update_advance)

                    # 网址
                    web_url = {
                                "github": "https://github.com/sanmusen214/BAAH",
                                "bilibili":"https://space.bilibili.com/7331920"
                            }
                    
                    with ui.row():
                        ui.link("Github", web_url["github"], new_tab=True)
                        ui.input("Github").bind_value_from(web_url, "github").style('width: 400px')
                        
                    with ui.row():
                        ui.link("Bilibili", web_url["bilibili"], new_tab=True)
                        ui.input("Bilibili").bind_value_from(web_url, "bilibili").style('width: 400px')

                    # 重要设置提醒
                    ui.label(gui_shared_config.get_text("BAAH_attention")).style('color: red; font-size: x-large')

            with splitter.after:
                with ui.column().style("padding: 20px"):
                    # ============配置文件区域===========
                    ui.label(gui_shared_config.get_text("config_file")).style("font-size: xx-large")

                    # 配置文件名 卡片
                    with ui.row():
                        for config_name in get_json_list():
                            with ui.link(target = f"/panel/{config_name}"):
                                with ui.card().props('flat bordered'):
                                    ui.label(config_name).style("font-size: large;")

                    # 添加配置
                    user_config_name = {"val":""}
                    with ui.row():
                        ui.input("Name").bind_value(user_config_name, "val")
                        ui.button("+", on_click=lambda: add_new_config(user_config_name["val"])).style(
                        "width: 30px; height: 30px; line-height: 30px; text-align: center; cursor: pointer;")


@ui.page("/")
def home_page():
    render_json_list()
