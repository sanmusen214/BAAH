import subprocess
from ..components.json_file_docker import get_json_list, add_new_config, copy_and_rename_config

from nicegui import ui, app

from ..components.check_update import only_check_version, get_newest_version
from ..components.exec_arg_parse import check_token_dialog
from ..define import gui_shared_config


def select_language(value):
    gui_shared_config.softwareconfigdict["LANGUAGE"] = value
    gui_shared_config.save_software_config()
    if value == "zh_CN":
        ui.notify("语言已切换为中文，重启生效")
    elif value == "en_US":
        ui.notify("Language has been changed, restart to take effect")
    else:
        ui.notify("言語が切り替わりました。再起動して有効になります。")

# 网址
web_url = {
        "github": "https://github.com/sanmusen214/BAAH",
        "bilibili":"https://space.bilibili.com/7331920"
    }

# 使用url
how_to_use_url = {
    "zh_CN": "https://gitee.com/sammusen/BAAH/blob/main/docs/README_cn.md",
    "en_US": "https://github.com/sanmusen214/BAAH/blob/main/docs/README_en.md"
    }

@ui.refreshable
def render_json_list():
    if check_token_dialog(render_json_list):
        with ui.splitter(value=50).classes('w-full h-full').style("height: calc(100vh - 2rem); overflow-y:auto") as splitter:
            with splitter.before:
                with ui.column().style("padding: 10px"):
                    ui.label(f"Blue Archive Aris Helper {gui_shared_config.NOWVERSION}").style('font-size: xx-large')
                    
                    # 项目链接
                    with ui.row():
                        ui.link("Github", web_url["github"], new_tab=True)
                        # ui.input("Github").bind_value_from(web_url, "github").style('width: 400px')
                        ui.link("Bilibili", web_url["bilibili"], new_tab=True)
                        # ui.input("Bilibili").bind_value_from(web_url, "bilibili").style('width: 400px')

                    # 语言切换
                    ui.toggle({"zh_CN":"中文", "en_US":"English", "jp_JP":"日本語"}, value=gui_shared_config.softwareconfigdict["LANGUAGE"], on_change=lambda e:select_language(e.value)).bind_value_from(gui_shared_config.softwareconfigdict, "LANGUAGE")

                    # 基本介绍
                    with ui.row().style("display: flex; justify-content: space-between; align-items: center;"):
                        ui.label(gui_shared_config.get_text("BAAH_desc"))

                    # 如何使用
                    with ui.row():
                        ui.link(gui_shared_config.get_text("notice_QA"), how_to_use_url.get(gui_shared_config.softwareconfigdict["LANGUAGE"], ""), new_tab=True)
                        ui.label("QQ: 715586983;1029291081").style('font-size: x-large; color: red;')

                    # 重要设置提醒
                    ui.label(gui_shared_config.get_text("BAAH_attention")).style('font-size: x-large')




                    #=================更新区域=================
                                        
                    # 显示更新信息
                    release_area = ui.card()
                    async def show_release():
                        result = await only_check_version()
                        with release_area:
                            ui.label(result.get("msg","")).style(f'font-size: x-large;{"color: red" if result.get("status",False) else "color: black"}')
                            ui.html(f'<div style="white-space: pre-line;font-size: large">{result.get("body","")}</div>')

                    ui.timer(0.1, show_release, once=True)
                    
                    # 一键更新，唤起更新程序，结束gui进程
                    def update_advance():
                        try:
                            subprocess.Popen(["BAAH_UPDATE.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE, close_fds=True)
                            # app.shutdown()
                        except Exception as e:
                            ui.notify(f"Failed to start BAAH_UPDATE.exe: {e}", type="warning")
                    
                    with ui.row():
                        # 下载更新包
                        ui.button(gui_shared_config.get_text("button_check_version"), on_click=lambda e, c=gui_shared_config:get_newest_version(c))
                        # 一键更新按钮
                        ui.button(gui_shared_config.get_text("button_update_advance"), on_click=update_advance)

            with splitter.after:
                with ui.column().style("padding: 20px"):
                    # ============配置文件区域===========
                    ui.label(gui_shared_config.get_text("config_file")).style("font-size: xx-large")

                    # 复制操作的相关参数：被复制的文件名，新文件名
                    copy_related_params = {"old_name":"", "new_name":""}
                    with ui.dialog() as dialog, ui.card():
                        ui.input(gui_shared_config.get_text("button_copy")).bind_value_from(copy_related_params, "old_name").set_enabled(False)
                        ui.input(gui_shared_config.get_text("button_rename")).bind_value_to(copy_related_params, "new_name")
                        with ui.row():
                            ui.button(gui_shared_config.get_text("button_hide"), color="white", on_click=dialog.close)
                            ui.button(gui_shared_config.get_text("button_save"), on_click=lambda e:[copy_and_rename_config(copy_related_params["old_name"], copy_related_params["new_name"]), dialog.close()])
                            

                    # 配置文件名 卡片
                    with ui.column():
                        for config_name in get_json_list():
                            with ui.row().classes("flex items-center"):
                                # config名
                                with ui.link(target = f"/panel/{config_name}"):
                                    with ui.card().props('flat bordered'):
                                        ui.label(config_name).style("font-size: large;")
                                # 复制按钮
                                ui.button(gui_shared_config.get_text("button_copy"), on_click=lambda e, c=config_name:[copy_related_params.update({"old_name":c, "new_name":""}), dialog.open()])

                    # 添加配置
                    user_config_name = {"val":""}
                    with ui.row().classes("flex items-center"):
                        ui.input("Name").bind_value(user_config_name, "val")
                        ui.button(gui_shared_config.get_text("button_add"), on_click=lambda: add_new_config(user_config_name["val"])).style(
                        "height: 30px; line-height: 30px; text-align: center; cursor: pointer;")


@ui.page("/")
def home_page():
    render_json_list()
