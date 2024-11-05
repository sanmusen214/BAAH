import subprocess
from nicegui import ui, app
from gui.components.check_update import get_newest_version


def set_BAAH(config, shared_softwareconfig):
    
    def select_language(value):
        shared_softwareconfig.softwareconfigdict["LANGUAGE"] = value
        shared_softwareconfig.save_software_config()
        if value == "zh_CN":
            ui.notify("语言已切换为中文，重启生效")
        else:
            ui.notify("Language has been changed, restart to take effect")

    
    with ui.column():
        ui.link_target("BAAH")
        ui.label(f"Blue Archive Aris Helper {config.NOWVERSION} ==> ({config.nowuserconfigname})").style('font-size: xx-large')
        
        ui.toggle({"zh_CN":"中文", "en_US":"English", "jp_JP":"日本語"}, value=shared_softwareconfig.softwareconfigdict["LANGUAGE"], on_change=lambda e:select_language(e.value)).bind_value_from(shared_softwareconfig.softwareconfigdict, "LANGUAGE")

        ui.label(config.get_text("BAAH_desc"))

        ui.label(config.get_text("BAAH_get_version"))

        # 下载更新包
        ui.button(config.get_text("button_check_version"), on_click=lambda e, c=config:get_newest_version(c))
        
        # 一键更新，唤起更新程序，结束gui进程
        def update_advance():
            try:
                subprocess.Popen(["BAAH_UPDATE.exe"], creationflags=subprocess.CREATE_NEW_CONSOLE, close_fds=True)
                app.shutdown()
            except Exception as e:
                ui.notify(f"Failed to start BAAH_UPDATE.exe: {e}", type="warning")
        ui.button(config.get_text("button_update_advance"), on_click=update_advance)
        
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

        ui.label(config.get_text("BAAH_attention")).style('color: red; font-size: x-large')
        
        ui.html('<iframe  src="//player.bilibili.com/player.html?aid=539065954&bvid=BV1pi4y1W7QB&cid=1413492023&p=1&autoplay=0" width="720px" height="480px" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>')