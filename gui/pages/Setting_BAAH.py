from nicegui import ui, run
import requests

def set_BAAH(config):
    
    def select_language(value):
        config.softwareconfigdict["LANGUAGE"] = value
        config.save_software_config()
        if value == "zh_CN":
            ui.notify("语言已切换为中文，重启生效")
        else:
            ui.notify("Language has been changed to English, restart to take effect")

    # 检查更新
    async def check_newest_version():
        try:
            r = await run.io_bound(requests.get, "https://api.github.com/repos/sanmusen214/BAAH/releases/latest", timeout=10)
            if r.status_code == 200:
                data = r.json()
                ui.notify(f'{config.get_text("notice_get_new_version")}: {data["tag_name"]}')
            else:
                ui.notify(config.get_text("notice_fail"))
        except:
            ui.notify(config.get_text("notice_fail"))
        
    
    with ui.column():
        ui.link_target("BAAH")
        ui.label("Blue Archive Aris Helper").style('font-size: xx-large')
        
        ui.toggle({"zh_CN":"中文", "en_US":"English"}, value=config.softwareconfigdict["LANGUAGE"], on_change=lambda e:select_language(e.value))

        ui.label(config.get_text("BAAH_desc"))

        ui.label(config.get_text("BAAH_get_version"))

        ui.button(config.get_text("button_check_version"), on_click=check_newest_version)
        
        web_url = {
                    "github": "https://github.com/sanmusen214/BAAH",
                    "bilibili":"https://space.bilibili.com/7331920"
                }
        
        ui.input("Github").bind_value_from(web_url, "github").style('width: 400px')
        ui.input("Bilibili").bind_value_from(web_url, "bilibili").style('width: 400px')
        

        ui.label(config.get_text("BAAH_attention")).style('color: red; font-size: x-large')