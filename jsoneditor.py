from gui import tab_area
from gui.components.check_update import check_version
from modules.configs.MyConfig import MyConfigger

from nicegui import ui, app


def main():
    app.on_connect(check_version)
    tab_area()
    # 运行GUI
    ui.run(title=f"BAAH{MyConfigger.NOWVERSION}", favicon="./DATA/assets/aris.ico", language="zh-CN", reload=True)


if __name__ in {"__main__", "__mp_main__"}:
    main()
